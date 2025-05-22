const { app, BrowserWindow, ipcMain, dialog, shell } = require("electron");
const path = require("path");

let mainWindow;

function createWindow() {
  try {
    mainWindow = new BrowserWindow({
      width: 950,
      height: 505,
      resizable: false,
      backgroundColor: '#1c1c1c',
      icon: path.join(__dirname, '../assets/icon.ico'),
      // remove the default titlebar
      titleBarStyle: 'hidden',
      // expose window controlls in Windows/Linux
      ...(process.platform !== 'darwin' ? { titleBarOverlay: true } : {}),
      titleBarOverlay: {
        color: '#1c1c1c',
      symbolColor: '#fa008a',
      height: 8
    },
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

ipcMain.handle("open-file", async (_event, filePath) => {
  if (filePath) {
    try {
      const result = await shell.openPath(filePath);
      if (result) {
        console.error("Failed to open file:", result);
      }
    } catch (err) {
      console.error("Error opening file:", err);
    }
  }
  });


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

// Export data mainline
ipcMain.handle("export-data-mainline", async (_, folderPath) => {
  try {
    const response = await fetch("http://localhost:5000/export-mainline", {
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
    const filePath = path.join(folderPath, "export_mainline.xlsx");

    // Save the file
    fs.writeFileSync(filePath, Buffer.from(buffer));
    console.log(`Export successful: ${filePath}`);
    return filePath;
  } catch (error) {
    console.error("Export error:", error);
    return null;
  }
});


// Export data lateral
ipcMain.handle("export-data-lateral", async (_, folderPath) => {
  try {
    const response = await fetch("http://localhost:5000/export-lateral", {
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
    const filePath = path.join(folderPath, "export_lateral.xlsx");

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

