from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from file_utils import find_ptdx_files, update_xml_files
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response



@app.route('/list-files', methods=['POST'])
def list_files():
    """Receives a project folder path and lists all ptdX files inside."""
    data = request.json
    project_folder = data.get('folderPath')

    if not project_folder or not os.path.isdir(project_folder):
        return jsonify({'error': 'Invalid project folder path'}), 400

    file_list = find_ptdx_files(project_folder)
    return jsonify({'files': file_list}), 200



@app.route('/update-files', methods=['POST'])
def update_files():
    """Receives updates for all ptdX files and applies them."""
    data = request.json
    folder_path = data.get('folderPath')
    updates = data.get('updates')

    if not folder_path or not os.path.isdir(folder_path):
        return jsonify({'error': 'Invalid folder path'}), 400

    updated_files = update_xml_files(folder_path, updates)
    return jsonify({'message': 'Files updated successfully', 'updated_files': updated_files}), 200



@app.route('/export', methods=['POST'])
def export_to_excel():
    """Generates an Excel spreadsheet with data from all ptdX files."""
    data = request.json
    folder_path = data.get('folderPath')

    if not folder_path or not os.path.isdir(folder_path):
        return jsonify({'error': 'Invalid folder path'}), 400

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
                    print(f"⚠️ Error parsing date '{raw_date}': {e}")
                    date = ""
            else:
                print("⚠️ No date found!")
                date = ""
                       
            height = root.findtext(".//A_002/Height", default="0")
            size = round(float(height) / 25.4, 2) if height else ""

            length_surveyed = root.findtext(".//I_002/Length_Surveyed", default="0")
            distance = round(float(length_surveyed) / 304.8, 2) if length_surveyed else ""

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
            print(f"⚠️ Error processing {file_path}: {str(e)}")

    # Create a DataFrame and save as Excel
    df = pd.DataFrame(extracted_data, columns=[
        "File Name", "Date", "Name", "Asset", "Upstream MH", "Downstream MH", "Size", "Distance", "Direction", "MSA", "Cleaning"
    ])

    export_path = os.path.join(folder_path, "export.xlsx")
    df.to_excel(export_path, index=False)

    return send_file(export_path, as_attachment=True)






if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)






