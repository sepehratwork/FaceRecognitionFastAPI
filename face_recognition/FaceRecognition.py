import glob
import logging
import cv2
from deepface import DeepFace


persons_db_path = "static/Person_db"
person_face_db_path = "static/Person_face_db"
persons = 1
metrics = ["cosine", "euclidean", "euclidean_l2"]
backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe', 'yolov8', 'yunet', 'fastmtcnn']
models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
video_path = "static/task-video.mp4"


def crop_faces(image):
    faces = DeepFace.extract_faces(img_path=image, target_size=(224, 224), detector_backend=backends[3])
    faces_list = []
    for face in faces:
        A_x = face["facial_area"]["x"]
        A_y = face["facial_area"]["y"]
        B_x = face["facial_area"]["x"] + face["facial_area"]["w"]
        B_y = face["facial_area"]["y"] + face["facial_area"]["h"]
        face_cropped = image[A_y:B_y, A_x:B_x]
        faces_list.append(face_cropped)
    return faces_list


def recognize():

    cap = cv2.VideoCapture(video_path)

    counter=0
    ret = True
    frames = []

    while ret:

        counter+=1

        ret, frame = cap.read()

        faces = crop_faces(frame)

        # finding match(es) for each face of the frame in the database
        print(f"frame {counter}")
        for face in faces:
            for j in range(persons):
                person_face_db = glob.glob(f"{person_face_db_path}/Person_{j+1}*.jpg")
                for k, face_db in enumerate(person_face_db):
                    image_face = cv2.imread(face_db)
                    result = DeepFace.verify(img1_path=face , img2_path=image_face,
                                                model_name=models[1], detector_backend=backends[6],
                                                distance_metric=metrics[0], enforce_detection=False)
                    if result["verified"]:
                        cv2.imwrite(f"frame_{counter}_facedb_{k}_{result['distance']}.jpg", face)
                        cv2.imwrite(f"frame_{counter}.jpg", frame)
                        logging.info(f"found person {j} in frame {counter}")
                        frames.append(f"frame {counter}")
    
    frames = set(frames)
    return frames
