
# ============================================================

from pathlib import Path
import shutil
import re
import os
import sys

print("Hello. Starting.....")

known_extension = []
unknown_extension = []
img = []
vid = []
doc = []
muz = []
arch = []


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ "
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g",    "_")

# dictinary for translate
TRANS = {}
list_of_files = []
list_new_files = []

# make translator
for c, l in zip(list(CYRILLIC_SYMBOLS), TRANSLATION):
    # TRANS[(c)] = l
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


# ============================================================

# command line args 
if len(sys.argv) < 2:
    user_input = os.getcwd()
else:
    user_input = sys.argv[1]
path = Path(user_input)
if path.exists():
    if path.is_dir():
        os.chdir(user_input)
    else:
        print(path, "is file")
else:
    print(path, " is not exist")
    sys.exit()

# ============================================================

# destination folder
current_location = os.getcwd()
print("Текущее местоположение > you want to sort dir>>>", current_location)
res = (input('are you shure??? \r\n "Y" for continue  >>>'))
print(res.lower())
if res.lower() != "y":
    print("Exit by user")
    sys.exit()


# create folders
def create_folders():
    try:
        os.mkdir("archives")
    except Exception as e:
        # print(f"Помилка при створенні папки: {str(e)}")
        ...
    try:
        os.mkdir("video")
    except Exception as e:
        # print(f"Помилка при створенні папки: {str(e)}")
        ...
    try:
        os.mkdir("audio")
    except Exception as e:
        # print(f"Помилка при створенні папки: {str(e)}")
        ...
    try:
        os.mkdir("documents")
    except Exception as e:
        # print(f"Помилка при створенні папки: {str(e)}")
        ...
    try:
        os.mkdir("images")
    except Exception as e:
        # print(f"Помилка при створенні папки: {str(e)}")
        ...


create_folders()  # call create folders


# translite name
def translate(name):
    # print(TRANS)
    # print(name.translate(TRANS))
    return name.translate(TRANS)


# normalisze name
def normalize(name) -> str:
    if "\\" in name:                       # if dir in dir
        new_name = name.split("\\")
        # new_name[-1]
        name = name.removesuffix(new_name[-1])
        # print("pervios name=", new_name[-1])
        pattern = "[^\w\\\.]"
        new_name[-1] = translate(new_name[-1])
        new_name[-1] = re.sub(pattern, "_", new_name[-1])
        name += new_name[-1]
        # print("noralise name=", name)
    else:
        pattern = "[^\w\\\.]"
        name = translate(name)
        name = re.sub(pattern, "_", name)
        # print("noralise name=", name)

    return name


# find & return type of files
def wich_type(var) -> str:
    var = var.upper()
    # print(var)
    if var.endswith(('.JPEG', '.PNG', '.JPG', '.SVG', '.BMP', '.GIF')):
        return "images"
    elif var.endswith(('.AVI', '.MP4', '.MOV', '.MKV', 'MP4')):
        return "video"
    elif var.endswith(('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX')):
        return "documents"
    elif var.endswith(('.MP3', '.OGG', '.WAV', '.AMR')):
        return "audio"
    elif var.endswith(('.ZIP', '.GZ', '.TAR')):
        return "archives"
        # known_extension+=var.endswith
    else:
        # unknown_extension += var.endswith(".")
        return "other_files"


# move file
def move_file(source_path, destination_path):
    try:
        shutil.move(source_path, destination_path)
        # print(f"Файл переміщено з {source_path} до {destination_path}")
    except Exception as e:
        print(f"Помилка під час переміщення файлу: {str(e)}")


# serch rename all files and add them to list, exept spec dirs
def rename_files(path="") -> None:
    global list_of_files
    p = Path(path)    # p Вказує на папку
    for i in p.iterdir():
        if i.is_dir():
            if str(i) in ["audio", "archives", "video",  "documents", "images"]:
                # print("ignoring dir--",i)
                ...
            else:
                new_name = normalize(str(i))
                os.rename(i, new_name)
                list_of_files += [i]
                # print("go in dir==", i)
                rename_files(path=new_name)
        elif i.is_file():
            new_name = normalize(str(i))
            os.rename(i, new_name)
            # print( i.name)
            # print("file =", i)
            list_of_files += [i]
        else:
            print("ankown object =", i)


rename_files()  # return list of all files (list_of_files)


# ============================================================


