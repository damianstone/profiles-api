from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

"""
CRUD SECTION -> for the CRUD use ViewSets

we use serializes here to make sure which data type we are expecting
Basically, make sure of the data type we are receiving / sendingis the one that we want

The response is a HTTP request

"""

"""APIView to a create a basic http request api"""


class HelloApi(APIView):

    # implement serializers to check the data types
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        # return a list of apiviews features
        an_apiview = [
            'Uses http methods as function (gte, post, patch, put, delete)',
            'Is similitar to a tradition Django View',
            'Gives the most control to the app logic',
            'map manually to URLs'
        ]

        return Response({'message': 'Hello world', 'an_apiview': an_apiview})

    def post(self, request):
        # hello message with our name
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        # update an object
        # to a specific URL with the id of the object we want to update
        # replace the ENTIRE object with the object with are providing
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        # handle a partial update of an object
        # only update the fields what we are providing in the request
        # update a specfic propertie of the object without update anything more
        # only update the fields
        # better than path for user profile changes
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        # Delete an object
        return Response({'method': 'DELETE'})


"""ViewSets to create a CRUD"""


class HelloViewSet(viewsets.ViewSet):

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        a_viewset = [
            'Uses http methods as function (gte, post, patch, put, delete)',
            'Is similitar to a tradition Django View',
            'Gives the most control to the app logic',
            'map manually to URLs'
        ]
        return Response({'message': 'Hello!', 'list': a_viewset})

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello aweonao {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    # pk = primary key
    def retrieve(self, request, pk=None):
        # handle getting an object by its ID

        return Response({'http-method': 'GET'})

    # update the entire object
    def update(self, request, pk=None):
        return Response({'http-method': 'PUT'})

    # update a part of an object
    def partial_update(self, request, pk=None):
        return Response({'http-method': 'PATCH'})

    def destroy(self, request, pk=None):
        return Response({'http-method': 'DELETE'})


# handle creating and updating profiles
class ProfileViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.ProfileSerializer
    queryset = models.UserProfile.objects.all()
    # how the user gonna be authenticate
    authentication_classes = (TokenAuthentication,)
    # how the user get permission | the implementation of auth
    permission_classes = (permissions.UpdateOwnProfile,)
    # to search users
    filter_backends = (filters.SearchFilter,)
    # search based on...
    search_fields = ('name', 'email',)

# handle creating user authentication tokens


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# handle creating, reading and updating profile feed items
class UserProfileFeedViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticatedOrReadOnly
    )

    # sets the user profile to the logged in user
    def perform_create(self, serializer):
        # save is a function incluiding by defult in serializerModel
        serializer.save(user_profile=self.request.user)
