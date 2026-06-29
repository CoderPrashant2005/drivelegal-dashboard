# main.py
from fastapi import FastAPI, Depends, HTTPException, Query, Security
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import SessionLocal, Violation, Vehicle, TrafficLaw, normalize_plate, get_or_create_vehicle, get_user_vehicles_and_violations
import uvicorn
import datetime

app = FastAPI(title="DriveLegal Backend API Engine Engine")

# =======================================================
# 🔒 1. API KEY SECURITY HANDSHAKE CONFIGURATION
# =======================================================
API_KEY_NAME = "X-API-KEY"
# Your newly designated secure project passkey
VALID_API_KEY = "DriveLegal_Project" 

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def validate_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=401, detail="Access Denied: API Key is missing from the header layout.")
    if api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Access Denied: Invalid secure token provided.")
    return api_key

# =======================================================
# 🌐 2. CORS MIDDLEWARE (Allows your main website to connect)
# =======================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your main website application to call endpoints directly
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Session Dependency Management
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📬 HELPER FUNCTION FOR ALERTS
def trigger_compliance_alert(violation_type, location, penalty):
    """
    This function routes the live alert. 
    For now, it prints directly to your backend log so you can see it fire in real-time!
    """
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print("\n" + "="*50)
    print(f"📬 [LIVE ALERT DISPATCHED AT {timestamp}]")
    print(f"⚠️ Traffic Offense: {violation_type}")
    print(f"📍 Location: {location}")
    print(f"💰 Fine Amount: ₹{penalty:,}")
    print("="*50 + "\n")

@app.get("/api/v1/dashboard-complete/{vehicle_id}")
def get_dashboard_data(vehicle_id: str, db: Session = Depends(get_db)):
    # 1. Fetch data from active database records — both scoped to THIS plate,
    #    not the whole table (that was the bug: vehicles used to ignore
    #    vehicle_id entirely and return every vehicle in the database).
    norm_id = normalize_plate(vehicle_id)
    violations = db.query(Violation).filter(Violation.vehicle_id == norm_id).all()
    vehicles = db.query(Vehicle).filter(Vehicle.plate == norm_id).all()

    # If this specific vehicle has no record yet, say so — rather than
    # only failing when the ENTIRE table happens to be empty.
    if not vehicles:
         raise HTTPException(status_code=404, detail="Vehicle identity structure target unallocated.")
         
    pending_v = [v for v in violations if v.status == "Pending"]
    paid_v = [v for v in violations if v.status == "Paid"]
    
    return {
        "summary": {
            "total_violations": len(violations),
            "pending_amount": sum(v.amt for v in pending_v),
            "pending_violations": len(pending_v),
            "paid_violations": len(paid_v),
            "total_vehicles": len(vehicles)
        },
        "vehicles": [{"plate": c.plate, "model": c.model, "tag": c.tag} for c in vehicles],
        "ai_score": {
            "score": max(100 - (len(pending_v) * 7), 30), # Deduct safety points dynamically
            "metrics": {"speeding": "Good" if len(pending_v) < 2 else "Needs Review", "braking": "Excellent"}
        },
        "violations": [{
            "type": v.type, "sec": v.sec, "loc": v.loc, 
            "lat": v.lat, "lon": v.lon, "amt": v.amt, 
            "status": v.status, "time": v.timestamp.strftime("%d %b %Y, %I:%M %p")
        } for v in violations],
        "payments": [{
            "type": v.type, "sec": v.sec, "loc": v.loc, "amt": v.amt, "time": v.timestamp.strftime("%d %b %Y")
        } for v in paid_v]
    }

