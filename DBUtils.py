import mysql.connector

from User import User

HOST = 'localhost'
USER_NAME = 'root'
PASSWORD = 'mysql'
DB = 'face_browser'


class DBUtils:
    _instance = None

    @staticmethod
    def get_instance():
        if not DBUtils._instance:
            DBUtils._instance = DBUtils()
        return DBUtils._instance

    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=HOST,
            database=DB,
            user=USER_NAME,
            password=PASSWORD
        )

    def disconnect(self):
        self.connection.close()

    def insert(self, sql):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
        except:
            self.connection.rollback()
        self.disconnect()

    def select(self, sql):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        self.disconnect()
        return records

    def create_user(self, first_name, last_name, email, mobile, username):
        sql = "INSERT INTO user (first_name, last_name, email, mobile, username) " \
              "VALUES ('{}', '{}', '{}', '{}', '{}')".format(first_name, last_name, email, mobile, username)
        self.insert(sql)

    def get_user(self, username):
        sql = "SELECT * FROM user WHERE username = '{}' LIMIT 1".format(username)
        record = self.select(sql)
        if record:
            user = User()
            user.user_id = record[0][0]
            user.first_name = record[0][1]
            user.last_name = record[0][2]
            user.email = record[0][3]
            user.mobile = record[0][4]
            user.username = record[0][5]

            return user
        else:
            return None

    def save_domain(self, user_id, domain, username, password):
        sql = "INSERT INTO domainInfo (user_id, domain, username, password) " \
              "VALUES  ('{}', '{}', '{}', '{}')".format(user_id, domain, username, password)
        self.insert(sql)

    def get_domain_info(self, user_id, url):
        sql = "SELECT * FROM domainInfo WHERE user_id=" + str(user_id)
        records = self.select(sql)
        for record in records:
            if record[2] in url:
                return record
        return None
