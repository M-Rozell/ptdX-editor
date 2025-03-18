import React, { useState } from "react";

const XMLForm = ({ folderPath }) => {
  
  const [formData, setFormData] = useState({
    WorkOrder: "",
    Owner: "",
    Customer: "",
    Project: "",
    Pipe_Use: "",
    Purpose: "",
  });

  const [exporting, setExporting] = useState(false); // Track export state
  
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

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
  
  
  const handleSubmit = () => {
    if (!folderPath) {
      console.error("Folder path is required");
      return;
    }

    // Prepare the updates by filtering out any empty fields
    const updates = Object.fromEntries(
      Object.entries(formData).filter(([_, value]) => value !== "")
    );

    console.log("Sending update request with:");
    console.log("Folder Path:", folderPath);
    console.log("Updates:", updates); // Log the form data

    
    
    fetch("http://localhost:5000/update-files", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ folderPath, updates: updates, }),
    })
      .then((res) => res.json())
      .then((data) => console.log("Update Success:", data))
      .catch((err) => console.error("Error updating files:", err));
  };


  const handleExport = async () => {
    if (!folderPath) {
      console.error("Folder path is required");
      return;
    }
  
    setExporting(true);
    try {
      const filePath = await window.electronAPI.exportData(folderPath);
      if (filePath) {
        console.log(`Exported file saved at: ${filePath}`);
      } else {
        console.error("Export failed.");
      }
    } catch (error) {
      console.error("Error exporting:", error);
    } finally {
      setExporting(false);
    }
  };

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
    <div>
      {Object.keys(formData).map((key) => (
        <div key={key} className="inputName">
          
          {/* Conditionally render dropdown for specific keys */}
          {key === "Pipe_Use" ? (
            <select
              name={key}
              value={formData[key]}
              onChange={handleChange}
            >
              <option value="">Select Pipe Use</option>
              {pipeUseOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.description}
                </option>
              ))}
            </select>
          ) : key === "Purpose" ? (
            <select
              name={key}
              value={formData[key]}
              onChange={handleChange}
            >
              <option value="">Select Purpose</option>
              {purposeOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.description}
                </option>
              ))}
            </select>
          ) : (
            <input
              type="text"
              name={key}
              placeholder={key}
              value={formData[key]}
              onChange={handleChange}
            />
          )}
        </div>
      ))}
      <div className="bottomBtnsWrapper">
      <button onClick={handleSubmit} className="bottomBtns">Save Changes</button>
      <button onClick={handleExport} className="bottomBtns" disabled={exporting}>
        {exporting ? "Exporting..." : "Export"}
      </button>
      <button onClick={handleClear} className="bottomBtns">Clear</button>
      </div>
    </div>
  );
};
  


export default XMLForm;
