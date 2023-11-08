import os
import pickle

FACE_DB_FILE = 'faces.db'


class FaceDB:
    _instance = None

    @staticmethod
    def get_instance():
        if not FaceDB._instance:
            FaceDB._instance = FaceDB()
        return FaceDB._instance

    def __init__(self):
        self.faces = {}
        if os.path.exists(FACE_DB_FILE):
            with open(FACE_DB_FILE, 'rb') as db_file:
                self.faces = pickle.load(db_file)

    def save_user(self, name, filename):
        self.faces[filename] = name
        with open(FACE_DB_FILE, 'wb') as db_file:
            pickle.dump(self.faces, db_file)

    def get_user(self, filename):
        return self.faces[filename]

    def get_all_user(self):
        return list(self.faces.keys())
