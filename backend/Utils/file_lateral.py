import os
import pandas as pd
from datetime import datetime
from .colors import cprint, COLORS
import xml.etree.ElementTree as ET
import logging
logger = logging.getLogger(__name__)

######################## Find ptdX Lateral files ########################
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





######################## Update ptdX Lateral files ########################
def update_xml_files_lateral(folder_path, updates):
    """Updates specified elements in all .ptdX files."""
    file_list_lateral = find_ptdx_files_lateral(folder_path)
    
    updated_files_lateral = []
    
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
                               
        # Background for A_003          
                    for a_003 in root_element.findall(".//A_003"):
                            material_element = a_003.find("Material")
                            material_value = material_element.text.strip() if material_element is not None and material_element.text else ""
                            # Modify <Material> from "ZZZ" to "XXX"
                            if material_value == "ZZZ":
                                material_element.text = "XXX"
                                material_value = "XXX"  # Update local variable for next steps
                                logging.info(f"4. Material has been updated to {material_element.text}")
                                updated = True
                            # Handle <Lining_Method> based on <Material>
                            lining_method_element = a_003.find("Lining_Method")
                            if material_value == "XXX":
                                if lining_method_element is None:
                                    lining_method_element = ET.Element("Lining_Method")
                                    a_003.append(lining_method_element)
                                if lining_method_element.text != "CIP":
                                    lining_method_element.text = "CIP"
                                    logging.info(f"6. Lining Method has been updated to {lining_method_element.text}")
                                    updated = True
                            else:
                                if lining_method_element is not None:
                                    a_003.remove(lining_method_element)
                                    logging.info(f"7. Lining Method has been removed")
                                    updated = True 

        # Update for A_003
                            # Apply user updates or ensure <Pipe_Use> exists with default "SS"
                            pipeUse_element = a_003.find("Pipe_Use")
                            if "Pipe_Use" in updates and updates["Pipe_Use"].strip():
                                new_pipeUse_value = updates["Pipe_Use"]
                                if pipeUse_element is None:
                                    pipeUse_element = ET.Element("Pipe_Use")
                                    a_003.append(pipeUse_element)
                                pipeUse_element.text = new_pipeUse_value
                                logging.info(f"Pipe Use has been updated with {new_pipeUse_value}")
                                updated = True
                            elif pipeUse_element is None:
                                # No update provided, and element doesn't exist — create with default "SS"
                                pipeUse_element = ET.Element("Pipe_Use")
                                pipeUse_element.text = "SS"
                                a_003.append(pipeUse_element)
                                logging.info(f"8. Pipe Use has been autofilled with SS")
                                updated = True
                            else:
                                logging.error(f"Pipe Use was not found")

                            owner_element = a_003.find("Owner")
                            if "Owner" in updates and updates["Owner"].strip():
                                new_owner_value = updates["Owner"]
                                if owner_element is None:
                                    owner_element = ET.Element("Owner")
                                    a_003.append(owner_element)
                                owner_element.text = new_owner_value
                                logging.info(f"Owner has been updated with {new_owner_value}")
                                updated = True


        # Update I_003 elements   
                    # Iterate over all I_003 elements
                    for i_003 in root_element.findall(".//I_003"):
                                              
                       # Apply user updates (if Customer is provided in the form, overwrite it)
                        customer_element = i_003.find("Customer")
                        if "Customer" in updates and updates["Customer"].strip():
                            new_customer_value = updates["Customer"]                           
                            if customer_element is None:
                                customer_element = ET.Element("Customer")
                                i_003.append(customer_element)                           
                            customer_element.text = new_customer_value # Always override with the new value
                            logging.info(f"Customer has been updated with {new_customer_value}")
                            updated = True
                        
                        
                        # Apply user updates (if Project is provided in the form, overwrite it)
                        project_element = i_003.find("Project")
                        if "Project" in updates and updates["Project"].strip():
                            new_project_value = updates["Project"]                           
                            if project_element is None:
                                project_element = ET.Element("Project")
                                i_003.append(project_element)                           
                            project_element.text = new_project_value # Always override with the new value
                            logging.info(f"Project has been updated with {new_project_value}")
                            updated = True

                         
                         
                         # Apply user updates (if WorkOrder is provided in the form, overwrite it)
                        work_order_element = i_003.find("WorkOrder")
                        if "WorkOrder" in updates and updates["WorkOrder"].strip():
                            new_work_order_value = updates["WorkOrder"]                           
                            if work_order_element is None:
                                work_order_element = ET.Element("WorkOrder")
                                i_003.append(work_order_element)
                            work_order_element.text = new_work_order_value # Always override with the new value
                            logging.info(f"WorkOrder has been updated with {new_work_order_value}")
                            updated = True
                        else:
                            logging.error(f"WorkOrder found string {work_order_element.text}")
                            

                                           
                        # Apply user updates or ensure <Purpose> exists with default "G"
                        purpose_element = i_003.find("Purpose")
                        if "Purpose" in updates and updates["Purpose"].strip():
                            new_purpose_value = updates["Purpose"]
                            if purpose_element is None:
                                purpose_element = ET.Element("Purpose")
                                i_003.append(purpose_element)
                            purpose_element.text = new_purpose_value # Always override with the new value
                            logging.info(f"Purpose has been updated with {new_purpose_value}")
                            updated = True
                        elif purpose_element is None:
                            # No update provided, and element doesn't exist — create with default "G"
                            purpose_element = ET.Element("Purpose")
                            purpose_element.text = "G"
                            i_003.append(purpose_element)
                            logging.info(f"9. Purpose has been autofilled with G")
                            updated = True
        
        
        # Background I_003 elements PO_Nunber, Technology       
                        # Background change: Remove <PO_Number> if it exists inside <I_003>
                        po_number_element = i_003.find("PO_Number")
                        if po_number_element is not None:
                            i_003.remove(po_number_element)
                            logging.info(f"10. PO Number has been removed")
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
                        updated_files_lateral.append(file_path)
                        cprint(f"File {file_path} updated!", COLORS["cyan"])
                    else:
                        cprint(f"No updates made for {file_path}", COLORS["red"])

                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")              
   
    return updated_files_lateral








############# Export Lateral data to Excel  ############
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
                    print(date)  # Example: 3/20/2025
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