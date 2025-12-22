# import pdfplumber
# print("Hello World!")
# pdf = pdfplumber.open(r'data\\technical_specification_sample.pdf')
# page = pdf.pages[0]
# page.extract_table()
# import win32com.client
# import win32com.client.connect
# outlook = win32com.client.GetActiveObject

# print(outlook)
# import glob
# import uuid

# from pdf2image import convert_from_path
# folder = r"D:\\Projects\\Test_Python\\drawing_pdf"
# lst = glob.glob(folder + "\\*.pdf")

# for pdf_file_path in lst:
#     images = convert_from_path(pdf_file_path, 500, poppler_path=r'D:\\Software_and_Tools\\Poppler_for_pdf_to_image\\Release-24.08.0-0\\poppler-24.08.0\\Library\\bin')
#     for i, image in enumerate(images):
#         fname = 'image'+str(uuid.uuid4())+str(i)+'.png'
#         image.save(fname, "PNG")
# import pymupdf
# import json

# pdf_file = r"data\\technical_specification_sample.pdf"

# doc = pymupdf.open(pdf_file)
# for page in doc: 
#   text = page.get_text()
#   tabs = page.find_tables()
#   if tabs.tables:
#     print(tabs[0].extract())

# print(text)

# ------------------------ OLLAMA DIRECT PROMPT EXTRACTION --------------------------------
# from openai import OpenAI

# client = OpenAI(
#     # This is the default and can be omitted
#     # base_url="https://ollama.com",
#     base_url="http://172.30.0.20:11434/v1",
#     api_key= "ollama" # os.environ.get("OPENAI_API_KEY"),
# )

# chat_completion = client.chat.completions.create(
#     messages=[{
#         'role': 'user',
#         'content': """
# can you give me value of possible key-value pairs you can find here from the following raw data ?
# Note:- Return in proper JSON format key and value like object, And also Explain Why did you choose that value.
# Raw Data:-

# FR-MKT-006
# GMM PFAUDLER LIMITED
# TECHNICAL SPECIFICATION
# FOR
# GLASS LINED EQUIPMENTS
# GMM Pfaudler Quote No: STANDARD
# Name: TEMPLATE
# Attention: Mitul Patel
# Date: 09/12/2025
# Page 1 of 5
# Rev. 5
# Model
# MSGL Reactor
# Tag No.
# 6300
# Capacity
# CE_6300L
# Glass
# Pfaudler World Wide 9100 (Dark Blue), Plug Free
# Code
# ASME SECTION VIII, DIV.I. (LATEST) - Unstamped
# Dimension
# 1950 ID And Overall Height 2825 mm mm, Other Dimension as per Our Bulletin DIN Reactors _
# CE".
# Nominal Volume
# 6300 Ltr
# Total Volume
# 7535 Ltr
# Shell Thickness
# 18 mm
# Top Dished End
# 20 mm
# Bottom Dished End
# 20 mm
# Weight
# Approximately 7000 Kgs..
# Jacket Type
# Plain Jacket with 2100 OD
# Jacket Volume
# 860 Ltr
# Shell Thickness
# 10 mm
# Dish Thickness
# 14 mm
# Heat Transfer Area
# 16.6 SQ.M
# Joint Efficiency
# Inner Vessel
# For No RT -> 0.7 = Inner Shell, 0.85 = Both Dished End
# Jacket
# For No RT -> 0.7 = Inner Shell, 0.85 = Dished End
# Design Pressure
# Inner Vessel
# F. V. / 6 bar(g)
# Jacket
# F. V. / 6 bar(g)
# Hydraulic Test
# Pressure
# Pressure tested in accordance with Code.
# Design
# Temperature
# Inner Vessel
# -28.8°C to 200°C
# Jacket
# -28.8°C to 200°C
# NDT
# Inner Vessel
# UT
# Main weld seams of inner vessel to be 100% ultrasonically tested for
# internal quality assurance measure only. 
# Jacket
# Nil
 
