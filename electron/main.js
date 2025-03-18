const { app, BrowserWindow, ipcMain, dialog } = require("electron");
const path = require("path");

let mainWindow;

function createWindow() {
  try {
    mainWindow = new BrowserWindow({
      width: 1000,
      height: 800,
      webPreferences: {
        preload: path.join(__dirname, "preload.js"),
        contextIsolation: true, // Keep security best practices
        enableRemoteModule: false,
      },
    });

    mainWindow.loadURL("http://localhost:5173");

    mainWindow.on("closed", () => {
      mainWindow = null;
    });
  } catch (error) {
    console.error("Error creating window:", error);
  }
}

// Register the IPC handler BEFORE app is ready
ipcMain.handle("open-folder-dialog", async () => {
  try {
    const { canceled, filePaths } = await dialog.showOpenDialog({
      properties: ["openDirectory"],
    });
    
    if (!canceled && filePaths.length > 0) {
      console.log("Folder Selected:", filePaths[0]); // Debugging
      return filePaths[0];
    }
    return canceled ? null : filePaths[0];
  } catch (error) {
    console.error("Error opening folder dialog:", error);
  }
});


ipcMain.handle("export-data", async (_, folderPath) => {
  try {
    const response = await fetch("http://localhost:5000/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ folderPath }),
    });

    if (!response.ok) {
      throw new Error("Failed to export data.");
    }

    // Get the file as a BLOB (binary large object)
    const buffer = await response.arrayBuffer();
    const fs = require("fs");
    const filePath = path.join(folderPath, "export.xlsx");

    // Save the file
    fs.writeFileSync(filePath, Buffer.from(buffer));
    console.log(`Export successful: ${filePath}`);
    return filePath;
  } catch (error) {
    console.error("Export error:", error);
    return null;
  }
});



// Electron app lifecycle
app.whenReady()
  .then(createWindow)
  .catch((error) => console.error("Error during app initialization:", error));

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

