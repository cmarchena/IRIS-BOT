import requests
import blackboxprotobuf
import os
import sys
import time
from filelocations import SCRIPTS, ASSETS

globalpath = ASSETS

def sendRequest(url):
    try:
        page = requests.get(url)

    except Exception as e:
        print("error:", e)
        return False

    if (page.status_code != 200):
        return False

    return page

def download_asset(url, file_name):
    pathname = globalpath
    for i in range(4,len(url.split("/"))-1):
        fpath = url.split("/")[i]
        pathname = os.path.join(pathname, fpath)

    if not os.path.isdir(pathname):
        os.makedirs(pathname)

    response = sendRequest(url)
    if response == False:
        return "Error: Could not download asset"
    
    with open(pathname+"/"+file_name, "wb") as f:
        f.write(response.content)
        print("Download complete!")
        
    #return file downloaded
    return pathname + "/" + file_name

if __name__ == "__main__":
    print(download_asset("https://choices-live.pixelberrystudios.com/assets/portraits_large/custom/3x/item_fem_professional_clothing_uniform_janitor_gray-v01.png", "test.png"))