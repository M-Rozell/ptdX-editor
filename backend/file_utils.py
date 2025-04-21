import os
import xml.etree.ElementTree as ET



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


def find_ptdx_lateral_files(project_folder):
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






# Update files function
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
                                        print(f"Updating <Distance> from {distance_value} to {adjusted_value} in {file_path}")
                                        distance_element.text = str(adjusted_value)

                                        # Add the adjusted value to <Length_Surveyed>
                                        length_surveyed_element = root_element.find(".//I_002/Length_Surveyed")
                                        if length_surveyed_element is not None and length_surveyed_element.text:
                                            length_surveyed_value = float(length_surveyed_element.text.strip())
                                            print(f"Updating <Length_Surveyed> from {length_surveyed_value} to {adjusted_value} in {file_path}")
                                            length_surveyed_element.text = str(adjusted_value)

                                        updated = True
                                except ValueError:
                                    print(f"Could not parse <Distance> value in {file_path}")

                    
                    
                    # Background change: Modify <Material> if it exists
                    for model in root_element.findall(".//A_002"):
                        material_element = model.find("Material")
                        if material_element is not None:
                                print(f"Found <Material>: {material_element.text}")  # Debug output
                                if material_element.text.strip() == "ZZZ":  # Ensure no whitespace issues
                                    print(f"Updating <Material> from 'ZZZ' to 'XXX' in {file_path}")
                                    material_element.text = "XXX"
                                    updated = True
                                else:
                                    print(f"<Material> is not 'ZZZ' in {file_path}, skipping.")

                    
                    for a_002 in root_element.findall(".//A_002"):
                        # Check if <Material> exists
                        material_element = a_002.find("Material")
                        material_value = material_element.text if material_element is not None else ""

                        # Determine if <Material> is "XXX" or has been changed to "XXX"
                        if material_value == "XXX" or ("Material" in updates and updates["Material"] == "XXX"):
                            pipe_joint_length_element = a_002.find("Pipe_Joint_Length")
                            if pipe_joint_length_element is not None: # If Material is "XXX" remove joint length
                                print(f"Removing <Pipe_Joint_Length> because <Material> is 'XXX' in {file_path}")
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
                                    print(f"Created <Lining_Method> in {file_path}")

                                if lining_method_element.text != "CIP":
                                    # Update <Lining_Method> to "CIP" if it's not already set
                                    print(f"Updating <Lining_Method> to 'CIP' because Material is 'XXX' in {file_path}")
                                    lining_method_element.text = "CIP"
                                    updated = True
                            else:
                                if lining_method_element is not None:
                                    # Remove <Lining_Method> if Material is anything other than "XXX"
                                    print(f"Removing <Lining_Method> because Material is '{material_value}' in {file_path}")
                                    a_002.remove(lining_method_element)
                                    updated = True


                    # Iterate over all I_002 elements
                    for i_002 in root_element.findall(".//I_002"):
                        # Background change: Remove <PO_Number> if it exists inside <I_002>
                        po_number_element = i_002.find("PO_Number")
                        if po_number_element is not None:
                            print(f"Removing <PO_Number> from {file_path}")
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
                                    print(f"Updating <{key}> to '{value}' in {file_path}")
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
                            print(f"Adding <Purpose> with default value 'G' in {file_path}")
                            updated = True

                        # Apply user updates (if Purpose is provided in the form, overwrite it)
                        if "Purpose" in updates:  # updates comes from the request
                            new_purpose_value = updates["Purpose"]
                            if purpose_element.text != new_purpose_value:
                                print(f"Updating <Purpose> to '{new_purpose_value}' in {file_path}")
                                purpose_element.text = new_purpose_value
                                updated = True

                         # Ensure <WorkOrder> exists if missing
                        work_order_element = i_002.find("WorkOrder")
                        if work_order_element is None:
                            work_order_element = ET.Element("WorkOrder")
                            work_order_element.text = updates.get("WorkOrder", "")  # Use provided value or empty string
                            i_002.append(work_order_element)
                            print(f"Adding <WorkOrder> with value '{work_order_element.text}' in {file_path}")
                            updated = True
                        elif "WorkOrder" in updates and work_order_element.text != updates["WorkOrder"]:
                            print(f"Updating <WorkOrder> to '{updates['WorkOrder']}' in {file_path}")
                            work_order_element.text = updates["WorkOrder"]
                            updated = True

                        # Apply user updates (if WorkOrder is provided in the form, overwrite it)
                        if "WorkOrder" in updates and updates["WorkOrder"].strip():
                            new_work_order_value = updates["WorkOrder"].strip()

                            work_order_element = i_002.find("WorkOrder")
                            if work_order_element is None:
                                work_order_element = ET.Element("WorkOrder")
                                i_002.append(work_order_element)
                                print(f"Adding <WorkOrder> with value '{new_work_order_value}' in {file_path}")
                            else:
                                print(f"Updating <WorkOrder> to '{new_work_order_value}' in {file_path}")

                            work_order_element.text = new_work_order_value
                            updated = True

                                # Ensure <Project> exists if missing
                        project_element = i_002.find("Project")
                        if project_element is None:
                            project_element = ET.Element("Project")
                            project_element.text = updates.get("Project", "")  # Use provided value or empty string
                            i_002.append(project_element)
                            print(f"Adding <Project> with value '{project_element.text}' in {file_path}")
                            updated = True
                        elif "Project" in updates and project_element.text != updates["Project"]:
                            print(f"Updating <Project> to '{updates['Project']}' in {file_path}")
                            project_element.text = updates["Project"]
                            updated = True

                        # Apply user updates (if Project is provided in the form, overwrite it)
                        if "Project" in updates:  # updates comes from the request
                            new_project_value = updates["Project"]
                            if project_element.text != new_project_value:
                                print(f"Updating <Project> to '{new_project_value}' in {file_path}")
                                project_element.text = new_project_value
                                updated = True


                        # Ensure <Pipe_Use> exists with default "G" if missing
                        pipeUse_element = a_002.find("Pipe_Use")
                        if pipeUse_element is None:
                            pipeUse_element = ET.Element("Pipe_Use")
                            pipeUse_element.text = "SS"
                            a_002.append(pipeUse_element)
                            print(f"Adding <Pipe_Use> with default value 'G' in {file_path}")
                            updated = True

                        # Apply user updates (if Pipe_Use is provided in the form, overwrite it)
                        if "Pipe_Use" in updates:  # updates comes from the request
                            new_pipeUse_value = updates["Pipe_Use"]
                            if pipeUse_element.text != new_pipeUse_value:
                                print(f"Updating <Pipe_Use> to '{new_pipeUse_value}' in {file_path}")
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
                                    print(f"Created <Total_Length> in {file_path}")

                                if total_length_element.text != length_surveyed_value:
                                    # Update <Total_Length> with <Length_Surveyed> value
                                    print(f"Updating <Total_Length> to '{length_surveyed_value}' because 'MSA' is not in <OF_002>/Code in {file_path}")
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
                                print(f"Created <Comments> in {file_path}")

                            print(f"Setting <Comments> to '{comment_text}' in {file_path}")
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
                        print(f"File {file_path} updated!")
                    else:
                        print(f"No updates made for {file_path}")

                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")              
    
    return updated_files







