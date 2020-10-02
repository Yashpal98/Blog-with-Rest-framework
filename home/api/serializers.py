from django.contrib.auth.models import User

from rest_framework import serializers


''' Serializer used to convert data into another format like json '''

class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {'paasword':{'write-only':True}}

    def save(self):
        user = User(
            email = self.validated_data['email'],
            username = self._validated_data['username']
        )
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match'})
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user

class AccountPropertiesSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ['pk', 'email', 'username', 'first_name', 'last_name']

class ChangePasswordSerializer(serializers.Serializer):
    
	old_password 				= serializers.CharField(required=True)
	new_password 				= serializers.CharField(required=True)
	confirm_new_password 		= serializers.CharField(required=True)