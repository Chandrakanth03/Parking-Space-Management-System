import streamlit as st
import cv2
import pickle
import cvzone
import numpy as np
import tempfile

# Function to process the video and image
def process_parking_detection(video_file, image_file):
    # Reading video
    cap = cv2.VideoCapture(video_file.name)

    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)

    width, height = 107, 48

    def checkParkingSpace(imgPro):
        spaceCounter = 0

        for i, pos in enumerate(posList):
            x, y = pos

            imgCrop = imgPro[y:y + height, x:x + width]
            count = cv2.countNonZero(imgCrop)

            if count < 900:
                color = (0, 255, 0)
                thickness = 5
                spaceCounter += 1
            else:
                color = (0, 0, 255)
                thickness = 2

            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
            cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                               thickness=2, offset=0, colorR=color)

        cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                           thickness=5, offset=20, colorR=(0, 200, 0))

    # Image to be used for parking slot detection
    img = cv2.imread(image_file.name)

    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, img = cap.read()
        if not success:
            break  # Break if the video ends

        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

        checkParkingSpace(imgDilate)
        cv2.imshow("Image", img)
        cv2.imshow("ImageThres", imgMedian)
        cv2.waitKey(10)
    
    cv2.destroyAllWindows()

# Streamlit UI
def main():
    st.title("Parking Slot Detection")

    # File uploader widgets
    uploaded_video = st.file_uploader("Upload Parking Lot Video", type=["mp4", "avi", "webm"])
    image_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

    if video_file and image_file:
        st.image(image_file, caption="Uploaded Image", use_column_width=True)

        # Use tempfile to store the uploaded files
        with tempfile.NamedTemporaryFile(delete=False) as temp_video, tempfile.NamedTemporaryFile(delete=False) as temp_image:
            temp_video.write(video_file.read())
            temp_image.write(image_file.read())

            st.video(temp_video.name)

            # Run parking detection process
            process_parking_detection(temp_video, temp_image)

if __name__ == '__main__':
    main()
