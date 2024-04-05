from rest_framework import serializers
from authentication.models import User




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']



class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length = 128, min_length = 6, write_only = True, style={'input_type': 'password'})      #Defines the passwor to only be write only, so it should not return it to the server

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 128, min_length = 6, write_only = True,style={'input_type': 'password'})      #Defines the password to only be write only, so it should not return it to the server

    class Meta:
        model = User
        fields = ('email', 'username','password','token')

        read_only_fields = ['token'] 

