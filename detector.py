import cv2
import time 

# define paths to the xml files

face_cascade_path = "haarcascade_frontalface_default.xml"
eye_cascade_path = "haarcascade_eye_tree_eyeglasses.xml"

# load the classifiers

face_cascade = cv2.CascadeClassifier(face_cascade_path)
glasses_cascade = cv2.CascadeClassifier(eye_cascade_path)

# start vid capture || webcam

cap = cv2.VideoCapture(0)

# check if cam opened successfully
if not cap.isOpened():
    print("Error: S'po hapet Kamera")
    exit()
    
print ("Kamera u hap, 'q' to exit")

# main loop for detection

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    #  detect faces 
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(50, 50)) 
    # scano te gjitha fytyrat ne frame te kapura
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        roi_gray = gray[y:y+h, x:x+w]
        
        # scano per syze te  fytyrat e roi (region of interest)
        glasses = glasses_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
        
        # krahaso skanimiet 
        if len(glasses) > 0:
            status = "Syze: Po"
            color = 90, 255, 0 
        else:
            status = "Syze: Jo"
            color = 0, 0, 255
            
            # trego statusin siper fytyrave
        cv2.putText(frame, status, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
        # shfaq rezulatet 
    cv2.imshow('Alarm Katerfenershash', frame)

        # exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    time.sleep(0.02)



cap.release()
cv2.destroyAllWindows()