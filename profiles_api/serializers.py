from rest_framework import serializers
from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password':{'write_only': True, 'style': {'input_type': 'password'}}}
    
    '''The create() function is part of the ModelSerializer and is documented here: https://www.django-rest-framework.org/api-guide/serializers #saving-instances It's the function that's called by the Django REST Framework. We override it in the serializer.py file to make it call the custom create_user() function we added on the models.py.'''
    def create(self, validated_data):
        '''Create and return a new user'''
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user


     
    









