import React, { useState } from "react";

const XMLForm = ({ folderPath }) => {
  const [formData, setFormData] = useState({
    Owner: "",
    Pipe_Use: "",
    Customer: "",
    Project: "",
    WorkOrder: "",
    Purpose: "",
  });

  const [exporting, setExporting] = useState(false); // Track export state
  
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Define options for Pipe_Use and Purpose dropdowns
  //SS=Sanitary Sewage Pipe
  //SW=Stormwater Pipe
  const pipeUseOptions = [
    { value: "SS", description: "Sanitary Sewage Pipe" },
    { value: "SW", description: "Stormwater Pipe" },
  ];
  //A=Maintenance Related
  //B=Infiltration/Inflow Investigation
  //C=Post Rehabilitation Survey
  //D=Pre-Rehabilitation Survey
  //E=Pre-Acceptance New Sewers
  //F=Routine Assessment
  //G=Capital Improvement Program Assessment
  //H=Resurvey For Any Reason
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

    console.log("📡 Sending update request with:");
    console.log("📂 Folder Path:", folderPath);
    console.log("📝 Updates:", updates); // Log the form data

    
    
    fetch("http://localhost:5000/update-files", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ folderPath, updates: updates, }),
    })
      .then((res) => res.json())
      .then((data) => console.log("✅ Update Success:", data))
      .catch((err) => console.error("❌ Error updating files:", err));
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
        console.log(`✅ Exported file saved at: ${filePath}`);
      } else {
        console.error("❌ Export failed.");
      }
    } catch (error) {
      console.error("❌ Error exporting:", error);
    } finally {
      setExporting(false);
    }
  };

  const handleClear = () => {
    setFormData({
      Owner: "",
      Pipe_Use: "",
      Customer: "",
      Project: "",
      WorkOrder: "",
      Purpose: "",
    });
    console.log("🧹 Form cleared!");
  };



  return (
    <div>
      <h3>Edit XML Files</h3>
      {Object.keys(formData).map((key) => (
        <div key={key}>
          <label>{key}:</label>
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
              value={formData[key]}
              onChange={handleChange}
            />
          )}
        </div>
      ))}
      <button onClick={handleSubmit}>Save Changes</button>
      <button onClick={handleExport} disabled={exporting}>
        {exporting ? "Exporting..." : "Export"}
      </button>
      <button onClick={handleClear}>Clear</button>
    </div>
  );
};
  


export default XMLForm;
