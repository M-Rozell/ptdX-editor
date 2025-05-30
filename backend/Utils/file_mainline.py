import os
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET
from .colors import cprint, COLORS
import logging
logger = logging.getLogger(__name__)



######################## Find ptdX Mainline files ########################
def find_ptdx_files(project_folder):
    """Recursively scans for .ptdX files that contain both A_002 and I_002 elements."""
    file_list = []
    for root, _, files in os.walk(project_folder):
        for file in files:
            if file.endswith('.ptdX'):
                file_path = os.path.join(root, file)
                try:
                    tree = ET.parse(file_path)
                    root_elem = tree.getroot()
                    # Check for A_002 and I_002 elements anywhere in the tree
                    if root_elem.find('.//A_002') is not None and root_elem.find('.//I_002') is not None:
                        file_list.append(file_path)
                except ET.ParseError:
                    # Skip malformed XML files
                    pass
    return file_list





######################## Update ptdX Mainline files ########################

def update_xml_files(folder_path, updates):
    """Updates specified elements in all .ptdX files."""
    updated_files = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.ptdX'):
                file_path = os.path.join(root, file)
                try:
                    tree = ET.parse(file_path)
                    root_element = tree.getroot()

                    updated = False

                    # Define the set of codes that require adjustment
                    valid_codes = {"AMH", "ACB", "ACOH", "ACOM", "ACOP", "ADP", "AEP", "AJB", 
                                "AM", "AOC", "ATC", "AWA", "AWW", "AZ", "MSA"}

        
        # Background  Distance, Material, Lining_Method, Comments                                
                    
                    # Initialize tracking variables
                    length_surveyed_value = None
                    code_contains_msa = False

                    # Get Direction and Manholes
                    direction_element = root_element.find(".//I_002/Direction")
                    direction_value = direction_element.text.strip() if direction_element is not None else ""

                    upstream_mh = root_element.findtext(".//A_002/Upstream_AP", default="")
                    downstream_mh = root_element.findtext(".//A_002/Downstream_AP", default="")

                    # Process each OF_002 entry
                    for of_002 in root_element.findall(".//OF_002"):
                        code_element = of_002.find("Code")
                        distance_element = of_002.find("Distance")
                        comments_element = of_002.find("Comments")

                        if code_element is None or distance_element is None:
                            continue

                        code_value = code_element.text.strip()

                        # Track if "MSA" appears in any code
                        if "MSA" in code_value:
                            code_contains_msa = True

                        try:
                            distance_value = float(distance_element.text.strip())
                        except ValueError:
                            print(f"Could not parse <Distance> value in {file_path}")
                            continue

                        # === Adjust Distance & Length_Surveyed for valid codes ===
                        if code_value in valid_codes and distance_value > 0:
                            adjusted_value = round(distance_value / 304.8) * 304.8  # Metric to Imperial, rounded
                            distance_element.text = str(adjusted_value)

                            # Update <Length_Surveyed>
                            length_surveyed_element = root_element.find(".//I_002/Length_Surveyed")
                            if length_surveyed_element is not None:
                                length_surveyed_element.text = str(adjusted_value)
                                length_surveyed_value = str(adjusted_value)
                                logging.info(f"1. Length has been updated from {distance_value} to {adjusted_value}")
                                updated = True

                        # === Set <Comments> based on code and distance ===
                        if direction_value == "D":
                            start_mh = upstream_mh
                            end_mh = downstream_mh
                        elif direction_value == "U":
                            start_mh = downstream_mh
                            end_mh = upstream_mh
                        else:
                            print(f"Unknown Direction '{direction_value}' in {file_path}, skipping.")
                            continue

                        start_codes = {"AMH", "ACB", "ACOH", "ACOM", "ACOP", "ADP", "AJB", "AM", "AOC", "ATC", "AWA", "AWW", "AZ"}
                        end_codes = {"AMH", "ACB", "ACOH", "ACOM", "ACOP", "ADP", "AEP", "AJB", "AM", "AOC", "ATC", "AWA", "AWW", "AZ"}

                        if code_value in start_codes and distance_value == 0:
                            comment_text = f"Start Inspection: {start_mh}"
                        elif code_value in end_codes and distance_value > 0:
                            comment_text = f"End Inspection: {end_mh}"
                            logging.info(f"2. Comments for Start and End Inspection have been updated")
                        else:
                            comment_text = None

                        if comment_text:
                            if comments_element is None:
                                comments_element = ET.Element("Comments")
                                of_002.append(comments_element)
                            comments_element.text = comment_text                            
                            updated = True

                        # === Set <Total_Length> if needed ===
                        if not code_contains_msa and length_surveyed_value:
                            for a_002 in root_element.findall(".//A_002"):
                                total_length_element = a_002.find("Total_Length")
                                if total_length_element is None:
                                    total_length_element = ET.Element("Total_Length")
                                    a_002.append(total_length_element)
                                if total_length_element.text != length_surveyed_value:
                                    total_length_element.text = length_surveyed_value
                                    logging.info(f"3. Total Length has been updated to {length_surveyed_value}")
                                    updated = True

                    
                    
        # Background for A_002          
                    for a_002 in root_element.findall(".//A_002"):
                            material_element = a_002.find("Material")
                            material_value = material_element.text.strip() if material_element is not None and material_element.text else ""
                            # Modify <Material> from "ZZZ" to "XXX"
                            if material_value == "ZZZ":
                                material_element.text = "XXX"
                                material_value = "XXX"  # Update local variable for next steps
                                logging.info(f"4. Material has been updated to {material_element.text}")
                                updated = True
                            # If <Material> is "XXX", remove <Pipe_Joint_Length>
                            if material_value == "XXX" or ("Material" in updates and updates["Material"] == "XXX"):
                                pipe_joint_length_element = a_002.find("Pipe_Joint_Length")
                                if pipe_joint_length_element is not None:
                                    a_002.remove(pipe_joint_length_element)
                                    logging.info(f"5. Pipe Joint Length removed")
                                    updated = True
                            # Handle <Lining_Method> based on <Material>
                            lining_method_element = a_002.find("Lining_Method")
                            if material_value == "XXX":
                                if lining_method_element is None:
                                    lining_method_element = ET.Element("Lining_Method")
                                    a_002.append(lining_method_element)
                                if lining_method_element.text != "CIP":
                                    lining_method_element.text = "CIP"
                                    logging.info(f"6. Lining Method has been updated to {lining_method_element.text}")
                                    updated = True
                            else:
                                if lining_method_element is not None:
                                    a_002.remove(lining_method_element)
                                    logging.info(f"7. Lining Method has been removed")
                                    updated = True  
                    
        # Update for A_002
                            # Apply user updates or ensure <Pipe_Use> exists with default "SS"
                            pipeUse_element = a_002.find("Pipe_Use")
                            if "Pipe_Use" in updates and updates["Pipe_Use"].strip():
                                new_pipeUse_value = updates["Pipe_Use"]
                                if pipeUse_element is None:
                                    pipeUse_element = ET.Element("Pipe_Use")
                                    a_002.append(pipeUse_element)
                                pipeUse_element.text = new_pipeUse_value
                                logging.info(f"Pipe Use has been updated with {new_pipeUse_value}")
                                updated = True
                            elif pipeUse_element is None:
                                # No update provided, and element doesn't exist — create with default "SS"
                                pipeUse_element = ET.Element("Pipe_Use")
                                pipeUse_element.text = "SS"
                                a_002.append(pipeUse_element)
                                logging.info(f"8. Pipe Use has been autofilled with SS")
                                updated = True
                            else:
                                logging.error(f"Pipe Use was not found")

                            owner_element = a_002.find("Owner")
                            if "Owner" in updates and updates["Owner"].strip():
                                new_owner_value = updates["Owner"]
                                if owner_element is None:
                                    owner_element = ET.Element("Owner")
                                    a_002.append(owner_element)
                                owner_element.text = new_owner_value
                                logging.info(f"Owner has been updated with {new_owner_value}")
                                updated = True

                    
        # Update I_002 elements   
                    # Iterate over all I_002 elements
                    for i_002 in root_element.findall(".//I_002"):
                       
                       
                       # Apply user updates (if Customer is provided in the form, overwrite it)
                        customer_element = i_002.find("Customer")
                        if "Customer" in updates and updates["Customer"].strip():
                            new_customer_value = updates["Customer"]                           
                            if customer_element is None:
                                customer_element = ET.Element("Customer")
                                i_002.append(customer_element)                           
                            customer_element.text = new_customer_value # Always override with the new value
                            logging.info(f"Customer has been updated with {new_customer_value}")
                            updated = True
                        
                        
                        # Apply user updates (if Project is provided in the form, overwrite it)
                        project_element = i_002.find("Project")
                        if "Project" in updates and updates["Project"].strip():
                            new_project_value = updates["Project"]                           
                            if project_element is None:
                                project_element = ET.Element("Project")
                                i_002.append(project_element)                           
                            project_element.text = new_project_value # Always override with the new value
                            logging.info(f"Project has been updated with {new_project_value}")
                            updated = True

                         
                         
                         # Apply user updates (if WorkOrder is provided in the form, overwrite it)
                        work_order_element = i_002.find("WorkOrder")
                        if "WorkOrder" in updates and updates["WorkOrder"].strip():
                            new_work_order_value = updates["WorkOrder"]                           
                            if work_order_element is None:
                                work_order_element = ET.Element("WorkOrder")
                                i_002.append(work_order_element)
                            work_order_element.text = new_work_order_value # Always override with the new value
                            logging.info(f"WorkOrder has been updated with {new_work_order_value}")
                            updated = True
                        else:
                            logging.error(f"WorkOrder found string {work_order_element.text}")
                            

                                           
                        # Apply user updates or ensure <Purpose> exists with default "G"
                        purpose_element = i_002.find("Purpose")
                        if "Purpose" in updates and updates["Purpose"].strip():
                            new_purpose_value = updates["Purpose"]
                            if purpose_element is None:
                                purpose_element = ET.Element("Purpose")
                                i_002.append(purpose_element)
                            purpose_element.text = new_purpose_value # Always override with the new value
                            logging.info(f"Purpose has been updated with {new_purpose_value}")
                            updated = True
                        elif purpose_element is None:
                            # No update provided, and element doesn't exist — create with default "G"
                            purpose_element = ET.Element("Purpose")
                            purpose_element.text = "G"
                            i_002.append(purpose_element)
                            logging.info(f"9. Purpose has been autofilled with G")
                            updated = True

                        
        # Background I_002 elements PO_Nunber, Technology       
                        # Background change: Remove <PO_Number> if it exists inside <I_002>
                        po_number_element = i_002.find("PO_Number")
                        if po_number_element is not None:
                            i_002.remove(po_number_element)
                            logging.info(f"10. PO Number has been removed")
                            updated = True

                        # Background change: Ensure correct values for inspection technology elements inside <I_002>                    
                        technology_updates = {
                            "Inspection_Technology_Used_CCTV": "true",
                            "Inspection_Technology_Used_Laser": "false",
                            "Inspection_Technology_Used_Sonar": "false",
                            "Inspection_Technology_Used_Sidewall": "false",
                            "Inspection_Technology_Used_Zoom": "false",
                            "Inspection_Technology_Used_Other": "false"
                        }
                        for key, value in technology_updates.items():
                            element = i_002.find(key)
                            if element is not None:
                                if element.text != value:
                                    element.text = value
                                    logging.info(f"11. Technology used has been autofilled with CCTV")
                                    updated = True
                            else:
                                print(f"<{key}> not found in {file_path}, skipping.")

                    

                # Finalizing    
                    if updated:
                        # Backup the original file before saving changes
                        backup_path = file_path + ".bak"

                        # Check if the .bak file already exists and remove it before creating a new one
                        if os.path.exists(backup_path):
                            os.remove(backup_path)  # Replace the existing .bak file

                        # Backup the original file by renaming it to .bak
                        os.rename(file_path, backup_path)
                                                         
                        tree.write(file_path, encoding="utf-8", xml_declaration=True)  # Save updated XML back to file
                        updated_files.append(file_path)
                        '''ET.dump(i_002)'''
                        cprint(f"File {file_path} updated!", COLORS["cyan"])
                    else:
                        cprint(f"No updates made for {file_path}", COLORS["red"])

                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")              
    
    return updated_files










