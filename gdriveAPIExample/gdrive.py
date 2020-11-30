from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    
    creds = None
    fileList=[]

    if os.path.exists('token'):
        with open('token', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("\n")

        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            print("\n")

        with open('token', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)
    while True:
        notFound=True
        while True:
            try:
                pgSize=int(input("Enter pagesize:\n"))
                if pgSize<1 or pgSize>1000:
                    print("\nValues must be within the range: [1, 1000]\n")
                else:
                    break
            except Exception as e:
                print(f"{e} Not a number.\n\n")
            

        results = drive_service.files().list(pageSize=pgSize, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
                filedict = {
                "name": item['name'],
                "id": item['id'],
                }
                fileList.append(filedict)


        file_id=input("\nEnter file id:\n")
        for item in fileList:
            try:
                if item['id']==file_id:
                        fileName=item["name"]
                        request = drive_service.files().get_media(fileId=file_id)
                        fh = open(fileName,'wb')
                        downloader = MediaIoBaseDownload(fh, request)
                        done = False
                        while done is False:
                            status, done = downloader.next_chunk()
                            print(f"Downloaded {int(status.progress() * 100)}%",end='\r')
                        fh.close()
                        notFound=False
                        break
            except:
                pass
        if notFound==True:
            print("\nRequested File not found.")
        print("\n")

    
if __name__ == '__main__':
    main()