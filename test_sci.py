import re
import requests
from bs4 import BeautifulSoup
from msvcrt import getch, kbhit
from colorama import init,Fore, Back, Style
init(autoreset=True)
import os
import wget
aborted=False
link_reference_scihub = 'https://sci-hub.tw/10.1016/j.wocn.2018.07.001'
link_reference="https://doi.org/10.1016/j.lwt.2020.109217"

notFound=False

# HEADER = '\033[95m'
# OKBLUE = '\033[94m'
# OKGREEN = '\033[92m'
# WARNING = '\033[93m'
# FAIL = '\033[91m'
# ENDC = '\033[0m'
# BOLD = '\033[1m'
# UNDERLINE = '\033[4m'

def clear(): 
    if os.name == 'nt': 
        _ = os.system('cls') 
    else: 
        _ = os.system('clear') 

while aborted!=True:
    print(Fore.MAGENTA+"## SciHub Paper Downloader ## ver: 0.0.5a \n## Copyright,Souvik Chakraborty.The author in no way promotes \"SciHub\" or related parties.\nThis is just a scraping tool.##\n")
    print(Fore.MAGENTA+"Enter the DOI of the desired paper. Refer formats below:")
    print("Link Reference: "+link_reference+"\n"+"No. Reference: 10.3389/fimmu.2020.00693\n")
    print(Fore.YELLOW+"Enter DOI url [CASE SENSITIVE]  O|R  DOI no. [CASE SENSITIVE]. You could paste it here. \n(For Windows platform, pre-Windows 10, refer \"Enabling copy paste in cmd\") \n\n")
    link=input()

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
        print(f"{Fore.RED}No links found: {e}")
        notFound=True
        getch()
        exit()

    print("\nProbable Link[s]..\n")
    newPdflist=[]
    for url in pdflist:
            if (".pdf" or "download=true" or "sci-hub") in str(url):
                print(Fore.GREEN+"https:"+url[0:-1])
                newPdflist.append(str("https:"+url[0:-1]))
    if len(newPdflist)<1:
        print(f"{Fore.RED}No links found. Make sure you are entering DOI correctly / Requested file might not be present on SciHub.")
        print(f"{Fore.BLUE}Press any key to continue..\n")
        notFound=True
        getch()
    else:
         pdfDown="https:"+pdflist[0][0:-1]
         # r1 = requests.get(pdfDown)
         print("\nDownloading...Please wait..\n")
         # fname = str(datetime.datetime.now().strftime("%f"))+".pdf"
         fname=wget.download(pdfDown)
         # print(fname)
         notFound=False
         print(Fore.GREEN+"\n\nSaved to "+os.path.abspath(fname)+"\n")
   

    op=True
    while op!=False:
        if notFound==False:
            print(Fore.GREEN+"\nPress 'Enter' to open. Press 'esc' to close.\n\nPress any other key to continue downloading...\n")
            keypress=getch()
            if keypress == chr(27).encode():
                aborted=True
                op=False
                exit()
            elif keypress == chr(13).encode():
                os.startfile(fname)
                print(Fore.BLUE+"Paused...Press any key to continue\n")
                getch()
                print(Style.BRIGHT+"\n==================================================\n")
                op=True
            else:
                op=False
                clear()
        elif notFound==True:
            print(Fore.GREEN+"\nPress 'esc' to close.\n\nPress any other key to continue downloading...\n")
            keypress=getch()
            if keypress == chr(27).encode():
                aborted=True
                op=False
                exit()
            else:
                op=False
                clear()

         