# Paint
# Pre-Treatment Removal by blasting.
# 2 Coats of RAL 5015 (Sky Blue)
# Corrosion
# Allowance
# Glassed Surface
# 0.0
# Wetted With Jacket
# Fluid
# 1.0
# Non Wetted Surface
# 0.5
# Page 2 of 5
# Stress Relief
# All heating cycles will be as required for glassing process.
# Drilling Standard
# GMM fItting PN - 10 DIN 2673 & Spare ASME 150#
# Material of
# Construction
# Shell, Head
# SA 516 Gr.60(EQ)
# Nozzle Necks & Body
# Flange
# SA 181 Gr. 60 / SA 836
# Split Flanges
# SA 516 Gr. 70 (CS)
# Manhole C-Clamps
# SA307 Gr. B / SA 563 Gr. B
# Fasteners
# Pressure Part
# MS - IS : 1363 / 1367 CL. 4.6 / 4
# Non-Pressure Part
# MS - IS : 1363 / 1367 CL. 4.6 / 4
# Gasket
# PTFE Enveloped NON ASBESTOS
# Manhole Cover
# MSGL
# Manhole Protection
# Ring
# MSGL
# Spring Balance
# Assembly
# MS
# Sight/Light Glass
# Flanges
# MS
# Earthing
# 01 No.- Earthing Cleat (MS)
# Lantern Support
# MS
# Lantern Guard
# MS
# Drive Base Ring
# MS
# Drive Hood
# Not Applicable
# Jacket (Shell, Head)
# SA 516 Gr. 60 / 70
# Jacket Nozzle
# Nozzle Neck : SA 106 Gr. B & Flanges : SA 105
# Jacket Coupling+Plug
# SA 105
# Spillage Collection
# Tray
# No
# Nozzles
# Top Head
# Page 3 of 5
# Nozzle
# No.
# Size
# (DN)
# Service
# Location
# Description
# N1
# 500
# Manhole
# Top Head
# MS Spring Loaded MSGL Manhole Cover With
# 100 Dia Sight Glass Assembly
# N2
# 150
# Spare
# Top Head
# Wooden Blind Flange
# N3
# 150
# Spare
# Top Head
# Wooden Blind Flange
# N5
# 250
# Baffle /
# Thermowell
# Top Head
# With Dial Thermometer.
# N6
# 150
# Light Glass
# Top Head
# Light Glass Assembly
# N7
# 250
# Spare
# Top Head
# Wooden Blind cover
# N9
# 150
# Spare
# Top Head
# Wooden Blind cover
# N10
# 150
# Spare
# Top Head
# Wooden Blind cover
# M
# 200
# Agitator
# Top Head
# Mechanical Seal
# L
# 150
# Outlet
# Btm
# head
# 150/100NB MSGL Glasslined bottom outlet
# valve
# Bottom Outlet Valve
# Gland
# MSGL Gland Type Upper To Open BOV 150x100 (GPF 204)
# Jacket Nozzle
# 04 Nos. DN80 Jacket Nozzle
# Support
# Side Bracket
# Agitator
# Flight
# Single
# Type
# Sweep Diameter (in mm)
# RCI
# 1100
# Shaft Diameter
# 100
# RPM
# 104
# Specific Gravity
# ≤ 1.6
# Viscosity
# 100 CPS
# Level Marking
# No
# Stirring Volume :
# 270-375 Ltr
# Baffle
# 1 No. Beavertail type Baffle with Flange Design
# Sensing Volume :
# 1010-1135 Ltr
# Drive
# Gear Box
# Bonfiglioli Make In-Line Helical Gear Box
# Motor
# BBL Make 15 (11 KW) HP IE2 Flameproof Motor
# Shaft Closure
# Hi-Fab Make Single Mechanical Seal
# Inborad Face
# Carbon vs SIC
# Sealing
# Viton
# Housing
# MS
# Other
# Page 4 of 5
# Alternate Seal
# No
# Accessories
# This document is confidential & proprietary in nature and is the exclusive property of GMM Pfaudler Limited. Any unauthorized
# distribution, disclosure, or dissemination of this document, in whole or in part, is strictly prohibited and may result in legal action. If you
# have received this document in error, please promptly notify us. Thank you for your cooperation.
# Page 5 of 5
# """
#     }],
#     model='gpt-oss:20b'
# )

