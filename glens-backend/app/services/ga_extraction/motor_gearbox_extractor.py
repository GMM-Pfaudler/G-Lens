from app.services.ga_extraction.corrosion_and_rpm_helper import extract_gearbox_section_from_json,extract_table_data,get_motor_speed_context_block
import re

def remove_leading_two_digits(s: str) -> str:
    return re.sub(r'^\d{2}', '', s).lstrip()

def extract_drive_data(file_path: str):
    raw_data = extract_table_data(file_path=file_path)
    # print(f"[DEBUG] Raw Data Length: {len(raw_data)}")

    drive_data = {}

    gearbox_section = extract_gearbox_section_from_json(raw_data)
    # print(f"[DEBUG] Gearbox Section: {gearbox_section}")
    if gearbox_section:
        cleaned_gearbox = remove_leading_two_digits(gearbox_section)
        drive_data["DRIVE GEARBOX"] = cleaned_gearbox

    motor_type_block = get_motor_speed_context_block(raw_data)
    # print(f"[DEBUG] Motor Block: {motor_type_block}")
    if motor_type_block:
        cleaned_motor = remove_leading_two_digits(motor_type_block)
        drive_data["DRIVE MOTOR"] = cleaned_motor

    # print(f"[FINAL DRIVE DATA] {drive_data}")
    return drive_data
