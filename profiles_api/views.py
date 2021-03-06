from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
''' TokenAuthentication is a random token string when the user login and then every request the user makes to that API which need to authenticate, the token string is added to the request and that's effectively works as a password to check that every request made is authenticated correctly'''
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
# from rest_framework.permissions import IsAuthenticatedOrReadOnly

from profiles_api import serializers 
from profiles_api import models
from profiles_api import permissions

class HelloApiView(APIView):
    '''Test API View'''
    serializer_class = serializers.HelloSerializer
    
    def get(self, request, format=None):
        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})
    
    def post(self, request):
        '''Create a hello message with our name'''
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                )

    def put(self, request, pk=None):
        '''Handle updating an object'''
        return Response({'method': 'PUT'})
    
    def patch(self, request, pk=None):
        '''Handle a partial update of an object'''
        return Response({'method': 'PATCH'})
    
    def delete(self,request, pk=None):
        '''Delete an object'''
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLS using Routers',
            'Provides more functionality with less code',
        ]
        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message."""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})
    
    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})
    
    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})
    
    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})
    

class UserProfileViewSet(viewsets.ModelViewSet):
    '''Handle creating and updating profiles'''
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)
class UserLoginApiView(ObtainAuthToken):
    '''Handle Creating user authentication tokens for login'''
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    '''Handles creating, reading and updating profile feed items'''
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)
    
    #To associate the serializer_class (user_profile) with the authenticated user, we use perform_create to save this linkage between both.   
    def perform_create(self, serializer):
        '''sets the user profile to the logged in user'''
        serializer.save(user_profile=self.request.user)



"""Note for permission_classes for UserProfileFeedViewSet: if we do not define permission_classes, in the case of logout (not authenticated), feeding post return to an error page. But, we permission_classes, a API page pops up with no access to an edit/update.
IsAuthenticated: Restrict viewing status feed updates to logged in users only
IsAuthenticatedOrReadOnly: Viewing/GET status feed updates to anyone!"""






