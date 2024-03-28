
from rest_framework.generics import GenericAPIView
from authentication.serializers import RegisterSerializer,LoginSerializer,UserSerializer
from rest_framework import response, status,permissions
from django.contrib.auth import authenticate
from authentication.jwt import JWTAuthentication
from authentication.models import User



# Create your views here.

class AuthUserAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes= [JWTAuthentication,]
    serializer_class = UserSerializer
 

    def get(self, request, ):
        user = request.user
        serializer = UserSerializer(user)
        return response.Response({"user" : serializer.data})


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():        
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response.Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)

        if user:
            # Generate JWT token
            token = user.token

            # Serialize user data including token
            serializer = self.serializer_class(user)
            response_data = serializer.data

            # Include token in response data
            response_data['token'] = token

            # Return serialized user data with token in response
            return response.Response(response_data, status=status.HTTP_200_OK)
        else:
            return response.Response({'message': "Invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)


