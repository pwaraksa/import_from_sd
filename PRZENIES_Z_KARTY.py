import os, re, glob, sys, time, datetime, shutil, time 

'''
##################################################
##########         VERSION 1.2          ##########
##################################################
Changelog:
-added choice function
-in choice function changed the variable name: when -> option
-changed the selection text to:  1. NOWA FOTOPULAPKA (lub: data wykonania zdjecia (poprawna data ustawiona w fotopulapce))" 
-changed the selection text to:	 2. STARA FOTOPULAPKA (lub: dzisiejsza data (zla data ustawiona w fotopulapce))"
-function count_photos counts jpg and mov 
'''

def detect_sd_card():
    drives=re.findall(r"[A-Z]+:.*$",os.popen("mountvol /").read(),re.MULTILINE)
    sd_card=""
    for drive in drives:
        if os.path.isdir(drive+"DCIM"):
            sd_card=drive
    return sd_card

def detect_dirs(sd_card):
    dirs=[]
    if os.path.isdir(sd_card+"DCIM\\100MEDIA"):
        dirs.append(sd_card+"DCIM\\100MEDIA\\")
    if os.path.isdir(sd_card+"DCIM\\100NVTIM"):
        dirs.append(sd_card+"DCIM\\100NVTIM\\")
    return dirs

def count_photos(photo_path):
    if os.path.isdir(photo_path):
        jpg_movCounter = len(glob.glob1(photo_path,"*.JPG"))+len(glob.glob1(photo_path,"*.MOV"))
        return jpg_movCounter

def get_str_from_timestamp(path): #e.g. 2019-07-16_192944
    s = os.path.getmtime(path)
    s = datetime.datetime.fromtimestamp(s)
    s = s.strftime('%Y-%m-%d_%H%M%S')
    return s
    
def set_timestamp_from_str(path, s): #e.g. 2019-07-16_192944
    date = datetime.datetime.strptime(s, '%Y-%m-%d_%H%M%S')
    timestamp=time.mktime(date.timetuple())
    os.utime(path, (timestamp, timestamp))

def name2timestamp(path):
    os.chdir(path)
    files=glob.glob("*")
    for file in files:
        ext = os.path.splitext(file)[1]
        new_file_name = get_str_from_timestamp(path+file)
        
        while os.path.isfile(path + new_file_name + ext):
            new_file_name += "_dup"

        os.rename(path+file,path+new_file_name+ext)
    
def name2currentdate(path):
    os.chdir(path)
    i=0
    files=glob.glob("*")
    for file in files:
        i+=1
        ext = os.path.splitext(file)[1]
        new_file_name = time.strftime("%Y-%m-%d_%H%M%S", time.gmtime()) + "__" + str(i)
        while os.path.isfile(path + new_file_name + ext):
            new_file_name += "_dup"
        os.rename(path+file,path+new_file_name+ext)
        set_timestamp_from_str(path+new_file_name+ext, new_file_name.split("__")[0].replace("_dup",""))
  
def del_dup(path):
    os.chdir(path)
    
    files=glob.glob("*_dup*")
    for file in files:
        try:
            os.remove(path+file)
        except: #plik zajety
            time.sleep(5)
            os.remove(path+file)
            
def move_photos(source, destination,count,when):

    print "Zmienianie nazw..." 
    if when=="1":
        name2timestamp(source)
    if when=="2":
        name2currentdate(source)
    os.chdir(source)
    i=0
    files=glob.glob("*")
    for file in files:
        filename=file
        i+=1
        while os.path.isfile(destination + filename):
            filename = filename.split(".")
            filename.insert(1,"_dup.")
            filename = "".join(filename)
        shutil.move(source+filename, destination)
        #os.system('move "{}" "{}"'.format(source+file,destination)) 
        print "{}/{}".format(i,count)
    print "Usuwanie duplikatow..."
    del_dup(destination)

def choice(options):
    option=""
    while option not in options:
        print "Wybierz " + " lub ".join(options)
        option=""
        option = raw_input()
    return option



###########################################################
sd_card=detect_sd_card()
if sd_card != "":
    print "Wykryto karte SD: " + sd_card
else:
    print "Nie wykryto karty SD"
    os.system("pause")
    sys.exit(1)

dirs=detect_dirs(sd_card)

for photo_path in dirs:
    count=count_photos(photo_path)
    if count == 0:
        print "Nie wykryto zdjec w folderze {}".format(photo_path)
        break
    else:
        print "Wykryto {} zdjec (w folderze {}).".format(str(count),photo_path)
        print "\nGdzie przeniesc zdjecia?" 
        print "1. Rozynsk" 
        print "2. Puszcza"
        where=choice(['1','2'])

        print "\nJaka date przypisac zdjeciom?" 
        print "1. NOWA FOTOPULAPKA (lub: data wykonania zdjecia (poprawna data ustawiona w fotopulapce))" 
        print "2. STARA FOTOPULAPKA (lub: dzisiejsza data (zla data ustawiona w fotopulapce))"
        when=choice(['1','2'])

        if where=="1": #ROZYNSK
            print "PRZENOSZENIE DO ZDJEC Z ROZYNSKA..." 
            path="C:\\Users\\user\\Desktop\\ZDJECIA_ROZYNSK\\"
            move_photos(photo_path,path,count,when)
        if where=="2": #PUSZCZA
            print "PRZENOSZENIE DO ZDJEC Z PUSZCZY..." 
            path="C:\\Users\\user\\Desktop\\ZDJECIA_PUSZCZA\\"
            move_photos(photo_path,path,count,when)

if len(dirs)==0:
    print "Nie znaleziono folderow 100MEDIA 100NVTIM na karcie SD"

print "Zakonczono."
os.system("pause")