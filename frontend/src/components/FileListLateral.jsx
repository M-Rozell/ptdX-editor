

const FileListLateral = ({ folderPathLateral, setFolderPathLateral, filesLateral, setFilesLateral, setUpdatedFilesLateral }) => {;

    const handleFolderSelection = async () => {
      if (window.electronAPI) {
        try {
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
            console.log("Files found:", data.files);
            setFilesLateral(data.files || []);
          }
        } catch (error) {
          console.error("Error selecting folder or fetching files:", error);
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
            {filesLateral.map((file, index) => (
              <li key={index}>{file}</li>
            ))}
          </ol>
  
        </fieldset>
      </div>
    );
  };
  
  export default FileListLateral;
  
  
    