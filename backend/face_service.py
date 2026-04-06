from deepface import DeepFace
import numpy as np

def get_embedding(image_path):
    result = DeepFace.represent(
        img_path=image_path,
        model_name="Facenet",
        enforce_detection=False
    )
    return np.array(result[0]["embedding"])
