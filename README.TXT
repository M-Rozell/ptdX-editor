npm run dev → Starts everything at once.
npm run backend → Runs Flask in the backend folder.
npm run frontend → Starts Vite in the frontend folder.
npm run electron → Waits for the frontend to start before launching Electron.
Electron App Window, open DevTools (Ctrl + Shift + I)
cd backend python app.py
E:\ptdX

Length is millimeters. To round: adjusted_value = round(distance_value / 304.8) * 304.8




project-root/
│── backend/
│   ├── app.py          # Flask server
│   ├── file_utils.py   # Handles file scanning & updates
│── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileList.jsx      # Displays files
│   │   │   ├── XMLForm.jsx       # Edit elements
│   │   ├── App.jsx
│   │   ├── main.jsx
│   ├── vite.config.js
│── electron.js         # Electron main process
│── package.json
│── concurrently.json   # Config for running frontend & backend




# Apply additional changes (Material, PO_Number, etc.)
                    apply_additional_changes(root_element, file_path)




def apply_additional_changes(root_element, ptdx_file_path):
    """Apply additional changes (Material, PO_Number, Inspection_Technology_Used_CCTV)"""
    # Modify <Material> element if its value is "ZZZ"
    for material in root_element.findall(".//A_002/Material"):
        if material.text == "ZZZ":
            material.text = "XXX"
            print(f"Updated Material to 'XXX' in {ptdx_file_path}")

    # Modify <PO_Number> element
    for poNumber in root_element.findall(".//I_002/PO_Number"):
        poNumber.text = " "
        print(f"Updating PO_Number in {ptdx_file_path}")

    # Modify Inspection_Technology_Used_CCTV in <I_002>
    for cctv in root_element.findall(".//I_002/Inspection_Technology_Used_CCTV"):
        cctv.text = "true"
        print(f"Updated Inspection_Technology_Used_CCTV to 'true' in {ptdx_file_path}")


        # Access <I_002> section
        a_002 = root_element.find(".//A_002")

        # Ensure <Lining_Method> exists and update
        lining_method = a_002.find("Lining_Method")
        if lining_method is None:
            lining_method = ET.SubElement(a_002, "Lining_Method")
            print("Created missing <Lining_Method> tag.")
        
        # Modify <Lining_Method> element if value is not "CP"
        update_lining_method = a_002.find("Lining_Method")
        for material in root_element.findall(".//A_002/Material"):
            if material.text == "XXX":
                update_lining_method.text = "CP"
                print("Lining_Method updated")
            else:
                a_002.remove(update_lining_method)
                print("Removed <Lining_Method>")

        

    # Check if <Code>MSA</Code> exists
    msa_exists = any(code.text == "MSA" for code in root_element.findall(".//Code"))

    if not msa_exists:
        # Find <Total_Length> and <Length_Surveyed>
        total_length = root_element.find(".//A_002/Total_Length")
        length_surveyed = root_element.find(".//I_002/Length_Surveyed")

        if total_length is not None and length_surveyed is not None:
            # Update <Total_Length> value
            print(f"Updating Total_Length in {ptdx_file_path} from {total_length.text} to {length_surveyed.text}")
            total_length.text = length_surveyed.text
        else:
            print(f"Missing required tags in {ptdx_file_path}")

