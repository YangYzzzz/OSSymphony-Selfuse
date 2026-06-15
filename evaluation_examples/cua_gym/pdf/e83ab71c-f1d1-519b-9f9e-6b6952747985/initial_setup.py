"""
Initial Setup: Create a 30-page safety manual PDF with WARNING, CAUTION, and DANGER keywords
Task ID: pdf_ro_024
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_024'
SAFETY_DIR = f'{WORKDIR}/safety'
OUTPUT = f'{SAFETY_DIR}/manual.pdf'

def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


# Safety manual content organized by chapter/section
# Designed to have exactly: WARNING x18, CAUTION x12, DANGER x5
CHAPTERS = [
    {
        "title": "INDUSTRIAL SAFETY MANUAL",
        "subtitle": "Revision 4.2 - Effective March 2025\nAcme Industrial Solutions Inc.",
        "pages": []
    },
    # Table of Contents page (page 2)
    {
        "title": "TABLE OF CONTENTS",
        "pages": [
            [
                "TABLE OF CONTENTS",
                "",
                "Chapter 1: General Safety Procedures ........................... 3",
                "  1.1 Introduction to Workplace Safety ........................ 3",
                "  1.2 Emergency Contact Information ........................... 3",
                "  1.3 Incident Reporting Protocol .............................. 4",
                "  1.4 Safety Training Requirements ............................. 4",
                "  1.5 Personal Protective Equipment (PPE) Standards ........... 5",
                "",
                "Chapter 2: Chemical Handling and Storage ....................... 6",
                "  2.1 Chemical Classification System .......................... 6",
                "  2.2 Chemical Storage Requirements ........................... 7",
                "  2.3 Spill Response Procedures ................................ 8",
                "  2.4 Chemical Waste Disposal .................................. 9",
                "  2.5 Laboratory Safety Protocols .............................. 10",
                "",
                "Chapter 3: Machinery and Equipment Safety ..................... 11",
                "  3.1 Machine Guarding Standards ............................... 11",
                "  3.2 Lockout/Tagout (LOTO) Procedures ........................ 12",
                "  3.3 Crane and Hoist Operations ............................... 13",
                "  3.4 Powered Industrial Trucks (Forklifts) ................... 14",
                "  3.5 Conveyor System Safety ................................... 15",
                "",
                "Chapter 4: Electrical Safety ................................... 16",
                "  4.1 Electrical Hazard Recognition ............................ 16",
                "  4.2 Electrical Panel Requirements ............................ 17",
                "  4.3 Extension Cord and Temporary Wiring ..................... 18",
                "  4.4 Static Electricity Control ............................... 19",
                "  4.5 Emergency Power Systems .................................. 20",
                "",
                "Chapter 5: Fire Prevention and Response ....................... 21",
                "  5.1 Fire Prevention Measures ................................. 21",
                "  5.2 Fire Extinguisher Requirements .......................... 22",
                "  5.3 Sprinkler and Suppression Systems ....................... 23",
                "  5.4 Evacuation Procedures .................................... 24",
                "  5.5 Fire Investigation and Reporting ........................ 25",
                "",
                "Chapter 6: Confined Spaces and Fall Protection ................ 26",
                "  6.1 Confined Space Identification ............................ 26",
                "  6.2 Confined Space Entry Procedures ......................... 27",
                "  6.3 Fall Protection Requirements ............................. 28",
                "  6.4 Ladder and Scaffold Safety ............................... 29",
                "  6.5 Aerial Lift and Elevated Work Platforms ................. 30",
            ],
        ]
    },
    # Chapter 1: General Safety (pages 3-5) - WARNING x3, CAUTION x2, DANGER x1
    {
        "title": "Chapter 1: General Safety Procedures",
        "pages": [
            [
                "1.1 Introduction to Workplace Safety",
                "",
                "This manual provides comprehensive guidelines for safe operation of all",
                "equipment and facilities at Acme Industrial Solutions. All personnel must",
                "read and understand this manual before commencing work.",
                "",
                "WARNING: All employees must wear personal protective equipment (PPE)",
                "at all times when present on the factory floor. Failure to comply will",
                "result in immediate removal from the work area.",
                "",
                "1.2 Emergency Contact Information",
                "",
                "Emergency Services: 911",
                "Plant Safety Office: ext. 4200",
                "Environmental Spill Hotline: ext. 4250",
                "Medical Station (Building A): ext. 4100",
                "",
                "CAUTION: Emergency exits must remain unobstructed at all times.",
                "Monthly inspections verify compliance with OSHA regulation 29 CFR 1910.36.",
            ],
            [
                "1.3 Incident Reporting Protocol",
                "",
                "All workplace incidents, regardless of severity, must be reported within",
                "24 hours using Form SA-201. Near-miss incidents require Form SA-202.",
                "",
                "WARNING: Failure to report incidents within the mandated timeframe",
                "may result in disciplinary action and potential regulatory penalties.",
                "",
                "1.4 Safety Training Requirements",
                "",
                "New employees must complete 40 hours of safety orientation before",
                "unaccompanied facility access. Annual refresher training (8 hours) is",
                "mandatory for all personnel. Specialized equipment training is required",
                "for operators in Zones C through F.",
                "",
                "DANGER: Untrained personnel are strictly prohibited from entering",
                "restricted zones. Unauthorized entry may result in fatal injury.",
                "",
                "CAUTION: Training certifications expire after 12 months and must",
                "be renewed before the expiration date to maintain facility access.",
            ],
            [
                "1.5 Personal Protective Equipment (PPE) Standards",
                "",
                "Required PPE by zone:",
                "  Zone A (Office): Safety glasses",
                "  Zone B (Warehouse): Hard hat, safety glasses, steel-toe boots",
                "  Zone C (Assembly): Full PPE including hearing protection",
                "  Zone D (Chemical): Chemical-resistant suit, respirator, face shield",
                "  Zone E (Welding): Welding helmet, flame-resistant clothing, gloves",
                "  Zone F (High Voltage): Arc-rated clothing, insulated gloves, face shield",
                "",
                "WARNING: PPE must be inspected before each use. Damaged or expired",
                "equipment must be replaced immediately. Do not modify or alter any",
                "protective equipment as this voids the manufacturer's safety rating.",
                "",
                "All PPE must conform to ANSI/ISEA standards as specified in",
                "Appendix C of this manual.",
            ],
        ]
    },
    # Chapter 2: Chemical Handling (pages 6-10) - WARNING x4, CAUTION x3, DANGER x1
    {
        "title": "Chapter 2: Chemical Handling and Storage",
        "pages": [
            [
                "2.1 Chemical Classification System",
                "",
                "All chemicals on-site are classified according to the Globally Harmonized",
                "System (GHS). Safety Data Sheets (SDS) are available at each workstation",
                "and in the central chemical registry (Building D, Room 102).",
                "",
                "Categories of chemicals used at this facility:",
                "  - Flammable liquids (acetone, toluene, isopropanol)",
                "  - Corrosive substances (hydrochloric acid, sodium hydroxide)",
                "  - Oxidizing agents (hydrogen peroxide, potassium permanganate)",
                "  - Toxic substances (lead compounds, chromium salts)",
                "",
                "WARNING: Never mix chemicals without explicit authorization from",
                "the Chemical Safety Officer. Incompatible chemical reactions can",
                "produce toxic gases, fires, or explosions.",
                "",
                "CAUTION: All chemical containers must be properly labeled with",
                "GHS-compliant labels including hazard pictograms and signal words.",
            ],
            [
                "2.2 Chemical Storage Requirements",
                "",
                "Storage cabinets must be organized by hazard class. The following",
                "separation distances must be maintained:",
                "",
                "  Flammables: Dedicated flammable storage cabinet, max 60 gallons",
                "  Corrosives: Acid cabinet separate from base cabinet, secondary containment",
                "  Oxidizers: Isolated from flammables by minimum 20 feet",
                "  Toxics: Locked cabinet with access log",
                "",
                "WARNING: Storage temperatures must not exceed manufacturer specifications.",
                "Temperature monitoring logs must be reviewed weekly by the shift supervisor.",
                "",
                "DANGER: Compressed gas cylinders must be secured in upright position",
                "with chains or straps. A falling cylinder can become a lethal projectile.",
                "",
                "Inventory management procedures require quarterly audits of all stored",
                "chemicals. Expired materials must be disposed of through the approved",
                "hazardous waste contractor (GreenChem Disposal, contract #AC-2024-1887).",
            ],
            [
                "2.3 Spill Response Procedures",
                "",
                "Minor spills (less than 1 liter of non-hazardous material):",
                "  1. Don appropriate PPE",
                "  2. Contain spill with absorbent material from nearest spill kit",
                "  3. Clean up and dispose of materials in designated waste container",
                "  4. Complete Spill Report Form SA-301",
                "",
                "WARNING: For spills involving flammable materials, eliminate all",
                "ignition sources within 50 feet before beginning cleanup. Ensure",
                "adequate ventilation before entering the spill area.",
                "",
                "Major spills (hazardous materials or volume exceeding 1 liter):",
                "  1. Evacuate immediate area (minimum 100-foot radius)",
                "  2. Activate emergency alarm system",
                "  3. Contact Chemical Safety Officer (ext. 4250)",
                "  4. Do NOT attempt cleanup - wait for HazMat response team",
                "",
                "CAUTION: All personnel involved in spill response must undergo",
                "medical evaluation within 24 hours, regardless of exposure symptoms.",
            ],
            [
                "2.4 Chemical Waste Disposal",
                "",
                "All chemical waste must be segregated by hazard class and stored in",
                "approved containers at designated accumulation points. Maximum storage",
                "time at accumulation points is 90 days per EPA regulations.",
                "",
                "Waste categories and container requirements:",
                "  - Halogenated solvents: Red containers, max 5 gallons",
                "  - Non-halogenated solvents: Blue containers, max 5 gallons",
                "  - Acid waste: White containers with acid-resistant lining",
                "  - Base waste: Yellow containers",
                "  - Heavy metal waste: Green containers, double-walled",
                "",
                "WARNING: Never dispose of chemical waste through regular trash,",
                "sinks, or storm drains. Violations carry penalties up to $50,000",
                "per incident under RCRA regulations.",
                "",
                "Waste pickup is scheduled every Tuesday and Thursday at 0600.",
                "Pickup requests must be submitted by 1400 the previous day.",
            ],
            [
                "2.5 Laboratory Safety Protocols",
                "",
                "Laboratory personnel must follow additional safety protocols beyond",
                "standard plant requirements. Lab coats, safety goggles, and closed-toe",
                "shoes are mandatory at all times within laboratory spaces.",
                "",
                "Fume hood requirements:",
                "  - Sash height: Maximum 18 inches during operation",
                "  - Face velocity: 80-120 feet per minute (verified semi-annually)",
                "  - No storage of chemicals inside fume hoods",
                "  - Emergency shut-off accessible from outside the hood",
                "",
                "CAUTION: Fume hood alarms must never be overridden or disabled.",
                "If a fume hood alarm sounds, immediately cease operations and",
                "contact Facilities Maintenance (ext. 4300).",
                "",
                "Glassware inspection is required before each use. Chipped or cracked",
                "glassware must be disposed of in designated sharps containers.",
            ],
        ]
    },
    # Chapter 3: Machinery and Equipment (pages 11-15) - WARNING x4, CAUTION x2, DANGER x1
    {
        "title": "Chapter 3: Machinery and Equipment Safety",
        "pages": [
            [
                "3.1 Machine Guarding Standards",
                "",
                "All rotating, reciprocating, and transversing machinery must have",
                "proper guards installed per OSHA 29 CFR 1910.212. Guards must be",
                "secure and in good condition before machine operation.",
                "",
                "Types of guards required:",
                "  - Fixed guards: Permanently attached to machine frame",
                "  - Interlocked guards: Machine stops when guard is opened",
                "  - Adjustable guards: Allow material feeding while protecting operator",
                "  - Self-adjusting guards: Opening adjusts to material size",
                "",
                "WARNING: Operating machinery with guards removed or disabled is",
                "a terminable offense. Guards must be replaced before restarting",
                "any machine after maintenance procedures.",
                "",
                "Guard inspection checklist (Form SA-401) must be completed at the",
                "start of each shift by the designated machine operator.",
            ],
            [
                "3.2 Lockout/Tagout (LOTO) Procedures",
                "",
                "Energy isolation is required before any maintenance, servicing, or",
                "adjustment of machinery where unexpected startup could cause injury.",
                "",
                "LOTO procedure steps:",
                "  1. Notify affected employees",
                "  2. Shut down equipment using normal stopping procedure",
                "  3. Isolate all energy sources (electrical, hydraulic, pneumatic, thermal)",
                "  4. Apply individual lock and tag at each energy isolation point",
                "  5. Verify zero-energy state by attempting restart",
                "  6. Perform maintenance work",
                "  7. Remove tools and verify clear area",
                "  8. Remove locks and tags (only by the person who applied them)",
                "",
                "DANGER: Only qualified and authorized personnel may perform",
                "lockout/tagout procedures. Each worker must use their own personal",
                "lock - sharing locks is strictly prohibited.",
                "",
                "WARNING: Stored energy (capacitors, springs, elevated components,",
                "pressurized lines) must be dissipated before work begins.",
            ],
            [
                "3.3 Crane and Hoist Operations",
                "",
                "Overhead cranes and hoists require specific training certification",
                "(Crane Operator Level II or higher). Pre-operation inspection includes:",
                "",
                "  - Wire rope condition (check for kinks, bird-caging, broken wires)",
                "  - Hook condition (check latch, throat opening, twist)",
                "  - Brake function test",
                "  - Limit switch verification",
                "  - Load capacity label legibility",
                "",
                "WARNING: Never exceed the rated capacity of any lifting device.",
                "Load weight must be verified before each lift. When in doubt,",
                "use a certified scale or consult the engineering department.",
                "",
                "CAUTION: All rigging hardware (shackles, slings, spreader bars)",
                "must be inspected before each use and removed from service if",
                "any defect is found. Inspection records are maintained in the",
                "Rigging Equipment Database (Building B, Crane Office).",
            ],
            [
                "3.4 Powered Industrial Trucks (Forklifts)",
                "",
                "Forklift operators must hold valid certification per OSHA 29 CFR",
                "1910.178. Certification requires:",
                "  - 16 hours classroom training",
                "  - 8 hours practical driving assessment",
                "  - Evaluation every 3 years",
                "",
                "Operating rules:",
                "  - Speed limit: 5 mph inside buildings, 10 mph outdoors",
                "  - Pedestrians always have right of way",
                "  - Sound horn at intersections and blind corners",
                "  - Forks must be lowered when traveling",
                "  - No passengers permitted on forklift",
                "",
                "WARNING: Forklifts must not be used to lift personnel unless",
                "an approved work platform with guardrails is properly secured",
                "to the forks. Improvised lifting of workers is prohibited.",
                "",
                "Daily pre-operation checklist (Form SA-402) is mandatory.",
            ],
            [
                "3.5 Conveyor System Safety",
                "",
                "Conveyor systems present multiple hazard points including nip points,",
                "shear points, and crushing zones. All conveyor guards must be in place",
                "before system startup.",
                "",
                "Emergency stop (E-stop) locations:",
                "  - Every 50 feet along conveyor path",
                "  - At each loading and unloading station",
                "  - At operator control panels",
                "  - At maintenance access points",
                "",
                "CAUTION: E-stop pull cords must be tested weekly. Results are",
                "logged in the Conveyor Safety Register (electronic system C-SAF).",
                "",
                "Personnel must never ride on conveyors, reach into moving conveyor",
                "sections, or attempt to clear jams while the system is energized.",
                "All jam clearing procedures require full LOTO compliance.",
            ],
        ]
    },
    # Chapter 4: Electrical Safety (pages 16-20) - WARNING x3, CAUTION x2, DANGER x1
    {
        "title": "Chapter 4: Electrical Safety",
        "pages": [
            [
                "4.1 Electrical Hazard Recognition",
                "",
                "Electrical hazards are categorized by severity level:",
                "",
                "  Level 1 (120V-240V): Standard power outlets, small equipment",
                "  Level 2 (240V-600V): Motor control centers, distribution panels",
                "  Level 3 (600V-15kV): Substation equipment, primary feeders",
                "  Level 4 (>15kV): Utility connections, transformer banks",
                "",
                "Arc flash boundaries are posted at all electrical panels rated",
                "above 240V. Minimum approach distances must be observed by all",
                "personnel, including qualified electrical workers.",
                "",
                "DANGER: Contact with energized conductors above 50V can cause",
                "fatal electrocution. Only qualified electricians with appropriate",
                "arc flash PPE may work on or near energized equipment.",
                "",
                "WARNING: Ground Fault Circuit Interrupters (GFCIs) are required",
                "on all 120V outlets in wet or damp locations. Test GFCIs monthly.",
            ],
            [
                "4.2 Electrical Panel Requirements",
                "",
                "Electrical panel clearance requirements per NEC Article 110.26:",
                "  - 36 inches clear in front of panel",
                "  - 30 inches wide working space",
                "  - Clear path to exit from working space",
                "",
                "Panel labeling must include:",
                "  - Circuit identification for every breaker",
                "  - Arc flash hazard label with incident energy level",
                "  - Emergency contact number",
                "  - Date of last arc flash study",
                "",
                "WARNING: Panels must never be blocked by storage, equipment, or",
                "materials. Violations are subject to immediate corrective action",
                "and may result in facility shutdown by the electrical inspector.",
                "",
                "CAUTION: Only qualified personnel may open electrical panel doors.",
                "Report any signs of overheating (discoloration, burning smell,",
                "buzzing sounds) to Electrical Maintenance immediately (ext. 4310).",
            ],
            [
                "4.3 Extension Cord and Temporary Wiring",
                "",
                "Extension cords are permitted only for temporary use (maximum 90 days).",
                "Permanent wiring must be installed for ongoing power needs.",
                "",
                "Extension cord requirements:",
                "  - Three-prong grounded type only",
                "  - Rated for intended load and environment",
                "  - No daisy-chaining (cord-to-cord connections)",
                "  - Not routed through doorways, windows, or ceilings",
                "  - Inspected before each use for damage",
                "",
                "WARNING: Damaged extension cords must be immediately removed from",
                "service and tagged for repair or disposal. Never repair extension",
                "cords with electrical tape as a permanent fix.",
                "",
                "Temporary power distribution units (spider boxes) require approval",
                "from the Electrical Safety Coordinator before installation.",
            ],
            [
                "4.4 Static Electricity Control",
                "",
                "Electrostatic discharge (ESD) protection is required in:",
                "  - Electronics assembly areas",
                "  - Flammable liquid handling areas",
                "  - Powder coating operations",
                "  - Clean room environments",
                "",
                "ESD prevention measures:",
                "  - Grounding straps on personnel",
                "  - Conductive flooring or floor mats",
                "  - Ionizing air blowers at workstations",
                "  - Humidity control (40-60% RH)",
                "",
                "CAUTION: Static discharge in flammable atmospheres can cause",
                "ignition and explosion. Bonding and grounding of containers is",
                "required during all flammable liquid transfer operations.",
                "",
                "ESD audit results are posted quarterly in each affected area.",
            ],
            [
                "4.5 Emergency Power Systems",
                "",
                "The facility is equipped with the following backup power systems:",
                "",
                "  - Diesel generators (Buildings A, C, E): 2000 kW each",
                "  - UPS systems (Server Room, Control Room): 500 kVA",
                "  - Emergency lighting: Battery-backed, 90-minute minimum duration",
                "",
                "Generator testing schedule:",
                "  - Weekly: No-load run, 30 minutes",
                "  - Monthly: Load bank test, 2 hours",
                "  - Annually: Full load test with transfer switch verification",
                "",
                "Emergency lighting is tested monthly (30-second flash test) and",
                "annually (90-minute duration test). Results recorded in Form SA-403.",
                "",
                "The emergency power transfer sequence activates automatically within",
                "10 seconds of utility power loss. Manual override is available at",
                "the main switchgear room (Building A, basement level).",
            ],
        ]
    },
    # Chapter 5: Fire Safety (pages 21-25) - WARNING x2, CAUTION x2, DANGER x1
    {
        "title": "Chapter 5: Fire Prevention and Response",
        "pages": [
            [
                "5.1 Fire Prevention Measures",
                "",
                "Hot work permits are required for any operation involving open flames,",
                "sparks, or temperatures capable of igniting materials. This includes:",
                "  - Welding and cutting",
                "  - Grinding and abrasive cutting",
                "  - Soldering and brazing",
                "  - Heat guns and propane torches",
                "",
                "Hot work permit requirements:",
                "  - Fire watch during and 60 minutes after hot work",
                "  - Combustibles cleared within 35-foot radius",
                "  - Fire extinguisher within 10 feet",
                "  - Permit posted at work location",
                "",
                "WARNING: Hot work in confined spaces requires additional ventilation",
                "monitoring and a separate confined space entry permit. Both permits",
                "must be active and posted before work begins.",
                "",
                "CAUTION: Spontaneous combustion risk exists with oily rags and",
                "certain chemical-soaked materials. Dispose in approved metal",
                "containers with self-closing lids immediately after use.",
            ],
            [
                "5.2 Fire Extinguisher Requirements",
                "",
                "Fire extinguisher locations and types:",
                "",
                "  Class A (ordinary combustibles): Every 75 feet of travel distance",
                "  Class B (flammable liquids): Within 50 feet of hazard",
                "  Class C (electrical): At each electrical room and panel cluster",
                "  Class D (combustible metals): At each metal machining station",
                "  Class K (cooking oils): In each kitchen/break room",
                "",
                "WARNING: Use only the correct class of extinguisher for the fire type.",
                "Using water on electrical or chemical fires can cause electrocution,",
                "explosion, or spread of the fire. See classification chart posted",
                "at each extinguisher station.",
                "",
                "Monthly visual inspections and annual professional service are",
                "required for all extinguishers per NFPA 10.",
            ],
            [
                "5.3 Sprinkler and Suppression Systems",
                "",
                "Automatic fire suppression systems installed at this facility:",
                "",
                "  - Wet pipe sprinkler: Office areas, warehouses, assembly halls",
                "  - Dry pipe sprinkler: Unheated areas, loading docks",
                "  - Pre-action system: Server rooms, archive storage",
                "  - Clean agent (FM-200): Electronics manufacturing areas",
                "  - Foam system: Flammable liquid storage areas",
                "",
                "CAUTION: Minimum 18-inch clearance below sprinkler heads must be",
                "maintained at all times. Storage stacked too close to sprinklers",
                "will impede water distribution and reduce system effectiveness.",
                "",
                "System impairment procedures require notification to the fire",
                "department and activation of fire watch within 1 hour of shutdown.",
                "",
                "Quarterly flow tests and annual full inspections are conducted by",
                "the certified fire protection contractor (SafeGuard Systems Inc.).",
            ],
            [
                "5.4 Evacuation Procedures",
                "",
                "Upon hearing the fire alarm (continuous tone, 3-pulse pattern):",
                "  1. Stop all work immediately",
                "  2. Shut down equipment if safe to do so (max 30 seconds)",
                "  3. Proceed to nearest exit following posted evacuation routes",
                "  4. Do NOT use elevators",
                "  5. Report to designated assembly point for headcount",
                "  6. Remain at assembly point until all-clear is given",
                "",
                "DANGER: Re-entering the building during an active alarm is",
                "strictly prohibited. Only authorized fire brigade members and",
                "emergency responders may enter during an active alarm condition.",
                "",
                "Assembly points:",
                "  Building A personnel: Parking Lot P1 (north side)",
                "  Building B personnel: Parking Lot P2 (east side)",
                "  Building C-F personnel: Open field area (south side)",
                "",
                "Evacuation drills are conducted quarterly, with one unannounced",
                "drill per year. Target evacuation time: under 5 minutes.",
            ],
            [
                "5.5 Fire Investigation and Reporting",
                "",
                "All fires, regardless of size or whether extinguished by personnel,",
                "must be reported to the Safety Department within 1 hour. Reports",
                "require Form SA-501 (Fire Incident Report).",
                "",
                "Investigation team composition:",
                "  - Safety Manager (lead investigator)",
                "  - Area supervisor",
                "  - Facilities engineer",
                "  - Employee representative",
                "  - Insurance company representative (for major incidents)",
                "",
                "Investigation findings are reviewed by the Safety Committee within",
                "5 business days. Corrective actions are tracked in the Safety",
                "Action Database until verified complete.",
                "",
                "Post-fire recovery procedures include air quality testing,",
                "structural assessment, and equipment inspection before the",
                "affected area can be returned to normal operations.",
            ],
        ]
    },
    # Chapter 6: Confined Spaces and Fall Protection (pages 26-30) - WARNING x2, CAUTION x1, DANGER x0
    {
        "title": "Chapter 6: Confined Spaces and Fall Protection",
        "pages": [
            [
                "6.1 Confined Space Identification",
                "",
                "A confined space is defined as any area that:",
                "  - Is large enough for a worker to enter and perform work",
                "  - Has limited or restricted means of entry/exit",
                "  - Is not designed for continuous human occupancy",
                "",
                "Permit-required confined spaces at this facility:",
                "  - Storage tanks (T-101 through T-115)",
                "  - Reactor vessels (R-201 through R-208)",
                "  - Pipelines (diameter > 24 inches)",
                "  - Underground vaults and pits",
                "  - Silos and hoppers",
                "",
                "WARNING: Atmospheric testing is mandatory before and during all",
                "confined space entries. Oxygen levels must be between 19.5% and",
                "23.5%. Combustible gas must be below 10% of LEL.",
                "",
                "Entry permits are valid for one shift only and must display the",
                "entrant, attendant, and entry supervisor names.",
            ],
            [
                "6.2 Confined Space Entry Procedures",
                "",
                "Pre-entry requirements:",
                "  1. Obtain confined space entry permit (Form SA-601)",
                "  2. Conduct hazard assessment",
                "  3. Verify isolation of energy sources (LOTO)",
                "  4. Perform atmospheric testing with calibrated gas detector",
                "  5. Position ventilation equipment",
                "  6. Establish communication protocol",
                "  7. Position rescue equipment and notify rescue team",
                "",
                "During entry:",
                "  - Continuous atmospheric monitoring",
                "  - Attendant must maintain visual or voice contact at all times",
                "  - Entrant must wear retrieval harness with lifeline",
                "  - Communication check every 15 minutes minimum",
                "",
                "WARNING: If atmospheric conditions change or any emergency arises,",
                "all entrants must evacuate immediately. The attendant must never",
                "enter the space to attempt rescue.",
                "",
                "CAUTION: Rescue teams must be contacted before entry begins, not",
                "after an emergency occurs. Response time must be verified as",
                "adequate for the specific confined space configuration.",
            ],
            [
                "6.3 Fall Protection Requirements",
                "",
                "Fall protection is required at heights of:",
                "  - 4 feet in general industry areas",
                "  - 6 feet in construction zones",
                "  - Any work over hazardous equipment regardless of height",
                "",
                "Acceptable fall protection systems:",
                "  - Guardrail systems (42 inches top rail, 21 inches mid rail)",
                "  - Personal fall arrest systems (PFAS)",
                "  - Safety net systems",
                "  - Positioning device systems",
                "  - Travel restraint systems",
                "",
                "Personal fall arrest system components must be inspected before",
                "each use. Annual formal inspection by competent person required.",
                "Harnesses involved in a fall arrest event must be removed from",
                "service and destroyed.",
                "",
                "Anchor points must support 5,000 pounds per attached worker",
                "or be designed with a safety factor of 2:1.",
            ],
            [
                "6.4 Ladder and Scaffold Safety",
                "",
                "Portable ladder requirements:",
                "  - Inspect before each use",
                "  - Set at 4:1 angle (1 foot out for every 4 feet up)",
                "  - Extend 3 feet above landing surface",
                "  - Secure at top or have helper hold base",
                "  - Face ladder while climbing, maintain 3 points of contact",
                "",
                "Scaffold requirements:",
                "  - Erected by qualified personnel only",
                "  - Full-width planking with guardrails and toe boards",
                "  - Base plates on solid, level surface",
                "  - Tagged with inspection status (Green=safe, Red=unsafe)",
                "",
                "Maximum scaffold loading capacities are posted on each scaffold.",
                "Never exceed the rated capacity. Material and personnel weights",
                "must both be considered when calculating total load.",
                "",
                "Scaffolds must be re-inspected after any adverse weather event",
                "including high winds (>25 mph), heavy rain, or seismic activity.",
            ],
            [
                "6.5 Aerial Lift and Elevated Work Platforms",
                "",
                "Types of aerial lifts at this facility:",
                "  - Scissor lifts (indoor use): Max height 30 feet",
                "  - Boom lifts (outdoor use): Max height 60 feet",
                "  - Personnel baskets (crane-mounted): Emergency use only",
                "",
                "Operator certification requirements:",
                "  - Manufacturer-specific training for each lift type",
                "  - Annual recertification",
                "  - Pre-operation inspection checklist (Form SA-602)",
                "",
                "Operating restrictions:",
                "  - Wind speed: Maximum 28 mph for boom lifts",
                "  - Ground conditions: Firm, level surface required",
                "  - Proximity to power lines: Maintain 10-foot minimum clearance",
                "  - Outriggers must be fully deployed before raising platform",
                "",
                "Fall protection (harness and lanyard) is required in all boom lifts.",
                "Scissor lifts require guardrails; PFAS is optional but recommended.",
                "",
                "End of Manual - Document Control: Rev 4.2, Safety Dept., March 2025",
            ],
        ]
    },
]


def create_initial():
    os.makedirs(SAFETY_DIR, exist_ok=True)

    doc = pymupdf.open()

    page_num = 0
    for chapter_idx, chapter in enumerate(CHAPTERS):
        if chapter_idx == 0:
            # Title page
            page = doc.new_page(width=595, height=842)
            page.insert_text(
                pymupdf.Point(297, 300),
                chapter["title"],
                fontsize=28,
                fontname="hebo",
                color=(0, 0, 0.5),
            )
            page.insert_text(
                pymupdf.Point(297, 360),
                chapter["subtitle"].split("\n")[0],
                fontsize=14,
                fontname="helv",
                color=(0.3, 0.3, 0.3),
            )
            page.insert_text(
                pymupdf.Point(297, 385),
                chapter["subtitle"].split("\n")[1] if "\n" in chapter["subtitle"] else "",
                fontsize=12,
                fontname="helv",
                color=(0.3, 0.3, 0.3),
            )
            # Add centered title
            rect = pymupdf.Rect(72, 250, 523, 300)
            page.insert_textbox(rect, chapter["title"], fontsize=28, fontname="hebo",
                                color=(0, 0, 0.5), align=pymupdf.TEXT_ALIGN_CENTER)
            page_num += 1
            continue

        for page_content in chapter["pages"]:
            page = doc.new_page(width=595, height=842)

            # Header with chapter title
            page.insert_text(
                pymupdf.Point(72, 45),
                chapter["title"],
                fontsize=9,
                fontname="heit",
                color=(0.4, 0.4, 0.4),
            )
            # Separator line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 52), pymupdf.Point(523, 52))
            shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
            shape.commit()

            # Page content
            y_position = 80
            for line in page_content:
                if not line:
                    y_position += 8
                    continue

                # Determine style based on content
                if line.startswith(("1.", "2.", "3.", "4.", "5.", "6.")):
                    if line[1] == ".":
                        # Subsection header (e.g., "1.1 Introduction")
                        fontname = "hebo"
                        fontsize = 13
                        color = (0, 0, 0.3)
                        y_position += 6
                    else:
                        fontname = "helv"
                        fontsize = 10
                        color = (0, 0, 0)
                elif line.startswith("  "):
                    # Indented content
                    fontname = "helv"
                    fontsize = 10
                    color = (0.1, 0.1, 0.1)
                elif line.startswith("WARNING:") or line.startswith("CAUTION:") or line.startswith("DANGER:"):
                    fontname = "hebo"
                    fontsize = 10
                    color = (0, 0, 0)
                else:
                    fontname = "helv"
                    fontsize = 10
                    color = (0, 0, 0)

                # Use textbox for word wrapping
                rect = pymupdf.Rect(72, y_position, 523, y_position + 100)
                excess = page.insert_textbox(
                    rect,
                    line,
                    fontsize=fontsize,
                    fontname=fontname,
                    color=color,
                )
                # Estimate lines used
                chars_per_line = 70
                num_lines = max(1, (len(line) + chars_per_line - 1) // chars_per_line)
                y_position += num_lines * (fontsize + 3)

            # Footer with page number
            page_num += 1
            page.insert_text(
                pymupdf.Point(280, 820),
                f"Page {page_num}",
                fontsize=9,
                fontname="helv",
                color=(0.5, 0.5, 0.5),
            )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify keyword counts
    doc = pymupdf.open(OUTPUT)
    warning_count = 0
    caution_count = 0
    danger_count = 0
    for page in doc:
        text = page.get_text("text")
        warning_count += text.count("WARNING")
        caution_count += text.count("CAUTION")
        danger_count += text.count("DANGER")
    doc.close()
    print(f'Keyword counts - WARNING: {warning_count}, CAUTION: {caution_count}, DANGER: {danger_count}')
    print(f'Total pages: {page_num}')

    # Verify no annotations exist
    doc = pymupdf.open(OUTPUT)
    annot_count = 0
    for page in doc:
        for annot in page.annots():
            annot_count += 1
    doc.close()
    print(f'Annotation count (should be 0): {annot_count}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
