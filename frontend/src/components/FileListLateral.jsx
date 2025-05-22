import React, { useState } from "react";
import useLoadingDots from "./loadingDots";
import TorchFlame from "./TorchFlame";
import TypewriterText from "./TypewriterText";

const FileListLateral = ({ folderPathLateral, setFolderPathLateral, filesLateral, setFilesLateral, setUpdatedFilesLateral }) => {

  const [loading, setLoading] = useState(false);
  const [noFilesFound, setNoFilesFound] = useState(false);
  const loadingDots = useLoadingDots(loading);
  

    const handleFolderSelection = async () => {
      if (window.electronAPI) {
        try {
          setLoading(true);
          setNoFilesFound(false);
          setFilesLateral([]); // Clear previous list
          
          const selectedFolder = await window.electronAPI.openFolderDialog();
          if (selectedFolder) {
            console.log("Selected Folder:", selectedFolder);
            setFolderPathLateral(selectedFolder);
  
            const response = await fetch("http://localhost:5000/list-files-lateral", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ folderPath: selectedFolder }),
            });
  
            const data = await response.json();
            const foundFiles = data.files || [];

            setFilesLateral(foundFiles);
            console.log("Lateral files found:", foundFiles);
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
      setFilesLateral([]);
      setFolderPathLateral("");
      setUpdatedFilesLateral([]);
    };

  
    return (
      <div>
        <fieldset>
          <legend>Lateral Files</legend>
  
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
              <div className="torchFlameContainer">
                <div className="torchLeft"><TorchFlame /></div>
                <div>
                      <TypewriterText text= "No ptdX exist here!!" speed={60}/>
                </div>
                <div className="torchRight"><TorchFlame /></div>
              </div>
            ) : (
              filesLateral.map((file, index) => <li key={index}>{file}</li>)
            )}
          </ol>
  
        </fieldset>
      </div>
    );
  };
  
  export default FileListLateral;
  
  
    