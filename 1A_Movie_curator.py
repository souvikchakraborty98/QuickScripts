import os
from random import seed
from random import randint
import msvcrt
from msvcrt import getch
import urllib.request, urllib.parse
from difflib import SequenceMatcher
import json
import pickle
from datetime import timedelta
from babelfish import Language
from subliminal import download_best_subtitles, region, save_subtitles
from subliminal.video import Video

store=["True","0000000"]
apikeyurl=""
flagIncorrectKey=False
path2 = os.path.dirname(os.path.abspath(__file__))+"\\configs\\"
apikey=""
dlSub=False
if not os.path.exists(path2):
    os.makedirs(path2)

def storeKey(db):
    fn= 'config'
    ops=os.path.join(path2, fn)
    outfile = open(ops,'wb')
    pickle.dump(store,outfile)
    outfile.close()
def loadKey():
    fn= 'config'
    ops=os.path.join(path2, fn)
    infile = open(ops,'rb')
    db=pickle.load(infile)
    infile.close()
    return db

def search_movie(search):
    
    if len(search) < 1: 
        return None

    try:
        url = serviceurl + urllib.parse.urlencode({'s': search})+apikeyurl
        print(f'Retrieving the data from IMDB now... \n')
        uh = urllib.request.urlopen(url)
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
            if str(json_data['Error'])=="Request limit reached!":
                  print("\n"+str(json_data['Error'])+"\n")
                  store[0]=True
            else:
                print("Could not get result from IMDB")
                return False 
            # if (nooftries<3):
            #   print(f"\nRefining Search....Trying Again.{nooftries+1}.....")
            # nnsearch=""
            # for i in search:
            #   if i.isspace()==False:
            #     nnsearch=nnsearch+i
            #   else:
            #       break
            # if nooftries<3:
            #   if search_movie(nnsearch,nooftries+1)!=True:
            #    return False 
            # else:
            #     print("\nBailing out..\n")      
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
            if str(e)=='HTTP Error 401: Unauthorized':
               print("\nIncorrect Key.\n")
               global flagIncorrectKey
               flagIncorrectKey=True
            else:
               print(f"ERROR: {e}")
            store[0]=True
            storeKey(store)


def findGenre(search):

#  store=["True","0000000"]
 nsearch=""
#  c=0
#  if search[0].isnumeric():
#     search=search[0:7]
#     for i in search:
#         if i=="." or i.isspace():
#             nsearch=nsearch+" "
#         else:
#             nsearch=nsearch+i
#  else:  
#   for i in search:
#      if i.isnumeric():
#          if c<1:
#              nsearch=nsearch+i
#          c+=1
#      elif i=="." or i.isspace():
#         nsearch=nsearch+" "
#      else:
#             nsearch=nsearch+i
    
#      if c>1:
#         break


 try:
    global store
    store=loadKey()
    global apikey
    if store[0]==False:
        apikey=store[1]
    elif store[0]==True:
        ak=input("Enter api key\n")    
        store[1]=ak
        store[0]=False
        apikey=store[1]
 except Exception as e:
      print("No key found\n")
      ak=input("Enter api key\n")   
      store[0]=False 
      store[1]=ak
      apikey=store[1]

 storeKey(store)
 global apikeyurl
 apikeyurl = '&apikey='+apikey

#  if nsearch[len(nsearch)-1].isnumeric():
#      nsearch=nsearch[0:len(nsearch)-1]
 videos = Video.fromname(stash[index])
 nsearch=str(videos.title)
#  print(nsearch)
 
 if nsearch==None:
     nsearch="qzx120254frerwfdcvs"

 if search_movie(nsearch.strip())!=False:
     try:
      url = serviceurl + urllib.parse.urlencode({'t': abv90[0]})+apikeyurl
      print(f'\nBest Match: "{abv90[0].upper()}"\n\nGetting genre now... \n')
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
         if flagIncorrectKey!=True:
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


serviceurl = 'http://www.omdbapi.com/?'
abv90=[]


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

print("Psst..Wanna download subtitles too? Y/N") 
consent=str(getch(),'utf-8')
if consent.lower()=='y':
    dlSub=True
    print("\nWill do sire!!\n")
else:
    print("\nNo subs..Got it.\n")

x='n'
while x!='y':
  index = randint(0, countGS-1)
  print("Launching "+str(stashnames[index]))
  findGenre(stashnames[index])
  print("\n\n......Good enough? Y/N\n")
  x=str(getch(),'utf-8')
  print("\n=================================================================================\n")
  if x.lower()=='y':
      if dlSub==True:
         print("\n\nGetting subtitles..Please Wait..\n\n")
         try:
            region.configure('dogpile.cache.dbm', arguments={'filename': 'cachefile.dbm'})
            videos = Video.fromname(stash[index])
            subtitles = download_best_subtitles([videos], {Language('eng')})
            best_subtitle = subtitles[videos][0]
            save_subtitles(videos, [best_subtitle])
            print("\nSubtitle downloaded.\n")
         except:
            print("\nCould not get subtitle :\\\n")
      os.startfile(stash[index])
  elif x.lower()=='n':
      print("Moving on...\n")
  else:
      print("\nWut? wut? i'll just assume it wasn't of your taste sire.\n")
