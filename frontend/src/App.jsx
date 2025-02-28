import React, { useState } from "react";
import FileList from "./components/FileList";
import XMLForm from "./components/XMLForm";
import "./css/App.css"




const App = () => {
  const [folderPath, setFolderPath] = useState("");
  const [files, setFiles] = useState([]);

  
  
  const handleFolderSelection = async () => {
    if (window.electronAPI) {
      try {
        const selectedFolder = await window.electronAPI.openFolderDialog();
        if (selectedFolder) {
          console.log("📂 Selected Folder:", selectedFolder); // Debugging
          setFolderPath(selectedFolder);
  
          fetch("http://localhost:5000/list-files", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ folderPath: selectedFolder }),
          })
            .then(res => res.json())
            .then(data => {
              console.log("📄 Files found:", data.files); // Debugging
              setFiles(data.files);
            })
            .catch(err => console.error("❌ Error fetching files:", err));
        }
      } catch (error) {
        console.error("❌ Error selecting folder:", error);
      }
    } else {
      console.error("❌ window.electronAPI is not defined");
    }
  };


  const handleClearList = () => {
    setFiles([])
  }

  return (
    <div>
      <h1 className="ptdXHeader">.ptdX editor</h1>
      <div className="btnDiv">
      <button onClick={handleFolderSelection} className="folderSelectionBtn">Load</button>
      </div>
      <XMLForm folderPath={folderPath} />
      <FileList files={files} />
      <button onClick={handleClearList} className="folderSelectionBtn">Clear Files</button>
    </div>
  );
};

export default App;



