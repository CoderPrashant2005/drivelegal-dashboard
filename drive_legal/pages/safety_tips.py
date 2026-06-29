import streamlit as st


def show_safety_tips():

    st.markdown("### 💡 Road Safety Predictive Advisor")
    st.caption(
        "Tailoring target guidelines powered by real-time safety metrics and demographic focus classes."
    )

    # ======================================
    # Safety Tips Database
    # ======================================

    tips_database = {
            "Cars": [
                {"icon": "💺", "text": "Mandatory Seatbelts (Section 194B MV Act): Ensure all occupants—both front and rear passengers—use secure seatbelts. Violations carry a ₹1,000 fine."},
                {"icon": "📱", "text": "Distracted Driving Avoidance: No driver may look at, hold, or type on any mobile device or interactive communication screen while operating a moving vehicle."},
                {"icon": "🚗", "text": "3-Second Distance Protocol: Always preserve a minimum 3-second follow gap threshold from leading vehicles; buffer up to 5-6 seconds under rainy or slippery conditions."},
                {"icon": "🛑", "text": "Zebra Lane Stoppage Policy: Stop completely before the white stop line markers at intersections whenever signaling triggers yellow or red flags."},
                {"icon": "👁️", "text": "Blind-Spot Mirror Audit: Check vehicle cabin and exterior side rearview mirrors thoroughly before initiating lane drift indicators or overtaking curves."},
                {"icon": "💨", "text": "Adherence to Variable Speed Limits: Obey explicit limits across urban corridors (typically 50 km/h) and expressways (80-100+ km/h as signposted)."},
                {"icon": "🚦", "text": "Amber Warning Protocol: Do not accelerate to beat a transitionary amber signal light; break smoothly if it is structurally safe to bring the car to a stop."},
                {"icon": "🍺", "text": "Zero Blood-Alcohol Tolerances (Section 185 MV Act): Operating with BAC above 30mg per 100ml results in immediate citation, heavy penalties, or potential arrest."},
                {"icon": "💡", "text": "High-Beam Hazard Constraints: Switch off high beams inside lit municipal limits; blinding approaching drivers is illegal and hazardous."},
                {"icon": "⚠️", "text": "Hazard Lights Proper Deployment: Use hazard blinkers exclusively during static emergency breakdowns or towing processes—not for rain or low-light cruising."},
                {"icon": "🅿️", "text": "Illegal Double-Parking Obstructions: Parking parallel to an already curbside-stationed car blocks civic transit corridors and results in vehicle towing fines."},
                {"icon": "🛞", "text": "Tire Tread Depth Inspections: Verify tire wear signatures do not fall below standard legal requirements (1.6mm) to minimize dangerous hydroplaning."},
                {"icon": "📋", "text": "Valid Documentation Records: Keep physical or digital copies of Registration Certificates (RC), active Insurance, and valid Pollution Certificates (PUC) present."},
                {"icon": "🔕", "text": "Silent Zoning Restrictions (Section 194F MV Act): Excessive, aggressive, or air-horn honking within hospital, school, or court zoning boundaries is prohibited."},
                {"icon": "🛠️", "text": "Rear-View Mirror Maintenance: Ensure the center internal rearview mirror (IRVM) is never blocked by rear passenger stacks, luggage, or curtains."},
                {"icon": "♿", "text": "Yielding for Emergency Ambulances (Section 194E MV Act): Failure to move aside or draw to the curb to give immediate passage to emergency fleets leads to a ₹10,000 penalty."},
                {"icon": "🌧️", "text": "Wiper Blade Performance Audits: Regularly inspect the integrity of windshield wiper rubber surfaces to prevent visual smear patterns during storms."},
                {"icon": "🔄", "text": "Roundabout Priority Standard: Yield right-of-way explicitly to vehicles moving within active roundabouts before steering your car past lines."},
                {"icon": "📦", "text": "Cabin Load Restrictions: Do not stack goods on top of passenger seating matrices that compromise clear visibility across lateral or rear frames."},
                {"icon": "🛑", "text": "Prohibited Overtaking Layouts: Never attempt to pass other cars across single solid or double solid yellow painted dividing lines."},
                {"icon": "🪟", "text": "Tinted Glass Compliance Codes: Visual transmission ratings must clear minimum legal criteria (70% for front/rear windscreens, 50% for side glazing layers)."},
                {"icon": "🔑", "text": "Safe Door Deployment Guards: Verify side traffic metrics before extending car doors outward to prevent collisions with cyclists."},
                {"icon": "🔋", "text": "Dashboard Advisory Warnings: Promptly address check-engine, ABS, or brake warning lights via authorized service technicians before road deployment."}
            ],
            "Bikes / Scooters": [
                {"icon": "🪖", "text": "Mandatory Protective Helmet Gear (Section 129 MV Act): Both rider and pillion passenger must wear ISI/BIS-approved helmets with chin straps fastened securely."},
                {"icon": "❌", "text": "Triple Riding Violations (Section 128 MV Act): Operation is legally constrained to a maximum of two riders per two-wheeled motor vehicle frame."},
                {"icon": "🧥", "text": "High-Visibility Attire Standards: Wear bright or light-reflective outerwear during twilight or night transit loops to improve tracking profiles."},
                {"icon": "🚛", "text": "Left-Side Truck Blind-Spot Warning: Never execute an overtaking move past heavy container trucks on their tight left-side lane flank."},
                {"icon": "🩴", "text": "Footwear Compliance Guidelines: Operating motorcycles or geared scooters while wearing open-toed slippers or flip-flops is unsafe and illegal."},
                {"icon": "👟", "text": "Ankle Guard Protection: Prioritize heavy, closed-toe shoes or boots over canvas footwear to protect feet from debris or mechanical impacts."},
                {"icon": "🦓", "text": "Pedestrian Walkway Violations: Steering two-wheelers onto concrete footpaths or raised sidewalks to bypass traffic blocks is heavily fined."},
                {"icon": "💬", "text": "Handheld Phone Balancing Constraints: Jamming mobile devices underneath helmet padding to take active calls is highly dangerous and illegal."},
                {"icon": "🏍️", "text": "Handlebar Grip Controls: Maintain contact with both hands on the handlebar assemblies except when executing transient physical hand-signaling indicators."},
                {"icon": "🔕", "text": "Modulated Silencer System Prohibitions: Altering exhaust assemblies or fitting custom loud multi-tone pipes violates environmental and noise statutes."},
                {"icon": "🔄", "text": "Safe Mirror Coverage Frameworks: Ensure left and right mirrors are fitted and adjusted to eliminate blind spots on your flanks."},
                {"icon": "📦", "text": "Lateral Overloading Constraints: Carrying oversized packages or freight boxes across scooter floorboards that project past handlebars is prohibited."},
                {"icon": "🎒", "text": "Free Left-Turn Clarification Laws: Do not automatically turn left on a red signal unless explicit regional signage permits it."},
                {"icon": "🌧️", "text": "Wet Surface Tramway Hazards: Reduce velocity when rolling across steel expansion junctions or oil-filmed tar layers during early showers."},
                {"icon": "🛑", "text": "Sudden Braking Weight Changes: Distribute application evenly across front and rear brakes; sudden rear lockups prompt slides."},
                {"icon": "⚠️", "text": "Inter-Lane Weaving Patterns: Avoid erratic zig-zag cutting maneuvers across slow lanes; maintain predictable path alignments."},
                {"icon": "🔍", "text": "Turn Indicator Cancel Protocols: Deactivate directional blinkers immediately after completing a turn to avoid confusing following drivers."},
                {"icon": "🛡️", "text": "Saree Guard Structural Laws: All commercial two-wheelers must maintain intact rear saree guard mesh frames to shield passenger clothing layers."},
                {"icon": "💨", "text": "Speed Threshold Compliance: Adhere to standard 30-40 km/h municipal limits; avoid exceeding safe handling capacities on minor roads."},
                {"icon": "🛞", "text": "Daily Tire Pressure Controls: Check pressure counts regularly; low counts compromise stability during sharp turning maneuvers."},
                {"icon": "🔦", "text": "Always-On Headlight Regulations (AHO): Modern bikes must keep headlights active even during clear daylight cycles to maximize tracking visibility."},
                {"icon": "📋", "text": "Digital License Verification: Maintain digital copies of your driver's license and documentation inside official national portals like DigiLocker."},
                {"icon": "🛑", "text": "Yielding to Heavy Transits: Give priority to heavily loaded freight trucks or buses negotiating tight turning radius intersections."}
            ],
            "Heavy Duty Vehicles": [
                {"icon": "⚖️", "text": "Strict Axle Load Capacity Limits (Section 113 MV Act): Do not operate past certified Gross Vehicle Weight maximums; overweighted chassis damage roadways."},
                {"icon": "⏰", "text": "Municipal No-Entry Window Codes: Heavy commercial vehicles must strictly follow municipal daytime city entry bans and restriction windows."},
                {"icon": "🛣️", "text": "Rigid Left-Lane Lane Discipline: Keep heavy multi-axle freight carriers tracking inside the far-left lane; do not occupy passing channels."},
                {"icon": "💤", "text": "Mandatory Operator Downtime Rules: Heavy operators must break for rest after 5 continuous hours of steering to combat driver fatigue."},
                {"icon": "👁️", "text": "Blind-Spot Proximity Signage: Affix high-visibility warning graphics to the rear body warning surrounding traffic to stay clear of blind zones."},
                {"icon": "📦", "text": "Secure Cargo Tarp Tariffs: Cover loose aggregate material shipments (sand, gravel, construction refuse) to prevent road debris hazards."},
                {"icon": "📐", "text": "Prohibited Dimension Overhangs: Carrying iron bars, girders, or lumber that projects past tailgates without red flags/lights is illegal."},
                {"icon": "🛑", "text": "Reflective Strips Conformity: Affix continuous red and yellow industrial retro-reflective tape around all trailer borders for nighttime visibility."},
                {"icon": "⚡", "text": "Electronic Speed Governor Regulations: All heavy transport vehicles must maintain functional, un-tampered speed limiters calibrated to legal caps."},
                {"icon": "🛑", "text": "Air Brake Reservoir Drainage: Discharge moisture accumulations from air tank valves daily to maintain uniform stopping pressure profiles."},
                {"icon": "🅿️", "text": "Highway Breakdown Parking Rules: Deploy warning triangles at least 50 meters back if stalled on highway flanks, and activate hazard arrays."},
                {"icon": "🔄", "text": "Turning Clearance Radii: Exercise extreme caution and look for cyclists before swinging wide to negotiate sharp street intersections."},
                {"icon": "🛠️", "text": "Daily Under-Chassis Inspection Arrays: Frequently verify structural shackle pins, air hoses, and dual-wheel inner tyre conditions."},
                {"icon": "📋", "text": "National Permit Compliance Portals: Cross-state logistics carriers must verify active payment clearings before crossing border outposts."},
                {"icon": "🚨", "text": "Reversing Siren Warnings: Heavy commercial vehicles must maintain active acoustic backup hazard beepers paired with reversing gear switches."},
                {"icon": "🔕", "text": "Pneumatic Air-Horn Ban Zones: Fitting high-decibel air horns or multi-tone sirens is illegal and subject to heavy environmental fines."},
                {"icon": "🛞", "text": "Wheel Chock Usage: Keep solid wood or rubber triangular wheel wedges inside cabins to lock wheels during incline parking cycles."},
                {"icon": "💨", "text": "Downhill Compression Braking: Utilize lower transmission gears to manage downhill velocity on mountain passes to prevent brake fade."},
                {"icon": "🌧️", "text": "Visibility Defogging Adjustments: Maintain active windshield blowers to avoid dangerous moisture condensation loops across broad front panels."},
                {"icon": "👁️", "text": "Clean Lens Arrays: Clear grit, mud, and dust from rear taillights and brake indicators before embarking on nighttime freight runs."},
                {"icon": "📋", "text": "Fitness Certificate Verifications (Section 56 MV Act): Transport vehicles are legally invalid without an active, certified vehicle fitness clearance document."},
                {"icon": "🛑", "text": "Railway Crossing Stop Procedures: Stop, look, and listen clearly at un-gated rural rail cross sections before easing heavy frames forward."},
                {"icon": "🛣️", "text": "Bridge Load Limit Indicators: Obey structural weight limit signs posted ahead of minor or historic bridges."}
            ],
            "Children": [
                {"icon": "🚼", "text": "Certified Child Restraint Codes (Section 194B MV Act): Children under 14 years old must be secured via specialized booster cushions or harness seats."},
                {"icon": "🎒", "text": "The 3-Step Crossing Checklist: Train children to look right, look left, and look right again before crossing any street channel."},
                {"icon": "🔒", "text": "Rear Cabin Door Child Locks: Always engage mechanical child safety locks on rear doors to prevent accidental opening during transit."},
                {"icon": "🛑", "text": "School Zone Velocity Thresholds: Reduce vehicle speeds to under 25-30 km/h whenever operating within marked school zones."},
                {"icon": "🚌", "text": "School Bus Safety Buffers: Exercise extreme caution when passing a stationary school bus; look out for children stepping onto the road."},
                {"icon": "🚶", "text": "Adult Pedestrian Supervision: Children under the age of 8 must always be accompanied by an adult when navigating or crossing road corridors."},
                {"icon": "🚲", "text": "Bicycle Helmet Rules: Young children riding non-motorized bicycles on public streets should wear appropriate safety helmets."},
                {"icon": "🎒", "text": "Reflective Backpack Elements: Choose school bags and apparel with reflective strips to increase visibility during early morning or late evening walks."},
                {"icon": "❌", "text": "Front Passenger Exclusions: Do not let children under 12 sit in the front passenger seat of cars equipped with active airbags."},
                {"icon": "🪟", "text": "Window Extremity Rules: Teach children never to extend hands, arms, or heads out of open car windows or sunroof systems."},
                {"icon": "🅿️", "text": "Driveway Blind-Zone Precautions: Check behind your vehicle before backing out of home garages or driveways where toddlers may be playing."},
                {"icon": "🏢", "text": "Sidewalk Walking Discipline: Teach children to walk on the inner side of pavement corridors, away from active curb edges."},
                {"icon": "🚫", "text": "Zero Unattended Cabin Incidents: Never leave children locked inside a parked vehicle, avoiding heatstroke hazards."},
                {"icon": "📱", "text": "Distracted Walking Education: Educate children to put away tablets and mobile screens while walking near vehicular traffic lanes."},
                {"icon": "🦓", "text": "Zebra Crossing Priority Instruction: Teach children to cross public streets exclusively at designated zebra crossings or pedestrian bridges."},
                {"icon": "🛑", "text": "Playing Near Roadways: Instruct children never to play games, skate, or chase balls near busy streets or open parking layouts."},
                {"icon": "🚕", "text": "Safe Curbside Egress: Always discharge children from the left side of the vehicle onto the safe sidewalk, never into the flow of traffic."},
                {"icon": "🎈", "text": "Bright Clothing Choices: Dress children in highly visible colors when walking in foggy or dark weather conditions."},
                {"icon": "🤝", "text": "Traffic Guard Guidance: Instruct children to follow the instructions of school crossing guards or traffic police officers near campus gates."},
                {"icon": "📣", "text": "Acoustic Awareness: Teach kids to listen for vehicle engines, horns, or reverse warning beepers when walking in parking lots."},
                {"icon": "🚲", "text": "Safe Bicycle Routing: Guide children to ride their bicycles only on dedicated paths or low-speed neighborhood streets."},
                {"icon": "🚨", "text": "Emergency Contacts Knowledge: Ensure older children know basic emergency services helpline contacts (e.g., 112) for roadside incidents."},
                {"icon": "🛑", "text": "Corner Visibility Obstructions: Teach children never to step onto the street from between closely parked cars or large structures."}
            ],
            "Elderly (Old)": [
                {"icon": "🚶", "text": "Grade-Separated Crossing Guidance: Prioritize pedestrian elevators, subways, or foot overbridges over busy arterial roads."},
                {"icon": "👓", "text": "Optical Prescription Maintenance: Ensure vision prescriptions are regularly updated to accurately gauge vehicle speeds and distances."},
                {"icon": "👟", "text": "Non-Slip Safety Footwear: Wear high-traction, supportive shoes to prevent trips or slips on uneven asphalt or pavement surfaces."},
                {"icon": "🎨", "text": "Bright Wardrobe Selections: Use brightly colored coats, umbrellas, or walking sticks to remain visible to motorists in low light."},
                {"icon": "🛑", "text": "Extended Intersection Margins: Wait for a fresh green pedestrian signal before starting to cross, ensuring ample time to complete the path."},
                {"icon": "👥", "text": "Assisted High-Density Crossings: Seek assistance from traffic wardens or fellow pedestrians when crossing multi-lane intersections."},
                {"icon": "🚏", "text": "Safe Transit Boarding Zones: Stand well clear of the curb at bus stops until the vehicle comes to a complete halt."},
                {"icon": "🚗", "text": "Driver Yielding Responsibilities: Drivers must legally yield right-of-way and give extra time to elderly pedestrians crossing intersections."},
                {"icon": "🦽", "text": "Wheelchair Ramp Etiquette: Keep sidewalk ramps and accessibility cutouts clear of parked cars or merchandise."},
                {"icon": "📱", "text": "Emergency Smartphone Access: Keep speed-dial shortcuts configured for emergency medical services and family members on mobile devices."},
                {"icon": "🌦️", "text": "Adverse Weather Isolation: Avoid walking near busy streets during heavy rain or thick fog, when visibility and stopping distances are compromised."},
                {"icon": "🚶", "text": "Zebra Lane Reliance: Cross exclusively within marked white lines where drivers are legally primed to look for pedestrians."},
                {"icon": "🔊", "text": "Auditory Awareness: Avoid using noise-isolating headphones while walking, to ensure sirens, horns, and engines can be heard clearly."},
                {"icon": "🛑", "text": "Median Refuge Islands: If a traffic signal changes mid-crossing, wait safely on the raised central median refuge island."},
                {"icon": "🚕", "text": "Safe Ride-Hailing Access: Instruct taxi and ride-share drivers to pull over into flat, safe zones away from active traffic before boarding or exiting."},
                {"icon": "👟", "text": "Reflective Cane Accents: Apply reflective high-visibility tape to walking sticks, canes, or walkers for added safety."},
                {"icon": "🏃", "text": "Avoid Sudden Strides: Maintain a steady walking pace; do not make sudden dashes across the street when cars are approaching."},
                {"icon": "🧱", "text": "Pavement Defect Awareness: Watch for cracked paving slabs, open utility grates, or slippery mud along municipal walkways."},
                {"icon": "🚦", "text": "Pedestrian Countdown Timers: Utilize intersections equipped with digital countdown displays to confirm if enough crossing time remains."},
                {"icon": "🤝", "text": "Community Support Systems: Encourage neighbors to help senior community members clear paths during monsoons or winter seasons."},
                {"icon": "🚗", "text": "Brake System Sensitivity: Motorists must pass elderly pedestrians with wide lateral clearance, avoiding startling maneuvers."},
                {"icon": "📑", "text": "Medical Information Cards: Carry a card detailing your blood group, emergency contacts, and vital medical conditions in your wallet."},
                {"icon": "🛑", "text": "Blind Corner Precautions: Avoid crossing near sharp street corners where approaching vehicles have a restricted field of view."}
            ],
            "Road Crossings": [
                {"icon": "🦓", "text": "Zebra Stripe Legal Compliance: Cross exclusively within marked white zebra borders; jaywalking across expressways is illegal and fineable."},
                {"icon": "🎧", "text": "Acoustic Isolation Risks: Remove headphones, earbuds, and mobile accessories before stepping into active traffic lanes."},
                {"icon": "👁️", "text": "Positive Eye Contact: Establish direct eye contact with approaching drivers to confirm they see you before crossing."},
                {"icon": "📱", "text": "Zero Screen-Walking Policies: Keep mobile screens down and out of sight while walking across active intersections."},
                {"icon": "🖐️", "text": "Assertive Hand Signaling: Extend your arm horizontally to signal your intention to cross to approaching drivers."},
                {"icon": "🚦", "text": "Pedestrian Signal Obedience: Cross only when the illuminated walking figure or green pedestrian signal is active."},
                {"icon": "🏃", "text": "No Sudden Lane Dashes: Walk briskly but predictably across lanes; never run unexpectedly in front of moving vehicles."},
                {"icon": "🧱", "text": "Avoid Climbing Traffic Barricades: Do not climb over concrete central medians or metal fencing to cross roads."},
                {"icon": "🚖", "text": "Parked Vehicle Blind Zones: Never step onto a street from directly between two closely parked vans, buses, or large obstructions."},
                {"icon": "💡", "text": "Night Visibility Maximization: Use a smartphone flashlight or wear reflective details when crossing unlit suburban roads at night."},
                {"icon": "🔄", "text": "Multi-Stage Lane Audits: When crossing multi-lane roads, verify each lane is clear individually before stepping into it."},
                {"icon": "🌧️", "text": "Wet Road Surface Adjustments: Allow extra distance for vehicles to stop on wet roads, as braking distances double in the rain."},
                {"icon": "🚧", "text": "Construction Zone Safety: Follow dedicated bypass signs and temporary walkways around roadworks, avoiding active machinery zones."},
                {"icon": "🚨", "text": "Emergency Vehicle Absolute Priority: Never step onto a crosswalk if an emergency vehicle with sirens active is approaching."},
                {"icon": "🚋", "text": "Railway Track Rules: Cross railway tracks only at authorized level crossings when gates are open; never crawl under closed barriers."},
                {"icon": "🚗", "text": "Stop Line Compliance Verification: Ensure vehicles have actually stopped behind the painted white stop line before stepping onto the crosswalk."},
                {"icon": "📐", "text": "Diagonal Crossing Prohibitions: Cross straight across the road at a 90-degree angle to minimize time spent in the conflict zone."},
                {"icon": "🏪", "text": "Commercial Loading Areas: Exercise extra caution near commercial loading docks where heavy vans frequently back out blindly."},
                {"icon": "🐕", "text": "Leashed Pet Control: Keep pets on a short, secure leash when crossing roads to prevent them from bolting into traffic."},
                {"icon": "🌫️", "text": "Foggy Weather Precautions: Double check for approaching vehicles during heavy fog, as low visibility compromises safety for both drivers and pedestrians."},
                {"icon": "🏫", "text": "School Gate Crowding Avoidance: Keep school entrance gates clear of pedestrian bottlenecks to allow children to exit safely onto paths."},
                {"icon": "🛑", "text": "Corner Visibility Verification: Ensure you have a clear view of oncoming traffic in both directions before stepping off the curb at an intersection."},
                {"icon": "🛡️", "text": "Traffic Police Signals: Prioritize the manual hand signals of a traffic police officer over automated traffic lights at busy intersections."}
            ]
        }

    # ======================================
    # Layout
    # ======================================

    left_col, right_col = st.columns([1, 2])

    with left_col:

        st.markdown("#### 🎯 Target Context")

        selected_category = st.radio(
            "Select Profile Group",
            [
                "Cars",
                "Bikes / Scooters",
                "Heavy Duty Vehicles",
                "Children",
                "Elderly (Old)",
                "Road Crossings"
            ]
        )

        st.markdown("---")

        risk_map = {
            "Cars": "Medium",
            "Bikes / Scooters": "High",
            "Heavy Duty Vehicles": "High",
            "Children": "Medium",
            "Elderly (Old)": "Medium",
            "Road Crossings": "High"
        }

        st.metric(
            "Risk Level",
            risk_map[selected_category]
        )

        #st.metric(
            ##len(tips_database[selected_category])
        #)

    with right_col:

        st.markdown(
            f"#### Guidelines for {selected_category}"
        )

        tips = tips_database[selected_category]

        for tip in tips:

            st.success(
                f"{tip['icon']} {tip['text']}"
            )

    st.markdown("---")

    '''st.markdown("### 🤖 AI Safety Recommendation")

    recommendation_map = {
        "Cars":
            "Focus on seatbelts, speed limits and avoiding distractions.",

        "Bikes / Scooters":
            "Always wear a helmet and maintain lane discipline.",

        "Heavy Duty Vehicles":
            "Monitor fatigue, blind spots and cargo security.",

        "Children":
            "Adult supervision and safe crossing education are critical.",

        "Elderly (Old)":
            "Use pedestrian facilities and improve visibility.",

        "Road Crossings":
            "Cross only at designated crossings and obey signals."
    }

    st.info(
        recommendation_map[selected_category]
    )'''