from pytube import YouTube

from tkinter import *

from tkinter import ttk

from threading import Thread

import os


window=Tk()


#screen_width = window.winfo_screenwidth()

#screen_height = window.winfo_screenheight()

#window.state("zoomed")



''' Main window '''


window.configure(height=650)

window.configure(width=550)

window.title("YouTube Downloader")



''' Function to locate Download Path of User '''


def download_path():
    
    home=os.path.expanduser("~")

    Downloads=os.path.join(home,'Downloads')

    return Downloads



''' Progress Bar to see the status of download '''


def on_progress(stream,chunk,file_handler,bytes_remaining):

    stat=int(100*(file_size-bytes_remaining)/file_size)

    global pb

    if stat%5==0:

        pb=ttk.Progressbar(frame,orient="horizontal",length=250,mode="determinate",maximum=100,value=stat)
        
        pb.place(relx=0.5,y=450,anchor=S)



''' On Complete Message '''


def on_complete(stream,file_handle):

    pb.place_forget()

    Button(frame,text="Download Completed",state=DISABLED,bg="light green",fg="white",width=40).place(relx=0.5,y=450,anchor=S)



''' Function to start new fresh download '''


def start2():

    frame.place_forget()

    Thread(target=start1).start()



''' Seperate Thread to creation to fetch details of video, Invokes when user clicks Check button '''


def fetch():
    
    Thread(target=fetch_det).start()



''' Function to fetch details of the Video, Invokes when seperate thread is created '''


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

        label1.place_forget()

        button1.place_forget()
        
        entry1.place_forget()

        txt1=yt.title[:80]

        Label(frame,text=txt1,bg="#c0dfd9",width=72).place(relx=0.5,y=100,anchor=CENTER)
        
        global res_in1

        res_in1=IntVar()

        rad2=Radiobutton(frame,text="Video and Audio",variable=res_in1,value=1,width=15,bg="#c0dfd9",command=result1)

        rad2.place(y=150,relx=0.2,anchor=CENTER)

        rad2.select()

        rad2=Radiobutton(frame,text="Video Only",variable=res_in1,value=2,width=15,bg="#c0dfd9",command=result1)

        rad2.place(y=150,relx=0.5,anchor=CENTER)

        rad2.deselect()

        rad2=Radiobutton(frame,text="Audio Only",variable=res_in1,value=3,width=15,bg="#c0dfd9",command=result1)

        rad2.place(y=150,relx=0.8,anchor=CENTER)

        rad2.deselect()

        Button(frame,text="Download More Files",width=45,bg="#b3c2bf",command=start2).place(relx=0.5,y=570,anchor=S)



''' Streams result Thread creation '''


def result1():

    Thread(target=res_rb).start()



''' Streams Result '''


def res_rb():

    global stream_list,res_in

    res_in=StringVar()

    if res_in1.get()==1:

        stream_list=yt.streams.filter(progressive=True, file_extension='mp4')

        res_list=[i.resolution+" : "+str(round(i.filesize/(1024*1024),2))+" MB" for i in stream_list.all() if i.resolution != None]

    if res_in1.get()==2:

        stream_list=yt.streams.filter(adaptive=True,only_video=True, file_extension='mp4')

        res_list=[i.resolution+" : "+str(round(i.filesize/(1024*1024),2))+" MB" for i in stream_list.all() if i.resolution != None]

    if res_in1.get()==3:

        stream_list=yt.streams.filter(adaptive=True,only_audio=True, file_extension='mp4')

        res_list=[i.abr+" : "+str(round(i.filesize/(1024*1024),2))+" MB" for i in stream_list.all() if i.abr != None]

    y_ref=250

    x_ref=150

    x1=1

    stream_list1=['1080p','720p','480p','360p','240p','144p','192kbps','128kbps']

    if res_in1.get() == 1 or res_in1.get()==2:

        str_list=[i.resolution for i in stream_list.all()]

    else:

        str_list=[i.abr for i in stream_list.all()]

    
    for i in range(8):

        rad=Radiobutton(frame,text=stream_list1[i],variable=res_in,value=stream_list1[i],width=10,bg="#c0dfd9")

        if stream_list1[i] not in str_list:

            rad.configure(state=DISABLED)

        if x1:

            rad.select()

            x1=0

        else:

            rad.deselect()

        if i==3:

            y_ref=250

            x_ref=270

        elif i==6:

            y_ref=250

            x_ref=400

        rad.place(y=y_ref,x=x_ref,anchor=CENTER)

        y_ref+=35


    Button(frame,text="Download",width=30,bg="#b3c2bf",command=yt_dw).place(relx=0.5,y=390,anchor=S)

    Label(frame,text=",  ".join(res_list),bg="#c0dfd9",width=72).place(relx=0.5,y=200,anchor=CENTER)



''' Seperate Thread creation to download file, Invokes when user clicks Download Button in GUI '''


def yt_dw():
    
    Thread(target=yt_dwnld).start()



''' Download function, Invokes when seperate thread is created '''


def yt_dwnld():

    try:

        if res_in1.get()==3:

            req_vid=stream_list.filter(abr=res_in.get()).first()

        else:

            req_vid=stream_list.filter(resolution=res_in.get()).first()

        global file_size

        file_size=req_vid.filesize

        req_vid.download(download_path())

        Thread(target=yt.register_on_progress_callback(on_progress),args=()).start()

        Thread(target=yt.register_on_complete_callback(on_complete),args=()).start()

    except:

        Button(frame,text="Download Error",state=DISABLED,bg="red",width=40).place(relx=0.5,y=420,anchor=S)



''' User Interface that is present at start '''


def start1():

    global frame

    frame=Frame(window)

    frame.configure(height=650,width=550)

    frame.place(relx=0.5,rely=0.5,anchor=CENTER)

    global url_in,entry1,button1,label1
    
    url_in=StringVar()

    label1=Label(frame,text="URL", width=15,bg="#c0dfd9")

    label1.place(x=10,y=100)

    entry1=Entry(frame,textvariable=url_in,width=48)

    entry1.focus()

    entry1.place(x=150,y=100)

    button1=Button(frame,text="Check",width=10,bg="#b3c2bf",command=fetch)

    button1.place(x=460,y=98)

    Button(frame,text="Exit",width=50,bg="#b3c2bf",command=window.destroy).place(relx=0.5,y=620,anchor=S)


    

Thread(target=start1).start()


window.mainloop()
