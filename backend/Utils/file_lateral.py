import os
import pandas as pd
from datetime import datetime
from .colors import cprint, COLORS
import xml.etree.ElementTree as ET
from .file_update_elements import update_elements

# Find ptdX Lateral files
def find_ptdx_files_lateral(project_folder):
    """Recursively scans for .ptdX files that contain both A_003 and I_003 elements."""
    file_list_lateral = []
    for root, _, files in os.walk(project_folder):
        for file in files:
            if file.endswith('.ptdX'):
                file_path = os.path.join(root, file)
                try:
                    tree = ET.parse(file_path)
                    root_elem = tree.getroot()
                    # Check for A_003 and I_003 elements anywhere in the tree
                    if root_elem.find('.//A_003') is not None and root_elem.find('.//I_003') is not None:
                        file_list_lateral.append(file_path)
                except ET.ParseError:
                    # Skip malformed XML files
                    pass
    return file_list_lateral





# Update ptdX Lateral files
def update_xml_files_lateral(folder_path, updates):
    """Updates specified elements in all .ptdX files."""
    file_list_lateral = find_ptdx_files_lateral(folder_path)
    
    updated_files_lateral = []
    cprint("update_xml_files_lateral called", COLORS["green"])
    
    for file_path in file_list_lateral:
                cprint(f"Processing: {file_path}", COLORS["yellow"])  
                try:
                    tree = ET.parse(file_path)
                    root_element = tree.getroot()
                    a_003 = root_element.find('.//A_003')
                    
                    if a_003 is not None:
                        # Find mainline file in parent folder
                        parent_folder = os.path.dirname(os.path.dirname(file_path))
                        for mainline_file in os.listdir(parent_folder):
                            if mainline_file.endswith('.ptdX'):
                                mainline_path = os.path.join(parent_folder, mainline_file)
                                try:
                                    mainline_tree = ET.parse(mainline_path)
                                    mainline_root = mainline_tree.getroot()
                                    a_002 = mainline_root.find('.//A_002')
                                    if a_002 is not None:
                                        upstream_ap = a_002.findtext('Upstream_AP')
                                        downstream_ap = a_002.findtext('Downstream_AP')
                                        
                                        if upstream_ap:
                                            up_mh = a_003.find('Upstream_MH')
                                            if up_mh is None:
                                                up_mh = ET.SubElement(a_003, 'Upstream_MH')
                                            up_mh.text = upstream_ap

                                        if downstream_ap:
                                            down_mh = a_003.find('Downstream_MH')
                                            if down_mh is None:
                                                down_mh = ET.SubElement(a_003, 'Downstream_MH')
                                            down_mh.text = downstream_ap
                                        
                                        break  # Done once we’ve found the mainline
                                except ET.ParseError:
                                    continue  # Skip malformed mainline files                    

                    updated = False

                    # Update elements inside <A_003>
                    updated |= update_elements(root_element, ".//A_003", updates)

                    # Update elements inside <I_003>
                    updated |= update_elements(root_element, ".//I_003", updates)
           

                    # Define the set of codes that require adjustment
                    valid_codes = {"AMH", "ACB", "ACOH", "ACOM", "ACOP", "ADP", "AEP", "AJB", 
                                "AM", "AOC", "ATC", "AWA", "AWW", "AZ", "MSA"}

                    # Adjust <Distance> and <Length_Surveyed> for specific codes
                    for of_003 in root_element.findall(".//OF_003"):
                        code_element = of_003.find("Code")
                        distance_element = of_003.find("Distance")

                        if code_element is not None and distance_element is not None:
                            code_value = code_element.text.strip()
                            if code_value in valid_codes:  # Check if code is in the allowed set
                                try:
                                    distance_value = float(distance_element.text.strip())
                                    if distance_value > 0:  
                                        adjusted_value = round(distance_value / 304.8) * 304.8 # Convert from Metric to Imperial and Round
                                        distance_element.text = str(adjusted_value)

                                        # Add the adjusted value to <Length_Surveyed>
                                        length_surveyed_element = root_element.find(".//I_003/Length_Surveyed")
                                        if length_surveyed_element is not None and length_surveyed_element.text:
                                            length_surveyed_value = float(length_surveyed_element.text.strip())
                                            length_surveyed_element.text = str(adjusted_value)

                                        updated = True
                                except ValueError:
                                    print(f"Could not parse <Distance> value in {file_path}")
                                   
                    # Background change: Modify <Material> if it exists
                    for model in root_element.findall(".//A_003"):
                        material_element = model.find("Material")
                        if material_element is not None:
                                if material_element.text.strip() == "ZZZ":  # Ensure no whitespace issues
                                    material_element.text = "XXX"
                                    updated = True
                   
                    for a_003 in root_element.findall(".//A_003"):
                        # Check if <Material> exists
                        material_element = a_003.find("Material")
                        material_value = material_element.text if material_element is not None else ""

                        # Determine if <Material> is "XXX" or has been changed to "XXX"
                        if material_value == "XXX" or ("Material" in updates and updates["Material"] == "XXX"):
                            pipe_joint_length_element = a_003.find("Pipe_Joint_Length")
                            if pipe_joint_length_element is not None: # If Material is "XXX" remove joint length
                                a_003.remove(pipe_joint_length_element)
                                updated = True

                    # Background change: Handle <Lining_Method> based on <Material> inside <A_003>
                    for a_003 in root_element.findall(".//A_003"):
                        material_element = a_003.find("Material")
                        
                        if material_element is not None:
                            material_value = material_element.text.strip()
                            lining_method_element = a_003.find("Lining_Method")

                            if material_value == "XXX":
                                if lining_method_element is None:
                                    # Create <Lining_Method> if it does not exist
                                    lining_method_element = ET.Element("Lining_Method")
                                    a_003.append(lining_method_element)

                                if lining_method_element.text != "CIP":
                                    # Update <Lining_Method> to "CIP" if it's not already set
                                    lining_method_element.text = "CIP"
                                    updated = True
                            else:
                                if lining_method_element is not None:
                                    # Remove <Lining_Method> if Material is anything other than "XXX"
                                    a_003.remove(lining_method_element)
                                    updated = True


                    # Iterate over all I_003 elements
                    for i_003 in root_element.findall(".//I_003"):
                        # Background change: Remove <PO_Number> if it exists inside <I_003>
                        po_number_element = i_003.find("PO_Number")
                        if po_number_element is not None:
                            i_003.remove(po_number_element)
                            updated = True

                        # Background change: Ensure correct values for inspection technology elements inside <I_003>                    
                        technology_updates = {
                            "Inspection_Technology_Used_CCTV": "true",
                            "Inspection_Technology_Used_Laser": "false",
                            "Inspection_Technology_Used_Sonar": "false",
                            "Inspection_Technology_Used_Sidewall": "false",
                            "Inspection_Technology_Used_Zoom": "false",
                            "Inspection_Technology_Used_Other": "false"
                        }

                        for key, value in technology_updates.items():
                            element = i_003.find(key)
                            if element is not None:
                                if element.text != value:
                                    element.text = value
                                    updated = True
                            else:
                                print(f"<{key}> not found in {file_path}, skipping.")

                        # Ensure <Purpose> exists with default "G" if missing
                        purpose_element = i_003.find("Purpose")
                        if purpose_element is None:
                            purpose_element = ET.Element("Purpose")
                            purpose_element.text = "G"
                            i_003.append(purpose_element)
                            updated = True

                        # Apply user updates (if Purpose is provided in the form, overwrite it)
                        if "Purpose" in updates:  # updates comes from the request
                            new_purpose_value = updates["Purpose"]
                            if purpose_element.text != new_purpose_value:
                                purpose_element.text = new_purpose_value
                                updated = True

                                 # Ensure <WorkOrder> exists if missing
                        work_order_element = i_003.find("WorkOrder")
                        if work_order_element is None:
                            work_order_element = ET.Element("WorkOrder")
                            work_order_element.text = updates.get("WorkOrder", "")  # Use provided value or empty string
                            i_003.append(work_order_element)
                            updated = True
                        elif "WorkOrder" in updates and work_order_element.text != updates["WorkOrder"]:
                            work_order_element.text = updates["WorkOrder"]
                            updated = True

                        # Apply user updates (if WorkOrder is provided in the form, overwrite it)
                        if "WorkOrder" in updates and updates["WorkOrder"].strip():
                            new_work_order_value = updates["WorkOrder"].strip()

                            work_order_element = i_003.find("WorkOrder")
                            if work_order_element is None:
                                work_order_element = ET.Element("WorkOrder")
                                i_003.append(work_order_element)
                            else:
                                work_order_element.text = new_work_order_value
                                updated = True

                        # Ensure <Project> exists if missing
                        project_element = i_003.find("Project")
                        if project_element is None:
                            project_element = ET.Element("Project")
                            project_element.text = updates.get("Project", "")  # Use provided value or empty string
                            i_003.append(project_element)
                            updated = True
                        elif "Project" in updates and project_element.text != updates["Project"]:
                            project_element.text = updates["Project"]
                            updated = True

                        # Apply user updates (if Project is provided in the form, overwrite it)
                        if "Project" in updates:  # updates comes from the request
                            new_project_value = updates["Project"]
                            if project_element.text != new_project_value:
                                project_element.text = new_project_value
                                updated = True

                        # Ensure <Pipe_Use> exists with default "G" if missing
                        pipeUse_element = a_003.find("Pipe_Use")
                        if pipeUse_element is None:
                            pipeUse_element = ET.Element("Pipe_Use")
                            pipeUse_element.text = "SS"
                            a_003.append(pipeUse_element)
                            updated = True

                        # Apply user updates (if Pipe_Use is provided in the form, overwrite it)
                        if "Pipe_Use" in updates:  # updates comes from the request
                            new_pipeUse_value = updates["Pipe_Use"]
                            if pipeUse_element.text != new_pipeUse_value:
                                pipeUse_element.text = new_pipeUse_value
                                updated = True
                    
                    
                    if updated:
                        # Backup the original file before saving changes
                        backup_path = file_path + ".bak"

                        # Check if the .bak file already exists and remove it before creating a new one
                        if os.path.exists(backup_path):
                            os.remove(backup_path)  # Replace the existing .bak file

                        # Backup the original file by renaming it to .bak
                        os.rename(file_path, backup_path)
                       
                        tree.write(file_path)  # Save updated XML back to file
                        updated_files_lateral.append(file_path)
                        cprint(f"File {file_path} updated!", COLORS["cyan"])
                    else:
                        cprint(f"No updates made for {file_path}", COLORS["red"])

                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")              
   
    return updated_files_lateral








