npm run dev → Starts everything at once.
npm run backend → Runs Flask in the backend folder.
npm run frontend → Starts Vite in the frontend folder.
npm run electron → Waits for the frontend to start before launching Electron.
Electron App Window, open DevTools (Ctrl + Shift + I)
cd backend python app.py
E:\ptdX

Length is millimeters. To round: adjusted_value = round(distance_value / 304.8) * 304.8




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




# Step 2: Update <Comments> based on <Code> and <Distance>
                    for of_002 in root_element.findall(".//OF_002"):
                        code_element = of_002.find("Code")
                        distance_element = of_002.find("Distance")
                        comments_element = of_002.find("Comments")

                        if code_element is not None and distance_element is not None:
                            code_value = code_element.text.strip()
                            try:
                                distance_value = float(distance_element.text.strip())
                            except ValueError:
                                print(f"⚠️ Could not parse <Distance> value in {file_path}")
                                continue  # Skip this entry if Distance is invalid

                            # Handle Start Inspection Comment
                            if code_value == "AMH" and distance_value == 0:
                                start_mh_element = root_element.find(".//I_002/Start_MH")
                                if start_mh_element is not None and start_mh_element.text:
                                    start_mh_value = start_mh_element.text.strip()
                                    comment_text = f"Start Inspection {start_mh_value}"
                                    if comments_element is None:
                                        comments_element = ET.Element("Comments")
                                        of_002.append(comments_element)
                                        print(f"Created <Comments> in {file_path}")

                                    print(f"Setting <Comments> to '{comment_text}' in {file_path}")
                                    comments_element.text = comment_text
                                    updated = True

                            # Handle End Inspection Comment
                            elif code_value in ["AMH", "AEP"] and distance_value > 0:
                                end_mh_element = root_element.find(".//I_002/End_MH")
                                if end_mh_element is not None and end_mh_element.text:
                                    end_mh_value = end_mh_element.text.strip()
                                    comment_text = f"End Inspection {end_mh_value}"
                                    if comments_element is None:
                                        comments_element = ET.Element("Comments")
                                        of_002.append(comments_element)
                                        print(f"Created <Comments> in {file_path}")

                                    print(f"Setting <Comments> to '{comment_text}' in {file_path}")
                                    comments_element.text = comment_text
                                    updated = True

