// components/FooterStatus.jsx
import React from "react";

const FooterStatus = ({ 
  showMainline, folderPath, files, updatedFiles, 
  showLateral, folderPathLateral, filesLateral, updatedFilesLateral 
}) => {
  const countFoundFiles = files.length;
  const countFoundFilesLateral = filesLateral.length;
  const countUpdatedFiles = updatedFiles.length;
  const countUpdatedFilesLateral = updatedFilesLateral.length;

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
        Files Updated: {showMainline && (
                          <span style={{color: countUpdatedFiles > 0 ? "#02fdd7" : "#FFFFE8"}}>
                            {countUpdatedFiles}
                          </span>)}
                      {showLateral && (
                          <span style={{color: countUpdatedFilesLateral > 0 ? "#02fdd7" : "#FFFFE8"}}>
                            {countUpdatedFilesLateral}
                          </span>)}
      </section>       
    </footer>
  );
};

export default FooterStatus;
