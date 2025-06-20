import React from "react";
import "../css/App.css"
import useLoadingDots from "./loadingDots";
import icon from "../assets/void.png"

const FooterStatus = ({ 
  showMainline, folderPath, files, updatedFiles, 
  showLateral, folderPathLateral, filesLateral, updatedFilesLateral,
  loading, setShowIntro
  
}) => {
  const countFoundFiles = files.length;
  const countFoundFilesLateral = filesLateral.length;
  const countUpdatedFiles = updatedFiles.length;
  const countUpdatedFilesLateral = updatedFilesLateral.length;
  const loadingDots = useLoadingDots(loading);
  const handleIconClick = () => {
    setShowIntro(true)
  }

 

  return (
    <footer>
      <section className="footerText">
        Selected Folder: {showMainline && <span>{folderPath}</span>}
                         {showLateral && <span>{folderPathLateral}</span>}
      </section>  
      
      <section className="footerText">
        Files Found: {showMainline && (
                        <span style={{color: countFoundFiles > 0 ? "#02fdd7" : "#FFFFE8"}}>
                          {countFoundFiles}
                        </span>)}
                    {showLateral && (
                        <span style={{color: countFoundFilesLateral > 0 ? "#02fdd7" : "#FFFFE8"}}>
                          {countFoundFilesLateral}
                        </span>)}
      </section> 
      
      <section className="footerText">
        Files Updated:  {loading ? (
                          <span className="updating">Updating{loadingDots}</span>
                              ) : (
                                <>
                                  {showMainline && (
                                    <span style={{ color: countUpdatedFiles > 0 ? "#02fdd7" : "#FFFFE8" }}>
                                      {countUpdatedFiles}
                                    </span>
                                  )}
                                  {showLateral && (
                                    <span style={{ color: countUpdatedFilesLateral > 0 ? "#02fdd7" : "#FFFFE8" }}>
                                      {countUpdatedFilesLateral}
                                    </span>
                                  )}
                                </>
                          )}             
      </section>
                    <img src={icon} 
                      alt="Icon" 
                      onClick={handleIconClick}
                      className="icon"
                    />     
    </footer>
  );
};

export default FooterStatus;
