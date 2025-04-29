import React, { useState,useEffect, lazy, Suspense } from "react";
import "./css/App.css"
import useLoadingDots from "./components/loadingDots";
import SpiralIntro from "./components/SpiralIntro";

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
    const [loading, setLoading] = useState(false);
    const [loadingDots, setLoadingDots] = useLoadingDots(loading);
    const [showIntro, setShowIntro] = useState(true);

    
useEffect(() => {
  const timeout = setTimeout(() => setShowIntro(false), 4000);
  return () => clearTimeout(timeout);
}, []);

    
    
    const handleMainlineClick = () => {
      setShowMainline(true);
      setShowLateral(false);
    };

    const handleLateralClick = () => {
      setShowLateral(true);
      setShowMainline(false);
    };
     

    return (
      <div className="bg-gray-900 min-h-screen text-white relative overflow-hidden">
        {showIntro && <SpiralIntro onFinish={() => setShowIntro(false)} />}
          {!showIntro && (
            <>  
        <header>
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
                      loading={loading}
                      setLoading={setLoading}
                      setLoadingDots={setLoadingDots}
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
                    loading={loading}
                    setLoading={setLoading}
                    setLoadingDots={setLoadingDots}
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
                  loading={loading}
                  loadingDots={loadingDots}
                />
              </Suspense>
          )} 
          </>
          )}          
      </div>
    );
  };

  
  export default App;



