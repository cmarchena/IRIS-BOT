from chapter_downloader import download_new_chapters, list_files
from filelocations import SCRIPTS as SCRIPTS
import os

def find_chapters(bname, bnum, cnum):
    downloads = download_new_chapters()
    books, chapters = list_files(SCRIPTS)
    for chapter in chapters:
        if bname+"_0"+bnum+"_chapter_"+cnum in chapter:
            return chapter
    return "No chapter found"

def send_chapter_to_bot(bname, bnum, cnum):
    chapter = find_chapters(bname, bnum, cnum)
    print("chapter=", chapter)
    if chapter == "No chapter found":
        return "No chapter found"
    #find chapter in directory and subdirectory
    for root, dirs, filenames in os.walk(SCRIPTS):
        for f in filenames:
            file_path = os.path.join(root, f)
            if chapter in file_path:
                return file_path
    return "No chapter found"

if __name__ == "__main__":
    print(send_chapter_to_bot("endless_summer", "1", "15"))