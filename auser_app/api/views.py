from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from Management.models import User, AbstractUser
from django.contrib.auth import authenticate
from auser_app.api.serializers import UserRegistrationSerializer



@api_view(['POST',])
def registration_view(request):

    email=request.data.get('email')
    if User.objects.filter(email=email).exists():
        return Response({"Message":"User mail_id already exists You can login now with your email and password."})

    if request.method == 'POST':
        data= request.data.copy()
        
        if data.get('role') == 'librarian':
            return Response(
                {"error": "You cannot register as a Librarian."},
                status=status.HTTP_400_BAD_REQUEST
            )

        data['role']='user'
        serializer = UserRegistrationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':"User Registration is Successful"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       
@api_view(['POST'])
def login_view(request):
    username= request.data.get("username") 
    password = request.data.get("password")  

    #check if user exists
    if not User.objects.filter(username=username).exists():
        return Response({"error":"user not Registerd"}, status=status.HTTP_400_BAD_REQUEST)

    #authenticate user
    user=authenticate(username=username, password=password)
    if user is not None:
        refresh=RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