# res = chat_completion.choices[0].message.content
# print(res)


# response = client.responses.create(
#     model="gpt-3.5-turbo",
#     instructions="You are a coding assistant that talks like a pirate.",
#     input="How do I check if a Python object is an instance of a class?",
# )

# print(response.output_text)



# Extraction Using KOR Library 

import json
import re
from langchain_core.globals import set_debug
# set_debug(True)
from langchain_openai import ChatOpenAI
from kor.nodes import Object, Text, Number
from kor import create_extraction_chain

# LangChain-compatible LLM wrapper
llm = ChatOpenAI(
    openai_api_base="http://172.30.0.20:11434/v1",
    openai_api_key="ollama",
    model="gpt-oss:20b"
    # model="gpt-oss:120b-cloud"
)

reactor_header_schema = Object(
    id="reactor_header",
    description="Extract Header Schema from GMM Pfaudler Documents.",
    attributes=[
                Text(
                    id="quote_no",
                    description="Value of 'GMM Pfaudler Quote No'",
                    examples=[
                        ("GMM Pfaudler Quote No: Q-2026-45", "Q-2026-45"),
                        ("Quote No.\nQ-3301", "Q-3301")
                    ]
                ),
                Text(
                    id="name",
                    description="Value of Name field",
                    examples=[
                        ("Name: Prototype Reactor", "Prototype Reactor"),
                        ("Name\nTest Reactor Unit", "Test Reactor Unit")
                    ]
                ),
                Text(
                    id="attention",
                    description="Person mentioned after 'Attention'",
                    examples=[
                        ("Attention: John Doe", "John Doe"),
                        ("Attention\nAlice Smith", "Alice Smith")
                    ]
                ),
                Text(
                    id="date",
                    description="Document date in DD/MM/YYYY format",
                    examples=[
                        ("Date: 15/01/2026", "15/01/2026"),
                        ("Date\n22/03/2026", "22/03/2026")
                    ]
                ),
                Text(
                    id="model",
                    description="Model name of the equipment.",
                    examples=[
                        ("Model\nXTR-500", "XTR-500"),
                        ("Reactor Model - TR-1200", "TR-1200")
                    ]
                ),
                Text(
                    id="tag_no",
                    description="Tag number associated with the reactor.",
                    examples=[
                        ("Tag No.\n5012", "5012"),
                        ("Tag No.\n1207", "1207")
                    ]
                ),
                Text(
                    id="capacity",
                    description="Capacity value stated in the spec.",
                    examples=[
                        ("Capacity\nCE_500L", "CE_500L"),
                        ("Total Capacity - CE_1200L", "CE_1200L")
                    ]
                ),
                Text(
                    id="glass",
                    description="Glass specification (e.g. type, color).",
                    examples=[
                        ("Glass\nPfaudler Clear 9200 (Light Blue)", "Pfaudler Clear 9200 (Light Blue)"),
                        ("Glass Specification - Pfaudler World 9300 (Green)", "Pfaudler World 9300 (Green)")
                    ]
                ),
                Text(
                    id="code",
                    description="Design code such as ASME or DIN.",
                    examples=[
                        ("Code: ASME SECTION VIII, DIV.I", "ASME SECTION VIII, DIV.I"),
                        ("Code: DIN 28011", "DIN 28011")
                    ]
                ),
                Text(
                    id="dimension",
                    description="Dimension details including ID, height, or any referenced bulletin notes.",
                    examples=[
                        ("Dimension: 1820 ID And Overall Height 2650 mm, Other dimension as per bulletin XYZ-12.", 
                        "1820 ID And Overall Height 2650 mm, Other dimension as per bulletin XYZ-12."),
                        ("Dimension\n2100 mm ID and total height 3000 mm, refer to DIN Series 500.", 
                        "2100 mm ID and total height 3000 mm, refer to DIN Series 500."),
                        ("Dimension : 1750 ID; Height 2400 mm; Additional notes as per internal bulletin.", 
                        "1750 ID; Height 2400 mm; Additional notes as per internal bulletin.")
                    ]
                ),
                Text(
                    id="weight",
                    description="Approximate equipment weight.",
                    examples=[
                        ("Weight: Around 6200 Kgs.", "Around 6200 Kgs."),
                        ("Weight\nApproximately 5400 kilograms.", "Approximately 5400 kilograms."),
                        ("Weight - Approx. 7500 kg", "Approx. 7500 kg")
                    ]
                ),
                Text(
                    id="hydraulic_test_pressure",
                    description="Hydraulic test pressure statement or compliance note.",
                    examples=[
                        ("Hydraulic Test Pressure: Tested as per applicable code.", "Tested as per applicable code."),
                        ("Hydraulic Test\nPressure - Pressure test conducted according to ASME guidelines.", 
                        "Pressure test conducted according to ASME guidelines."),
                        ("Hydraulic Test Pressure: Verified per standard inspection procedures.", 
                        "Verified per standard inspection procedures.")
                    ]
                ),
                Text(
                    id="paint",
                    description="Painting details including coatings, colors, and pre-treatment.",
                    examples=[
                        ("Paint: Surface cleaned with blasting, followed by 1 coat of epoxy primer and 2 coats of RAL 6005.", 
                        "Surface cleaned with blasting, followed by 1 coat of epoxy primer and 2 coats of RAL 6005."),
                        ("Paint\nBlasted metal with dual coating of industrial blue paint.", 
                        "Blasted metal with dual coating of industrial blue paint."),
                        ("Paint - Anti-corrosive primer + polyurethane topcoat (RAL 2002).", 
                        "Anti-corrosive primer + polyurethane topcoat (RAL 2002).")
                    ]
                ),
                Text(
                    id="stress_relief",
                    description="Stress relief or heat treatment details.",
                    examples=[
                        ("Stress Relief: Thermal cycle applied as per manufacturing process.", 
                        "Thermal cycle applied as per manufacturing process."),
                        ("Stress Relief\nHeat treatment performed depending on vessel size.", 
                        "Heat treatment performed depending on vessel size."),
                        ("Stress Relief - Stress relieving cycle executed according to standard practice.", 
                        "Stress relieving cycle executed according to standard practice.")
                    ]
                ),
                Text(
                    id="drilling_standard",
                    description="Drilling or flange standard used for fittings.",
                    examples=[
                        ("Drilling Standard: Fittings conform to PN-16 DIN 2633 & spare ANSI 150#.", 
                        "Fittings conform to PN-16 DIN 2633 & spare ANSI 150#."),
                        ("Drilling Standard\nDIN PN-10 flanges with additional ASME Class 150 spare.", 
                        "DIN PN-10 flanges with additional ASME Class 150 spare."),
                        ("Drilling Standard - As per PN-6 DIN 2576 and backup ASME 125#.", 
                        "As per PN-6 DIN 2576 and backup ASME 125#.")
                    ]
                ),
                Text(
                    id="support",
                    description="Support type or structural mounting details.",
                    examples=[
                        ("Support: Saddle type support.", "Saddle type support."),
                        ("Support\nBase ring support provided.", "Base ring support provided."),
                        ("Support - Wall mounted brackets.", "Wall mounted brackets.")
                    ]
                ),
                Text(
                    id="accessories",
                    description="Information on the extra added accessories.",
                    examples=[
                        ("Accessories: Insulation Cleats on Jacket.", "Insulation Cleats on Jacket."),
                        ("SuAccessoriespport\nBase ring support provided.", "Base ring support provided."),
                        ("Accessories - Insulation Cleats on jacket with support.", "Insulation Cleats on jacket with support."),
                    ],
                ),
            ]
)

