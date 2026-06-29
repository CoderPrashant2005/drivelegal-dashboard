# seed_laws.py
from models import SessionLocal, TrafficLaw, engine, Base

print("Wiping out old traffic laws...")
# Safely target and drop only the traffic_laws table
TrafficLaw.__table__.drop(bind=engine, checkfirst=True)

print("Rebuilding traffic laws table...")
# Recreate the table structure cleanly
TrafficLaw.__table__.create(bind=engine, checkfirst=True)

# Fully populated flat dictionary covering all 24 entries from your document
raw_state_rules = {
    "Delhi": [
        "Urban areas: 50 km/h. Rural roads: 60–80 km/h (where applicable). Expressways/NRJs: 80–100 km/h (as signposted).",
        "Helmets mandatory for riders and pillion on two-wheelers.",
        "Seatbelts mandatory for drivers and front-seat passengers in cars.",
        "Obey all traffic signals (red, amber, green). Right turns at red are generally not permitted unless explicitly allowed by signs.",
        "Pedestrian signals have priority where present; wait for walk signals.",
        "Park in designated areas; follow posted signs. No parking near fire hydrants, bus stops, or double-yellow zones (where marked).",
        "Improper/illegal parking can lead to fines, towing, and vehicle immobilization."
    ],
    "Punjab": [
        "Urban: 50–60 km/h. Rural: 80–90 km/h. Highways/expressways: signposted (typically 100–120+ km/h where allowed).",
        "Helmets mandatory for riders and pillion on two-wheelers.",
        "Seatbelts mandatory for drivers and front passengers in cars.",
        "Obey all signals; no right turn on red unless permitted by sign.",
        "Pedestrian signals have priority at crossings.",
        "Park in designated areas; avoid blocking driveways, entrances, or signage.",
        "No parking near fire hydrants, bus stops, or marked no-parking zones."
    ],
    "Haryana": [
        "Urban: 50–60 km/h. Rural: 80–90 km/h. Highways: signposted (often 100–110+ km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front-seat passengers.",
        "Follow all signals; no right turn on red unless signs allow.",
        "Pedestrian signals prioritized at crossings.",
        "Use designated spots; avoid fire lanes and blocked entrances."
    ],
    "Rajasthan": [
        "Urban: 50–60 km/h. Rural: 60–80 km/h. Highways: signposted (often 100–120 km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for front-seat occupants.",
        "Obey signals; right turns on red not allowed unless posted.",
        "Pedestrian signals have priority where present.",
        "Park in marked zones; respect no-parking boards."
    ],
    "Uttar Pradesh": [
        "Urban: 50 km/h. Rural: 60–80 km/h. Expressways/highways: as signposted (often 100–120 km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front passengers.",
        "All signals must be obeyed; red-right-turn-on-red not generally allowed.",
        "Pedestrian signals have priority.",
        "Park in designated areas; avoid blocking traffic flow and hydrants."
    ],
    "Uttarakhand": [
        "Urban: 50 km/h. Rural: 60–80 km/h. Highways: signposted (typical 80–110+ km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for front occupants in cars.",
        "Obey all signals; right turns on red not allowed unless signage permits.",
        "Pedestrian signals respected.",
        "Park only in legal spots; avoid restricted zones and entrances.",
        "Park in designated zones; no parking near hydrants, bus stops, or no-parking areas."
    ],
    "Maharashtra": [
        "Urban: 50–60 km/h. Rural: 80–90 km/h. Expressways: signposted (often 100–120+ km/h where allowed).",
        "Helmets mandatory for riders and pillions on two-wheelers.",
        "Seatbelts mandatory for drivers and front passengers in cars.",
        "Obey all traffic signals; no turning on red unless signage allows.",
        "Pedestrian signals have priority at crossings.",
        "Park in designated areas; avoid blocking driveways, entrances, or hydrants."
    ],
    "Karnataka": [
        "Urban: 50–60 km/h. Rural: 80–90 km/h. Highways: signposted (often 100–120+ km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front-seat passengers.",
        "Follow signals; no right turns on red unless posted.",
        "Pedestrian signals prioritized at crossings.",
        "Park in marked zones; avoid no-parking zones and hydrants."
    ],
    "Tamil Nadu": [
        "Urban: 50–60 km/h. Rural: 80–90 km/h. Highways: signposted (often 100–120 km/h where allowed).",
        "Helmets required for riders and pillions.",
        "Seatbelts required for drivers and front passengers.",
        "Obey all signals; right turns on red generally not allowed.",
        "Pedestrian signals have precedence.",
        "Park only in designated spaces; avoid obstructing traffic."
    ],
    "West Bengal": [
        "Urban: 50–60 km/h. Rural: 70–90 km/h. Highways: signposted (often 100–120+ km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Front-seat seatbelts mandatory in cars.",
        "Follow signals; no right turn on red unless signposted.",
        "Pedestrian signals have priority.",
        "Park in legal zones; avoid no-parking zones and hydrants."
    ],
    "Gujarat": [
        "Urban: 40–60 km/h. Rural: 80–90 km/h. Highways: signposted (often 100–120+ km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front passengers.",
        "Obey signals; no right turn on red unless posted.",
        "Pedestrian signals honored at crossings.",
        "Park in designated areas; respect no-parking zones."
    ],
    "Madhya Pradesh": [
        "Urban: 40–60 km/h. Rural: 60–80 km/h. Highways: signposted (often 100–120+ km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front passengers.",
        "Follow all signals; red-right-turn-on-red not typically allowed.",
        "Pedestrian signals have priority.",
        "Park in marked areas; avoid blocking hydrants and entrances."
    ],
    "Andhra Pradesh": [
        "Urban: 50–60 km/h. Rural: 60–80 km/h. Highways: signposted (often 80–100+ km/h where allowed).",
        "Helmets mandatory for riders and pillions on two-wheelers.",
        "Seatbelts mandatory for drivers and front passengers in cars.",
        "Obey all signals; right turns on red not allowed unless posted.",
        "Pedestrian signals have priority at crossings.",
        "Park in designated zones; avoid hydrants and no-parking zones."
    ],
    "Kerala": [
        "Urban: 50–60 km/h. Rural: 60–80 km/h. Highways: signposted (often 80–100+ km/h).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front-seat passengers.",
        "Follow signals; no right turn on red unless signage allows.",
        "Pedestrian signals prioritized.",
        "Park in marked spaces; avoid blocking entrances and hydrants."
    ],
    "Telangana": [
        "Urban: 50–60 km/h. Rural: 60–80 km/h. Highways: signposted (often 80–120+ km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front passengers.",
        "Obey all signals; no red-right-turn-on-red unless posted.",
        "Pedestrian signals given priority.",
        "Park in designated zones; avoid hydrants and bus stops."
    ],
    "Himachal Pradesh": [
        "Urban: 40–50 km/h. Rural: 60–80 km/h. Highways: signposted (often 80–100+ km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front passengers.",
        "Follow signals; pedestrian signals prioritized.",
        "Park in legal spots; avoid restricted zones and entrances."
    ],
    "Tripura": [
        "Urban: 40–50 km/h. Rural: 60–80 km/h. Highways: signposted (often 80–100+ km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front passengers.",
        "Obey signals; no right turn on red unless posted.",
        "Pedestrian signals prioritized.",
        "Park in designated areas; avoid hydrants and bus stops."
    ],
    "Puducherry": [
        "Urban: 40–50 km/h. Rural: 60–80 km/h. Highways: signposted (often 80–100+ km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front passengers.",
        "Obey signals; right turns on red generally not allowed.",
        "Park in designated zones; avoid no-parking zones and hydrants."
    ],
    "Jammu & Kashmir": [
        "Urban: 40–50 km/h. Rural: 60–80 km/h. Highways: signposted (often 80–100+ km/h where allowed).",
        "Helmets mandatory for riders and pillions on two-wheelers.",
        "Seatbelts mandatory for drivers and front passengers in cars.",
        "Obey all signals; red-right-turn-on-red not allowed unless posted.",
        "Pedestrian signals have priority at crossings.",
        "Park in designated areas; avoid hydrants, bus bays, and no-parking zones."
    ],
    "Ladakh": [
        "Urban: 40–50 km/h. Rural: 60–80 km/h. Highways: signposted (often 80–100+ km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front passengers in cars.",
        "Obey all signals; no right turns on red unless posted.",
        "Pedestrian signals may be limited in remote areas; proceed with caution.",
        "Park in designated zones; avoid restricted areas and hydrants."
    ],
    "Chhattisgarh": [
        "Urban: 50–60 km/h. Rural: 60–80 km/h. Highways: signposted (often 80–100+ km/h where allowed).",
        "Helmets mandatory for riders and pillions on two-wheelers.",
        "Seatbelts mandatory for drivers and front passengers in cars.",
        "Obey all signals; red-right-turn-on-red not allowed unless posted.",
        "Pedestrian signals prioritized at crossings.",
        "Park in designated zones; avoid hydrants and no-parking zones."
    ],
    "Chandigarh": [
        "Urban: 40–50 km/h. Rural: 60–70 km/h. Highways: signposted (often 80–100+ km/h where allowed).",
        "Helmets mandatory for riders and pillions on two-wheelers.",
        "Seatbelts mandatory for drivers and front passengers in cars.",
        "Follow all signals; no right turn on red unless signage allows.",
        "Pedestrian signals prioritized at crossings.",
        "Park in marked spaces; avoid blocking driveways and hydrants."
    ],
    "Dadra and Nagar Haveli and Daman and Diu": [
        "Urban: 40–50 km/h. Rural: 60–80 km/h. Highways: signposted (often 80–100+ km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front passengers in cars.",
        "Obey signals; red-right-turn-on-red not generally allowed.",
        "Pedestrian signals prioritized where present.",
        "Park in designated zones; avoid hydrants and no-parking zones."
    ],
    "Lakshadweep": [
        "Urban: 40–50 km/h. Rural: 50–70 km/h. Highways: signposted (often 60–80+ km/h where allowed).",
        "Helmets mandatory for riders and pillions on two-wheelers.",
        "Seatbelts mandatory for drivers and front passengers in cars.",
        "Obey signals; pedestrian signals given priority where available.",
        "Park in designated zones; avoid restricted/blocked areas."
    ],
    "Andaman and Nicobar Islands": [
        "Urban: 40–50 km/h. Rural: 60–80 km/h. Highways: signposted (often 80–100+ km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front passengers in cars.",
        "Obey all signals; no right turns on red unless posted.",
        "Pedestrian signals prioritized at crossings.",
        "Park in designated zones; avoid hydrants and no-parking zones."
    ],
    
    "Arunachal Pradesh": [
        "Urban: 40–50 km/h. Rural: 60–80 km/h. Highways: signposted (often 80–100 km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front passengers.",
        "Obey signals; right turns on red not allowed unless posted.",
        "Pedestrian signals prioritized at crossings.",
        "Park in designated zones; avoid restricted mountain passes and blocking single-lane routes."
    ],
    "Assam": [
        "Urban: 50–60 km/h. Rural: 70–80 km/h. Highways: signposted (often 80–100+ km/h where allowed).",
        "Helmets mandatory for riders and pillions on two-wheelers.",
        "Seatbelts mandatory for drivers and front passengers in cars.",
        "Obey all signals; no right turn on red unless permitted by sign.",
        "Pedestrian signals prioritized at crossings.",
        "Park in designated areas; avoid blocking bus bays, hydrants, or no-parking zones."
    ],
    "Manipur": [
        "Urban: 40–50 km/h. Rural: 60–80 km/h. Highways: signposted (often 80–100 km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for front-seat occupants.",
        "Obey signals; right turns on red not allowed unless posted.",
        "Pedestrian signals respected where present.",
        "Park in marked areas; avoid blocking driveways and narrow bazaar corridors."
    ],
    "Meghalaya": [
        "Urban: 40–50 km/h. Rural: 60–80 km/h. Highways: signposted (often 80–100 km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front passengers.",
        "Obey signals; red-right-turn-on-red not allowed unless signage permits.",
        "Pedestrian signals have priority.",
        "Park only in legal spots; strictly avoid blocking hilly traffic movement or emergency lanes."
    ],
    "Mizoram": [
        "Urban: 30–40 km/h. Rural: 50–70 km/h. Highways: signposted (often 70–90 km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for front-seat passengers.",
        "Follow all signals; pedestrian crossings are highly prioritized.",
        "Park strictly in designated spaces; adhere to local community-enforced sequential parking rules on narrow hill roads."
    ],
    "Nagaland": [
        "Urban: 40–50 km/h. Rural: 60–80 km/h. Highways: signposted (often 80–100 km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front passengers.",
        "Obey all traffic signals; no right turn on red unless posted.",
        "Pedestrian signals prioritized.",
        "Use designated parking bays; avoid blocking terrain-critical single lanes and market paths."
    ],
    "Sikkim": [
        "Urban: 30–40 km/h. Rural: 50–70 km/h. Highways: signposted (often 70–90 km/h where allowed).",
        "Helmets mandatory for riders and pillions.",
        "Seatbelts mandatory for drivers and front passengers in cars.",
        "Follow all signals; strict adherence to lane driving regulations.",
        "Park only in authorized parking complexes or designated curbside areas; vehicle immobilization and heavy fines apply for blocking mountain highways."
    ]
}

db = SessionLocal()
try:
    for state, rules in raw_state_rules.items():
        for rule_text in rules:
            law_entry = TrafficLaw(state=state, description=rule_text)
            db.add(law_entry)
    db.commit()
    print("✨ PostgreSQL database successfully populated with all 24 regional state/UT lines!")
except Exception as e:
    db.rollback()
    print(f"❌ Error seeding laws database layout: {e}")
finally:
    db.close()