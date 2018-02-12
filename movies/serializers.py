from django.db import IntegrityError
from rest_framework import serializers
from models import Movie, Genre, MovieRole
from rest_framework import exceptions
# from rbac.serializers import RoleSerializer

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('create_dttm', 'update_dttm')
    
    def to_internal_value(self, data):
        name = data.get('name')
        if not name or '':
            raise exceptions.ValidationError({"name_errors": [
                "name is a required field and cannot be empty"]})

        # validation for slug
        slug = data['name'].lower().replace('-','_')
        exists, obj = Genre.slug_exists(slug)
        if exists:
            raise exceptions.ValidationError({"slug_errors": [
                        "There is a movie with same slug so choose  different name"]})            
        return {
                'name': data['name']
              }

    def create(self, validated_data):
        slug = validated_data['name'].lower().replace('-','_')
        new_genre = Genre(name=validated_data['name'],slug = slug)
        new_genre.save()
        # add genre
        return new_genre


class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    # role = RoleSerializer(many=True)

    def to_representation(self, instance):
        ret = super(MovieSerializer, self).to_representation(instance)
        ret['99popularity'] = ret['popularity_99']
        del ret['popularity_99']
        return ret

    def to_internal_value(self, data):
        popularity_99 = data.get('99popularity')
        # validation for popularity_99
        # print isinstance(popularity_99,float)
        
        if  not (popularity_99 and isinstance(popularity_99,float)):
            raise exceptions.ValidationError({
                                '99popularity_errors': ['This field is required and should be float .']
                                })
        else:
            if float(popularity_99) > 100.0 or float(popularity_99) < 0:
                raise exceptions.ValidationError({
                                '99popularity_errors':[
                                'This field value should be between 0 to 100.']
                                })

        director = data.get('director')
        # validation for director
        if not (director and isinstance(director,unicode)):
            raise exceptions.ValidationError({
                                'director_errors': ['This field is required and should be string.']
                                })

        genre = data.get('genre')

        imdb_score = data.get('imdb_score')
        # validation for imdb_score
        
        if not (imdb_score and isinstance(imdb_score,float)):
            raise exceptions.ValidationError({
                                'imdb_score_errors': ['This field is required and should be float.']
                                })
        else:
            if float(imdb_score) > 10.0 or float(imdb_score) < 0:
                raise exceptions.ValidationError({
                                'imdb_score_errors':
                                ['This field value should be between 0 to 10.']
                                })

        name = data.get('name')
        # validation for director
        if not (name and isinstance(name,unicode)):
            raise exceptions.ValidationError({
                                'name': ['This field is required and should be string.']
                                })

        return {
                'popularity_99': float(popularity_99),
                'director': director,
                'genre': genre,
                'imdb_score': float(imdb_score),
                'name': name
              }

    def create(self, validated_data):
        new_movie = Movie(name=validated_data['name'],
                               director=validated_data['director'],
                               popularity_99=validated_data['popularity_99'],
                               imdb_score=validated_data['imdb_score']
                               )
        new_movie.save()
        # add genre
        # print genre
        # print validated_data        
        # print isinstance(validated_data["genre"],list)
        if "genre" in validated_data and isinstance(validated_data["genre"],list): 
            for genre in validated_data['genre']:
                # print 'the genre is',genre
                exists, obj = Genre.name_exists(genre)
                # print obj
                # print exists
                if exists:
                    new_movie.genre.add(obj)
                # print '==================================== '
                serializer = GenreSerializer(data={"name":genre})
                if serializer.is_valid():
                    obj = serializer.save()
                    new_movie.genre.add(obj)
        return new_movie

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.popularity_99 = validated_data.get('popularity_99',
                                                    instance.popularity_99)
        instance.imdb_score = validated_data.get('imdb_score',
                                                 instance.imdb_score)
        instance.director = validated_data.get('director', instance.director)
        # update genre
        # print genre
        # print validated_data
        if "genre" in validated_data and isinstance(validated_data["genre"],list): 
            instance.genre = []
            for genre in validated_data['genre']:
                # print genre
                exists, obj = Genre.name_exists(genre)
                if exists:
                    instance.genre.add(obj)
                else:
                    serializer = GenreSerializer(data={"name":genre})
                    if serializer.is_valid():
                        obj = serializer.save()
                        instance.genre.add(obj)
                    else:
                        raise exceptions.ValidationError({
                            "slug_errors": ["There is a movie with same slug so choose  different name"
                                    ]})            
        return instance
    class Meta:
        model = Movie
        fields = ('name', 'director', 'popularity_99', 'genre', 'imdb_score', 'id')

class MovieRoleSerializer(serializers.ModelSerializer):
    # # role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    # role = RoleSerializer(read_only=False,required=False)

    class Meta:
        model = MovieRole
        fields = ('role_id', 'movie_id', 'id')
        