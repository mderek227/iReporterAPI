import unittest
import json

from run import create_app
from api.models.models import RedFlag, red_flags


class TestEndpoints(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.app = app.test_client()
        self.red_flags = red_flags

        self.signup_fields = {
            "username": "derek",
            "password": 12345,
            "email": "derek@gmail.com",
        }

        self.login_field = {
            "username": "derek",
            "password": "12345"
        }

        self.app.post(
            '/api/auth/signup', content_type='application/json',
            data=json.dumps(
                dict(
                    username=self.signup_fields['username'],
                    email=self.signup_fields['email'],
                    password=self.signup_fields['password'],
                )
            )
        )
        login_result = self.app.post('/api/auth/login', content_type='application/json',
                                    data=json.dumps(
                                                   dict(
                                                       username=self.login_field['username'],
                                                       password=self.login_field['password'])
                                               )

                                         )
        self.result = json.loads(login_result.data)
        self.user_generated_token = self.result['token']

    def test_token(self):
        self.assertNotEqual(self.result['token'], " ")

    def signup_user(self):
        register_user = dict(username="derek", email="derek@gmail.com", password=12345)
        response = self.app.post('/api/auth/signup', json=register_user, headers={"token": self.user_generated_token})
        assert "message" in str(response.data)

    def login_user(self):
        register_user = dict(username="derek", email="derek@gmail.com", password=12345)
        response = self.app.post('/api/auth/signup', json=register_user, headers={"token": self.user_generated_token})
        assert "message" in str(response.data)

    def test_data_structure(self):
        self.assertTrue(isinstance(red_flags, list))

    def test_create_red_flag(self):
        post_record = dict(red_flag_latitude=32.454545, red_flag_longitude=10.323232, red_flag_desc="Bribery",
                          user_id=1, status="Resolved")
        response = self.app.post('/api/v1/red_flag', json=post_record, headers={"token": self.user_generated_token})
        assert "message" in response.data
        assert response.status_code == 201
        assert response.headers["Content-Type"] == "application/json"

    def test_empty_red_flag_latitude_fields(self):
        post_record = dict(red_flag_latitude=" ", red_flag_longitude=10.323232, red_flag_desc="Bribery",
                          user_id=1,  status="Resolved")
        response = self.app.post('/api/v1/red_flag', json=post_record,headers={"token": self.user_generated_token})
        assert "error" in str(response.data)
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"
        assert "Latitude coordinates can not be empty" in json.loads(response.data)['error']['red_flag_latitude']

    def test_empty_red_flag_longitude_fields(self):
        post_record = dict(red_flag_latitude=32.454545, red_flag_longitude=" ", red_flag_desc="Bribery",
                          user_id=1, status="Resolved")
        response = self.app.post('/api/v1/red_flag', json=post_record ,headers={"token": self.user_generated_token})
        assert "error" in str(response.data)
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"
        assert "Longitude coordinates can not be empty" in json.loads(response.data)['error']['red_flag_longitude']

    def test_empty_red_flag_desc_fields(self):
        post_record = dict(red_flag_latitude=32.454545, red_flag_longitude=10.323232, red_flag_desc="",
                          user_id=1, status="Resolved")
        response = self.app.post('/api/v1/red_flag', json=post_record,headers={"token": self.user_generated_token})
        assert "error" in str(response.data)
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"
        assert "Description cannot be empty" in json.loads(response.data)['error']['red_flag_desc']


    def test_empty_status_fields(self):
        post_record = dict(red_flag_latitude=32.454545, red_flag_longitude=10.323232, red_flag_desc="Bribery",
                          user_id=1, status=" ")
        response = self.app.post('/api/v1/red_flag', json=post_record, headers={"token": self.user_generated_token})
        assert "error" in str(response.data)
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"
        assert "status can not be empty" in json.loads(response.data)['error']['status']

    def test_user_id_fields(self):
        post_record = dict(red_flag_latitude=32.454545, red_flag_longitude=10.323232, red_flag_desc="Bribery",
                          user_id=-1, status="Resolved")
        response = self.app.post('/api/v1/red_flag', json=post_record, headers={"token": self.user_generated_token})
        assert "error" in str(response.data)
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"
        assert "user_id cant be less than 0" in json.loads(response.data)['error']['user_id']

    def test_invalid_red_flag_latitude_field_inputs(self):
        post_record = dict(red_flag_latitude="location", red_flag_longitude=10.323232, red_flag_desc="Bribery",
                          user_id=-1, status="Resolved")
        response = self.app.post('/api/v1/red_flag', json=post_record, headers={"token": self.user_generated_token})
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"
        assert "should be an integer" == json.loads(response.data)['error']['red_flag_latitude']

    def test_invalid_red_flag_longitude_field_inputs(self):
        post_record = dict(red_flag_latitude=32.454545, red_flag_longitude="location", red_flag_desc="Bribery",
                          user_id=1, status="Resolved")
        response = self.app.post('/api/v1/red_flag', json=post_record,headers={"token": self.user_generated_token} )
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"
        assert "should be an integer" == json.loads(response.data)['error']['red_flag_longitude']

    def test_invalid_status_field_inputs(self):
        post_record = dict(red_flag_latitude=32.454545, red_flag_longitude=10.323232, red_flag_desc="Bribery",
                          user_id=1, status="Resolved")
        response = self.app.post('/api/v1/red_flag', json=post_record,headers={"token": self.user_generated_token} )
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"
        assert "status should be a string" == json.loads(response.data)['error']['status']

    def test_user_id_field_inputs(self):
        post_record = dict(red_flag_latitude=32.454545, red_flag_longitude=10.323232, red_flag_desc="Bribery",
                          user_id="nine", status="Resolved")
        response = self.app.post('/api/v1/red_flag', json=post_record,headers={"token": self.user_generated_token} )
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"
        assert "user_id should be an integer" == json.loads(response.data)['error']['user_id']

    def test_invalid_red_flag_desc_field_inputs(self):
        post_record = dict(red_flag_latitude=32.454545, red_flag_longitude=10.323232, red_flag_desc=525,
                          user_id=1, status="Resolved")
        response = self.app.post('/api/v1/red_flag', json=post_record, headers={"token": self.user_generated_token})
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"
        assert "should be a string" == json.loads(response.data)['error']['red_flag_desc']

    def test_get_all_red_flags(self):
        post_record = dict(red_flag_latitude=32.454545, red_flag_longitude=10.323232, red_flag_desc="Bribery",
                          user_id=1, status="Resolved")
        post_record2 = dict(red_flag_latitude=15.121212, red_flag_longitude=25.040404, red_flag_desc="Nepotism",
                           user_id=2, status="Rejected")
        response = self.app.post('/api/v1/red_flag', json=post_record,headers={"token": self.user_generated_token})
        response2 = self.app.post('/api/v1/red_flag', json=post_record2,headers={"token": self.user_generated_token} )
        response3 = self.app.get('/api/v1/red_flag', headers={"token": self.user_generated_token})
        assert response3.status_code == 200
        assert response3.headers["Content-Type"] == "application/json"
        assert "Bribery" and "Nepotism" in str(response3.data)

    def test_get_red_flag_by_id(self):
        response = self.app.post('/api/v1/red_flag',headers={"token": self.user_generated_token} )
        response1 = self.app.get('/api/v1/red_flag/1' ,headers={"token": self.user_generated_token})
        response2 = self.app.get('api/v1/red_flag/w',headers={"token": self.user_generated_token} )
        assert response1.status_code == 200
        assert response2.status_code == 404
        assert response1.headers["Content-Type"] == "application/json"

    def test_red_flag_by_user_id(self):
        response = self.app.post('/api/v1/red_flag',headers={"token": self.user_generated_token})
        response1 = self.app.get('/api/v1/users/1/red_flag',headers={"token": self.user_generated_token})
        response2 = self.app.get('/api/v1/users/w/red_flag',headers={"token": self.user_generated_token})
        assert response1.status_code == 200
        assert response2.status_code == 404
        assert response1.headers["Content-Type"] == "application/json"

    def test_cancel_red_flag(self):
        response = self.app.post('/api/v1/red_flag',headers={"token": self.user_generated_token})
        response2 = self.app.get('/api/v1/red_flag/h/cancel', headers={"token": self.user_generated_token})
        assert response2.status_code == 404
        
