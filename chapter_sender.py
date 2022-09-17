from chapter_downloader import download_new_chapters, list_files
import os

def find_chapters(bname, bnum, cnum):
    chapters = list_files("scripts")
    for chapter in chapters:
        if bname+"_0"+bnum+"_chapter_"+cnum in chapter:
            return chapter
    return "No chapter found"

def send_chapter_to_bot(bname, bnum, cnum):
    chapter = find_chapters(bname, bnum, cnum)
    print(chapter)
    if chapter == "No chapter found":
        return "No chapter found"
    #find chapter in directory and subdirectory
    for root, dirs, filenames in os.walk('scripts'):
        for f in filenames:
            file_path = os.path.join(root, f)
            if chapter in file_path:
                return file_path
    return "No chapter found"