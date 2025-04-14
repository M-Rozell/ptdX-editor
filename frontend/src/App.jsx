import React, { useState } from "react";
import FileListMainline from "./components/FileListMainline";
import XMLFormMainline from "./components/XMLFormMainline";
import FileListLateral from "./components/FileListLateral";
import XMLFormLateral from "./components/XMLFormLateral";
import "./css/App.css"

  
  const App = () => {
    const [folderPath, setFolderPath] = useState("");
    const [files, setFiles] = useState([]);
    const [folderPathLateral, setFolderPathLateral] = useState("");
    const [filesLateral, setFilesLateral] = useState([]);
    const [showMainline, setShowMainline] = useState(false)
    const [showLateral, setShowLateral] = useState(false);
    const [updatedFiles, setUpdatedFiles] = useState([]);
    const [updatedFilesLateral, setUpdatedFilesLateral] = useState([]);

    const handleMainlineClick = () => {
      setShowMainline(true);
      setShowLateral(false);
    };

    const handleLateralClick = () => {
      setShowLateral(true);
      setShowMainline(false);
    };
    const countFoundFiles = files.length;
    const countFoundFilesLateral = filesLateral.length;
    const countUpdatedFiles = updatedFiles.length;
    const countUpdatedFilesLateral = updatedFilesLateral.length; 

    return (
      <div>
        
        <header>
            <h1 className="ptdXHeader">.ptdX Editor</h1>
          <div className="headerBtns">
            <button type="button" 
                    className="folderSelectionBtn" 
                    onClick={handleMainlineClick}
                    style={{ backgroundColor: showMainline ? "#FFFFE8" : "#303030",
                    color: showMainline ? "#050505" : "#FFFFE8" }}>
              Mainline
            </button>
            <button type="button" 
                    className="folderSelectionBtn" 
                    onClick={handleLateralClick}
                    style={{ backgroundColor: showLateral ? "#FFFFE8" : "#303030",
                    color: showLateral ? "#050505" : "#FFFFE8" }}>
              Lateral
            </button>
          </div>
        </header>
  
        <main className="filesFormWrapper">    
          <section>
          {showMainline &&
              <div className="editFilesWrapper"> 
                <div className="filesWrapper">
                  <section aria-labelledby="form-title">
                      <FileListMainline 
                        folderPath={folderPath} 
                        setFolderPath={setFolderPath}
                        files={files}
                        setFiles={setFiles}
                        setUpdatedFiles={setUpdatedFiles} 
                      />
                    </section>
                </div>
                  
                <div className="formWrapper">
                  <section aria-labelledby="form-title">
                      <XMLFormMainline 
                      folderPath={folderPath}
                      updatedFiles={updatedFiles}
                      setUpdatedFiles={setUpdatedFiles}
                      />
                  </section>
                </div>
              </div>}
          </section>
            
          <section>
          {showLateral &&
            <div className="editFilesWrapper">   
                <div className="filesWrapper">
                  <section aria-labelledby="form-title">
                    <FileListLateral
                      folderPathLateral={folderPathLateral} 
                      setFolderPathLateral={setFolderPathLateral}
                      filesLateral={filesLateral}
                      setFilesLateral={setFilesLateral}
                      setUpdatedFilesLateral={setUpdatedFilesLateral}
                    />
                  </section>
                </div>

                <div className="formWrapper">
                  <section aria-labelledby="form-title">
                    <XMLFormLateral 
                    folderPathLateral={folderPathLateral}
                    updatedFilesLateral={updatedFilesLateral}
                    setUpdatedFilesLateral={setUpdatedFilesLateral}
                     />
                  </section>
                </div>                 
            </div>}
          </section>
       
        </main>
        
        
        <footer>          
          <section>Selected Folder: {showMainline && <span>{folderPath}</span>}             
                                    {showLateral && <span>{folderPathLateral}</span>}
            </section>  

          <section>Files Found: {showMainline && <span>{countFoundFiles}</span>}           
                                {showLateral && <span>{countFoundFilesLateral}</span>}
            </section>
  
          <section>Files Updated: {showMainline && <span>{countUpdatedFiles}</span>}
                                  {showLateral && <span>{countUpdatedFilesLateral}</span>}
          </section> 
      
        </footer>      
      
      </div>
    );
  };

  
  export default App;