def sort_files(path="") -> None:
    global list_new_files
    p = Path(path)    # p Вказує на папку
    for i in p.iterdir():
        if i.is_dir():
            if str(i) in ["audio", "archives", "video",  "documents", "images"]:
                # print("ignor dir--",i)
                ...
            else:
                list_new_files += [i]
                sort_files(path=str(i))
                # print("go in dir==", i)
        elif i.is_file():
            list_new_files += [i]
            # print( i.name)
            if wich_type(str(i)) == "images":
                move_file(str(i), "images\\"+i.name)

            elif wich_type(str(i)) == "documents":
                move_file(str(i), "documents\\"+i.name)

            elif wich_type(str(i)) == "audio":
                move_file(str(i), "audio\\"+i.name)

            elif wich_type(str(i)) == "video":
                move_file(str(i), "video\\"+i.name)

            elif wich_type(str(i)) == "archives":
                move_file(str(i), "archives\\"+i.name)

            else:
                if i.name.rfind('.') != -1:
                    unknown_extension.append(i.name[i.name.rfind('.'):])

        else:
            # print("file =", i.name)
            print("ankown object =", i.name)
            ...


sort_files()

# ============================================================


def archives():
    p = Path("archives")    # p Вказує на папку
    for i in p.iterdir():
        if i.is_file():
            # print(i)
            # print (str(i).rindex('.') )
            # print (   str(i)[:  str(i).rindex('.') ]   )
            shutil.unpack_archive(i,  str(i)[: str(i).rindex('.')])


archives()

# ============================================================


def empty_dirs_delet(path=""):
    p = Path(path)    # p Вказує на папку
    for i in p.iterdir():
        if i.is_dir():
            if str(i) in ["audio", "archives", "video",  "documents", "images"]:
                # print("ignor dir--",i)
                ...
            else:
                # print("go in dir==", i)
                contents = os.listdir(i)
                # print("content=" , contents)
                if len(contents) == 0:
                    # print("deleting empty dir =", i)
                    shutil.rmtree(i)
                    empty_dirs_delet(path="")
                else:
                    empty_dirs_delet(path=i)


empty_dirs_delet()


# ============================================================

# make files list
def lists(path="") -> None:
    p = Path(path)    # p Вказує на папку
    for i in p.iterdir():
        if i.is_dir():
            if str(i) in ["archives"]:
                # print("ignor dir--",i)
                ...
            else:
                lists(path=str(i))
        elif i.is_file():
            # print( i.name)
            if wich_type(str(i)) == "images":
                known_extension.append(i.name[i.name.rfind('.'):])
                img.append(i.name)
                move_file(str(i), "images\\"+i.name)

            elif wich_type(str(i)) == "documents":
                known_extension.append(i.name[i.name.rfind('.'):])
                doc.append(i.name)
                move_file(str(i), "documents\\"+i.name)

            elif wich_type(str(i)) == "audio":
                known_extension.append(i.name[i.name.rfind('.'):])
                muz.append(i.name)
                move_file(str(i), "audio\\"+i.name)

            elif wich_type(str(i)) == "video":
                known_extension.append(i.name[i.name.rfind('.'):])
                vid.append(i.name)
                move_file(str(i), "video\\"+i.name)

            elif wich_type(str(i)) == "archives":
                known_extension.append(i.name[i.name.rfind('.'):])
                arch.append(i.name)
                move_file(str(i), "archives\\"+i.name)

            else:
                ...
                # if i.name.rfind('.') != -1:
                #     unknown_extension.append(i.name[i.name.rfind('.'):])

        else:
            # print("file =", i.name)
            print("ankown object =", i.name)
            ...


lists()

# ============================================================

# making list of archives
a = Path('archives')
for i in a.iterdir():
    if i.is_dir():
        ...
    if i.is_file():
        known_extension.append(i.name[i.name.rfind('.'):])
        arch.append(i.name)

# ============================================================

# print lists

print("\nunknown_extensions=")
print(set(unknown_extension))

print("\nknown_extensions=")
print(set(known_extension))

print('\nimages=')
print(img)
print('\nvideos=')
print(vid)
print('\ndocuments=')
print(doc)
print('\nmuzic=')
print(muz)
print('\narchives=')
print(arch)


# ============================================================

# happy end

print("\nThe and")


# ============================================================


if __name__ == '__main__':
    print("You imported hello.py")
