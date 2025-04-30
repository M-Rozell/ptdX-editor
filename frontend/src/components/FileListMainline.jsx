import React, { useState } from "react";
import useLoadingDots from "./loadingDots";

const FileListMainline = ({ folderPath, setFolderPath, files, setFiles, setUpdatedFiles }) => {

  const [loading, setLoading] = useState(false);
  const [noFilesFound, setNoFilesFound] = useState(false);
  const loadingDots = useLoadingDots(loading);


  const handleFolderSelection = async () => {
    if (window.electronAPI) {
      try {
        setLoading(true);
        setNoFilesFound(false);
        setFiles([]); // Clear previous list

        const selectedFolder = await window.electronAPI.openFolderDialog();
        if (selectedFolder) {
          console.log("Selected Folder:", selectedFolder);
          setFolderPath(selectedFolder);

          const response = await fetch("http://localhost:5000/list-files", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ folderPath: selectedFolder }),
          });

          const data = await response.json();
          const foundFiles = data.files || [];

          setFiles(foundFiles);
          console.log("Mainline files found:", foundFiles);
          if (foundFiles.length === 0) {
            setNoFilesFound(true);
          }
        }
      } catch (error) {
        console.error("Error selecting folder or fetching files:", error);
      } finally {
        setLoading(false);
      }
    } else {
      console.error("window.electronAPI is not defined");
    }
  };


  const handleClearFiles = () => {
    setFiles([]);
    setFolderPath("");
    setUpdatedFiles([]);
  };


  return (
    <div>
      <fieldset>
        <legend>Mainline Files</legend>
          <div className="filesBtnWrapper">
            <button type="button" onClick={handleFolderSelection} className="folderSelectionBtn">
              Load Files
            </button>
            <button type="button" onClick={handleClearFiles} className="folderSelectionBtn">
              Clear Files
            </button>
          </div>  
          <ol>
          {loading ? (
              <p className="loading">Loading{loadingDots}</p>
            ) : noFilesFound ? (
              <li>No ptdX files found.</li>
            ) : (
              files.map((file, index) => <li key={index}>{file}</li>)
            )}
          </ol>        
      </fieldset>
    </div>
  );
};

export default FileListMainline;


  