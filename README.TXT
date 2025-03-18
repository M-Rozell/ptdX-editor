npm run dev → Starts everything at once.
npm run backend → Runs Flask in the backend folder.
npm run frontend → Starts Vite in the frontend folder.
npm run electron → Waits for the frontend to start before launching Electron.
Electron App Window, open DevTools (Ctrl + Shift + I)
cd backend python app.py
git init, git add ., git commit -m "", git push origin -u main

Length is millimeters. To round: adjusted_value = round(distance_value / 304.8) * 304.8
colors #93A8AC #7A9B76 #1C2321



project-root/
│── backend/
│   ├── app.py          # Flask server
│   ├── file_utils.py   # Handles file scanning & updates
│── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileList.jsx      # Displays files
│   │   │   ├── XMLForm.jsx       # Edit elements
│   │   ├── App.jsx
│   │   ├── main.jsx
│   ├── vite.config.js
│── electron.js         # Electron main process
│── package.json
│── concurrently.json   # Config for running frontend & backend





