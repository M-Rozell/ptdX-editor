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
    console.error("❌ Error creating window:", error);
  }
}

// Register the IPC handler BEFORE app is ready
ipcMain.handle("open-folder-dialog", async () => {
  try {
    const { canceled, filePaths } = await dialog.showOpenDialog({
      properties: ["openDirectory"],
    });
    
    if (!canceled && filePaths.length > 0) {
      console.log("📂 Folder Selected:", filePaths[0]); // Debugging
      return filePaths[0];
    }
    return canceled ? null : filePaths[0];
  } catch (error) {
    console.error("❌ Error opening folder dialog:", error);
  }
});




// Electron app lifecycle
app.whenReady()
  .then(createWindow)
  .catch((error) => console.error("❌ Error during app initialization:", error));

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

