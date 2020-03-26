import re
import requests
from bs4 import BeautifulSoup
from msvcrt import getch
import datetime
import os

link_reference_scihub = 'https://sci-hub.tw/10.1016/j.wocn.2018.07.001'
link_reference="https://doi.org/10.1016/j.lwt.2020.109217"

print("## SciHub Paper Downloader ## ver: 0.0.5a \n## Copyright, Souvik Chakraborty. The author in no way promotes \"SciHub\" or related parties.\nThis is just a scraping tool.##\n")
print("Enter the DOI of the desired paper. Refer formats below:")
link=input("Link Reference: "+link_reference+"\n"+"No. Reference: 10.3389/fimmu.2020.00693\n\nEnter DOI url [CASE SENSITIVE]  O|R  DOI no. [CASE SENSITIVE] \n\n")

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
    print(f"No links found: {e}")
    getch()
    exit()

print("\nProbable Link[s]..\n")

for url in pdflist:
        if (".pdf" or "download=true" or "sci-hub") in str(url):
            print("https:"+url[0:-1])

pdfDown="https:"+pdflist[0][0:-1]

r1 = requests.get(pdfDown)

fname = str(datetime.datetime.now().strftime("%f"))+".pdf"

print("Downloading...Please wait..\n")
with open(fname, "wb") as mypdf:
    mypdf.write(r1.content)
    # total_length = int(r1.headers.get('content-length'))
    # # print(total_length)
    # for ch in progress.bar(r1.iter_content(chunk_size = 10240), expected_size=(total_length/1024) + 1):
    #     if ch:
    #         Pypdf.write(ch)


print("\n..Done.\nSaved to "+os.path.abspath(fname)+"\n\nPress any key to exit...")
getch()