reactor_blocks_schema = Object(
    id="reactor_block_schema",
    description="Extract Specific Blocks data from GMM Pfaudler documents.",
    attributes=[
        # 1 — Dimension Block
        Object(
            id="dimension",
            description="Dimension details including volume and thickness information.",
            attributes=[
                Text(id="summary"),
                Text(id="nominal_volume"),
                Text(id="total_volume"),
                Text(id="shell_thickness"),
                Text(id="top_dished_end_thickness"),
                Text(id="bottom_dished_end_thickness")
            ]
        ),

        # 2 — Jacket Block
        Object(
            id="jacket",
            description="Jacket-related specifications.",
            attributes=[
                Text(id="type"),
                Text(id="volume"),
                Text(id="shell_thickness"),
                Text(id="dish_thickness"),
                Text(id="heat_transfer_area")
            ]
        ),

        # 3 — Joint Efficiency Block
        Object(
            id="joint_efficiency",
            description="Efficiency parameters for weld joints.",
            attributes=[
                Text(id="inner_vessel"),
                Text(id="jacket")
            ]
        ),

        #4 - Design Pressure
        Object(
            id="design_pressure",
            description="Pressure values for components.",
            attributes=[
                Text(id="inner_vessel"),
                Text(id="jacket")
            ]
        ),

        # 5 - Design Temp
        Object(
            id="design_temperature",
            description="Temperature Values for components.",
            attributes=[
                Text(id="inner_vessel"),
                Text(id="jacket")
            ]
        ),

        # 6 - NDT
        Object(
            id="ndt",
            description="NDT Values for Components",
            attributes=[
                Text(id="inner_vessel"),
                Text(id="jacket"),
            ]
        ),

        # 7 - Corrosion Allowance
        Object(
            id="corrosion_allowance",
            description = "corrosion values for different surfaces.",
            attributes=[
                Text(id="glassed_surface"),
                Text(id="wetted_with_jacket_fluid"),
                Text(id="non_wetted_surface")
            ]
        ),
    ]
)

