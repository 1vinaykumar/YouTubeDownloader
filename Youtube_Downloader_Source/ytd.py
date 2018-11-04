from pytube import YouTube

from tkinter import *

from tkinter import ttk

import threading

from threading import Thread

import os


window=Tk()

#screen_width = window.winfo_screenwidth()

#screen_height = window.winfo_screenheight()

#window.state("zoomed")

window.configure(height=600)

window.configure(width=550)

window.title("YouTube Downloader")

frame=Frame(window)

frame.configure(height=550,width=550)

frame.place(relx=0.5,rely=0.4,anchor=CENTER)



def download_path():
    
    home=os.path.expanduser("~")

    Downloads=os.path.join(home,'Downloads')

    return Downloads



'''def on_progress(stream,chunk,file_handler,bytes_remaining):

    global thd1,txt123

    ij=-1

    txt123=int(100*(file_size-bytes_remaining)/file_size)

    if ij!=txt123:

        thd1=Thread(target=progress,args=())

        thd1.start()

        


def progress():
    
    ttk.Progressbar(frame,orient="horizontal",length=300,mode="determinate",maximum=100,value=txt123).place(relx=0.5,rely=0.72,anchor=S)'''



def fetch_det():

    txt1=""

    res_list=["Not Available"]

    url=url_in.get().strip()

    try:

        global yt

        yt=YouTube(url)

    except:

        txt1="Invalid URL"

        yt=""

    else:

        txt1=yt.title[:80]

        global stream_list

        stream_list=yt.streams.filter(progressive=True, file_extension='mp4')

        res_list=[i.resolution+" : "+str(round(i.filesize/(1024*1024),2))+" MB" for i in stream_list.all()]

        global res_in

        res_in=StringVar()

        y_ref=210

        x=1

        for i in stream_list.all():

            rad=Radiobutton(frame,text=i.resolution,variable=res_in,value=i.resolution,width=10,bg="#c0dfd9")

            if x:

                rad.select()

                x=0

            else:

                rad.deselect()

            rad.place(y=y_ref,relx=0.5,anchor=CENTER)

            y_ref+=30
        
        Button(frame,text="Download",width=25,bg="#b3c2bf",command=yt_dw).place(x=300,y=320)

    Label(frame,text=txt1,bg="#c0dfd9",width=72).place(relx=0.5,y=120,anchor=CENTER)

    Label(frame,text=",  ".join(res_list),bg="#c0dfd9",width=72).place(relx=0.5,y=160,anchor=CENTER)

    Button(frame,text="Exit",width=25,bg="#b3c2bf",command=window.destroy).place(x=50,y=320)



def yt_dw():

    global thd

    thd=Thread(target=yt_dwnld,args=())

    thd.start()



def yt_dwnld():

    try:
        
        req_vid=stream_list.filter(resolution=res_in.get()).first()
    
        global file_size

        file_size=req_vid.filesize

        req_vid.download(download_path())

        txt_dis="Download Completed"

    except:
        
        txt_dis="  Download Error  "

    res_txt=Text(frame,width=41,height=3,fg="green",bg="#c0dfd9")

    if txt_dis=="Download Error":
        
        res_txt.configure(fg="red")

    res_txt.tag_configure('bold_big',font=('Times New Roman',27,'bold'))

    res_txt.insert(END,txt_dis,'bold_big')

    res_txt.place(relx=0.5,rely=0.85,anchor=S)



url_in=StringVar()

Label(frame,text="URL", width=15,bg="#c0dfd9").place(x=10,y=50)

ent1=Entry(frame,textvariable=url_in,width=48)

ent1.focus()

ent1.place(x=150,y=50)

Button(frame,text="Check",width=10,bg="#b3c2bf",command=fetch_det).place(x=460,y=48)


window.mainloop()
