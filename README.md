# 🅿️ Parking Space Management System using OpenCV and Streamlit

A smart parking space monitoring system that detects and displays vacant and occupied parking slots in real-time using OpenCV and Streamlit.

---

## 📽️ Demo

> Upload a parking lot video and see live slot detection with vacancy count.

![Demo](demo/demo.gif)  
*Note: Replace with your actual demo image or video link if available*

---

## 🖼️ UI Screenshots

### 🎨 Slot Picker Tab
![Slot Picker](https://github.com/Chandrakanth03/Parking-Space-Management-System/blob/main/photos/slot_picker.png.png)

### 📹 Detection Tab
![Detection](https://github.com/Chandrakanth03/Parking-Space-Management-System/blob/main/photos/detection_tab.png)

### 📦 Export/Import Tab
![Export Import](https://github.com/Chandrakanth03/Parking-Space-Management-System/blob/main/photos/export_tab.png)

> Make sure to place the above images in an `images/` folder in your repository.

---

## 📁 Project Structure

```bash
parking-space-management/
│
├── main.py                  # Main Streamlit app
├── CarParkPos               # Pickled slot positions
├── videos/                  # Sample videos
├── images/                  # Sample images & screenshots
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## 🚀 Features

- 🖼️ Upload parking lot image and draw slots manually
- 🎥 Upload parking video to detect occupied & free slots
- 🔄 Real-time slot status detection using image processing
- 💾 Save/load slot data (export/import)
- 📊 Displays count of available slots

---

## 🔧 Tech Stack

- **Python**
- **OpenCV**
- **Streamlit**
- **cvzone**
- **Numpy**

---

## 🖥️ How It Works

### 1. Slot Picker Tab 🎨
- Upload a clear parking lot image.
- Draw rectangles over parking slots manually.
- Save the selected slot coordinates.

### 2. Detection Tab 📹
- Upload a video showing the same parking lot.
- Click "Start Detection" to analyze the parking video.
- Real-time slot detection will highlight:
  - ✅ Green slots: Empty
  - ❌ Red slots: Occupied

### 3. Export/Import Tab 📦
- **Export**: Download and save your parking slot configuration.
- **Import**: Load pre-saved parking slot configuration to avoid redrawing.

---

## 🛠️ Installation

```bash
# Clone the repository
https://github.com/<your-username>/Parking-Space-Management-System.git

# Navigate to the project directory
cd Parking-Space-Management-System

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run main.py
```

---

## 🌐 Deployment
You can deploy this on:
- Streamlit Cloud
- Heroku (via `Procfile` + `requirements.txt`)
- Render

> Guide available upon request (just ask!)

---

## 📸 Sample Files
- `images/` → Add sample images to draw slots.
- `videos/` → Add sample video of parking area.

---

## 🙋‍♂️ Author

**Chandrakant**
- GitHub: [Chandrakant-2004](https://github.com/Chandrakant-2004)

---

## 📄 License

MIT License

---

## 💡 Note
- Use a clear, top-down parking lot image.
- Make sure video and image are from the same orientation.
