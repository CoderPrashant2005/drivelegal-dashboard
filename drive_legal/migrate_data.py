# migrate_data.py
#
# One-time (re-runnable) migration script: copies vehicles + violations from
# MySQL (drive_legal, port 3307) into PostgreSQL (drive_legal, via models.py),
# using only the fields the dashboard actually needs.
#
# Run this from inside the drive_legal folder (same place as main.py and
# models.py), with the venv active, AFTER running add_owner_columns.py once:
#
#   python add_owner_columns.py     (only needed once, ever)
#   python migrate_data.py          (safe to re-run any time)
#
# Safe to re-run: vehicles are upserted by plate (no duplicates). If a
# vehicle already exists in Postgres (e.g. auto-created earlier by the
# /violations/trigger endpoint with no model/owner), this script will now
# BACKFILL any missing model/user_id/owner on the existing row instead of
# skipping it outright -- this fixes the "model shows None" bug we hit
# with GJ01CV7854.

import pymysql
from datetime import datetime

from models import SessionLocal, Vehicle, Violation, normalize_plate

# ----------------------------------------------------------------------
# 1. MySQL connection (source)
# ----------------------------------------------------------------------
MYSQL_CONFIG = dict(
    host="localhost",
    port=3307,
    user="root",
    password="Root@1234",
    database="drive_legal",
)

# Status mapping: MySQL enum -> Postgres Pending/Paid
STATUS_MAP = {
    "PENDING": "Pending",
    "APPROVED": "Pending",   # approved by analyst, not yet paid
    "OVERDUE": "Pending",
    "DISPUTED": "Pending",
    "REJECTED": "Paid",      # closed, nothing owed
    "PAID": "Paid",
}


def fetch_mysql_data():
    """Pull vehicles (joined with users for owner name) + violations
    (joined with locations) from MySQL."""
    conn = pymysql.connect(**MYSQL_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                v.vehicle_id,
                v.user_id,
                v.vehicle_number,
                v.model_name,
                u.full_name AS owner_name
            FROM vehicles v
            LEFT JOIN users u ON v.user_id = u.user_id
        """)
        vehicles = cur.fetchall()

        cur.execute("""
            SELECT
                v.vehicle_id,
                v.section_number,
                v.violation_type,
                v.penalty_amount,
                v.status,
                v.violation_time,
                l.address,
                l.city,
                l.state,
                l.latitude,
                l.longitude
            FROM violations v
            LEFT JOIN locations l ON v.location_id = l.location_id
        """)
        violations = cur.fetchall()

        return vehicles, violations
    finally:
        conn.close()


def migrate():
    print("Connecting to MySQL...")
    mysql_vehicles, mysql_violations = fetch_mysql_data()
    print(f"Found {len(mysql_vehicles)} vehicles and {len(mysql_violations)} violations in MySQL.\n")

    db = SessionLocal()

    # Map MySQL vehicle_id (numeric) -> normalized plate string,
    # since Postgres Violation.vehicle_id is a plate string, not a numeric FK.
    vehicle_id_to_plate = {}

    vehicles_created = 0
    vehicles_backfilled = 0
    vehicles_unchanged = 0

    print("Migrating vehicles...")
    for v in mysql_vehicles:
        plate = normalize_plate(v["vehicle_number"])
        if not plate:
            continue
        vehicle_id_to_plate[v["vehicle_id"]] = plate

        existing = db.query(Vehicle).filter(Vehicle.plate == plate).first()

        if not existing:
            new_vehicle = Vehicle(
                plate=plate,
                model=v["model_name"],
                tag="Secondary",
                user_id=v["user_id"],
                owner=v["owner_name"],
            )
            db.add(new_vehicle)
            vehicles_created += 1
            continue

        # Already exists (e.g. auto-created by /violations/trigger with no
        # model/owner). Backfill any missing fields from MySQL instead of
        # silently skipping -- this is the fix for the GJ01CV7854 bug.
        changed = False
        if not existing.model and v["model_name"]:
            existing.model = v["model_name"]
            changed = True
        if existing.user_id is None and v["user_id"] is not None:
            existing.user_id = v["user_id"]
            changed = True
        if not existing.owner and v["owner_name"]:
            existing.owner = v["owner_name"]
            changed = True

        if changed:
            vehicles_backfilled += 1
        else:
            vehicles_unchanged += 1

    db.commit()
    print(f"  Created: {vehicles_created}, backfilled: {vehicles_backfilled}, unchanged: {vehicles_unchanged}\n")

    print("Migrating violations...")
    violations_created = 0
    violations_skipped = 0
    violations_orphaned = 0

    for viol in mysql_violations:
        plate = vehicle_id_to_plate.get(viol["vehicle_id"])
        if not plate:
            # Violation references a vehicle that had no usable plate
            violations_orphaned += 1
            continue

        mapped_status = STATUS_MAP.get((viol["status"] or "").upper(), "Pending")

        # Build location string: prefer address, fall back to city/state
        loc_parts = [p for p in [viol["address"], viol["city"], viol["state"]] if p]
        loc = ", ".join(dict.fromkeys(loc_parts)) if loc_parts else None

        timestamp = viol["violation_time"] or datetime.utcnow()
        amt = float(viol["penalty_amount"]) if viol["penalty_amount"] is not None else 0.0
        lat = float(viol["latitude"]) if viol["latitude"] is not None else None
        lon = float(viol["longitude"]) if viol["longitude"] is not None else None

        # De-dupe check: same plate + type + section + amount + timestamp
        existing = db.query(Violation).filter(
            Violation.vehicle_id == plate,
            Violation.type == viol["violation_type"],
            Violation.sec == viol["section_number"],
            Violation.amt == amt,
            Violation.timestamp == timestamp,
        ).first()

        if existing:
            violations_skipped += 1
            continue

        new_violation = Violation(
            vehicle_id=plate,
            type=viol["violation_type"],
            sec=viol["section_number"],
            loc=loc,
            lat=lat,
            lon=lon,
            amt=amt,
            status=mapped_status,
            timestamp=timestamp,
        )
        db.add(new_violation)
        violations_created += 1

    db.commit()
    print(f"  Created: {violations_created}, already existed: {violations_skipped}, orphaned (no matching vehicle): {violations_orphaned}\n")

    db.close()
    print("Migration complete.")


if __name__ == "__main__":
    migrate()