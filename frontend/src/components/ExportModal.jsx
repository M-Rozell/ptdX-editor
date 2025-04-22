import React from "react";
import useLoadingDots from "./loadingDots";

const ExportModal = ({ filePath, onClose, loading}) => {
  const loadingDots = useLoadingDots(loading);

  if (!filePath && !loading) return null;
  
  const handleOpenLocation = async () => {
    if (filePath && window.electronAPI?.openFile) {
      try {
        await window.electronAPI.openFile(filePath);
        onClose();
      } catch (err) {
        console.error("Failed to open file:", err);
      }
    }
  };

  

  return (

      <>
        {loading ? (
          <span className="exporting">Exporting{loadingDots}</span>
        ) : (
          <>
          <button type="button" className="exitModalBtn" onClick={onClose}></button>
            <h2 className="modalH2">Export Successful!</h2>
            <p className="modalP">Your file was saved to:</p>
            <div className="modalFilePath" onClick={handleOpenLocation}>
              {filePath}
            </div>
          </>
        )}
      </>
  );
};

export default ExportModal;
