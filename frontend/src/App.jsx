import React, { useState, lazy, Suspense } from "react";
import "./css/App.css"

const FileListMainline = lazy(() => import("./components/FileListMainline"));
const XMLFormMainline = lazy(() => import("./components/XMLFormMainline"));
const FileListLateral = lazy(() => import("./components/FileListLateral"));
const XMLFormLateral = lazy(() => import("./components/XMLFormLateral"));
const FooterStatus = lazy(() => import("./components/footer"));

  
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
          <Suspense fallback={<div>Loading Mainline...</div>}>
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
              </div>
              </Suspense>
              }
          </section>
            
          <section>
          {showLateral &&
          <Suspense fallback={<div>Loading Lateral...</div>}>
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
            </div>
            </Suspense>
            }
          </section>
       
        </main>          
        {(showMainline || showLateral) && (
              <Suspense fallback={<div>Loading footer...</div>}>
                <FooterStatus
                  showMainline={showMainline}
                  folderPath={folderPath}
                  files={files}
                  updatedFiles={updatedFiles}
                  showLateral={showLateral}
                  folderPathLateral={folderPathLateral}
                  filesLateral={filesLateral}
                  updatedFilesLateral={updatedFilesLateral}
                />
              </Suspense>
          )}       
                  
      </div>
    );
  };

  
  export default App;



