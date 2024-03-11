import os
import sys
import tkinter
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, messagebox, simpledialog
from tkinter.simpledialog import askstring
import pytube.exceptions
from pytube import YouTube
from pytube import Playlist
from PIL import ImageTk, Image


indexI = 0
indexF = 0

class askBox():
    def __init__(self, len):
        irwindow = tkinter.Toplevel()

        irwindow.title("")
        irwindow.overrideredirect(True)
        irwindow.geometry('%dx%d+%d+%d' % (356, 120, (window.winfo_screenwidth()/2) - 178, (window.winfo_screenheight()/2) - 60))
        irwindow.configure(bg="#3A6A79")
        irwindow.iconphoto(True, PhotoImage(file=resource_path('pudim.png')))
        window.attributes('-disabled', True)
        window.attributes('-disabled', False)

        ircanvas = Canvas(
            irwindow,
            bg="#3A6A79",
            height=120,
            width=356,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        ircanvas.place(x=0, y=0)
        irentry_image_1 = PhotoImage(
            file=resource_path("entry_3.png"))
        irentry_bg_1 = ircanvas.create_image(
            98.0,
            62.5,
            image=irentry_image_1
        )
        irentry_1 = Entry(
            irwindow,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        irentry_1.place(
            x=74.0,
            y=49.0,
            width=48.0,
            height=25.0
        )

        irentry_image_2 = PhotoImage(
            file=resource_path("entry_4.png"))
        ircanvas.create_image(
            258.0,
            62.5,
            image=irentry_image_2
        )
        irentry_2 = Entry(
            irwindow,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        irentry_2.place(
            x=234.0,
            y=49.0,
            width=48.0,
            height=25.0
        )
        irentry_1.insert(0, 1)
        irentry_2.insert(0, len)

        ircanvas.create_text(
            8.0,
            0.0,
            anchor="nw",
            text="Playlist detectada, defina o intervalo de download",
            fill="#FFFFFF",
            font=("Itim Regular", 16 * -1)
        )

        ircanvas.create_text(
            170.0,
            56.0,
            anchor="nw",
            text="A",
            fill="#FFFFFF",
            font=("Itim Regular", 24 * -1)
        )

        button_image_4 = PhotoImage(
            file=resource_path("button_4.png"))
        button_4 = Button(
            irwindow,
            image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: setIndex(str(irentry_1.get()), str(irentry_2.get()), irwindow),
            relief="flat"
        )
        button_4.place(
            x=122.0,
            y=86.0,
            width=112.0,
            height=27.0
        )

        irwindow.resizable(False, False)
        window.wait_window(irwindow)


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
    canvas.itemconfig(tagOrId=text_line1, text="")
    canvas.itemconfig(tagOrId=text_line2, text="")
    canvas.itemconfig(tagOrId=text_line3, text="")
    window.update()
    err = 0
    url = str(entry_1.get())
    pl = 0
    path = str(entry_2.get())
    if "&list=" in url or "?list=" in url:
        pl = 1

    if pl == 0:
        try:
            ytv = YouTube(url)
        except pytube.exceptions.RegexMatchError:
            return
        lprint(text_line1, "Download de arquivo único de vídeo")
        lprint(text_line2, str(ytv.title))
        lprint(text_line3, "Baixando: 1/1")
        stream = ytv.streams.get_by_itag(22)
        try:
            stream.download(filename=f'{ytv.title}.mp4', output_path=path)
        except Exception:
            lprint(text_line2, "Nome inválido")
            stream.download(filename=f'Invalid name.mp4', output_path=path)
            err =1
        if err==0:
            lprint(text_line3, "Concluído com sucesso")
        elif err==1:
            lprint(text_line3, "Concluído com nome inválido")
    elif pl == 1:
        try:
            ytpl = Playlist(url)
        except pytube.exceptions.RegexMatchError:
            return
        pllen = ytpl.length
        vurl = ytpl.video_urls
        askIndexRange(pllen)
        lprint(text_line1, "Download de Playlist de vídeo")
        global indexI, indexF
        for idx in range(pllen):
            if indexI - 1 <= idx < indexF:
                ytv = YouTube(vurl[idx])
                lprint(text_line2, ytv.title)
                lprint(text_line3, f"Baixando {idx + 1}/{pllen}")
                while(True):
                    try:
                        stream = ytv.streams.get_by_itag(22)
                        break
                    except Exception:
                        pass
                try:
                    stream.download(filename=f'{ytv.title}.mp4', output_path=path)
                except Exception:
                    lprint(text_line2, f"Nome inválido ({idx+1})")
                    stream.download(filename=f'Index-{idx+1}.mp4', output_path=path)
                    err = err + 1
        if err == 0:
            lprint(text_line3, "Concluído com sucesso")
        elif err > 0:
            lprint(text_line3, f"Download concluído, {err} nome(s) inválido(s)")
        lprint(text_line2, "")
        indexI = 0
        indexF = 0

def downloadAudio():
    canvas.itemconfig(tagOrId=text_line1, text="")
    canvas.itemconfig(tagOrId=text_line2, text="")
    canvas.itemconfig(tagOrId=text_line3, text="")
    window.update()
    err = 0
    url = str(entry_1.get())
    pl = 0
    path = str(entry_2.get())
    if "&list=" in url or "?list=" in url:
        pl = 1

    if pl == 0:
        try:
            ytv = YouTube(url)
        except pytube.exceptions.RegexMatchError:
            return
        lprint(text_line1, "Download de arquivo único de áudio")
        lprint(text_line2, str(ytv.title))
        lprint(text_line3, "Baixando: 1/1")
        stream = ytv.streams.get_by_itag(22)
        try:
            stream.download(filename=f'{ytv.title}.mp3', output_path=path)
        except Exception:
            lprint(text_line2, "Nome inválido")
            stream.download(filename=f'Invalid name.mp3', output_path=path)
            err =1
        if err==0:
            lprint(text_line3, "Concluído com sucesso")
        elif err==1:
            lprint(text_line3, "Concluído com nome inválido")
    elif pl == 1:
        try:
            ytpl = Playlist(url)
        except pytube.exceptions.RegexMatchError:
            return
        pllen = ytpl.length
        vurl = ytpl.video_urls
        askIndexRange(pllen)
        lprint(text_line1, "Download de Playlist de áudio")
        global indexI, indexF
        for idx in range(pllen):
            if indexI-1 <= idx < indexF:
                ytv = YouTube(vurl[idx])
                lprint(text_line2, ytv.title)
                lprint(text_line3, f"Baixando {idx + 1}/{pllen}")
                while(True):
                    try:
                        stream = ytv.streams.get_by_itag(22)
                        break
                    except Exception:
                        pass
                try:
                    stream.download(filename=f'{ytv.title}.mp3', output_path=path)
                except Exception:
                    lprint(text_line2, f"Nome inválido ({idx+1})")
                    stream.download(filename=f'Index-{idx+1}.mp3', output_path=path)
                    err = err + 1
        if err == 0:
            lprint(text_line3, "Concluído com sucesso")
        elif err > 0:
            lprint(text_line3, f"Download concluído, {err} nome(s) inválido(s)")
        lprint(text_line2, "")
        indexI = 0
        indexF = 0


def lprint(line, text):
    canvas.itemconfig(tagOrId=line, text=text)
    window.update()

def askIndexRange(len):
    askBox(len=len)

def setIndex(i, f, irwindow):
    global indexI, indexF
    indexI = int(i)
    indexF = int(f)
    irwindow.destroy()


window = Tk()
window.title("Youtube Downloader by Senkkou")
window.geometry("472x251")
window.configure(bg="#3A6A79")
window.iconphoto(True, PhotoImage(file=resource_path('pudim.png')))


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
entry_2.insert(0, f'{os.path.expanduser("~")}'+r'\Downloads')

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
