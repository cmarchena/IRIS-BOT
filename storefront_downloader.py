#download protobin file from link
import requests
import os
import sys
import time
import re
import json
import urllib.request
import urllib.parse
import urllib.error

link = "https://choices-live.pixelberrystudios.com/storefront-2.4.protobin"
#save file as storefront-dd-mm-yyyy.protobin
file_name = "storefront-" + time.strftime("%d-%m-%Y") + ".protobin"

def download_file(url, file_name):
    #if file exists, ignore
    if os.path.exists(file_name):
        print("File already exists!")
        return
    #download file
    else:
        with open(file_name, "wb") as file:
            response = requests.get(url, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None: # no content length header
                file.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    file.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
                    sys.stdout.flush()

    print("\nDownload complete!")

#decode protobin to proto
def decode_protobin(file_name):
    print("Decoding ", file_name, "...")
    os.system("protoc --decode_raw < " + file_name + "> "+file_name[:-9]+".proto.txt")
    print("Protobin decoded!")
    #replace {base_url} with https://choices-live.pixelberrystudios.com
    with open(file_name[:-9]+".proto.txt", "r") as file:
        lines = file.readlines()
        for i in range(len(lines)):
            if "base_url" in lines[i]:
                lines[i] = lines[i].replace(r"{base_url}", "https://choices-live.pixelberrystudios.com")
            if "res" in lines[i]:
                lines[i] = lines[i].replace(r"{res}", "3x")
            if "size" in lines[i]:
                lines[i] = lines[i].replace(r"{size}", "large")
        with open(file_name[:-9]+".proto.txt", "w") as file:
            file.writelines(lines)
    print("Placeholders replaced!")
    os.system("rm " + file_name)

if __name__ == "__main__":
    download_file(link, file_name)
    decode_protobin(file_name)