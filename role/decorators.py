import logging
from functools import wraps
from django.db import IntegrityError
from django.conf import settings
from rest_framework import status
from rest_framework import exceptions
from django.core.cache import cache
from models import Permission, Role, User, RolePermission, UserRole

def iam(permission = None,*args, **kwargs):
    def deco(f):
        def abstract_session_token(request):
            session_token_header_key = 'HTTP_SESSION_TOKEN'
            user_id = cache.get(request.META.get(session_token_header_key))
            return user_id

        @wraps(f)
        def decorated_function(*args, **kwargs):
            is_admin = False
            # has_permission = False
            # user_name_auth = False
            # user_name = kwargs.get('user_name')
            user_id = abstract_session_token(args[1])
            if not user_id:
                raise exceptions.ValidationError({"success": False,
                    "error": {
                        "token_errors": [
                            "Token not found"
                            ]
                    }
                })

            user_role = UserRole.objects.filter(user_id = user_id, role_id__permission__slug = permission)
            # print user_role.query
            admin = User.objects.filter(id = user_id, role__slug = 'admin')
            if not  user_role.exists():
                raise exceptions.ValidationError({"success": False,
                    "error": {
                        "not_allowed": [
                            "User not allowed"
                            ]
                    }
                })

            # print 'the request is here',args[1]
            # print args

            return f(auth = {'is_admin':admin.exists(),'has_permission':True, 'user_id':user_id },*args, **kwargs)
        return decorated_function
    return deco