reactor_moc_schema = Object(
    id="reactor_moc_data",
    description="Extract detailed data of Material of Specification from GMM Pfaudler documents.",
    attributes=[
        #8 - Material of Construction
        Object(
            id="material_of_construction",
            description ="Material Related specification and vlaues.",
            attributes=[
                Text(id="shell_head"),
                Text(id="nozzle_neck_&_body_flange"),
                Text(id="split_flanges"),
                Text(id="manhole_c_clamps"),
                Object(
                    id="fasteners",
                    description="Specifications for pressure and non-pressure part fasteners.",
                    attributes=[
                        Text(id="pressure_part"),
                        Text(id="non_pressure_part")
                    ]
                ),
                Text(id="gasket"),
                Text(id="manhole_cover"),
                Text(id="manhole_protection_ring"),
                Text(id="spring_balance_assembly"),
                Text(id="sight_light_glass_flanges"),
                Text(id="earthing"),
                Text(id="lantern_support"),
                Text(id="lantern_guard"),
                Text(id="drive_base_ring"),
                Text(id="drive_hood"),
                Text(id="jacket_shell_head"),
                Text(id="jacket_nozzle"),
                Text(id="jacket_coupling+plug"),
                Text(id="spillage_collection_tray")
            ]
        ),
    ]
)

reactor_drive_baffle_schema = Object(
    id="reactor_drive_baffle_schema",
    description="Extract Drive and Baffle data from GMM Pfuadler documents.",
    attributes=[
        # 9 - Baffle
        Object(
            id="baffle",
            description="Baffle and it's volume details",
            attributes=[
                Text(id="type"),
                Text(id="sensing_volume")
            ]
        ),

        # 10 - Drive
        Object(
            id="drive",
            description="Drive and Shaft Closure related values.",
            attributes=[
                Text(id="gear_box"),
                Text(id="motor"),
                Object(
                    id="shaft_closure",
                    description="values for Shaft Closure.",
                    attributes=[
                        Text(id="type"),
                        Text(id="inboard_face"),
                        Text(id="sealing"),
                        Text(id="housing"),
                        Text(id="other"),
                        Text(id="alternate_seal")
                    ]
                )
            ]
        ),
    ]
)

