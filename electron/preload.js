const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  openFolderDialog: () => ipcRenderer.invoke("open-folder-dialog"),
  exportDataMainline: (folderPath) => ipcRenderer.invoke("export-data-mainline", folderPath),
  exportDataLateral: (folderPath) => ipcRenderer.invoke("export-data-lateral", folderPath),
  openFile: (filePath) => ipcRenderer.invoke("open-file", filePath),
});

