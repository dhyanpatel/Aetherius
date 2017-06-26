import json, requests
import getlyrics

print(dir(getlyrics))
request = requests.get('http://lyric-api.herokuapp.com/api/find/John%20Lennon/Imagine')
print(request.content)
data = request.json()

print(data['lyric'])
print(str(data['lyric']).split())