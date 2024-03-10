import os
import sys
import tkinter
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog
from pytube import YouTube
from pytube import Playlist
from PIL import ImageTk, Image

def selectFolder():
    entry_2.delete(0, 'end')
    entry_2.insert(0, str(filedialog.askdirectory()))


def resource_path(relative_path):
    relative_path = r"assets/frame0/"+relative_path
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def downloadVideo():
    err = 0
    url = str(entry_1.get())
    pl = 0
    path = str(entry_2.get())
    if "&list=" in url or "?list=" in url:
        pl = 1

    if pl == 0:
        ytv = YouTube(url)
        stream = ytv.streams.get_by_itag(22)
        try:
            stream.download(filename=f'{ytv.title}.mp4', output_path=path)
        except Exception:
            stream.download(filename=f'Invalid name.mp4', output_path=path)
            err =1

        canvas.itemconfig(tagOrId=text_line1, text="Baixado arquivo em vídeo")
        canvas.itemconfig(tagOrId=text_line2, text=ytv.title)
        if err==0:
            canvas.itemconfig(tagOrId=text_line3, text="Concluído com sucesso")
        elif err==1:
            canvas.itemconfig(tagOrId=text_line3, text="Download concluído, porém com nome inválido")
    elif pl == 1:
        ytpl = Playlist(url)
        pllen = ytpl.length
        vurl = ytpl.video_urls

        for idx in range(pllen):
            ytv = YouTube(vurl[idx])
            #canvas.itemconfig(tagOrId=text_line2, text=ytv.title)
            #canvas.itemconfig(tagOrId=text_line3, text=f"Baixando {idx + 1}/{pllen}")
            while(True):
                try:
                    stream = ytv.streams.get_by_itag(22)
                    break
                except Exception:
                    pass
            try:
                stream.download(filename=f'{ytv.title}.mp4', output_path=path)
            except Exception:
                stream.download(filename=f'Index-{idx}.mp4', output_path=path)
                err = 1
            canvas.itemconfig(tagOrId=text_line1, text="Playlist baixada em vídeo")
            canvas.itemconfig(tagOrId=text_line2, text=f'{pllen} vídeos')
            if err == 0:
                canvas.itemconfig(tagOrId=text_line3, text="Concluídos com sucesso")
            elif err == 1:
                canvas.itemconfig(tagOrId=text_line3, text="Download concluído, houve nome inválido")


def downloadAudio():
    err = 0
    url = str(entry_1.get())
    pl = 0
    path = str(entry_2.get())
    if "&list=" in url or "?list=" in url:
        pl = 1

    if pl == 0:
        ytv = YouTube(url)
        stream = ytv.streams.get_audio_only()
        try:
            stream.download(filename=f'{ytv.title}.mp3', output_path=path)
        except Exception:
            stream.download(filename=f'Invalid name.mp3', output_path=path)
        canvas.itemconfig(tagOrId=text_line1, text="Baixado arquivo em áudio")
        canvas.itemconfig(tagOrId=text_line2, text=ytv.title)
        if err == 0:
            canvas.itemconfig(tagOrId=text_line3, text="Concluído com sucesso")
        elif err == 1:
            canvas.itemconfig(tagOrId=text_line3, text="Download concluído, porém com nome inválido")
    elif pl == 1:
        ytpl = Playlist(url)
        pllen = ytpl.length
        vurl = ytpl.video_urls

        for idx in range(pllen):
            ytv = YouTube(vurl[idx])
            while(True):
                try:
                    stream = ytv.streams.get_audio_only()
                    break
                except Exception:
                    pass
            try:
                stream.download(filename=f'{ytv.title}.mp3', output_path=path)
            except Exception:
                stream.download(filename=f'Index-{idx}.mp3', output_path=path)
            canvas.itemconfig(tagOrId=text_line1, text="Playlist baixada em áudio")
            canvas.itemconfig(tagOrId=text_line2, text=f'{pllen} áudios')
            if err == 0:
                canvas.itemconfig(tagOrId=text_line3, text="Concluídos com sucesso")
            elif err == 1:
                canvas.itemconfig(tagOrId=text_line3, text="Download concluído, houve nome inválido")


window = Tk()
window.title("Youtube Downloader by Senkkou")
window.geometry("472x251")
window.configure(bg="#3A6A79")

icon = ImageTk.PhotoImage(Image.open(resource_path('pudim.png')))
window.iconphoto(True, icon)


canvas = Canvas(
    window,
    bg="#3A6A79",
    height=251,
    width=472,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
entry_image_1 = PhotoImage(
    file=resource_path("entry_1.png"))
entry_bg_1 = canvas.create_image(
    270.5,
    75.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=101.5,
    y=62.0,
    width=338.0,
    height=25.0
)

entry_image_2 = PhotoImage(
    file=resource_path("entry_2.png"))
entry_bg_2 = canvas.create_image(
    189.0,
    211.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=101.5,
    y=198.0,
    width=175.0,
    height=25.0
)

image_image_1 = PhotoImage(
    file=resource_path("image_1.png"))
image_1 = canvas.create_image(
    236.0,
    21.0,
    image=image_image_1
)

canvas.create_text(
    314.0,
    234.0,
    anchor="nw",
    text="https://github.com/senkkou",
    fill="#FFFFFF",
    font=("Inter", 12 * -1)
)


button_image_1 = PhotoImage(
    file=resource_path("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: downloadAudio(),
    relief="flat"
)
button_1.place(
    x=328.0,
    y=110.0,
    width=70.0,
    height=70.0
)

button_image_2 = PhotoImage(
    file=resource_path("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: downloadVideo(),
    relief="flat"
)
button_2.place(
    x=402.0,
    y=110.0,
    width=70.0,
    height=70.0
)

button_image_3 = PhotoImage(
    file=resource_path("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: selectFolder(),
    relief="flat"
)
button_3.place(
    x=297.0,
    y=194.0,
    width=35.0,
    height=35.0
)

image_image_2 = PhotoImage(
    file=resource_path("image_2.png"))
image_2 = canvas.create_image(
    45.0,
    209.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=resource_path("image_3.png"))
image_3 = canvas.create_image(
    169.0,
    145.0,
    image=image_image_3
)

text_line2 = canvas.create_text(
    33.0,
    137.0,
    anchor="nw",
    text="",
    fill="#FFFFFF",
    font=("Inter", 13 * -1)
)

text_line3 = canvas.create_text(
    33.0,
    157.0,
    anchor="nw",
    text="",
    fill="#FFFFFF",
    font=("Inter", 13 * -1)
)

text_line1 = canvas.create_text(
    33.0,
    117.0,
    anchor="nw",
    text="",
    fill="#FFFFFF",
    font=("Inter", 13 * -1)
)

image_image_4 = PhotoImage(
    file=resource_path("image_4.png"))
image_4 = canvas.create_image(
    48.0,
    75.0,
    image=image_image_4
)
window.resizable(False, False)
window.mainloop()