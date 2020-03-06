import urllib.request, urllib.parse
from difflib import SequenceMatcher
import json
from msvcrt import getch
serviceurl = 'http://www.omdbapi.com/?'
apikey = '&apikey='+'da05069b'

abv90=[]

def match(s1, s2):
     s2p=s2[0:len(s1)]
     s1p=''.join(d for d in s1 if d.isalnum())
     s2p=''.join(d for d in s2p if d.isalnum())
     print("\n"+s1p+"--->"+s2p+"\n")
     return SequenceMatcher(None, s1p, s2p ).ratio()*100

def search_movie(search):
    if len(search) < 1: 
        return None

    try:
        url = serviceurl + urllib.parse.urlencode({'s': search})+apikey
        print(f'Retrieving the data of "{search}" now... \n')
        uh = urllib.request.urlopen(url)
        print(url+"\n")
        data = uh.read()
        json_data=json.loads(data)
        # list_keys=['Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre', 'Director', 'Writer', 
        #        'Actors', 'Plot', 'Language', 'Country', 'Awards', 'Ratings', 
        #        'Metascore', 'imdbRating', 'imdbVotes', 'imdbID']
        if json_data['Response']=='True':
            for k in json_data["Search"]:
                print(k['Title'])
            
        for k in json_data["Search"]:
               print("Similarity "+str(match(str(k['Title']),fn)))
               if match(str(k['Title']),fn)>=90.0:
                    abv90.append(str(k['Title']))

    except Exception as e:
        print(f"ERROR: {e}")


search = input('\nEnter: ')
fn=input("\nEnter filename\n")

search_movie(search)

print("Most similar..\n")
for i in abv90:
    print(i)
getch()

