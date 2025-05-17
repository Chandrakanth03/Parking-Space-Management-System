import streamlit as st
import cv2
import pickle
import cvzone
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io

# Load positions file
positions_file = 'CarParkPos'

def load_positions():
    try:
        with open(positions_file, 'rb') as f:
            return pickle.load(f)
    except:
        return []

def save_positions(pos_list):
    with open(positions_file, 'wb') as f:
        pickle.dump(pos_list, f)

def check_parking_space(img, img_pro, pos_list, width, height):
    space_counter = 0
    for pos in pos_list:
        x, y = pos
        img_crop = img_pro[y:y + height, x:x + width]
        count = cv2.countNonZero(img_crop)
        color = (0, 255, 0) if count < 900 else (0, 0, 255)
        thickness = 5 if count < 900 else 2
        if count < 900:
            space_counter += 1
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)
    return space_counter, img

# Streamlit App
st.set_page_config(page_title="Parking Slot Detector")
st.title("🅿️ Parking Slot Detection")

# ✅ CSS override to ensure full image width and layout control
st.markdown("""
    <style>
    .main .block-container {
        padding: 1rem 2rem;
        max-width: none;
    }
    img {
        max-width: 100%;
        height: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Adjustable slot dimensions
width = st.sidebar.slider("Slot Width", min_value=50, max_value=200, value=107)
height = st.sidebar.slider("Slot Height", min_value=30, max_value=150, value=48)

# Tabs
tabs = st.tabs(["🎨 Slot Picker", "📹 Detection", "📦 Export/Import"])

# Slot Picker Tab
with tabs[0]:
    st.header("Draw Slots Over Image")
    uploaded_image = st.file_uploader("Upload a Parking Lot Image", type=["jpg", "png"])

    if uploaded_image:
        image = Image.open(uploaded_image).convert("RGB")
        image_np = np.array(image)

        # ✅ Display actual image size
        st.image(image_np, caption="Image to Pick Slots", use_column_width=False)

        # ✅ Canvas matches actual image size
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",
            stroke_width=2,
            stroke_color="#000000",
            background_image=image,
            update_streamlit=True,
            height=image_np.shape[0],
            width=image_np.shape[1],
            drawing_mode="rect",
            key="canvas",
        )

        if st.button("Save Slots"):
            pos_list = []
            if canvas_result.json_data is not None:
                for obj in canvas_result.json_data["objects"]:
                    left, top = int(obj["left"]), int(obj["top"])
                    pos_list.append((left, top))
                save_positions(pos_list)
                st.success("Slots saved successfully!")

# Inside Detection Tab
with tabs[1]:
    st.header("Real-Time Parking Slot Detection")
    uploaded_video = st.file_uploader("Upload Parking Lot Video", type=["mp4", "avi"])

    if uploaded_video:
        pos_list = load_positions()
        tfile = f"temp_{uploaded_video.name}"
        detection_key = f"detection_done_{uploaded_video.name}"

        # Save uploaded video temporarily
        with open(tfile, 'wb') as f:
            f.write(uploaded_video.read())

        cap = cv2.VideoCapture(tfile)
        stframe = st.empty()
        count_placeholder = st.empty()

        if st.button("Start Detection"):
            if st.session_state.get(detection_key):
                st.warning("This video was already processed. Reload or upload a new video to run detection again.")
            else:
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
                    img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                       cv2.THRESH_BINARY_INV, 25, 16)
                    img_median = cv2.medianBlur(img_thresh, 5)
                    kernel = np.ones((3, 3), np.uint8)
                    img_dilate = cv2.dilate(img_median, kernel, iterations=1)

                    space_counter, processed_frame = check_parking_space(frame, img_dilate, pos_list, width, height)
                    stframe.image(processed_frame, channels="BGR", use_column_width=True)
                    count_placeholder.markdown(f"### Free Slots: {space_counter}/{len(pos_list)}")
                cap.release()
                st.session_state[detection_key] = True  # Mark video as processed
                st.success("Detection Complete!")

# Export/Import Tab
with tabs[2]:
    st.header("Backup and Share Slot Positions")

    # Export
    if st.button("Export Slot Data"):
        pos_list = load_positions()
        b = io.BytesIO()
        pickle.dump(pos_list, b)
        b.seek(0)
        st.download_button("Download Slot Data", b, file_name="CarParkPos.pkl")

    # Import
    uploaded_pkl = st.file_uploader("Upload Slot Data File", type=["pkl"])
    if uploaded_pkl:
        pos_list = pickle.load(uploaded_pkl)
        save_positions(pos_list)
        st.success("Slot data imported successfully!")
