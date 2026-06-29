# add_owner_columns.py
#
# Safely adds the new user_id and owner columns to the EXISTING vehicles
# table in PostgreSQL, without dropping or touching any existing data.
#
# This is intentionally separate from models.py's __main__ block, which
# uses drop_all() and would destroy your migrated data if run again.
#
# Run ONCE:
#   python add_owner_columns.py

from sqlalchemy import text
from models import engine

STATEMENTS = [
    "ALTER TABLE vehicles ADD COLUMN IF NOT EXISTS user_id INTEGER;",
    "ALTER TABLE vehicles ADD COLUMN IF NOT EXISTS owner VARCHAR;",
    "CREATE INDEX IF NOT EXISTS ix_vehicles_user_id ON vehicles (user_id);",
]

def run():
    with engine.begin() as conn:
        for stmt in STATEMENTS:
            print(f"Running: {stmt}")
            conn.execute(text(stmt))
    print("\nDone. Existing rows are untouched; user_id/owner are NULL until migrate_data.py backfills them.")

if __name__ == "__main__":
    run()
