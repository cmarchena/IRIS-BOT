from storefront_downloader import decode_protobin, download_file
import os
import sys
import time
import re
import json
from filelocations import SCRIPTS as SCRIPTS

#open storefront-dd-mm-yyyy.proto and get all links inside it
def get_links(file_name):
    with open(file_name, "r") as file:
        links = []
        text = file.read()
        match = re.search(r"https:\/\/choices-live.pixelberrystudios.com\/.*\.protobin", text)
        #append match to links
        while match:
            links.append(match.group(0))
            text = text[match.end():]
            match = re.search(r"https:\/\/choices-live.pixelberrystudios.com\/.*\.protobin", text)
        print(len(links))
        return links

def download_new_chapters():
    download_file("https://choices-live.pixelberrystudios.com/storefront-2.4.protobin", "storefront-2.4.protobin")
    decode_protobin("storefront-2.4.protobin")
    links = get_links("storefront-2.4.proto.txt")
    downloaded = []
    #what is the current directory name?
    current_dir = os.getcwd().split("/")[-1]
    print("Current directory: ", current_dir)
    if os.path.exists("scripts"):
        os.chdir("scripts")
    for link in links:
        #create folders according to link
        folder_name = link.split("/")[-2]
        file_name = link.split("/")[-1].split(".")[0]
        if not os.path.exists(folder_name):
            os.system("mkdir " + folder_name)
        #download protobin file from link
        if os.path.exists(folder_name + "/" + file_name + ".proto.txt"):
            continue
        else:
            print("Downloading ", file_name, "...")
            downloaded.append(file_name)
            download_file(link, folder_name + "/" + file_name + ".protobin")
            if link[-8:] == "protobin":
                decode_protobin(folder_name + "/" + file_name + ".protobin")
    print("Done!")
    return downloaded

#function to list all files in a directory including subdirectories
def list_files(dir):
    files = []
    print("current directory: ", dir)
    #return all folders in dir
    folders = [f.path for f in os.scandir(dir) if f.is_dir()]
    for root, dirs, filenames in os.walk(dir):
        for f in filenames:
            file_path = os.path.join(root, f)
            #append the last part of the path to the list
            file_name = file_path.split("/")[-1]
            files.append(file_name[:-10])
    return sorted(folders), sorted(files)

if __name__ == "__main__":
    print(download_new_chapters())
    if os.path.exists("scripts"):
        os.chdir("scripts")
        print(list_files("scripts"))
    else:
        print(list_files(os.getcwd()))