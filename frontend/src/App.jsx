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

    const countFoundFiles = files.length;
    const countFoundFilesLateral = filesLateral.length;
    const countUpdatedFiles = updatedFiles.length;
    const countUpdatedFilesLateral = updatedFilesLateral.length;
    
    const handleMainlineClick = () => {
      setShowMainline(true);
      setShowLateral(false);
    };

    const handleLateralClick = () => {
      setShowLateral(true);
      setShowMainline(false);
    };
     

    return (
      <div>
        
        <header>
          <div></div>
          <div className="headerBtns">
            <button type="button" 
                    className="folderSelectionBtn" 
                    onClick={handleMainlineClick}
                    style={{ backgroundColor: showMainline ? "#585454" : "#303030",
                    color: showMainline ? "#FFFFE8" : "#FFFFE8" }}>
              Mainline
            </button>
            <button type="button" 
                    className="folderSelectionBtn" 
                    onClick={handleLateralClick}
                    style={{ backgroundColor: showLateral ? "#585454" : "#303030",
                    color: showLateral ? "#FFFFE8" : "#FFFFE8" }}>
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
          <section className="footerText">Selected Folder: {showMainline && <span>{folderPath}</span>}             
                                    {showLateral && <span>{folderPathLateral}</span>}
          </section>  
          <section className="footerText">Files Found: {showMainline && <span style={{color: countFoundFiles > 0 ? "#02fdd7" : "#FFFFE8"}}>{countFoundFiles}</span>}           
                                {showLateral && <span style={{color: countFoundFilesLateral > 0 ? "#02fdd7" : "#FFFFE8"}}>{countFoundFilesLateral}</span>}
          </section> 
          <section className="footerText">Files Updated: {showMainline && <span style={{color: countUpdatedFiles > 0 ? "#02fdd7" : "#FFFFE8"}}>{countUpdatedFiles}</span>}
                                  {showLateral && <span style={{color: countUpdatedFilesLateral > 0 ? "#02fdd7" : "#FFFFE8"}}>{countUpdatedFilesLateral}</span>}
          </section>       
        </footer>      
      
      </div>
    );
  };

  
  export default App;



