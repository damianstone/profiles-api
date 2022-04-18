from rest_framework import serializers

from profiles_api import models

""" 
Serializers in Django REST Framework are responsible for converting 
objects into data types understandable by javascript and front-end frameworks

also to check the types that enter to the api
"""


class HelloSerializer(serializers.Serializer):
    # name field for testing out APIView
    name = serializers.CharField(max_length=10)


class ProfileSerializer(serializers.ModelSerializer):
    # name field for testing out APIView

    class Meta:
        model = models.UserProfile
        # what the object will have (the fields u gonna show)
        fields = ('id', 'name', 'email', 'password')
        extra_kwards = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    """Create and return a new object"""

    def create(self, validated_data):
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user

# serializers profile feed items


class ProfileFeedItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}
