from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import Http404
from rest_framework import status
from movies.models import Genre, Movie, MovieRole
from rest_framework import exceptions
from movies.serializers import GenreSerializer, MovieSerializer, MovieRoleSerializer
from role.decorators import iam
import logging
LOGGER = logging.getLogger(__name__)


class BaseAPIView(APIView):
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

class GenreAPIView(BaseAPIView):
    """
        APIView for Genre CRUD
    """
    def get_object(self, id):
        try:
            return Genre.objects.get(id = id)
        except Genre.DoesNotExist:
            raise exceptions.ValidationError({"success": False,
                "error": {
                    "genre_errors": [
                        "genre details not found"
                        ]
                }
            })

    def get(self, request):
        id = request.query_params.get('genre_id',None)
        if id:
            genre = self.get_object(id)
            serializer = GenreSerializer(genre)
        else:
            genre = Genre.objects.all()
            serializer = GenreSerializer(genre, many=True)
        
        return Response({'data':serializer.data,'success':True}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except:
                return Response({'error':serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'data':serializer.data,'success':True}, status=status.HTTP_201_CREATED)
        return Response({'error':serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,format=None):
        id = request.data.get('genre_id',None)
        genre = self.get_object(id)
        if genre:
            serializer = GenreSerializer(genre, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'success':True}, status=status.HTTP_200_OK)
        return Response({'error':serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        id = request.data.get('genre_id',None)
        genre = self.get_object(id)
        if genre:
            genre.delete()
            return Response({'success':True},status=status.HTTP_204_NO_CONTENT)
        return Response({'error':{'genre':["NOT PRESENT"]}, 'success':False}, status=status.HTTP_400_BAD_REQUEST)


class MovieAPIView(BaseAPIView):
    """
        APIView for Movie CRUD
    """
    def get_object(self, id):
        try:
            return Movie.objects.get(id=id, is_active = True)
        except Movie.DoesNotExist:
            raise exceptions.ValidationError({"success": False,
                "error": {
                    "movie_errors": [
                        "movie details not found"
                        ]
                }
            })

    
    @iam(permission = 'read_movie')
    def get(self, request, auth, format=None, *args, **kwargs):
        id = request.query_params.get('movie_id',None)
        role_exists = Movie.objects.filter(role__permission__slug = "read_movie", role__user_role__id = auth['user_id'], is_active = True)
        if id:
            role_exists = role_exists.filter(id = id)
            if auth['is_admin'] or role_exists.exists():
                movie = self.get_object(id)
                serializer = MovieSerializer(movie)
            else:
                return Response({'data':[],'success':True}, status=status.HTTP_200_OK)

        else:
            if auth['is_admin']:
                movie = Movie.objects.filter(is_active = True)
            else:
                movie = role_exists.distinct('id')
            serializer = MovieSerializer(movie, many=True)
        
        return Response({'data':serializer.data,'success':True}, status=status.HTTP_200_OK)

    @iam(permission = 'create_movie')
    def post(self, request, auth, format=None, *args, **kwargs):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'success':True}, status=status.HTTP_201_CREATED)
        return Response({'error':serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)

    @iam(permission = 'update_movie')        
    def put(self, request, auth, format=None, *args, **kwargs):
        id = request.data.get('movie_id',None)
        movie = self.get_object(id)
        serializer = MovieSerializer(movie, data=request.data)
        if movie:
            role_exists = Movie.objects.filter(role__permission__slug =  "update_movie", role__user_role__id = auth['user_id'], id=id, is_active= True ).distinct('id')
            if auth['is_admin'] or role_exists.exists() :

                if serializer.is_valid():
                    # try:
                    serializer.save()
                    # except Exception as e:
                    #     Response({'error':e.message, 'success':False}, status=status.HTTP_400_BAD_REQUEST)
                    return Response({'data':serializer.data,'success':True}, status=status.HTTP_200_OK)
        return Response({'error':serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)

    @iam(permission = 'delete_movie')    
    def delete(self, request, auth, format=None, *args, **kwargs):
        id = request.data.get('movie_id',None)
        movie = self.get_object(id)
        if movie :
            role_exists = Movie.objects.filter(role__permission__slug =  "delete_movie", role__user_role__id = auth["user_id"], id=id, is_active= True ).distinct('id')
            if auth['is_admin'] or role_exists.exists() :
                movie.is_active = False
                movie.save()
                return Response({'success':True})
            else:
                return Response({'error':{'unauthorized':["UNAUTHORIZED USER"]}, 'success':False}, status=status.HTTP_400_BAD_REQUEST)    
        return Response({'error':{'movie':["NOT PRESENT"]}, 'success':False}, status=status.HTTP_400_BAD_REQUEST)

class MovieRoleAPIView(BaseAPIView):
    """
        APIView for MovieRole CRUD
    """
    def get_object(self, role_id, movie_id):
        try:
            return MovieRole.objects.get(role_id = role_id, movie_id = movie_id)
        except MovieRole.DoesNotExist:
            raise exceptions.ValidationError({"success": False,
                "error": {
                    "movie_role_errors": [
                        "Movie-Role details not found"
                        ]
                }
            })

    @iam(permission = 'read_movie_role')
    def get(self, request, auth, format=None, *args, **kwargs):
        role_id = request.query_params.get('role_id',None)
        movie_id = request.query_params.get('movie_id',None)
        if role_id and movie_id:
            movie_role = self.get_object(role_id,movie_id)
            serializer = MovieRoleSerializer(movie_role)
        else:
            movie_role = MovieRole.objects.all()
            serializer = MovieRoleSerializer(movie_role, many=True)
        
        return Response({'data':serializer.data,'success':True}, status=status.HTTP_200_OK)

    @iam(permission = 'create_movie_role')
    def post(self, request, auth, format=None, *args, **kwargs):
        serializer = MovieRoleSerializer(data=request.data)
        # print request.data
        # print serializer.is_valid()
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'success':True}, status=status.HTTP_201_CREATED)
        return Response({'error':serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)

    @iam(permission = 'delete_movie_role')    
    def delete(self, request, auth, format=None, *args, **kwargs):
        role_id = request.data.get('role_id',None)
        movie_id = request.data.get('movie_id',None)
        movie_role = self.get_object(role_id,movie_id)
        if movie_role:
            movie_role.delete()
            return Response({'success':True})
        return Response({'error':{'movie-role':["NOT PRESENT"]}, 'success':False}, status=status.HTTP_400_BAD_REQUEST)
