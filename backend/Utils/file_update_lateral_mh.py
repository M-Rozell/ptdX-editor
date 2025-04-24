import os
import xml.etree.ElementTree as ET

def update_lateral_mh(file_path):
    # Step 1: Get MainlineFolder (one level up)
    mainline_folder = os.path.dirname(os.path.dirname(file_path))

    # Step 2: Find the mainline .ptdX file (should be in mainline_folder, not in subdirs)
    mainline_file = None
    for file in os.listdir(mainline_folder):
        full_path = os.path.join(mainline_folder, file)
        if os.path.isfile(full_path) and file.endswith(".ptdX"):
            try:
                tree = ET.parse(full_path)
                root = tree.getroot()
                if root.find('.//A_002') is not None and root.find('.//I_002') is not None:
                    mainline_file = full_path
                    break
            except ET.ParseError:
                continue

    if not mainline_file:
        print(f"No mainline .ptdX file found in {mainline_folder}")
        return

    # Step 3: Extract Upstream_AP and Downstream_AP from mainline file
    tree_main = ET.parse(mainline_file)
    root_main = tree_main.getroot()

    upstream_ap = root_main.findtext('.//A_002/Upstream_AP', default='')
    downstream_ap = root_main.findtext('.//A_002/Downstream_AP', default='')

    # Step 4: Write to Upstream_MH and Downstream_MH in lateral file
    tree_lat = ET.parse(file_path)
    root_lat = tree_lat.getroot()

    a_003 = root_lat.find('.//A_003')
    if a_003 is not None:
        up_elem = a_003.find('Upstream_MH')
        if up_elem is None:
            up_elem = ET.SubElement(a_003, 'Upstream_MH')
        up_elem.text = upstream_ap

        down_elem = a_003.find('Downstream_MH')
        if down_elem is None:
            down_elem = ET.SubElement(a_003, 'Downstream_MH')
        down_elem.text = downstream_ap

        # Save changes
        tree_lat.write(file_path, encoding='utf-8', xml_declaration=True)
        