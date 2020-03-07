import urllib.request, urllib.parse
from difflib import SequenceMatcher
import json
from msvcrt import getch
import pickle
import os

serviceurl = 'http://www.omdbapi.com/?'
apikeyurl=""
l=["True","0000000"]
abv90=[]
apikey=""

def storeKey(db):
    fn= 'testconfig'
    ops=os.path.join(path, fn)
    outfile = open(ops,'wb')
    pickle.dump(l,outfile)
    outfile.close()
def loadKey():
    fn= 'testconfig'
    ops=os.path.join(path, fn)
    infile = open(ops,'rb')
    db=pickle.load(infile)
    infile.close()
    return db
    

def search_movie(search,nooftries):
    if len(search) < 1: 
        return None

    try:
        url = serviceurl + urllib.parse.urlencode({'s': search})+apikeyurl
        print(f'Retrieving the data of "{search}" now... \n')
        uh = urllib.request.urlopen(url)
        print(url+"\n")
        data = uh.read()
        json_data=json.loads(data)
        #for reference	
        # list_keys=['Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre', 'Director', 'Writer', 
        #        'Actors', 'Plot', 'Language', 'Country', 'Awards', 'Ratings', 
        #        'Metascore', 'imdbRating', 'imdbVotes', 'imdbID']
        if json_data['Response']=='True':
            for k in json_data["Search"]:
                print(k['Title'])
                abv90.append(str(k['Title']))
                return True
        else:
            if str(json_data['Error'])=="Request limit reached!":
                print("\n"+str(json_data['Error'])+"\n")
                l[1]=True
            else:
                print("No results found")

            if nooftries<3:
              print(f"\nRefining Search....Trying Again.{nooftries+1}......")
            nnsearch=""
            for i in search:
              if i.isspace()==False:
                nnsearch=nnsearch+i
              else:
                  break
            if nooftries<3:
              if search_movie(nnsearch,nooftries+1)!=True:
                 getch()
                 exit()     
            else:
                print("\nBailing out..\n")

        # for k in json_data["Search"]:
        #        print("Similarity "+str(match(str(k['Title']),fn)))
        #        if match(str(k['Title']),fn)>=90.0:
        #             abv90.append(str(k['Title']))

    except Exception as e:
        print(f"ERROR: {e}")
        l[0]=True
        storeKey(l)

path = os.path.dirname(os.path.abspath(__file__))+"\\configs\\"

if not os.path.exists(path):
    os.makedirs(path)
try:
    l=loadKey()
    if l[0]==False:
        apikey=l[1]
    elif l[0]==True:
        ak=input("Enter api key\n")    
        l[1]=ak
        l[0]=False
        apikey=l[1]
except Exception as e:
    print("No key found\n")
    ak=input("Enter api key\n")   
    l[0]=False 
    l[1]=ak
    apikey=l[1]

storeKey(l)
apikeyurl = '&apikey='+apikey
search = input('\nEnter: ')
nsearch=""
c=0
if search[0].isnumeric():
    search=search[0:7]
    for i in search:
        if i=="." or i.isspace():
            nsearch=nsearch+" "
        else:
            nsearch=nsearch+i
else:  
  for i in search:
     if i.isnumeric():
         if c<1:
             nsearch=nsearch+i
             print(nsearch)
         c+=1
     elif i=="." or i.isspace():
        nsearch=nsearch+" "
        print(nsearch)
     else:
            nsearch=nsearch+i
            print(nsearch)
    
     if c>1:
        break

if nsearch[len(nsearch)-1].isnumeric():
     nsearch=nsearch[0:len(nsearch)-1]
     print(nsearch)

print(f"Processed: {nsearch.strip()}\n")

search_movie(nsearch.strip(),0)

try:
    url = serviceurl + urllib.parse.urlencode({'t': abv90[0]})+apikeyurl
    print(f'\nBest Match: "{abv90[0]}" Getting genre now... \n')
    uh = urllib.request.urlopen(url)
    print(url+"\n")
    data = uh.read()
    json_data=json.loads(data)
    list_keys=['Genre']
    if json_data['Response']=='True':
      for k in list_keys:
        if k in list(json_data.keys()):
            print(f"{k}: {json_data[k]}") 

except Exception as e:
     print(f"Error: {e}")

            
getch()