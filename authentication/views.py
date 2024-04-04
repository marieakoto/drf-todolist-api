
from rest_framework.views import APIView
from authentication.serializers import RegisterSerializer,LoginSerializer,UserSerializer
from rest_framework import response, status,permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response



class AuthUserAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, ):
        user = request.user
        serializer = self.serializer_class(user)
        return response.Response({"user" : serializer.data})


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():        
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response.Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(username=email, password=password)

        serializer = self.serializer_class(user)
        response_data = serializer.data

        refresh = RefreshToken.for_user(user)
        token = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        
        response_data['token'] = token

        return Response(response_data, status=status.HTTP_200_OK)

        # return JsonResponse(
        #         {"status": "success", "data": {"token": token, "user": request.data.get('username')}},
        #         status=status.HTTP_200_OK,
        #         safe=False,
        #     )

        

        # if user:
        #     # Generate JWT token
        #     token = user.token

        #     # Serialize user data including token
        #     serializer = self.serializer_class(user)
        #     response_data = serializer.data

        #     # Include token in response data
        #     response_data['token'] = token

        #     # Return serialized user data with token in response
        #     return response.Response(response_data, status=status.HTTP_200_OK)
        # else:
        #     return response.Response({'message': "Invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)


