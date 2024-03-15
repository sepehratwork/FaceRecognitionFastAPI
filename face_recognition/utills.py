import cv2
import glob
from face_recognition import FaceRecognition
import logging


def create_person_face_db(persons_db_path, person_face_db_path, persons):
    for i in range(persons):
        images = glob.glob(f"{persons_db_path}/Person_{i+1}*.jpg")
        for j, image in enumerate(images):
            image = cv2.imread(image)
            face = FaceRecognition.crop_faces(image)[0]
            cv2.imwrite(f"{person_face_db_path}/Person_{i+1}_face_{j+1}.jpg", face)