def update_elements(parent_element, parent_tag, updates):
    """Updates specific XML elements inside <A_002> or <I_002>."""
    parent = parent_element.find(parent_tag)
    updated = False

    # Define the elements that we need to update
    elements_to_update = [
        "Owner", "City", "Pipe_Use",  # Inside <A_002>
        "Customer", "Project", "WorkOrder", "Purpose"  # Inside <I_002>
    ]

    if parent is not None:
        for key in elements_to_update:
            if key in updates:  # Only update if the key is in the updates dictionary
                element = parent.find(key)
                if element is not None:
                    if element.text != updates[key]:  # Only update if the value has changed
                        print(f"Updating {key} to {updates[key]}")  # Log the update
                        element.text = updates[key]  # Update the element value
                        updated = True
                    else:
                        print(f"{key} is already the same. No update needed.")
                else:
                    print(f"No element found for {key} inside {parent_tag}")

    return updated









# Update files function
def update_xml_files_lateral(folder_path, updates):
    """Updates specified elements in all .ptdX files."""
    updated_files_lateral = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.ptdX'):
                file_path = os.path.join(root, file)
                try:
                    tree = ET.parse(file_path)
                    root_element = tree.getroot()

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
                                        print(f"Updating <Distance> from {distance_value} to {adjusted_value} in {file_path}")
                                        distance_element.text = str(adjusted_value)

                                        # Add the adjusted value to <Length_Surveyed>
                                        length_surveyed_element = root_element.find(".//I_003/Length_Surveyed")
                                        if length_surveyed_element is not None and length_surveyed_element.text:
                                            length_surveyed_value = float(length_surveyed_element.text.strip())
                                            print(f"Updating <Length_Surveyed> from {length_surveyed_value} to {adjusted_value} in {file_path}")
                                            length_surveyed_element.text = str(adjusted_value)

                                        updated = True
                                except ValueError:
                                    print(f"Could not parse <Distance> value in {file_path}")

                    
                    
                    # Background change: Modify <Material> if it exists
                    for model in root_element.findall(".//A_003"):
                        material_element = model.find("Material")
                        if material_element is not None:
                                print(f"Found <Material>: {material_element.text}")  # Debug output
                                if material_element.text.strip() == "ZZZ":  # Ensure no whitespace issues
                                    print(f"Updating <Material> from 'ZZZ' to 'XXX' in {file_path}")
                                    material_element.text = "XXX"
                                    updated = True
                                else:
                                    print(f"<Material> is not 'ZZZ' in {file_path}, skipping.")

                    
                    for a_003 in root_element.findall(".//A_003"):
                        # Check if <Material> exists
                        material_element = a_003.find("Material")
                        material_value = material_element.text if material_element is not None else ""

                        # Determine if <Material> is "XXX" or has been changed to "XXX"
                        if material_value == "XXX" or ("Material" in updates and updates["Material"] == "XXX"):
                            pipe_joint_length_element = a_003.find("Pipe_Joint_Length")
                            if pipe_joint_length_element is not None: # If Material is "XXX" remove joint length
                                print(f"Removing <Pipe_Joint_Length> because <Material> is 'XXX' in {file_path}")
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
                                    print(f"Created <Lining_Method> in {file_path}")

                                if lining_method_element.text != "CIP":
                                    # Update <Lining_Method> to "CIP" if it's not already set
                                    print(f"Updating <Lining_Method> to 'CIP' because Material is 'XXX' in {file_path}")
                                    lining_method_element.text = "CIP"
                                    updated = True
                            else:
                                if lining_method_element is not None:
                                    # Remove <Lining_Method> if Material is anything other than "XXX"
                                    print(f"Removing <Lining_Method> because Material is '{material_value}' in {file_path}")
                                    a_003.remove(lining_method_element)
                                    updated = True


                    # Iterate over all I_003 elements
                    for i_003 in root_element.findall(".//I_003"):
                        # Background change: Remove <PO_Number> if it exists inside <I_003>
                        po_number_element = i_003.find("PO_Number")
                        if po_number_element is not None:
                            print(f"Removing <PO_Number> from {file_path}")
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
                                    print(f"Updating <{key}> to '{value}' in {file_path}")
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
                            print(f"Adding <Purpose> with default value 'G' in {file_path}")
                            updated = True

                        # Apply user updates (if Purpose is provided in the form, overwrite it)
                        if "Purpose" in updates:  # updates comes from the request
                            new_purpose_value = updates["Purpose"]
                            if purpose_element.text != new_purpose_value:
                                print(f"Updating <Purpose> to '{new_purpose_value}' in {file_path}")
                                purpose_element.text = new_purpose_value
                                updated = True

                                 # Ensure <WorkOrder> exists if missing
                        work_order_element = i_003.find("WorkOrder")
                        if work_order_element is None:
                            work_order_element = ET.Element("WorkOrder")
                            work_order_element.text = updates.get("WorkOrder", "")  # Use provided value or empty string
                            i_003.append(work_order_element)
                            print(f"Adding <WorkOrder> with value '{work_order_element.text}' in {file_path}")
                            updated = True
                        elif "WorkOrder" in updates and work_order_element.text != updates["WorkOrder"]:
                            print(f"Updating <WorkOrder> to '{updates['WorkOrder']}' in {file_path}")
                            work_order_element.text = updates["WorkOrder"]
                            updated = True

                        # Apply user updates (if WorkOrder is provided in the form, overwrite it)
                        if "WorkOrder" in updates and updates["WorkOrder"].strip():
                            new_work_order_value = updates["WorkOrder"].strip()

                            work_order_element = i_003.find("WorkOrder")
                            if work_order_element is None:
                                work_order_element = ET.Element("WorkOrder")
                                i_003.append(work_order_element)
                                print(f"Adding <WorkOrder> with value '{new_work_order_value}' in {file_path}")
                            else:
                                print(f"Updating <WorkOrder> to '{new_work_order_value}' in {file_path}")

                            work_order_element.text = new_work_order_value
                            updated = True

                        # Ensure <Project> exists if missing
                        project_element = i_003.find("Project")
                        if project_element is None:
                            project_element = ET.Element("Project")
                            project_element.text = updates.get("Project", "")  # Use provided value or empty string
                            i_003.append(project_element)
                            print(f"Adding <Project> with value '{project_element.text}' in {file_path}")
                            updated = True
                        elif "Project" in updates and project_element.text != updates["Project"]:
                            print(f"Updating <Project> to '{updates['Project']}' in {file_path}")
                            project_element.text = updates["Project"]
                            updated = True

                        # Apply user updates (if Project is provided in the form, overwrite it)
                        if "Project" in updates:  # updates comes from the request
                            new_project_value = updates["Project"]
                            if project_element.text != new_project_value:
                                print(f"Updating <Project> to '{new_project_value}' in {file_path}")
                                project_element.text = new_project_value
                                updated = True

                        # Ensure <Pipe_Use> exists with default "G" if missing
                        pipeUse_element = a_003.find("Pipe_Use")
                        if pipeUse_element is None:
                            pipeUse_element = ET.Element("Pipe_Use")
                            pipeUse_element.text = "SS"
                            a_003.append(pipeUse_element)
                            print(f"Adding <Pipe_Use> with default value 'G' in {file_path}")
                            updated = True

                        # Apply user updates (if Pipe_Use is provided in the form, overwrite it)
                        if "Pipe_Use" in updates:  # updates comes from the request
                            new_pipeUse_value = updates["Pipe_Use"]
                            if pipeUse_element.text != new_pipeUse_value:
                                print(f"Updating <Pipe_Use> to '{new_pipeUse_value}' in {file_path}")
                                pipeUse_element.text = new_pipeUse_value
                                updated = True


                    # Background change: Update <Total_Length> with <Length_Surveyed> if "MSA" is NOT in <Code>
                    code_elements = root_element.findall(".//OF_003/Code")
                    code_contains_msa = any(code_element.text and "MSA" in code_element.text for code_element in code_elements)

                    if not code_contains_msa:
                        length_surveyed_element = root_element.find(".//I_003/Length_Surveyed")
                        
                        if length_surveyed_element is not None and length_surveyed_element.text:
                            length_surveyed_value = length_surveyed_element.text.strip()
                            
                            for a_003 in root_element.findall(".//A_003"):
                                total_length_element = a_003.find("Total_Length")

                                if total_length_element is None:
                                    # Create <Total_Length> if it does not exist
                                    total_length_element = ET.Element("Total_Length")
                                    a_003.append(total_length_element)
                                    print(f"Created <Total_Length> in {file_path}")

                                if total_length_element.text != length_surveyed_value:
                                    # Update <Total_Length> with <Length_Surveyed> value
                                    print(f"Updating <Total_Length> to '{length_surveyed_value}' because 'MSA' is not in <OF_003>/Code in {file_path}")
                                    total_length_element.text = length_surveyed_value
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
                        print(f"File {file_path} updated!")
                    else:
                        print(f"No updates made for {file_path}")

                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")              
    
    return updated_files_lateral


