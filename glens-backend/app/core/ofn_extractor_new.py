from pathlib import Path
import json
import re
import os
from langchain_core.globals import set_debug
from langchain_openai import ChatOpenAI
from kor.nodes import Object, Text, Number
from kor import create_extraction_chain
import pymupdf
# import pymupdf.layout
import pymupdf4llm

set_debug=True
os.environ["TESSDATA_PREFIX"]= "D:\\Software_Tools\\tesseract-5.5.1\\tessdata"

llm = ChatOpenAI(
    openai_api_base="http://172.30.0.20:11434/v1",
    openai_api_key="ollama",
    model="gpt-oss:20b"
)



class OFNPDFExtractor:
    def __init__(self,input_folder, output_folder="output"):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)

    def extract_single_pdf(self,file_path):
        ofn = pymupdf.open(file_path)
        # texts = []
        # for page in ofn:
        #     texts.append(page.to_mar())
        
        # ofn_data = "\n".join(texts)
        ofn_data = pymupdf4llm.to_markdown(ofn)
        sections = ["header","blocks","moc","drive_baffle","agitator","insulation","nozzle"]
        results = {}
        for section in sections:
            results[section] = self.get_section_result(section, ofn_data)

        return results

    def get_section_result(self,section,text):
        section_chain = self.get_extraction_chain(section)
        section_result = section_chain.invoke(text)
        result_json = self.extract_result_json(section_result)
        print(result_json)
        return result_json

    def get_extraction_chain(self, section):
        section_schema = self.get_section_schema(section)
        extraction_chain = create_extraction_chain(llm = llm, node=section_schema,encoder_or_encoder_class="json")

        return extraction_chain
    @staticmethod
    def get_section_schema(section):

        if section == "header":
            schema = Object(
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
                                    ("Reactor Model - TR-1200", "TR-1200"),
                                    ("MSGL Reactor with Insulation (Non-GMP Model)","MSGL Reactor")
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
                                    ("Support - Wall mounted brackets.", "Wall mounted brackets."),
                                    ("Support \n Side Bracket.", "Side Bracket")
                                ]
                            ),
                            Text(
                                id="accessories",
                                description="Information on the extra added accessories.",
                                many=True,
                                examples=[
                                    ("Accessories: Insulation Cleats on Jacket.", "Insulation Cleats on Jacket."),
                                    ("SuAccessoriespport\nBase ring support provided.", "Base ring support provided."),
                                    ("Accessories - Insulation Cleats on jacket with support.", "Insulation Cleats on jacket with support."),
                                ],
                            ),
                        ]
            )

        elif section == "blocks":
            schema = Object(
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

        elif section == "moc":
            schema = Object(
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

        elif section == "drive_baffle":
            schema = Object(
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

        elif section == "agitator":
            schema = Object(
                id="reactor_agitator_schema",
                description="Extract Agitator Specification from GMM Pfaudler documents.",
                attributes=[
                    # ------ Agitator Table -----------------------
                    Object(
                        id="agitator",
                        description=".",
                        attributes=[

                            # --- HEADER FIELD ---
                            Text(id="flight", description="Agitator flight type (e.g., Single or Double)."),

                            # --- TABLE ROWS (MULTIPLE) ---
                            Object(
                                id="agitator_types",
                                many=True,
                                description="agitator specifications",
                                attributes=[
                                    Text(id="type",description="Types of the agitator"),
                                    Text(id="position",description="Position of the agitator"),
                                    Text(id="sweep_diameter_mm", description="Agitator sweep diameter description")
                                ],
                                examples=[
                                    ("RCI - Bottom As Per Gmm Standards",{"type":"RCI","position":"Bottom","sweep_diameter_mm":"As Per Gmm Standards"}),
                                    ("PBT - Top 150mm",{"type":"PBT","position":"Top","sweep_diameter_mm":"150mm"})
                                ]
                            ),

                            # --- EXTRA FIELDS AFTER TABLE ---
                            Number(id="shaft_diameter", description="Diameter of the Shaft"),
                            Number(id="rpm", description="RPM"),
                            Text(id="specific_gravity", description="specific gravity for agitator"),
                            Text(id="viscosity", description="Viscosity of liquid for agitator"),
                            Text(id="level_marking", description="Level marking"),
                            Text(id="stirring_volume", description="Stirring Volume")
                        ]
                    ),
                ]
            )

        elif section == "insulation":
            schema = Object(
                id="insulation_schema",
                attributes=[
                    Object(
                        # 11 - Insulation Block
                            id="insulation",
                            description="Insulation specifications (multiple sections like Top Head/Jacket/Cladding), each with Material and THK.",
                            many=True,
                            attributes=[
                                        Text(id="section"),
                                        Text(id="material"),
                                        Text(id="thk"),
                                    ]
                    )
                ]
            )


        elif section == "nozzle":
            schema = Object(
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
                                ],
                                examples=[("L 80 Outlet Btm\nhead\n80/50NB MSGL Glasslined bottom outlet\nvalve",{"nozzle_no":"L","size_dn":80,"service":"Outlet","location":"Btm head","description":"n80/50NB MSGL Glasslined bottom outlet valve"})]
                            ),

                            # --- AFTER TABLE SECTION ---
                            Object(
                                id="bottom_outlet_valve",
                                description="Bottom outlet valve specifications.",
                                attributes=[
                                    Text(id="type"),
                                    Text(id="name")
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
        
        return schema
    @staticmethod
    def extract_result_json(result):
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


if __name__ == "__main__":
    OFNExtractor = OFNPDFExtractor(".",".")
    results = OFNExtractor.extract_single_pdf("glens-backend\\app\\core\\088837_AE_250L_section_2.pdf")
    print(results)

