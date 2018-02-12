from movies.models import *
import json
data = json.load(open('imdb.json'))
genres = []
genre_set = set()
for i in data:
 genres.append(i['genre'])

for i in genres:
 for k in i:
  genre_set.add(str(k).strip())

for i  in genre_set:
 Genre(name = i, slug=i.lower().replace('-','_')).save()

from movies.models import *
import json
data = json.load(open('imdb.json'))
for i in data:
 popularity_99 = i['99popularity']
 name = i['name']
 imdb_score = i['imdb_score']
 director = i['director']
 genres = []
 print genres
 print popularity_99
 print name
 print imdb_score
 print director
 m = Movie(name = name, popularity_99 = popularity_99, imdb_score = imdb_score, director = director)
 m.save() 
 for ge in i['genre']:
  print ge
  gen = Genre.objects.filter(name = str(ge).strip())[0]
  m.genre.add(gen)

# purav1 = User(email_id = 'purav@hod.life',password = '123456')
# purav1.save()

#  from movies.models import *
#  from rbac.models import *
#  mapper1 = MovieAuth(movie = Movie.objects.get(id =2), role = Role.objects.get(slug = 'viewer'))
#  mapper1.save()
 
User(email_id = 'purav237@gmail.com', password = '123456').save()
User(email_id = 'sachin@gmail.com', password = '123456').save()
User(email_id = 'dhoni@gmail.com', password = '123456').save()
User(email_id = 'virat@gmail.com', password = '123456').save()
User(email_id = 'yuvraj@gmail.com', password = '123456').save()
	