reactor_agitator_schema = Object(
    id="reactor_agitator_schema",
    description="Extract Agitator Specification from GMM Pfaudler documents.",
    attributes=[
        # ------ Agitator Table -----------------------
        Object(
            id="agitator",
            description=".",
            attributes=[

                # --- HEADER FIELD ---
                Text(id="flight", description="Agitator flight type (e.g., Single)."),

                # --- TABLE ROWS (MULTIPLE) ---
                Object(
                    id="agitator_types",
                    many=True,
                    description="""Extract all fields exactly as defined in the schema.
                                    RULES:
                                    - If a field is missing in the document, set it to "".
                                    - Never omit fields.
                                    - Always include all fields, even if empty.
                                    - Follow the schema structure strictly.""",
                    attributes=[
                        Text(id="type"),
                        Number(id="sweep_diameter_mm")
                    ]
                ),

                # --- EXTRA FIELDS AFTER TABLE ---
                Number(id="shaft_diameter"),
                Number(id="rpm"),
                Text(id="specific_gravity"),
                Text(id="viscosity"),
                Text(id="level_marking"),
                Text(id="stirring_volume")
            ]
        ),
    ]
)

reactor_insulation_schema = Object(
    id="reactor_insulation_schema",
    description="Extract detailed Insulaton specification from GMM Pfaudler documents.",
    attributes=[
        # 11 - Insulation Block
        Object(
            id="insulation",
            description="Insulation specifications (multiple sections like Top Head/Jacket/Cladding), each with Material and THK.",
            attributes=[
                Object(
                    id="sections",
                    many=True,
                    description="One entry per insulated section (e.g., Top Head, Jacket, Cladding).",
                    attributes=[
                        Text(id="section"),
                        Text(id="material"),
                        Text(id="thk"),
                    ]
                )
            ]
        ),
    ]
)

# Schema
reactor_nozzle_schema = Object(
    id="reactor_nozzle_schema",
    description="Extract detailed Nozzle Table specifications from GMM Pfaudler documents.",
    attributes=[
        # ---------------- Nozzle Table ------------
        Object(
            id="nozzle_section",
            description="All nozzle-related information including nozzle table and additional valves/nozzles.",
            attributes=[

                # --- NOZZLE TABLE (MANY ROWS) ---
                Object(
                    id="nozzles",
                    description="Individual nozzle entries.",
                    many=True,
                    attributes=[
                        Text(id="nozzle_no"),
                        Number(id="size_dn"),
                        Text(id="service"),
                        Text(id="location"),
                        Text(id="description"),
                    ]
                ),

                # --- AFTER TABLE SECTION ---
                Object(
                    id="bottom_outlet_valve",
                    description="Bottom outlet valve specifications.",
                    attributes=[
                        Text(id="type"),
                    ]
                ),

                Object(
                    id="jacket_nozzle",
                    description="Jacket nozzle count and specifications.",
                    attributes=[
                        Text(id="description")
                    ]
                ),
            ]
        ),

        
        
    ]
)

# Extraction chain (now works!)
header_chain = create_extraction_chain(
    llm=llm,
    node=reactor_header_schema,
    encoder_or_encoder_class="json",
)

blocks_chain = create_extraction_chain(
    llm=llm,
    node=reactor_blocks_schema,
    encoder_or_encoder_class="json",
)

moc_chain = create_extraction_chain(
    llm=llm,
    node=reactor_moc_schema,
    encoder_or_encoder_class="json",
)

drive_baffle_chain = create_extraction_chain(
    llm=llm,
    node=reactor_drive_baffle_schema,
    encoder_or_encoder_class="json",
)