######################## Export Mainline data to Excel   ########################
def export_mainline_to_excel(folder_path: str) -> str:
    """Parses ptdX files and exports relevant mainline data to an Excel file."""
    if not folder_path or not os.path.isdir(folder_path):
        raise ValueError("Invalid folder path")

    file_list = find_ptdx_files(folder_path)
    extracted_data = []

    for file_path in file_list:
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            file_name = os.path.basename(file_path)
            name = root.findtext(".//I_002/Surveyed_By", default="")
            direction = root.findtext(".//I_002/Direction", default="")
            cleaning = root.findtext(".//I_002/PreCleaning", default="")
            asset = root.findtext(".//A_002/Pipe_Segment_Reference", default="")
            upstream_mh = root.findtext(".//A_002/Upstream_AP", default="")
            downstream_mh = root.findtext(".//A_002/Downstream_AP", default="")

            raw_date = root.findtext(".//I_002/Inspection_Timestamp", default="")
            if raw_date:
                try:
                    # Extract only the YYYY-MM-DD part (remove everything after 'T')
                    date_part = raw_date.split("T")[0]

                    # Convert to datetime and get the date part
                    parsed_date = datetime.strptime(date_part, "%Y-%m-%d").date()

                    # Format the date part as M/D/YYYY
                    date = "{}/{}/{}".format(parsed_date.month, parsed_date.day, parsed_date.year)
                    print(date)  # Example: 2/20/2025
                except ValueError as e:
                    print(f"Error parsing date '{raw_date}': {e}")
                    date = ""
            else:
                print("No date found!")
                date = ""
                       
            # Convert from Metric to Imperial
            height = root.findtext(".//A_002/Height", default="0")
            size = round(float(height) / 25.4, 2) if height else ""

            length_surveyed = root.findtext(".//I_002/Length_Surveyed", default="0")
            distance = round(float(length_surveyed) / 304.8, 2) if length_surveyed else ""

            # Grab comments where MSA is present
            msa_comments = ""
            for of_002 in root.findall(".//OF_002"):
                code = of_002.findtext("Code", default="")
                if code == "MSA":
                    msa_comments = of_002.findtext("Comments", default="")
                    break  # Use the first occurrence

            extracted_data.append([
                file_name, date, name, asset, upstream_mh, downstream_mh, size, distance, direction, msa_comments, cleaning
            ])

        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

    # Create a DataFrame and save as Excel
    df = pd.DataFrame(extracted_data, columns=[
        "File Name", "Date", "Name", "Asset", "Upstream MH", "Downstream MH", "Size", "Distance", "Direction", "MSA", "Cleaning"
    ])

    export_path = os.path.join(folder_path, "export_mainline.xlsx")
    df.to_excel(export_path, index=False)

    return export_path





