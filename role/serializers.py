from rest_framework import serializers
from models import Permission, Role, User, RolePermission, UserRole, UNIQUE
from rest_framework import exceptions
from django.core.cache import cache
from rest_framework import status
import hashlib
import uuid
from common.redis_constants import TTL

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('name','id')

    def to_internal_value(self, data):
        name = data.get('name')
        if not name or '':
            raise exceptions.ValidationError({"success": False,"error": {"name_errors": [
                "name is a required field and cannot be empty"]}})            

        # validation for slug
        slug = name.lower().replace('-','_')
        slug = slug.replace(' ','_')
        exists, obj = Permission.slug_exists(slug)
        if exists:
            raise exceptions.ValidationError({"success": False,"error": {"slug_errors": [
                ' %s Already exists'%slug]}})            
        return {
                'name': data['name']
              }
    
    def create(self, validated_data):
        slug = validated_data['name'].lower().replace('-','_').strip()
        slug = slug.replace(' ','_')
        new_permission = Permission(name=validated_data['name'],slug = slug)
        new_permission.save()
        # add permission
        return new_permission


class RoleSerializer(serializers.ModelSerializer):
    permission = PermissionSerializer(many=True)
    class Meta:
        model = Role
        fields = ('name','id', 'permission')

    def to_internal_value(self, data):
        name = data.get('name')
        if not name or '':
            raise exceptions.ValidationError({
                                'name': 'name is a required field and cannot be empty'
                                })
        # validation for slug
        slug = name.lower().replace('-','_')
        slug = slug.replace(' ','_')
        exists, obj = Role.slug_exists(slug)
        if exists:
            raise exceptions.ValidationError({
                                'slug': ' %s Already exists'%slug
                                })
        return {
                'name': data['name']
              }
    
    def create(self, validated_data):
        slug = validated_data['name'].lower().replace('-','_').strip()
        slug = slug.replace(' ','_')
        new_permission = Role(name=validated_data['name'],slug = slug)
        new_permission.save()
        # add permission
        return new_permission


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=True)
    def to_internal_value(self, data):
        email_id = data.get('email_id')
        password = data.get('password')
        if not email_id or '':
            raise exceptions.ValidationError({
                                'email_id': 'email_id is a required field and cannot be empty'
                                })
        if not password or '':
            raise exceptions.ValidationError({
                                'password': 'password is a required field and cannot be empty'
                                })
        return {
                'email_id': data['email_id'],
                'password':data['password']
              }


    # login function
    def user_login(self,request):
        # if isinstance(request.data.get('email_id'),str) and isinstance(request.data.get('password'),str):
        email_id = request.data.get('email_id',None)
        password = request.data.get('password',None)
        password = hashlib.sha256(password + UNIQUE).hexdigest()
        session_token = None
        ttl = 0
        try :
            user_obj = User.objects.get(email_id = email_id, password = password )
            print user_obj
            session_token = uuid.uuid4()
            cache.set(session_token, user_obj.id, TTL)
            return session_token, cache.ttl(session_token)
        except :
            return session_token,ttl

    class Meta:
        model = User
        fields = ('email_id', 'role', 'id')

class RolePermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RolePermission
        fields = ('role_id', 'permission_id', 'id')
        

class UserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRole
        fields = ('user_id', 'role_id', 'id')
        

