from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from Utils import find_ptdx_files, update_xml_files, find_ptdx_files_lateral, update_xml_files_lateral, export_mainline_to_excel, export_lateral_to_excel
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

    file_list = find_ptdx_files(project_folder)  # Expecting a list of file paths

    return jsonify({'files': [os.path.basename(path) for path in file_list]}), 200




@app.route('/list-files-lateral', methods=['POST'])
def list_lateral_files():
    """Receives a project folder path and lists all ptdX files inside."""
    data = request.json
    project_folder = data.get('folderPath')

    if not project_folder or not os.path.isdir(project_folder):
        return jsonify({'error': 'Invalid project folder path'}), 400

    file_list_lateral = find_ptdx_files_lateral(project_folder)  # Expecting a list of file paths

    return jsonify({'files': [os.path.basename(path) for path in file_list_lateral]}), 200




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




@app.route('/update-files-lateral', methods=['POST'])
def update_files_lateral():
    """Receives updates for all ptdX files and applies them."""
    data = request.json
    folder_path = data.get('folderPathLateral')
    updates = data.get('updates')

    if not folder_path or not os.path.isdir(folder_path):
        return jsonify({'error': 'Invalid folder path'}), 400

    updated_files_lateral = update_xml_files_lateral(folder_path, updates)
    return jsonify({'message': 'Files updated successfully', 'updated_files': updated_files_lateral}), 200




@app.route('/export-mainline', methods=['POST'])
def export_to_excel_mainline():
    data = request.json
    folder_path = data.get('folderPath')

    try:
        export_path = export_mainline_to_excel(folder_path)
        return send_file(export_path, as_attachment=True)
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': f"Export failed: {str(e)}"}), 500
    


@app.route('/export-lateral', methods=['POST'])
def export_to_excel_lateral():
    data = request.json
    folder_path = data.get('folderPath')

    try:
        export_path = export_lateral_to_excel(folder_path)
        return send_file(export_path, as_attachment=True)
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': f"Export failed: {str(e)}"}), 500
    





if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)






