# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from role.models import Role
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank = False)
    slug = models.CharField(max_length=100, unique=True, null=False, blank = False, editable = False)
    create_dttm = models.DateTimeField(auto_now_add=True)
    update_dttm = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % self.slug

    @staticmethod
    def name_exists(name):
        exists = False
        genre = Genre.objects.filter(name=name)
        if genre.exists():
            exists = True
            genre = genre[0]
        return exists,genre

    @staticmethod
    def slug_exists(slug):
        exists = False
        genre = Genre.objects.filter(slug=slug)
        if genre.exists():
            exists = True
            genre = genre[0]
        return exists,genre

    class Meta(object):
        db_table = "genre"
        # name & slug combination should be unqiue always
        unique_together = ('name', 'slug',)


class Movie(models.Model):
    name = models.CharField(max_length=100, null=False, blank = False)
    director = models.CharField(max_length=100,null=False, blank = False)
    popularity_99 = models.DecimalField(max_digits=4, decimal_places=1)
    imdb_score = models.DecimalField(max_digits=4, decimal_places=1)
    genre = models.ManyToManyField(Genre)
    role = models.ManyToManyField(Role, through='MovieRole', related_name='re_role')
    create_dttm = models.DateTimeField(auto_now_add=True)
    update_dttm = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta(object):
        db_table = "movie"
        
        # Not putting unique constraint on director and movie name as same director can direct a movie with same name  
        # unique_together = ('name', 'director',)
    
    def __unicode__(self):
        return "%s" % self.name


class MovieRole(models.Model):
    movie_id = models.ForeignKey(Movie, db_column='movie_id', on_delete=models.CASCADE, null=False, blank = False)
    role_id = models.ForeignKey(Role, db_column='role_id', on_delete=models.CASCADE, null=False, blank = False)
    create_dttm = models.DateTimeField(auto_now_add=True)
    update_dttm = models.DateTimeField(auto_now=True)
    
    class Meta(object):
        db_table = "movie_role"
        unique_together = ('movie_id','role_id')