# =======================================================
# ✨ NEW: Per-user vehicles + violations (purely additive route)
# Given ANY plate the user is identified by, finds the owning user_id
# and returns EVERY vehicle + violation belonging to that user — powers
# the "My Vehicles" multi-vehicle picker and "My Violations" pages so
# they show real per-user data instead of hardcoded mock data.
# Every route above this is completely untouched.
# =======================================================
@app.get("/api/v1/user-vehicles/{plate}")
def get_user_vehicles(plate: str, db: Session = Depends(get_db)):
    result = get_user_vehicles_and_violations(db, plate)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="No user record linked to this plate yet. Re-run the MySQL migration, or this vehicle was created without owner data."
        )

    vehicles = result["vehicles"]
    violations = result["violations"]

    pending_v = [v for v in violations if v.status == "Pending"]
    paid_v = [v for v in violations if v.status == "Paid"]

    # Monthly trend (Jan-Dec bucket counts) computed from real violation timestamps
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_counts = {m: 0 for m in month_labels}
    for v in violations:
        monthly_counts[month_labels[v.timestamp.month - 1]] += 1

    owner_name = vehicles[0].owner if vehicles else None

    return {
        "owner": owner_name,
        "vehicles": [
            {
                "plate": v.plate,
                "model": v.model,
                "tag": v.tag,
                "owner": v.owner,
                "total_violations": len([x for x in violations if x.vehicle_id == v.plate]),
                "pending_violations": len([x for x in pending_v if x.vehicle_id == v.plate]),
                "total_fines": sum(x.amt for x in violations if x.vehicle_id == v.plate),
            }
            for v in vehicles
        ],
        "summary": {
            "total_violations": len(violations),
            "pending_violations": len(pending_v),
            "paid_violations": len(paid_v),
            "total_fines": sum(v.amt for v in violations),
        },
        "monthly_trend": monthly_counts,
        "violations": [{
            "id": v.id,
            "vehicle_plate": v.vehicle_id,
            "type": v.type, "sec": v.sec, "loc": v.loc,
            "lat": v.lat, "lon": v.lon, "amt": v.amt,
            "status": v.status, "time": v.timestamp.strftime("%d %b %Y, %I:%M %p")
        } for v in violations]
    }

# Endpoint allowing remote sensors to post violations in real-time
# SECURED: Validates with your new password
@app.post("/api/v1/violations/trigger", dependencies=[Depends(validate_api_key)])
def trigger_violation(data: dict, db: Session = Depends(get_db)):
    try:
        # Auto-create the vehicle if this plate hasn't been seen on this
        # side of the system yet. Without this, the Violation insert below
        # fails the vehicle_id -> vehicles.plate FK constraint for any
        # plate that wasn't manually seeded — which is exactly why
        # approved violations from MySQL were never showing up here.
        plate = normalize_plate(data["vehicle_id"])
        get_or_create_vehicle(db, plate=plate, model=data.get("model"))

        new_ticket = Violation(
            vehicle_id=plate,
            type=data["type"],
            sec=data["sec"],
            loc=data["loc"], 
            lat=data["lat"], 
            lon=data["lon"], 
            amt=data["amt"]
        )
        db.add(new_ticket)
        db.commit()
        
        # =======================================================
        # 🔄 THE INTEGRATION LOOP
        # Fires the alert output immediately following database confirmation
        # =======================================================
        trigger_compliance_alert(
            violation_type=data["type"],
            location=data["loc"],
            penalty=data["amt"]
        )
        
        return {"status": "success", "message": "Violation registered dynamically over Secure Api Channel."}
        
    except Exception as e:
        db.rollback()
        print("Database Error:", str(e)) 
        raise HTTPException(status_code=500, detail=f"Error occurred while registering violation: {str(e)}")

# Vehicle details endpoint with comprehensive violation history 
# SECURED: Validates with your new password
@app.get("/api/v1/vehicle/{plate}", dependencies=[Depends(validate_api_key)])
def get_vehicle_details(plate: str, db: Session = Depends(get_db)):
    norm_plate = normalize_plate(plate)
    vehicle = db.query(Vehicle).filter(Vehicle.plate == norm_plate).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Requested vehicle profile not found.")
        
    violations = db.query(Violation).filter(Violation.vehicle_id == norm_plate).all()
    
    return {
        "plate": vehicle.plate,
        "model": vehicle.model,
        "tag": vehicle.tag,
        "total_history_count": len(violations),
        "history": [{
            "id": v.id,
            "type": v.type,
            "sec": v.sec,
            "loc": v.loc,
            "amt": v.amt,
            "status": v.status,
            "timestamp": v.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        } for v in violations]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)