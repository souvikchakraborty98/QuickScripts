import re
import requests
from bs4 import BeautifulSoup
from msvcrt import getch, kbhit
import os
import wget
aborted=False
link_reference_scihub = 'https://sci-hub.tw/10.1016/j.wocn.2018.07.001'
link_reference="https://doi.org/10.1016/j.lwt.2020.109217"

os.system('color')

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def clear(): 
    if os.name == 'nt': 
        _ = os.system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear') 

while aborted!=True:
    print(HEADER+"## SciHub Paper Downloader ## ver: 0.0.5a \n## Copyright,Souvik Chakraborty."+UNDERLINE+"The author in no way promotes \"SciHub\" or related parties.\nThis is just a scraping tool.##\n"+ENDC)
    print(HEADER+"Enter the DOI of the desired paper. Refer formats below:"+ENDC)
    link=input("Link Reference: "+link_reference+"\n"+"No. Reference: 10.3389/fimmu.2020.00693\n\n"+OKBLUE+"Enter DOI url [CASE SENSITIVE]  O|R  DOI no. [CASE SENSITIVE] \n\n"+ENDC)

    if link[0:4]=="http":
        link="https://sci-hub.tw/"+link
    else:
        link="https://sci-hub.tw/https://doi.org/"+link


    # link="https://sci-hub.tw/"+link

    print(link)
    try:
        r = requests.get(link)
    except Exception as e:
        print(f"Request Failed: {e}")
    soup = BeautifulSoup(r.text, "html.parser")
    pdflist=[]
    try:
     for i in soup.find_all('a'):
            urls=re.findall('//(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(i))
            # print(re.search('pdf',i.get('onclick')))
            print(urls)

            for url in urls:
             pdflist.append(url)
    except Exception as e:
        print(f"{FAIL}No links found: {e}{ENDC}")
        getch()
        exit()

    print("\nProbable Link[s]..\n")

    for url in pdflist:
            if (".pdf" or "download=true" or "sci-hub") in str(url):
                print(OKGREEN+"https:"+url[0:-1]+ENDC)

    pdfDown="https:"+pdflist[0][0:-1]

    # r1 = requests.get(pdfDown)
    print("\nDownloading...Please wait..\n")
    # fname = str(datetime.datetime.now().strftime("%f"))+".pdf"
    fname=wget.download(pdfDown)
    # print(fname)

    # with open(fname, "wb") as mypdf:
    #     mypdf.write(r1.content)
        # total_length = int(r1.headers.get('content-length'))
        # # print(total_length)
        # for ch in progress.bar(r1.iter_content(chunk_size = 10240), expected_size=(total_length/1024) + 1):
        #     if ch:
        #         Pypdf.write(ch)

    print(OKGREEN+"\n\nSaved to "+os.path.abspath(fname)+"\n"+ENDC)

    op=True
    while op!=False:
        print(BOLD+"\nPress 'Enter' to open. Press 'esc' to close.\n\nPress any other key to continue downloading...\n"+ENDC)
        keypress=getch()
        if keypress == chr(27).encode():
            aborted=True
            op=False
            exit()
        elif keypress == chr(13).encode():
            os.startfile(fname)
            print(OKBLUE+"Paused...Press any key to continue\n"+ENDC)
            getch()
            print(BOLD+"\n==================================================\n"+ENDC)
            op=True
        else:
            op=False
            clear()
         



