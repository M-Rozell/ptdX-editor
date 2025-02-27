from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from file_utils import find_ptdx_files, update_xml_files
import xml.etree.ElementTree as ET


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






if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)






