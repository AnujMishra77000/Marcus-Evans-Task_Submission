from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from User_app.api.serializers import UserRegistrationSerializer




@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email

            refresh = RefreshToken.for_user(account)
            data['token'] = {
                                 'refresh': str(refresh),
                                 'access': str(refresh.access_token),
                             }
             
@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
