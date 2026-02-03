import jwt
from django.conf import settings
from django.http import JsonResponse

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):

        excluded_paths = ['/api/user/login', '/api/user/register']        

        if request.path in excluded_paths:
            return self.get_response(request)
        
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JsonResponse({
                "status": "error",
                "message": "Token required"
            })
        
        token = auth_header

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithm = "HS256")

            request.user = payload

        except jwt.ExpiredSignatureError:
            return JsonResponse({
                "status": "error",
                "message": "Token is no more valid"
            })
        
        except jwt.InvalidTokenError:
            return JsonResponse({
                "status": "error",
                "message": "Invalid Token "
            })
        
        response = self.get_response(request)
        return response

