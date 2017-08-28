import requests
import re
from threading import Timer
from tkinter import *

s = requests.Session()

t = 0

def callback():
    global t
    t.cancel()
    root.destroy()

root = Tk()
root.protocol("WM_DELETE_WINDOW", callback)
listb = Listbox(root)

old=0
oldn=0
newn=0
uid=""

def buildwindow():
    root.geometry('300x300+500+300')
    root.title('pp变化查看')
    root.iconbitmap('icon.ico')
    readuid()
    catchdefaultpp()
    sleeppp()
    root.mainloop()

def sleeppp():
    catchpp()
    global t
    t = Timer(2, sleeppp)
    t.start()

def readuid():
    file = open("uid.txt", 'r')
    line = file.read()
    file.close()
    global uid
    uid=line[4:]

def catchdefaultpp():
    global uid
    ppurl="https://osu.ppy.sh/api/get_user?k=41b91bdb921841db7e56ddb23b2142998eaee76e&u="+uid

    data = s.get(ppurl).content
    ddata = data.decode('utf-8')
    pplist = re.compile('pp_raw":"(.*?)"')
    ppnum = re.findall(pplist, ddata)
    global oldn
    oldn=float(ppnum[0])
    global old
    old=oldn

    listb.insert(END,"初始:"+str(oldn)+"pp  "+"现在:"+str(oldn)+"pp")
    listb.pack(fill=BOTH,expand=1)
    root.update_idletasks()

def catchpp():
    try:
        global uid
        ppurl = "https://osu.ppy.sh/api/get_user?k=41b91bdb921841db7e56ddb23b2142998eaee76e&u=" + uid

        data = s.get(ppurl).content
        ddata = data.decode('utf-8')
        pplist = re.compile('pp_raw":"(.*?)"')
        ppnum = re.findall(pplist, ddata)

        global oldn
        global newn
        newn = float(ppnum[0])
        print(newn)
        if newn>oldn:
            ins=str(round(newn-oldn,2))
            print(ins)
            oldn=newn
            listb.insert(END,"+"+ins+"pp！")
            listb.delete(0, 0)
            global old
            listb.insert(0, "初始:" + str(old) + "pp  " + "现在:" + str(newn) + "pp")
            listb.pack(fill=BOTH, expand=1)
            root.update_idletasks()
    except:
        pass

if __name__ == "__main__":
    buildwindow()