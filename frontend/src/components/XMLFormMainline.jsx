import React, { useState, lazy, Suspense } from "react";
const ExportModal = lazy(() => import("./ExportModal"));

const XMLFormMainline = ({ folderPath, setUpdatedFiles, loading, setLoading, formData,
  setFormData}) => {
 

  const [showModal, setShowModal] = useState(false);
  const [exporting, setExporting] = useState(false); 
  const [exportedFilePath, setExportedFilePath] = useState(null);
  
  // Define options for Pipe_Use and Purpose dropdowns
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
    if (!folderPath) {
      console.error("Folder path is required");
      return;
    }

    const updates = Object.fromEntries(
      Object.entries(formData).filter(([_, value]) => value !== "")
    );
    setLoading(true);

    fetch("http://localhost:5000/update-files", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ folderPath, updates }),
    })
      .then((res) => res.json())
      .then((data) => { console.log("Update Success:", data)
        setUpdatedFiles(data.updated_files || []);
      })
      .catch((err) => console.error("Error updating files:", err))
      .finally(() => {
        setLoading(false);
      });
    };

  
    const handleExport = async () => {
    if (!folderPath) {
      console.error("Folder path is required");
      return;
    }
    setExporting(true);
    try {
      setShowModal(true);
      const filePath = await window.electronAPI.exportDataMainline(folderPath);
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
    }
  };

  const closeModal = () => {
    setExportedFilePath(null);
    setShowModal(false);
  }

  const handleClear = () => {
    setFormData({
      WorkOrder: "",
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
        <legend>Edit Mainline</legend>
        
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
            >Export</button>
            
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
                    <ExportModal 
                      filePath={exportedFilePath} 
                      onClose={closeModal}
                      loading={exporting}
                    />
                  </div>
                </div>
            </Suspense>
            )}
      </fieldset>
    </form>
  );  
};
  
export default XMLFormMainline;
