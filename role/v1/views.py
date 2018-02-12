from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import Http404
from rest_framework import status
from rest_framework import exceptions
from role.serializers import PermissionSerializer, RoleSerializer, UserSerializer, RolePermissionSerializer, UserRoleSerializer
from role.models import Permission, Role, User, RolePermission, UserRole
import logging
from role.decorators import iam

LOGGER = logging.getLogger(__name__)

class BaseAPIView(APIView):
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

class PermissionAPIView(BaseAPIView):
    """
        APIView for Permission CRUD
    """
    def get_object(self, id):
        try:
            return Permission.objects.get(id=id)
        except Permission.DoesNotExist:
            raise exceptions.ValidationError({"success": False,
                "error": {
                    "permission_errors": [
                        "Permission Details not found"
                        ]
                }
            })

    def get(self, request):
        id = request.query_params.get('permission_id',None)
        if id:
            permission = self.get_object(id)
            serializer = PermissionSerializer(permission)
        else:
            permission = Permission.objects.all()
            serializer = PermissionSerializer(permission, many=True)
        
        return Response({'data':serializer.data,'success':True}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'success':True}, status=status.HTTP_201_CREATED)
        return Response({'error':serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,format=None):
        id = request.data.get('permission_id',None)
        permission = self.get_object(id)
        if permission:
            serializer = PermissionSerializer(permission, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'success':True}, status=status.HTTP_200_OK)
        return Response({'error':serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        id = request.data.get('permission_id',None)
        permission = self.get_object(id)
        if permission:
            permission.delete()
            return Response({'success':True})
        return Response({'error':{"permission":["NOT PRESENT"]}, 'success':False}, status=status.HTTP_400_BAD_REQUEST)

class RolePermissionAPIView(BaseAPIView):
    """
        APIView for RolePermission CRUD
    """
    def get_object(self, role_id, permission_id):
        try:
            return RolePermission.objects.get(role_id = role_id, permission_id = permission_id)
        except RolePermission.DoesNotExist:
            raise exceptions.ValidationError({"success": False,
                "error": {
                    "role_permission_errors": [
                        "Role-Permission Details not found"
                        ]
                }
            })
    
    def get(self, request):
        role_id = request.query_params.get('role_id',None)
        permission_id = request.query_params.get('permission_id',None)
        if role_id and permission_id:
            role_permission = self.get_object(role_id, permission_id)
            serializer = RolePermissionSerializer(role_permission)
        else:
            role_permission = RolePermission.objects.all()
            serializer = RolePermissionSerializer(role_permission, many=True)
        
        return Response({'data':serializer.data,'success':True}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = RolePermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'success':True}, status=status.HTTP_201_CREATED)
        return Response({'error':serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        role_id = request.data.get('role_id',None)
        permission_id = request.data.get('permission_id',None)
        role_permission = self.get_object(role_id,permission_id)
        if role_permission:
            role_permission.delete()
            return Response({'success':True})
        return Response({'error':{"role-permission":["NOT PRESENT"]}, 'success':False}, status=status.HTTP_400_BAD_REQUEST)


class RoleAPIView(BaseAPIView):
    """
        APIView for RolePermission CRUD
    """
    def get_object(self, id):
        try:
            return Role.objects.get(id = id)
        except Role.DoesNotExist:
            raise exceptions.ValidationError({"success": False,
                "error": {
                    "role_errors": [
                        "role details not found"
                        ]
                }
            })
    
    def get(self, request):
        id = request.query_params.get('role_id',None)
        if id:
            role = self.get_object(id)
            serializer = RoleSerializer(role)
        else:
            role = Role.objects.all()
            serializer = RoleSerializer(role, many=True)
        
        return Response({'data':serializer.data,'success':True}, status=status.HTTP_200_OK)

    def put(self, request,format=None):
        id = request.data.get('role_id',None)
        role = self.get_object(id)
        if role:
            serializer = RoleSerializer(role, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'success':True}, status=status.HTTP_200_OK)
        return Response({'error':serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'success':True}, status=status.HTTP_201_CREATED)
        return Response({'error':serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        id = request.data.get('role_id',None)
        role = self.get_object(id)
        if role:
            role.delete()
            return Response({'success':True})
        return Response({'error':{"role":["NOT PRESENT"]}, 'success':False}, status=status.HTTP_400_BAD_REQUEST)

class UserRoleAPIView(BaseAPIView):
    """
        APIView for UserRole CRUD
    """
    def get_object(self, role_id, user_id):
        try:
            return UserRole.objects.get(role_id = role_id, user_id = user_id)
        except UserRole.DoesNotExist:
            raise exceptions.ValidationError({"success": False,
                "error": {
                    "user_role_errors": [
                        "user-role details not found"
                        ]
                }
            })

    @iam(permission = 'read_user_role')
    def get(self, request, auth, format=None, *args, **kwargs):
        role_id = request.query_params.get('role_id',None)
        user_id = request.query_params.get('user_id',None)
        if role_id and user_id:
            user_role = self.get_object(role_id,user_id)
            serializer = UserRoleSerializer(user_role)
        else:
            user_role = UserRole.objects.all()
            serializer = UserRoleSerializer(user_role, many=True)
        
        return Response({'data':serializer.data,'success':True}, status=status.HTTP_200_OK)

    @iam(permission = 'create_user_role')
    def post(self, request, auth, format=None, *args, **kwargs):
        serializer = UserRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'success':True}, status=status.HTTP_201_CREATED)
        return Response({'error':serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)

    @iam(permission = 'delete_user_role')
    def delete(self, request, auth, format=None, *args, **kwargs):
        role_id = request.data.get('role_id',None)
        user_id = request.data.get('user_id',None)
        user_role = self.get_object(role_id,user_id)
        if user_role:
            user_role.delete()
            return Response({'success':True})
        return Response({'error':{"user-role":["NOT PRESENT"]}, 'success':False}, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(BaseAPIView):
    """
        APIView for User CRUD
    """
    def get_object(self, user_id):
        try:
            return User.objects.get(id = user_id)
        except User.DoesNotExist:
            raise exceptions.ValidationError({"success": False,
                "error": {
                    "user_errors": [
                        "user details not found"
                        ]
                }
            })

    def get(self, request):
        user_id = request.query_params.get('user_id',None)
        if user_id:
            user = self.get_object(user_id)
            serializer = UserSerializer(user)
        else:
            user = User.objects.all()
            serializer = UserSerializer(user, many=True)
        
        return Response({'data':serializer.data,'success':True}, status=status.HTTP_200_OK)

class LoginAPIView(BaseAPIView):   

    def post(self, request):
        # calling serializer function to store the session
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            token,ttl =  serializer.user_login(request)
            if token:
                return Response({'data':{'token':token, 'ttl':ttl},'success':True}, status=status.HTTP_200_OK)
            else:
                return Response({'error':{"invalid":['Invalid password and email_id']}, 'success':False}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error':serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)
