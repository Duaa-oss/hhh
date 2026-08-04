import cv2
from deepface import DeepFace

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        if isinstance(result, list):
            result = result[0]

        x = result['region']['x']
        y = result['region']['y']
        w = result['region']['w']
        h = result['region']['h']

        face = frame[y:y+h, x:x+w]

        if face.size != 0:
            blur = cv2.GaussianBlur(face, (99, 99), 30)
            frame[y:y+h, x:x+w] = blur

        emotion = result['dominant_emotion']

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, emotion, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)

    except Exception:
        pass

    cv2.imshow("Face Expression + blur ", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()