agitator_chain = create_extraction_chain(
    llm=llm,
    node=reactor_agitator_schema,
    encoder_or_encoder_class="json",
)

insulation_chain = create_extraction_chain(
    llm=llm,
    node=reactor_insulation_schema,
    encoder_or_encoder_class="json",
)

nozzle_chain = create_extraction_chain(
    llm=llm,
    node=reactor_nozzle_schema,
    encoder_or_encoder_class="json",
)


raw_text = """
FR-MKT-006
GMM PFAUDLER LIMITED
TECHNICAL SPECIFICATION
FOR
GLASS LINED EQUIPMENTS
GMM Pfaudler Quote No: 060333
Name: Alkem Laboratories Ltd
Attention: ABHISHEK MAHADIK
Date: 11/12/2025
Page 1 of 5
Rev. 5
Model
MSGL Reactor with Insulation (Non-GMP Model)
Tag No.
R-2109
Capacity
CE_4000L - NEW
Glass
Pfaudler Pharma Glass PPG (Light Blue), Plug Free
Code
ASME SECTION VIII, DIV.I. (LATEST) - Unstamped
Dimension
1756 ID And Overall Height 2285 mm, Other Dimension as per Our Bulletin DIN Reactors _ CE".
Nominal Volume
Total Volume
Shell Thickness
Jacket Type
Spiral Jacket with 1900 OD
Jacket Volume
Heat Transfer Area
Design Pressure
Inner Vessel
F. V. / 6 bar(g)
Jacket
F. V. / 6 bar(g)
Hydraulic Test
Pressure
Pressure tested in accordance with Code.
Design
Temperature
Inner Vessel
-28.8°C to 200°C
Jacket
-28.8°C to 200°C
NDT
Inner Vessel
UT
Main weld seams of inner vessel to be 100% ultrasonically tested for
internal quality assurance measure only. 
Jacket
 
Paint
Pre-Treatment Removal by blasting.
2 Coats of RAL 5015 (Sky Blue)
Corrosion
Allowance
Glassed Surface
0.0
Wetted With Jacket Fluid
1.0
Non Wetted Surface
0.5
Stress Relief
All heating cycles will be as required for glassing process.
Drilling
Standard
GMM fItting PN - 10 DIN 2673 & Spare ASME 150#
Material of
Construction
Shell, Head
SA 516 Gr.60(EQ)
Nozzle Necks & Body
Flange
SA 181 Gr. 60 / SA 836
Split Flanges
SA 516 Gr. 70 (CS)
Manhole C-Clamps
SA307 Gr. B / SA 563 Gr. B - Zinc Electro Plated (20µ) & Yellow
Passivation
Fasteners
Pressure Part
MS - IS : 1363 / 1367 CL. 4.6 / 4
Page 2 of 5
Non-Pressure Part
MS - IS : 1363 / 1367 CL. 4.6 / 4
Gasket
PTFE Enveloped NON ASBESTOS
Manhole Cover
MS-PFA Lined
Manhole Protection Ring
MS-PFA Lined
Spring Balance Assembly
MS
Sight/Light Glass Flanges
MS
Earthing
02 No.- Earthing Boss (SS)
Lantern Support
MS
Lantern Guard
SS304
Drive Base Ring
MS
Drive Hood
SS304
Jacket (Shell, Head)
SA 516 Gr. 60 / 70
Jacket Nozzle
Nozzle Neck : SA 106 Gr. B & Flanges : SA 105
Jacket Coupling+Plug
SA 105
Spillage Collection Tray
Yes
Nozzles
Top Head
Page 3 of 5
Nozzle
No.
Size
(DN)
Service
Location
Description
N1
500
Manhole
Top Head
MS Spring Loaded MS PFA
LINED Manhole Cover &
Protection Ring With 100 Dia
Sight Glass Assembly
N2
250
BAFFLE
Top Head
WITH M12 TANTALUM TIP &
RTD SENSOR WITH 150 X 80
REDUCING FLANGE + MSGL
BLIND FLANGE
N3
150
PROCESS INLET WITH DIP PIPE
Top Head
WITH 80NB CS PTFE DIP PIPE +
MSGL BLIND FLANGE
N5
100
RUPTURE DISCU/PSV/COMPOUND
GAUGE/PRESSURE INDICATOR
TRANSMITTER/N2 INLET
Top Head
WITH 100 X 80 REDUCING
FLANGE + MSGL BLIND FLANGE
N6
100
Light Glass
Top Head
Light Glass Assembly
N7
100
VAPOUR OUTLET
Top Head
WITH MSGL BLIND FLANGE
N9
150
REFLUX LINE
Top Head
WITH 150 X 40 REDUCING
FLANGE + MSGL BLIND FLANGE
N10
250
Spare
Top Head
WITH MSGL BLIND FLANGE
M
200
Agitator Entry
Top Head
Mechanical seal
L
100
Outlet
Btm
head
100/80NB MSGL Glasslined
bottom outlet valve with M12
Tantalum Tip & RTD Sensor
Bottom Outlet Valve
Gland
MSGL Gland Type Upper To Open BOV 100x80 + T/Tip + RTD Sensor
(GPF 2801)
Jacket Nozzle
04 Nos. DN50 Jacket Nozzle
Support
Side Bracket
Agitator
Flight
Double
Type
Sweep Diameter (in mm)
RCI - Bottom
RCI - Top
Shaft Diameter
100
RPM
96
Specific Gravity
≤ 1.2
Viscosity
100 CPS
Level Marking
Yes
Baffle
1 No. Beavertail type Baffle with FlangeDesign & M12 tantalum tip - Extra Long
Page 4 of 5
Drive
Gear Box
Bonfiglioli Make In-Line Helical Gear Box
Motor
BBL Make 7.5 (5.5 KW) HP IE2 + Invertor Duty Flameproof Motor
Shaft Closure
Leak-Proof Make Single Mechanical Seal
Inborad Face
Carbon vs SIC
Sealing
Teflon
Housing
MS
Other
Alternate Seal
No
Insulation
Top Head
Material
Mineral wool
THK
25 MM
Jacket
Material
Mineral wool + Puff
THK
75+50 MM
Cladding
Material
SS304
THK
3 MM
Accessories
Volumatric Marking Required
This document is confidential & proprietary in nature and is the exclusive property of GMM Pfaudler Limited. Any unauthorized
distribution, disclosure, or dissemination of this document, in whole or in part, is strictly prohibited and may result in legal action. If you
have received this document in error, please promptly notify us. Thank you for your cooperation.
Page 5 of 5
"""

def extract_json(result):
    raw = result.get("raw", "").strip()

    if not raw:
        return {}

    # Remove <json> tags
    raw = raw.replace("<json>", "").replace("</json>", "")

    # Extract first {...} JSON block
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return {}

    try:
        return json.loads(match.group(0))
    except Exception:
        return {}

header_result = header_chain.invoke(raw_text)
blocks_result = blocks_chain.invoke(raw_text)
moc_result = moc_chain.invoke(raw_text)
drive_baffle_result = drive_baffle_chain.invoke(raw_text)
agitator_result = agitator_chain.invoke(raw_text)
insulation_result = insulation_chain.invoke(raw_text)
nozzle_result = nozzle_chain.invoke(raw_text)

header = extract_json(header_result)
blocks = extract_json(blocks_result)
moc = extract_json(moc_result)
drive_baffle = extract_json(drive_baffle_result)
agitator = extract_json(agitator_result)
insulation = extract_json(insulation_result)
nozzle = extract_json(nozzle_result)

tech_result = {
    "header": header,
    "blocks": blocks,
    "moc": moc,
    "drive_baffle": drive_baffle,
    "agitator": agitator,
    "insulation": insulation,
    "nozzle": nozzle,
}

print(json.dumps(tech_result, indent=2))
