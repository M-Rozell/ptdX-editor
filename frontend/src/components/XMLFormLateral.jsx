import React, { useState, lazy, Suspense } from "react";

const ExportModal = lazy(() => import("./ExportModal"));

const XMLFormLateral = ({ folderPathLateral, updatedFilesLateral, setUpdatedFilesLateral }) => {
  
  const [formData, setFormData] = useState({
    WorkOrder: "",
    Owner: "",
    Customer: "",
    Project: "",
    Pipe_Use: "",
    Purpose: "",
  });

  const [exporting, setExporting] = useState(false); 
  const [exportedFilePath, setExportedFilePath] = useState(null);
  const [showModal, setShowModal] = useState(false);
  
  // Options for Pipe_Use and Purpose dropdowns
  const pipeUseOptions = [
    { value: "SS", description: "Sanitary Sewage Pipe" },
    { value: "SW", description: "Stormwater Pipe" },
  ];
 
  const purposeOptions = [
    { value: "A", description: "Maintenance Related" },
    { value: "B", description: "Infiltration/Inflow Investigation" },
    { value: "C", description: "Post Rehabilitation Survey" },
    { value: "D", description: "Pre-Rehabilitation Survey" },
    { value: "E", description: "Pre-Acceptance New Sewers" },
    { value: "F", description: "Routine Assessment" },
    { value: "G", description: "Capital Improvement Program Assessment" },
    { value: "H", description: "Resurvey For Any Reason" },  
  ];
  
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };
  
  const handleSubmit = () => {
    if (!folderPathLateral) {
      console.error("Folder path is required");
      return;
    }

    const updates = Object.fromEntries(
      Object.entries(formData).filter(([_, value]) => value !== "")
    );

    fetch("http://localhost:5000/update-files-lateral", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ folderPathLateral, updates }),
    })
      .then((res) => res.json())
      .then((data) => {console.log("Update Success:", data)
        setUpdatedFilesLateral(data.updated_files || []);
      })
      .catch((err) => console.error("Error updating files:", err));
  };

  const handleExport = async () => {
    if (!folderPathLateral) {
      console.error("Folder path is required");
      return;
    }
  
    setExporting(true);
    try {
      const filePath = await window.electronAPI.exportData(folderPathLateral);
      if (filePath) {
        console.log(`Exported file saved at: ${filePath}`);
        setExportedFilePath(filePath);
      } else {
        console.error("Export failed.");
      }
    } catch (error) {
      console.error("Error exporting:", error);
    } finally {
      setExporting(false);
      setShowModal(true);
    }
  };

  const closeModal = () => {
    setExportedFilePath(null);
    setShowModal(false);
  }

  const handleClear = () => {
    setFormData({
      Work_Order: "",
      Owner: "",
      Customer: "",
      Project: "",
      Pipe_Use: "",
      Purpose: "",
    });
    console.log("Form cleared!");
  };


  return (
    <form onSubmit={handleSubmit} aria-labelledby="form-title">
      <fieldset className="formFieldset">
        <legend>Edit Lateral</legend>
        
        {Object.keys(formData).map((key) => (
          <div key={key} className="inputWrapper">
            <label htmlFor={key}>{key.replace(/_/g, " ")}:</label>
            
            {key === "Pipe_Use" ? (
              <select
                id={key}
                name={key}
                value={formData[key]}
                onChange={handleChange}
              >
                <option value=""></option>
                {pipeUseOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.description}
                  </option>
                ))}
              </select>
            ) : key === "Purpose" ? (
              <select
                id={key}
                name={key}
                value={formData[key]}
                onChange={handleChange}
              >
                <option value=""></option>
                {purposeOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.description}
                  </option>
                ))}
              </select>
            ) : (
              <input
                type="text"
                id={key}
                name={key}
                //placeholder={key.replace(/_/g, " ")}
                value={formData[key]}
                onChange={handleChange}
              />
            )}
          </div>
        ))}
      
      <div className="bottomBtnsWrapper">
        <button 
          type="button"
          onClick={handleSubmit} 
          className="bottomBtns"
        >Save Changes</button>
        
        <button 
          type="button" 
          onClick={handleExport} 
          className="bottomBtns" 
          aria-live="polite"
        >
          Export
        </button>
        <button 
          type="button" 
          onClick={handleClear} 
          className="bottomBtns"
        >Clear</button>
      </div>

      {showModal && (
        <Suspense fallback={<div>Loading Modal...</div>}>
      <div className="modal-overlay">
        <div className="modal-content">
          <ExportModal filePath={exportedFilePath} onClose={closeModal} />
        </div>
      </div>
      </Suspense>
      )}
      
      </fieldset>
    </form>
  );
  
};
  


export default XMLFormLateral;
