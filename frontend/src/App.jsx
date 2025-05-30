import "./css/App.css"
import SplashTempest from "./components/SplashTempest";
import useLoadingDots from "./components/loadingDots";
import React, { useState, lazy, Suspense } from "react";
import icon from "./assets/void.png"

const FileListMainline = lazy(() => import("./components/FileListMainline"));
const XMLFormMainline = lazy(() => import("./components/XMLFormMainline"));
const FileListLateral = lazy(() => import("./components/FileListLateral"));
const XMLFormLateral = lazy(() => import("./components/XMLFormLateral"));
const FooterStatus = lazy(() => import("./components/Footer"));

  
  const App = () => {
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [folderPath, setFolderPath] = useState("");
    const [showIntro, setShowIntro] = useState(true);
    const [filesLateral, setFilesLateral] = useState([]);
    const [updatedFiles, setUpdatedFiles] = useState([]);
    const [showLateral, setShowLateral] = useState(false);
    const [showMainline, setShowMainline] = useState(true);
    const [loadingDots, setLoadingDots] = useLoadingDots(loading);
    const [folderPathLateral, setFolderPathLateral] = useState("");
    const [updatedFilesLateral, setUpdatedFilesLateral] = useState([]);
    const [mainlineFormData, setMainlineFormData] = useState({
      WorkOrder: "",
      Owner: "",
      Customer: "",
      Project: "",
      Pipe_Use: "",
      Purpose: "",});
    const [lateralFormData, setLateralFormData] = useState({
      WorkOrder: "",
      Owner: "",
      Customer: "",
      Project: "",
      Pipe_Use: "",
      Purpose: "",});
    
    
      
        const handleMainlineClick = () => {
          setShowMainline(true);
          setShowLateral(false);
        };

        const handleLateralClick = () => {
          setShowLateral(true);
          setShowMainline(false);
        };

        const handleIconClick = () => {
          setShowIntro(true)
        }
     

    return (
      <div>
        {showIntro && <SplashTempest onFinish={() => setShowIntro(false)} />}
          {!showIntro && (
            <div className="fadeInElement">
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
                              formData={mainlineFormData}
                              setFormData={setMainlineFormData}
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
                            formData={lateralFormData}
                            setFormData={setLateralFormData}
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
                              <img src={icon} 
                                alt="Icon" 
                                onClick={handleIconClick}
                                className="icon"
                              />
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
              </div> 
            )}                     
        </div>
      );
  };

  
  export default App;



