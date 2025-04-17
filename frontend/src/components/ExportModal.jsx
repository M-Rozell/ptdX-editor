import React from "react";

const ExportModal = ({ filePath, onClose }) => {
  if (!filePath) return null;

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
        <button
            type="button"
            className="exitModalBtn"
            onClick={onClose}
          > 
          </button>
        <h2 className="">Export Successful!</h2>
        <p className="">Your file was saved to:</p>
            <div 
                className="modalFilePath"
                onClick={handleOpenLocation}>
            {filePath}
            </div>
        <div>
          
        </div>
    </>
  );
};

export default ExportModal;
