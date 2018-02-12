Testing Flow:
1. Login using email_id and password with v1/login api and get the token
2. Put the token as Session-Token in the header for accessing apis like v1/movie, v1/movie-role, v1/user-role

Implementation of role_checking as module
@iam is a decorato in role.decorators.py which is passed 'permission' as parameter and based on permission and Session-Token it decides whether user has permission or not

ENDPOINT Without requirement of token
v1/genre 
v1/permission
v1/role
v1/user
v1/role-permission 

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
	ADMIN - all permission for all movies and permission to change user role and movie role
	MODERATOR - [UPDATE MOVIE, READ MOVIE, DELETE MOVIE] permssion for movies where moderator is assigned
	VIEWER - READ MOVIE permisson for the movie where it is assigned



