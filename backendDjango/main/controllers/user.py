from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from main.models import User
from main.serializers import UserSerializer
from main.validator import UserValidatorForm
from main.helpers import Helpers

@csrf_exempt
def save(request):
    if request.method == "POST":

        password = request.POST.get("password", False)
        passwordEncoded = make_password(password)
        
        form = UserValidatorForm(request.POST) 

        if form.is_valid():


            user = User(
                name     = request.POST.get("name"),
                surname  = request.POST.get("surname"),
                nick     = request.POST.get("nick").lower(),
                email    = request.POST.get("email").lower(),
                bio     = request.POST.get("bio", False),
                password = passwordEncoded)
        else:
            return JsonResponse(
            {"status": "Error",
             "message": "Validation error"})
        
        try:
            userFinds = User.objects.filter(Q(email = user.email.lower()) | Q(nick = user.nick.lower())) 
        except:
            return JsonResponse(
            {"status": "Error",
             "message": "Error searching user"})
        
        if userFinds:
            return JsonResponse({
                "status": "error",
                "message": "User is already registered."
            })
        
        else:

            user.save()

            userSz = UserSerializer(user, many=False)

            return JsonResponse({
                "status": "success",
                "user": userSz.data
            })

@csrf_exempt
def login(request):
    if request.method == "POST":

        if request.POST and request.POST.get("email", False) and request.POST.get("password", False):

            email   = request.POST.get("email", False)
            password = request.POST.get("password", False) 

            userLogin = User.objects.filter(email = email)[0]

            passwordEncoded = userLogin.password

            if check_password(password, passwordEncoded) == True:

                userLoginS = UserSerializer(userLogin, many=False)

                token = Helpers.generate_jwt(userLoginS.data)

                return JsonResponse(
                {"status": "Success",
                 "user": userLoginS.data,
                "message": "No token"})

            else:
                
                return JsonResponse(
                {"status": "Error",
                "message": "Password is wrong"})
        
        else:
            
            return JsonResponse(
            {"status": "Error",
             "message": "Data error"})

        return JsonResponse({
            "status": "Success",
            "action": "Login"
    }) 
    else:
        return JsonResponse(
            {"status": "Error",
             "message": "HTTP method is not allowed"}, status=405)

@csrf_exempt
def profile(request):
    if request.method == "POST":
        
        if id:
            try:
                user = User.objects.get(id=id)

                userS = UserSerializer(user, many=False)

                return JsonResponse({
                    "status": "Success",
                    "message": userS.data
            }) 
                
            except Exception as e:

                return JsonResponse({
                    "status": "Success",
                    "message": "Error"
            })
        
        else:
            return JsonResponse(
                {"status": "Error",
                "message": "Not id"})
    
    else:
        return JsonResponse(
            {"status": "Error",
             "message": "HTTP method is not allowed"}, status=405)
    
