import cv2
import dlib
import numpy as np
import time

# --- 1. Load Dlib Models ---
# The Dlib HOG (Histogram of Oriented Gradients) face detector is much more robust than Haar.
detector = dlib.get_frontal_face_detector()

# Load the pre-trained landmark predictor.
# NOTE: The file 'shape_predictor_68_face_landmarks.dat' must be in the same folder.
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# --- 2. Helper Functions ---

def get_landmarks(im, detector_obj, predictor_obj):
    """Detects face and returns 68 landmarks as a NumPy matrix."""
    
    # Dlib detects faces in the grayscale image
    rects = detector_obj(im, 1)

    if len(rects) > 0:
        # Get the 68 landmark points for the first face found
        return np.matrix([[p.x, p.y] for p in predictor_obj(im, rects[0]).parts()])
    return None

def check_for_glasses(frame, landmarks):
    """Crops the nose bridge region and uses Canny Edge detection to find the frame."""
    
    # 1. Define the ROI (Region of Interest) based on landmarks
    
    # We use the region between the inner eye corners (landmarks 39 and 42) and the nose bridge (27-30).
    # This minimizes background noise.
    
    # Define vertical bounds (y-axis): 
    # Use landmark 37 (inner top left eye) and landmark 30 (nose tip)
    y_top = landmarks[37, 1] - 5
    y_bottom = landmarks[30, 1] + 5 
    
    # Define horizontal bounds (x-axis): 
    # Use landmark 36 (outer left eye) and landmark 45 (outer right eye)
    x_left = landmarks[36, 0] + 5  
    x_right = landmarks[45, 0] - 5 

    # Ensure bounds are valid
    if y_top < 0 or y_bottom > frame.shape[0] or x_left < 0 or x_right > frame.shape[1] or x_left >= x_right or y_top >= y_bottom:
        return False # Invalid ROI

    # Crop the ROI from the color frame
    roi = frame[y_top:y_bottom, x_left:x_right]
    
    if roi.size == 0:
        return False

    # 2. Image Processing (Edge Detection)
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blur to smooth out noise (skin texture)
    blurred = cv2.GaussianBlur(roi_gray, (3, 3), 0)
    
    # Apply Canny Edge Detection (tweak the thresholds 50, 150 based on your lighting)
    edges = cv2.Canny(blurred, 50, 150)
    
    # 3. Decision Logic
    
    # Calculate the average intensity of edges (normalized measure)
    edge_intensity = np.sum(edges)
    roi_area = edges.shape[0] * edges.shape[1]
    avg_edge_intensity = edge_intensity / roi_area
    
    # --- Tuning Point ---
    # This threshold is the core of the detection. Tweak this value (e.g., 20, 30, 40)
    # until it reliably detects your specific glasses. Start at 30.
    EDGE_THRESHOLD = 30  
    
    # Optionally display the ROI and edges for visual tuning:
    # cv2.imshow("ROI", roi)
    # cv2.imshow("Edges", edges)
    
    if avg_edge_intensity > EDGE_THRESHOLD:
        return True # Glasses detected (strong horizontal edge found)
    else:
        return False # No strong horizontal edge found

# --- 3. Main Loop ---

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: S'po hapet Kamera")
    exit()
    
print ("Kamera u hap, 'q' to exit")

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Get landmarks
    landmarks = get_landmarks(gray, detector, predictor)
    
    # Default status before detection
    status = "Duke skanuar..."
    color = (0, 165, 255) # Orange
    
    if landmarks is not None:
        # Pass the current frame and landmarks to the detection function
        is_wearing_glasses = check_for_glasses(frame, landmarks)
        
        # Determine status and color
        if is_wearing_glasses:
            status = "Syze: PO (Dlib)"
            color = (0, 255, 0) # Green
        else:
            status = "Syze: JO (Dlib)"
            color = (0, 0, 255) # Red

        # Draw the status text near the nose bridge (using landmark 27 for positioning)
        nose_point = landmarks[27]
        cv2.putText(frame, status, (nose_point[0,0] - 50, nose_point[0,1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Optional: Draw a box around the face (using Dlib's rect)
        for rect in detector(gray, 1):
             cv2.rectangle(frame, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (255, 0, 0), 2)
             
        # Optional: Draw the 68 points on the face for visualization
        for idx, point in enumerate(landmarks):
             pos = (point[0, 0], point[0, 1])
             cv2.circle(frame, pos, 1, (255, 255, 0), -1)
        
    # Show the results
    cv2.imshow('Dlib Glasses Detector', frame)

    # Exit condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    time.sleep(0.01)


cap.release()
cv2.destroyAllWindows()