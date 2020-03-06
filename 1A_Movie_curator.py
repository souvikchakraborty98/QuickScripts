import os
from random import seed
from random import randint
import msvcrt
from msvcrt import getch
import urllib.request, urllib.parse
from difflib import SequenceMatcher
import json

serviceurl = 'http://www.omdbapi.com/?'
apikey = '&apikey='+'da05069b'


abv90=[]

def search_movie(search,nooftries):
    
    if len(search) < 1: 
        return None

    try:
        url = serviceurl + urllib.parse.urlencode({'s': search})+apikey
        print(f'Retrieving the data from IMDB now... \n')
        uh = urllib.request.urlopen(url)
        # print(url+"\n")
        data = uh.read()
        json_data=json.loads(data)
        # list_keys=['Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre', 'Director', 'Writer', 
        #        'Actors', 'Plot', 'Language', 'Country', 'Awards', 'Ratings', 
        #        'Metascore', 'imdbRating', 'imdbVotes', 'imdbID']
        if json_data['Response']=='True':
            for k in json_data["Search"]:
                # print(k['Title'])
                abv90.append(str(k['Title']))
                return True
        else:
            print("Could not get title on IMDB")
            if (nooftries<3):
              print(f"\nRefining Search....Trying Again.{nooftries+1}.....")
            nnsearch=""
            for i in search:
              if i.isspace()==False:
                nnsearch=nnsearch+i
              else:
                  break
            if nooftries<3:
              if search_movie(nnsearch,nooftries+1)!=True:
               return False 
            else:
                print("\nBailing out..\n")      
            # getch()
            # exit()            
        # for k in json_data["Search"]:
        #        print("Similarity "+str(match(str(k['Title']),fn)))
        #        if match(str(k['Title']),fn)>=90.0:
        #             abv90.append(str(k['Title']))

    except Exception as e:
        if str(e)=="<urlopen error [Errno 11001] getaddrinfo failed>":
            print("Could not establish connection..")
            return False
        else:
            print(f"ERROR: {e}")


def findGenre(search):

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
         c+=1
     elif i=="." or i.isspace():
        nsearch=nsearch+" "
     else:
            nsearch=nsearch+i
    
     if c>1:
        break

 if nsearch[len(nsearch)-1].isnumeric():
     nsearch=nsearch[0:len(nsearch)-1]

 if search_movie(nsearch.strip(),0)!=False:
     try:
      url = serviceurl + urllib.parse.urlencode({'t': abv90[0]})+apikey
      print(f'\nBest Match: "{abv90[0]}"\nGetting genre now... \n')
      uh = urllib.request.urlopen(url)
     #   print(url+"\n")
      data = uh.read()
      json_data=json.loads(data)
      list_keys=['Genre']
      if json_data['Response']=='True':
        for k in list_keys:
          if k in list(json_data.keys()):
              print(f"{k}: {json_data[k]}")
  
      abv90.clear()
     except Exception as e:
          print(f"Error: {e}")
    


def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        try:
           fullPath = os.path.join(dirName, entry)
           if os.path.isdir(fullPath):
              allFiles = allFiles + getListOfFiles(fullPath)
           else:
              allFiles.append(fullPath)
        except:
            pass
                
    return allFiles 

path = os.path.dirname(os.path.abspath(__file__))+"\\"
if not os.path.exists(path):
    os.makedirs(path)

basepath = path
listOfFiles = getListOfFiles(basepath)
countGS=0
stashnames=[]
stash=[]
for i in listOfFiles:
    temp=i.split('\\')
    tempFn=str(temp[len(temp)-1])
    if tempFn[len(tempFn)-3:len(tempFn)] == "mp4" or tempFn[len(tempFn)-3:len(tempFn)] == "avi" :
        stash.append(i)
        stashnames.append(tempFn)
        countGS+=1
    

x='n'
while x!='y':
  index = randint(0, countGS-1)
  print("Launching "+str(stashnames[index]))
  findGenre(stashnames[index])
  print("......Good enough? Y/N\n")
  x=str(getch(),'utf-8')
  if x.lower()=='y':
     os.startfile(stash[index])
  elif x.lower()=='n':
      print("moving on...")
  else:
      print("\nwut? wut? i'll just assume it wasn't of your taste sire.\n")

