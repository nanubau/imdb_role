Testing Flow:
1. Login using email_id and password with v1/login api and get the token (token stored in redis and hass ttl of 30 minutes)
2. Put the token as Session-Token in the header for accessing apis like 
		
		v1/movie,
		v1/movie-role - admin can update roles on movie
		v1/user-role - admin can update roles to as user



Implementation of role_checking as module
@iam is a decorator in role.decorators.py

Which is passed 'permission' as parameter and based on permission and Session-Token it decides whether user has permission or not

Implementation of user having mutiple role is done by
	Creating many to many 'role' field in User model through UserRole model 

Implementation of movie having mutiple role is done by
	Creating many to many 'role' field in User model through MovieRole model

ENDPOINT Without requirement of token

	v1/permission - list permission and CUD operation
	v1/role - list roles with permission and CUD operation
	v1/user - list all users will roles and permission, and and CUD operation
	v1/role-permission - list role id and permission and and CUD operation

Permission 

	CREATE MOVIE
	READ MOVIE
	UPDATE MOVIE
	DELETE MOVIE
	CREATE USER-ROLE
	READ USER-ROLE
	DELETE USER-ROLE
	CREATE MOVIE-ROLE
	READ MOVIE-ROLE
	DELETE MOVIE-ROLE

ROLE

	ADMIN
	MODERATOR
	VIEWER

ROLE-PERMISSION

	ADMIN       all permission for all movies and permission to change user role and movie role
	MODERATOR   [UPDATE MOVIE, READ MOVIE, DELETE MOVIE] permssion for movies where moderator is assigned
	VIEWER      READ MOVIE permisson for the movie where it is assigned



