# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import hashlib
# Create your models here.

UNIQUE = 'UserROLE123_@'

class Permission(models.Model):
    name = models.CharField(max_length=30, unique = True, null=False, blank = False)
    slug = models.CharField(max_length=30, unique = True, null=False, blank = False)
    create_dttm = models.DateTimeField(auto_now_add=True)
    update_dttm = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s" % self.slug

    @staticmethod
    def name_exists(name):
        exists = False
        permission = Permission.objects.filter(name=name)
        if permission:
            exists = True
        return exists,permission

    @staticmethod
    def slug_exists(slug):
        exists = False
        permission = Permission.objects.filter(slug=slug)
        if permission:
            exists = True
        return exists,permission

    class Meta(object):
        db_table = "permission"


class Role(models.Model):
    name = models.CharField(max_length=30, unique = True, null=False, blank = False)
    slug = models.CharField(max_length=30, unique = True, null=False, blank = False)
    permission = models.ManyToManyField(Permission, through='RolePermission', related_name='role_permission')
    create_dttm = models.DateTimeField(auto_now_add=True)
    update_dttm = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % self.slug

    @staticmethod
    def name_exists(name):
        exists = False
        role = Role.objects.filter(name=name)
        if role:
            exists = True
        return exists,role

    @staticmethod
    def slug_exists(slug):
        exists = False
        role = Role.objects.filter(slug=slug)
        if role:
            exists = True
        return exists,role
        
    class Meta(object):
        db_table = "roles"


class User(models.Model):
    email_id = models.EmailField(unique = True, null=False, blank = False)
    password = models.CharField(max_length=64, null=False, blank = False)
    role = models.ManyToManyField(Role, through='UserRole', related_name='user_role')
    create_dttm = models.DateTimeField(auto_now_add=True)
    update_dttm = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.password = hashlib.sha256(self.password + UNIQUE).hexdigest()
        super(User, self).save(*args, **kwargs)
    
    @staticmethod
    def exists(email_id):
        exists = False
        users = User.objects.filter(email_id=email_id)
        if users:
            exists = True
        return exists

    def __unicode__(self):
        return "%s__%s" % (str(self.id), str(self.email_id))
   
    class Meta(object):
        db_table = "users"

class RolePermission(models.Model):
    permission_id = models.ForeignKey(Permission, db_column='permission_id', on_delete=models.CASCADE, null=False, blank = False)
    role_id = models.ForeignKey(Role, db_column='role_id', on_delete=models.CASCADE, null=False, blank = False)
    create_dttm = models.DateTimeField(auto_now_add=True)
    update_dttm = models.DateTimeField(auto_now=True)
    # is_active = models.BooleanField(default=True)
    class Meta(object):
        db_table = "roles_permission"
        unique_together = ('permission_id','role_id')

class UserRole(models.Model):
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE, null=False, blank = False)
    role_id = models.ForeignKey(Role, db_column='role_id', on_delete=models.CASCADE, null=False, blank = False)
    create_dttm = models.DateTimeField(auto_now_add=True)
    update_dttm = models.DateTimeField(auto_now=True)
    class Meta(object):
        db_table = "user_role"
        unique_together = ('user_id','role_id')