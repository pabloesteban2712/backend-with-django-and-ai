import jwt
import datetime

from django.conf import settings

class Helpers():
    def generate_jwt(payload):
        payload['exp'] = datetime.datetime.now() + datetime.timedelta(365)

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm = "HS256")
        
        return token