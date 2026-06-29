# models.py
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
DATABASE_URL = "postgresql://postgres:Shinchan1234@localhost:5432/drive_legal"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
class Vehicle(Base):
    __tablename__ = "vehicles"
    plate = Column(String, primary_key=True, index=True)
    model = Column(String)
    tag = Column(String, default="Secondary") # Primary / Secondary
    # --- NEW (additive, nullable -> safe for existing rows) ---
    user_id = Column(Integer, index=True, nullable=True)   # MySQL users.user_id (source system)
    owner = Column(String, nullable=True)                  # MySQL users.full_name (denormalized for fast lookups)
class Violation(Base):
    __tablename__ = "violations"
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String, ForeignKey("vehicles.plate"))
    type = Column(String)
    sec = Column(String)
    loc = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    amt = Column(Float)
    status = Column(String, default="Pending") # Pending / Paid
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
class TrafficLaw(Base):
    __tablename__ = "traffic_laws"
    id = Column(Integer, primary_key=True, index=True)
    state = Column(String, index=True, nullable=False)        # e.g., "Delhi", "Punjab", "Maharashtra"
    description = Column(String, nullable=False)              # The actual rules text details
def normalize_plate(raw: str) -> str:
    """Strip spaces and uppercase, so 'GJ 01 AB 1234' and 'GJ01AB1234' are
    treated as the same plate — must match the normalization used on the
    MySQL side (violationController.js) or the same vehicle will fork into
    two records again, just on this side of the system instead."""
    return raw.strip().upper().replace(" ", "") if raw else None
def get_or_create_vehicle(db, plate: str, model: str = None) -> "Vehicle":
    """Look up a vehicle by (normalized) plate; create it if missing.
    Violation.vehicle_id is a foreign key to vehicles.plate, so inserting a
    violation for a plate that has no vehicle row yet fails the FK
    constraint. Call this BEFORE inserting any Violation row — it's the
    Postgres-side equivalent of the "find or create vehicle" logic already
    used in violationController.js for the MySQL database."""
    norm = normalize_plate(plate)
    if not norm:
        return None
    vehicle = db.query(Vehicle).filter(Vehicle.plate == norm).first()
    if vehicle:
        return vehicle
    vehicle = Vehicle(plate=norm, model=model, tag="Secondary")
    db.add(vehicle)
    db.commit()
    return vehicle
def get_user_vehicles_and_violations(db, plate: str):
    """Given ANY plate, find the user who owns it, then return every
    vehicle + violation belonging to that same user.

    Used by the 'My Vehicles' (multi-vehicle picker) and 'My Violations'
    (user-scoped violation list) pages so they show real per-user data
    instead of one hardcoded vehicle. Returns None if the plate has no
    associated user_id (e.g. legacy rows migrated before this column
    existed, or vehicles auto-created by the /violations/trigger endpoint
    without going through the MySQL migration)."""
    norm = normalize_plate(plate)
    anchor = db.query(Vehicle).filter(Vehicle.plate == norm).first()
    if not anchor or anchor.user_id is None:
        return None

    vehicles = db.query(Vehicle).filter(Vehicle.user_id == anchor.user_id).all()
    plates = [v.plate for v in vehicles]
    violations = db.query(Violation).filter(Violation.vehicle_id.in_(plates)).all() if plates else []
    return {"vehicles": vehicles, "violations": violations}
# Execute table generation logic in database context
if __name__ == "__main__":
    print("🧹 Wiping old table structures to prevent foreign key conflicts...")
    # This forces a clean slate so the "vehicles" table primary key exists before "violations" links to it
    Base.metadata.drop_all(bind=engine) 
    
    print("🏗️ Rebuilding database schemas...")
    Base.metadata.create_all(bind=engine)
    print("🚀 Database schemas successfully built!")
    
    # ==========================================
    # AUTOMATIC VEHICLE SEEDING
    # ==========================================
    print("🚘 Checking target vehicle records...")
    db = SessionLocal()
    try:
        target_plate = "DL01AB1234"
        test_car = Vehicle(
            plate=target_plate,
            model="Hyundai Creta",
            tag="Primary"
        )
        db.add(test_car)
        db.commit()
        print(f"✅ Vehicle identity '{target_plate}' successfully allocated to database!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")