# Export Lateral data to Excel
def export_lateral_to_excel(folder_path: str) -> str:
    """Parses ptdX files and exports relevant lateral data to an Excel file."""
    if not folder_path or not os.path.isdir(folder_path):
        raise ValueError("Invalid folder path")

    file_list = find_ptdx_files_lateral(folder_path)
    extracted_data = []

    for file_path in file_list:
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            file_name = os.path.basename(file_path)
            name = root.findtext(".//I_003/Surveyed_By", default="")
            direction = root.findtext(".//I_003/Direction", default="")
            cleaning = root.findtext(".//I_003/PreCleaning", default="")
            asset = root.findtext(".//A_003/Pipe_Segment_Reference", default="")
            upstream_mh = root.findtext(".//A_003/Upstream_MH", default="")
            downstream_mh = root.findtext(".//A_003/Downstream_MH", default="")

            raw_date = root.findtext(".//I_003/Inspection_Timestamp", default="")
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
            height = root.findtext(".//A_003/Height", default="0")
            size = round(float(height) / 25.4, 2) if height else ""

            length_surveyed = root.findtext(".//I_003/Length_Surveyed", default="0")
            distance = round(float(length_surveyed) / 304.8, 2) if length_surveyed else ""

            # Grab comments where MSA is present
            msa_comments = ""
            for of_003 in root.findall(".//OF_003"):
                code = of_003.findtext("Code", default="")
                if code == "MSA":
                    msa_comments = of_003.findtext("Comments", default="")
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

    export_path = os.path.join(folder_path, "export_lateral.xlsx")
    df.to_excel(export_path, index=False)

    return export_path