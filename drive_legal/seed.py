# seed.py
from models import SessionLocal, Vehicle

def seed_initial_vehicle():
    db = SessionLocal()
    try:
        # Check if the target test car already exists
        target_plate = "DL01AB1234"
        exists = db.query(Vehicle).filter(Vehicle.plate == target_plate).first()
        
        if not exists:
            print(f"🚘 Registering target vehicle {target_plate} into database records...")
            test_car = Vehicle(
                plate=target_plate,
                model="Hyundai Creta",
                tag="Primary"
            )
            db.add(test_car)
            db.commit()
            print("✅ Vehicle identity successfully allocated!")
        else:
            print("ℹ️ Vehicle already registered. System ready.")
            
    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_initial_vehicle()