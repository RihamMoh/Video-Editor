import ffmpeg
import cv2
from tkinter import *
from PIL import ImageTk,Image

import tkinter.ttk as ttk
from tkinter import filedialog
import cv2
import numpy as np
import datetime
import os
root=Tk()
def disign_window(title,geo,ico):
    root.title(title)
    root.geometry(geo)
    root.iconbitmap(ico)
    root.configure(bg='white')
disign_window('Video Editor',"1000x490", 'icon.ico')
s = ttk.Style()

s.configure('TFrame', background='white')
s.configure('TNotebook', background='white')
s.configure('TScale', background='white')
s.configure('TLabelframe', background='white')
canvas=Canvas(root
              ,width=560
              ,heigh=400,
              bg='black')
canvas.place(x=400,y=10)



fram1=ttk.LabelFrame(root,text='Fram Pos')
fram1.place(x=10,y=420)
def update_value():
    scale.config(value=fram)
#var=IntVar(value=50)
def set_fram(event):
    global fram
    fram=scale.get()
    if int(fram) !=fram:
        fram=round(fram)
    l.config(text=to_time(fram))
    run_video(fram)

global scale
scale=ttk.Scale(root, from_=0, 
                to=100,length=550,
                orient='horizontal',value=0,state='disabled')
scale.place(x=408,y=430)

img=PhotoImage(file='front.png')
canvas.create_image(0,0,image=img,anchor=NW)
global fps
fps=25
class menu_com():
    def open_file():
        global video,length_fram
        root.file_name=filedialog.askopenfilename(initialdir="c:",
                                                  title='select a video file',
                                                  filetypes=((
                                                      "VLC file","*.ts"),
                                                      ("MP4 file","*.mp4"),
                                                      ("All file","*.*")))
        global inp,a,v,fps
        b.config(state='NORMAL')
        inp=ffmpeg.input(root.file_name)
        a=inp['a']
        v=inp['v']
        video = cv2.VideoCapture(root.file_name)

        fps=video.get(cv2.CAP_PROP_FPS)
        no_error=True

        global fram
        fram=0
        length_fram=video.get(cv2.CAP_PROP_FRAME_COUNT)

        scale.config(to=length_fram,value=0)
        scale.config(state='NORMAL')
        run_video(0)
def to_time(fram_):
    global fps
    return str(datetime.timedelta(seconds=fram_/fps))

def run_video(fram_num):
    global img
    try:
        l.config(text=to_time(fram_num))
        video.set(cv2.CAP_PROP_POS_FRAMES,fram_num); # Where frame_no is the frame you want
        ret,frame = video.read() # Read the frame
   
        img=ImageTk.PhotoImage(
            Image.fromarray(
                cv2.cvtColor (
                    cv2.resize(
                        frame,
                        (560,400),
                        interpolation=cv2.INTER_NEAREST),
                    cv2.COLOR_BGR2RGB)))
        canvas.create_image(0,0,image=img,anchor = NW)
    except:
        pass
scale.config(command=set_fram)
 #video_name is the video being called
global fram
fram=0
i=to_time(fram)
l=Label(fram1,text=i,bg='white')
l.pack()
global fram_p
fram_p=1;
fram_list=[
    0,
    1,
    10,
    20,
    30,
    40,
    100,
    200
    ]
notbook= ttk.Notebook(root)
  
tab1 = ttk.Frame(notbook,width=380,height=380)
tab2 = ttk.Frame(notbook,width=380,height=380)
  
notbook.add(tab1, text ='Tab 1')
notbook.add(tab2, text ='Tab 2')
notbook.place(x=10,y=10)
global dic
dic={}
def change_ac(event):
    dic['c:a']=str(ac_click.get())
def change_vc(event):
    dic['c:v']=str(vc_click.get())
def change_crf(event):
    dic['crf']=str(crf_click.get())
def change_fram_p(event):
    global fram_p
    fram_p=Click.get()
def change_audio(event):
    global a
    a=inp[str('a:'+str(audio_click.get()))]
    print(str('a:'+str(audio_click.get())))
Click=IntVar()
Click.set(fram_list[0])
op=ttk.OptionMenu(tab1,Click, *fram_list,command=change_fram_p)
op.place(x=10,y=10)
vc_click=StringVar()
ac_click=StringVar()
crf_click=StringVar()
audio_click=IntVar()
vc_list=[
    'ac3',
    'ac3',
    'copy'
    ]
ac_list=[
    'libx264',
    'libx264',
    'copy'
    ]

crf_list=[
    'copy',
    'copy',
    '20',
    '25'
    ]
audio_list=[
    0,
    0,
    1
    ]
op1=ttk.OptionMenu(tab1,vc_click, *vc_list,command=change_vc)
op1.place(x=63,y=10)
op2=ttk.OptionMenu(tab1,ac_click, *ac_list,command=change_ac)
op2.place(x=123,y=10)
op3=ttk.OptionMenu(tab1,crf_click, *crf_list,command=change_crf)
op3.place(x=203,y=10)
op3=ttk.OptionMenu(tab1,audio_click, *audio_list,command=change_audio)
op3.place(x=10,y=50)
def move_video_right(event):
    global fram
    if fram < length_fram:
        

        fram+=fram_p
      
        scale.config(value=fram)
        run_video(fram)
def move_video_left(event):
    global fram
    if fram > 1:
        fram-=fram_p
        scale.config(value=fram)
        run_video(fram)


def video():    
    pass
def start_trim():
    global dic
    dic['ss']=to_time(scale.get())
    b1.config(state='NORMAL')
def end_trim():
    dic['to']=to_time(scale.get())
    con.config(state='NORMAL')
def convert_():
    global outfile
    out=filedialog.asksaveasfilename(defaultextension=".ts",
                                     initialdir="c:",
                                     title='save file')
    b1.config(state='disabled')
    b.config(state='NORMAL')
    con.config(state='disabled')
    outfile=ffmpeg.output(a,v,out,**dic)
    print(outfile.compile())
    if os.path.isfile(out)==True:
        ffmpeg.run(outfile,overwrite_output=True,capture_stdout=True)
    else:
        ffmpeg.run(outfile)
b=ttk.Button(tab2,text='start trim',command=start_trim,state='disabled')
b1=ttk.Button(tab2,text='end trim',command=end_trim,state='disabled')
con=ttk.Button(tab2,text='convert',command=convert_,state='disabled')
b.place(x=10,y=10)
b1.place(x=100,y=10)
con.place(x=190,y=10)
main_menu=Menu(root)
root.config(menu=main_menu)
menu=[
      Menu(main_menu,tearoff=0),
      Menu(main_menu,tearoff=0),
      Menu(main_menu,tearoff=0)
      ]
main_menu.add_cascade(label='file',menu=menu[0])
main_menu.add_cascade(label='edit',menu=menu[1])
main_menu.add_cascade(label='option',menu=menu[2])

menu[0].add_command(label='file')    
menu[0].add_command(label='New',command=menu_com.open_file) 
menu[0].add_command(label='Exit',command=root.destroy)










#bind
root.bind("<Left>",move_video_left)
root.bind("<Right>",move_video_right)


root.mainloop()