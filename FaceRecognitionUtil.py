import face_recognition

from FaceDB import FaceDB


class FaceRecognitionUtil:
    def recognize(self, filename):
        users = FaceDB.get_instance().get_all_user()
        print(users)
        for user in users:
            known_image = face_recognition.load_image_file(user)
            unknown_image = face_recognition.load_image_file(filename)
            if len(face_recognition.face_encodings(unknown_image)) != 0:
                biden_encoding = face_recognition.face_encodings(known_image)[0]
                unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
                results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
                if results[0]:
                    return FaceDB.get_instance().get_user(user)
        return None
