import os
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET
from .colors import cprint, COLORS
from .file_update_elements import update_elements



# Find ptdX Mainline files
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





# Update ptdX Mainline files in the Background
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

                    # Update elements inside <A_002>
                    updated |= update_elements(root_element, ".//A_002", updates)

                    # Update elements inside <I_002>
                    updated |= update_elements(root_element, ".//I_002", updates)

                    # Define the set of codes that require adjustment
                    valid_codes = {"AMH", "ACB", "ACOH", "ACOM", "ACOP", "ADP", "AEP", "AJB", 
                                "AM", "AOC", "ATC", "AWA", "AWW", "AZ", "MSA"}

                    # Adjust <Distance> and <Length_Surveyed> for specific codes
                    for of_002 in root_element.findall(".//OF_002"):
                        code_element = of_002.find("Code")
                        distance_element = of_002.find("Distance")

                        if code_element is not None and distance_element is not None:
                            code_value = code_element.text.strip()
                            if code_value in valid_codes:  # Check if code is in the allowed set
                                try:
                                    distance_value = float(distance_element.text.strip())
                                    if distance_value > 0:  
                                        adjusted_value = round(distance_value / 304.8) * 304.8 # Convert from Metric to Imperial and Round
                                        distance_element.text = str(adjusted_value)

                                        # Add the adjusted value to <Length_Surveyed>
                                        length_surveyed_element = root_element.find(".//I_002/Length_Surveyed")
                                        if length_surveyed_element is not None and length_surveyed_element.text:
                                            length_surveyed_value = float(length_surveyed_element.text.strip())
                                            length_surveyed_element.text = str(adjusted_value)

                                        updated = True
                                except ValueError:
                                    print(f"Could not parse <Distance> value in {file_path}")
                                       
                    # Background change: Modify <Material> if it exists
                    for model in root_element.findall(".//A_002"):
                        material_element = model.find("Material")
                        if material_element is not None:
                                if material_element.text.strip() == "ZZZ":  # Ensure no whitespace issues
                                    material_element.text = "XXX"
                                    updated = True
                   
                    for a_002 in root_element.findall(".//A_002"):
                        # Check if <Material> exists
                        material_element = a_002.find("Material")
                        material_value = material_element.text if material_element is not None else ""

                        # Determine if <Material> is "XXX" or has been changed to "XXX"
                        if material_value == "XXX" or ("Material" in updates and updates["Material"] == "XXX"):
                            pipe_joint_length_element = a_002.find("Pipe_Joint_Length")
                            if pipe_joint_length_element is not None: # If Material is "XXX" remove joint length
                                a_002.remove(pipe_joint_length_element)
                                updated = True

                    # Background change: Handle <Lining_Method> based on <Material> inside <A_002>
                    for a_002 in root_element.findall(".//A_002"):
                        material_element = a_002.find("Material")
                        
                        if material_element is not None:
                            material_value = material_element.text.strip()
                            lining_method_element = a_002.find("Lining_Method")

                            if material_value == "XXX":
                                if lining_method_element is None:
                                    # Create <Lining_Method> if it does not exist
                                    lining_method_element = ET.Element("Lining_Method")
                                    a_002.append(lining_method_element)

                                if lining_method_element.text != "CIP":
                                    # Update <Lining_Method> to "CIP" if it's not already set
                                    lining_method_element.text = "CIP"
                                    updated = True
                            else:
                                if lining_method_element is not None:
                                    # Remove <Lining_Method> if Material is anything other than "XXX"
                                    a_002.remove(lining_method_element)
                                    updated = True

                    # Iterate over all I_002 elements
                    for i_002 in root_element.findall(".//I_002"):
                        # Background change: Remove <PO_Number> if it exists inside <I_002>
                        po_number_element = i_002.find("PO_Number")
                        if po_number_element is not None:
                            i_002.remove(po_number_element)
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
                                    updated = True
                            else:
                                print(f"<{key}> not found in {file_path}, skipping.")

                        # Ensure <Purpose> exists with default "G" if missing
                        purpose_element = i_002.find("Purpose")
                        if purpose_element is None:
                            purpose_element = ET.Element("Purpose")
                            purpose_element.text = "G"
                            i_002.append(purpose_element)
                            updated = True

                        # Apply user updates (if Purpose is provided in the form, overwrite it)
                        if "Purpose" in updates:  # updates comes from the request
                            new_purpose_value = updates["Purpose"]
                            if purpose_element.text != new_purpose_value:
                                purpose_element.text = new_purpose_value
                                updated = True

                         # Ensure <WorkOrder> exists if missing
                        work_order_element = i_002.find("WorkOrder")
                        if work_order_element is None:
                            work_order_element = ET.Element("WorkOrder")
                            work_order_element.text = updates.get("WorkOrder", "")  # Use provided value or empty string
                            i_002.append(work_order_element)
                            updated = True
                        elif "WorkOrder" in updates and work_order_element.text != updates["WorkOrder"]:
                            work_order_element.text = updates["WorkOrder"]
                            updated = True

                        # Apply user updates (if WorkOrder is provided in the form, overwrite it)
                        if "WorkOrder" in updates and updates["WorkOrder"].strip():
                            new_work_order_value = updates["WorkOrder"].strip()

                            work_order_element = i_002.find("WorkOrder")
                            if work_order_element is None:
                                work_order_element = ET.Element("WorkOrder")
                                i_002.append(work_order_element)
                            else:
                                work_order_element.text = new_work_order_value
                                updated = True

                                # Ensure <Project> exists if missing
                        project_element = i_002.find("Project")
                        if project_element is None:
                            project_element = ET.Element("Project")
                            project_element.text = updates.get("Project", "")  # Use provided value or empty string
                            i_002.append(project_element)
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
                        pipeUse_element = a_002.find("Pipe_Use")
                        if pipeUse_element is None:
                            pipeUse_element = ET.Element("Pipe_Use")
                            pipeUse_element.text = "SS"
                            a_002.append(pipeUse_element)
                            updated = True

                        # Apply user updates (if Pipe_Use is provided in the form, overwrite it)
                        if "Pipe_Use" in updates:  # updates comes from the request
                            new_pipeUse_value = updates["Pipe_Use"]
                            if pipeUse_element.text != new_pipeUse_value:
                                pipeUse_element.text = new_pipeUse_value
                                updated = True

                    # Background change: Update <Total_Length> with <Length_Surveyed> if "MSA" is NOT in <Code>
                    code_elements = root_element.findall(".//OF_002/Code")
                    code_contains_msa = any(code_element.text and "MSA" in code_element.text for code_element in code_elements)

                    if not code_contains_msa:
                        length_surveyed_element = root_element.find(".//I_002/Length_Surveyed")
                        
                        if length_surveyed_element is not None and length_surveyed_element.text:
                            length_surveyed_value = length_surveyed_element.text.strip()
                            
                            for a_002 in root_element.findall(".//A_002"):
                                total_length_element = a_002.find("Total_Length")

                                if total_length_element is None:
                                    # Create <Total_Length> if it does not exist
                                    total_length_element = ET.Element("Total_Length")
                                    a_002.append(total_length_element)

                                if total_length_element.text != length_surveyed_value:
                                    # Update <Total_Length> with <Length_Surveyed> value
                                    total_length_element.text = length_surveyed_value
                                    updated = True

                    # Update <Comments> based on <Code>, <Distance>, and <Direction>
                    direction_element = root_element.find(".//I_002/Direction")
                    direction_value = direction_element.text.strip() if direction_element is not None else ""

                    for of_002 in root_element.findall(".//OF_002"):
                        code_element = of_002.find("Code")
                        distance_element = of_002.find("Distance")
                        comments_element = of_002.find("Comments")

                        if code_element is not None and distance_element is not None:
                            code_value = code_element.text.strip()
                            try:
                                distance_value = float(distance_element.text.strip())
                            except ValueError:
                                print(f"Could not parse <Distance> value in {file_path}")
                                continue  # Skip this entry if Distance is invalid

                            # Determine correct manhole based on Direction
                            upstream_mh = root_element.findtext(".//A_002/Upstream_AP", default="")
                            downstream_mh = root_element.findtext(".//A_002/Downstream_AP", default="")

                            if direction_value == "D":
                                start_mh = upstream_mh
                                end_mh = downstream_mh
                            elif direction_value == "U":
                                start_mh = downstream_mh
                                end_mh = upstream_mh
                            else:
                                print(f"Unknown Direction '{direction_value}' in {file_path}, skipping.")
                                continue

                            # Handle Start Inspection Comment
                            if code_value in ["AMH", "ACB", "ACOH", "ACOM", "ACOP", "ADP", "AJB", 
                                "AM", "AOC", "ATC", "AWA", "AWW", "AZ"] and distance_value == 0:
                                comment_text = f"Start Inspection: {start_mh}"
                            # Handle End Inspection Comment
                            elif code_value in ["AMH", "ACB", "ACOH", "ACOM", "ACOP", "ADP", "AEP", "AJB", 
                                "AM", "AOC", "ATC", "AWA", "AWW", "AZ"] and distance_value > 0:
                                comment_text = f"End Inspection: {end_mh}"
                            else:
                                continue  # Skip if no matching condition

                            if comments_element is None:
                                comments_element = ET.Element("Comments")
                                of_002.append(comments_element)

                            comments_element.text = comment_text
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
                        updated_files.append(file_path)
                        cprint(f"File {file_path} updated!", COLORS["cyan"])
                    else:
                        cprint(f"No updates made for {file_path}", COLORS["red"])

                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")              
    
    return updated_files




# Export Mainline data to Excel
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





