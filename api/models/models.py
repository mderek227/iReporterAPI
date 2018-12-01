red_flags = []


class RedFlag:

    def __init__(self, red_flag_id, red_flag_latitude, red_flag_longitude, red_flag_desc, user_id,status):
        self.red_flag_id = red_flag_id
        self.red_flag_latitude = red_flag_latitude
        self.red_flag_longitude = red_flag_longitude
        self.red_flag_desc = red_flag_desc
        self.user_id = user_id
        self.status = status

    def to_dict(self):
        """A method to Convert the red_flag instance to a dictionary"""
        red_flag = {
            'red_flag_id': self.red_flag_id,
            'red_flag_latitude': self.red_flag_latitude,
            'red_flag_longitude': self.red_flag_longitude,
            'red_flag_desc': self.red_flag_desc,
            'user_id': self.user_id,
            'status': self.status
        }
        return red_flag


users_list = []


class Users:

    def __init__(self, user_id, username, password, email):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email

    def to_dict(self):
        user = {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'email': self.email
        }
        return user

