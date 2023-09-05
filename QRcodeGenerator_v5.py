import tkinter as tk
import pyperclip
import pyqrcode
import os
from PIL import Image, ImageOps, ImageTk, ImageDraw, ImageFont
from pyqrcode import create
from tkinter import colorchooser

destination = 'C:/QR Codes'
available_drives = []
available_scale = []
available_padding = []


#-----------custom------------ 
foreground_color_qr = '#000001' 
background_color_qr = '#fffffe'
border_color_qr = '#fffffe'
padding_qr = 5
scale_size_qr = 5
text = "Text Here"
text_x = 10
text_y = 5
text_color = '#000001'
font_size = 15
font_type = 'arial'
#-----------custom-------------

for driveLetter in [chr(i) + ':' for i in range(65,91)]:
    if os.path.exists(driveLetter):
        available_drives.append(driveLetter[0])

for i in range(1,21):
    available_scale.append(i)  

for i in range(1,21):
    available_padding.append(i)      

def chech_file(destination, name): 
    if os.path.exists(os.path.join(destination, name)):
        number = 1
        while os.path.exists(os.path.join(destination, f"{os.path.splitext(name)[0]}({number}).png")):
            number += 1
        return f"{os.path.splitext(name)[0]}({number}).png"  
    else:
        return name
    
def update_widget(link, app_qr):
    label_qr.config(image=app_qr)
    messageText.config(state='normal')
    messageText.delete('1.0', tk.END)
    messageText.insert('1.0', link)
    messageText.config(state='disabled')

def remove_temp(temp_file):
    if os.path.isfile(temp_file):
        try:
            os.remove(temp_file)
        except Exception:
            pass    

def view_qr():
    global destination, app_qr, foreground_color_qr, background_color_qr, padding_qr, border_color_qr, scale_size_qr, text, text_x, text_y, text_color, font_size, font_type
    
    destination = user_drive.get() + ':/QR Codes'
    if not os.path.isdir(destination):    
        os.mkdir(destination)  

    try: 
        link = pyperclip.paste()
        first_qr = pyqrcode.create(link)
        name = chech_file(destination, 'QR.png')
        
        temp_file = destination + '/temp_noBoarder ' + name

        scale_size_qr = int(scale_options.get())
        first_qr.png(temp_file, scale=scale_size_qr, module_color=foreground_color_qr, background=background_color_qr)

        image = Image.open(temp_file)

        padding_qr = int(padding_options.get())
        last_qr = ImageOps.expand(image, border=padding_qr, fill=border_color_qr)

        draw = ImageDraw.Draw(last_qr)

        textofqr()
        font_text = ImageFont.truetype(f"{font_type}.ttf", font_size) 
        draw.text((text_x, text_y), text, font=font_text, fill=text_color)

        app_qr = ImageTk.PhotoImage(last_qr)

        remove_temp(temp_file)
        update_widget(link, app_qr)

        show_message('View QR code')

    except Exception:
        show_message('Faild to convert to QR code')          

def openfolder():
    global destination
    destination = user_drive.get() + ':/QR Codes'
    if os.path.isdir(destination):
        os.startfile(destination)
    else:     
        show_message('Folder does not exist')

def save_qr_img():
    global destination, app_qr, foreground_color_qr, background_color_qr, padding_qr, border_color_qr, scale_size_qr, text, text_x, text_y, text_color, font_size, font_type

    destination = user_drive.get() + ':/QR Codes'
    if not os.path.isdir(destination):    
        os.mkdir(destination)     

    try: 
        link = pyperclip.paste()
        first_qr = pyqrcode.create(link)
        name = chech_file(destination, 'QR.png')

        end_file = destination + '/' + name
        temp_file = destination + '/temp_noBoarder ' + name

        scale_size_qr = int(scale_options.get())
        first_qr.png(temp_file, scale=scale_size_qr, module_color=foreground_color_qr, background=background_color_qr)

        image = Image.open(temp_file)

        padding_qr = int(padding_options.get())
        last_qr = ImageOps.expand(image, border=padding_qr, fill=border_color_qr)

        draw = ImageDraw.Draw(last_qr)

        textofqr()
        font_text = ImageFont.truetype(f"{font_type}.ttf", font_size) 
        draw.text((text_x, text_y), text, font=font_text, fill=text_color)

        app_qr = ImageTk.PhotoImage(last_qr)
        last_qr.save(end_file)

        remove_temp(temp_file)
        update_widget(link, app_qr)

        show_text = f"QR code {name} is saved"
        show_message(show_text)

    except Exception:
        show_message('Faild to convert to QR code')

def show_message(message):
    messageText.config(state='normal')
    messageText.delete('1.0', tk.END)
    messageText.insert('1.0', message)
    messageText.config(state='disabled')         

def color_foreground():
    global foreground_color_qr
    foreground_color_qr = colorchooser.askcolor()[1]
    if foreground_color_qr == None:
        foreground_color_qr = '#000001'
    foregroundColor.config(background = foreground_color_qr)
    text_show = f"Changed the foreground color to {foreground_color_qr}"
    show_message(text_show)

def color_background():
    global background_color_qr
    background_color_qr = colorchooser.askcolor()[1]
    if background_color_qr == None:
        background_color_qr = '#ffffffe'
    backgroundColor.config(background = background_color_qr)
    text_show = f"Changed the boackground color to {background_color_qr}"
    show_message(text_show)

def color_boarder():
    global border_color_qr
    border_color_qr = colorchooser.askcolor()[1]
    if border_color_qr == None:
        border_color_qr = '#fffffe'
    borderColor.config(background = border_color_qr)
    text_show = f"Changed the border color to {border_color_qr}"
    show_message(text_show)  

def textofqr():
    global text, text_x, text_y, text_color, font_size, font_type
    text = qrtext.get("1.0", tk.END)
    try:   
        text_x = int(qrtext_x.get("1.0", tk.END))
    except Exception:
        text_x = 10
    try:       
        text_y = int(qrtext_y.get("1.0", tk.END))
    except Exception:
        text_y = 5
    try:        
        font_size = int(qrtext_size.get("1.0", tk.END))
    except Exception:
        font_size = 15

def color_qrtext():
    global text_color
    text_color = colorchooser.askcolor()[1]
    if text_color == None:
        text_color = '#000001'    
    qrtext_color.config(background = text_color)
    text_show = f"Changed the text color to {text_color}"
    show_message(text_show) 
    
# this is the base64 of the app 
icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAACXBIWXMAAABgAAAAYADwa0LPAAAAP1BMVEVM5GAAAAAAAABM42FM5l8AAABN6F1HcExN5F9M5GBL4WFP519N5F8AAAAAAABN5F9O7GIAAABM5GFN5GAAAAD1gOjXAAAAE3RSTlOqnp2JUKohAJ6dIiBTISLrDSBUAY0pYwAAAGdJREFUGNNtjlsOgCAMBBdoBRR83/+sFhsbg87PppO0XcQOxDEBaSCaHbOrItIhZMCdgheBJgBwE/wnPiuDDHkCqmf2mwhCYwl3komwmtAepWja0b1o2tsQNF89TDw9bEV7EGmK6LgAjUgImomZfGYAAAAASUVORK5CYII='

app = tk.Tk()

app.iconphoto(True, tk.PhotoImage(data=icon)) # if the icon is defined remove the comment from this line
app.geometry('560x420+600+100')
app.title('QRcode Generator')
app.config(bg = '#1e1e1e')
app.resizable(False, False)
bgimg1= tk.PhotoImage(file = "assets/background.png") # change file= -> data= if base64 
limg1= tk.Label(app, i=bgimg1)
limg1.place(x=-1, y=-1)

second_window = tk.Toplevel(app)
second_window.geometry('350x350+249+100')
second_window.title("QRcode Generator")
second_window.config(bg = '#1e1e1e')
second_window.maxsize(1005, 1005)
bgimg2= tk.PhotoImage(file = "assets/secondQRbg.png") # change file= -> data= if base64 
limg2= tk.Label(second_window, i=bgimg2)
limg2.place(x=-1, y=-1)

messageText = tk.Text(app, height=3, width=55, font=('Arial', 10), foreground='#3fdc44', background='#1e1e1e', borderwidth=3)
messageText.place(x = 160, y = 70)
messageText.insert("1.0", 'Delete QR Text if not needed\nEnter any thing and change the properties')
messageText.config(state='disabled')

clickCreat_img = tk.PhotoImage(file='assets/creatQR.png')
clickCreat = tk.Button(app, image=clickCreat_img, borderwidth=0, background='#1e1e1e', activebackground='#1e1e1e', command= save_qr_img)
clickCreat.place(x = 425, y = 10)

openFolder_img = tk.PhotoImage(file='assets/openFolder.png')
openFolder = tk.Button(app,image=openFolder_img ,borderwidth=0, background='#3fdc44', activebackground='#3fdc44', command= openfolder)
openFolder.place(x = 10, y = 75)

viewQr_img = tk.PhotoImage(file='assets/ViewQR.png')
viewQr = tk.Button(app, image=viewQr_img,borderwidth=0, background='#1e1e1e', activebackground='#1e1e1e', command= view_qr)
viewQr.place(x = 425, y = 150)

label_qr = tk.Label(second_window, text='-QR code will be displayed here\n\n-Use any text\n\n-Use this format for a URL\nhttps://www.google.com/',font=('Arial', 16), foreground='#ffffff', background='#1e1e1e')
label_qr.place(x = 20, y = 20)

user_drive = tk.StringVar()
user_drive.set(available_drives[0])
drop_menu1 = tk.OptionMenu(app, user_drive , *available_drives)
drop_menu1.place(x = 42, y = 35)
drop_menu1.config(font=('Arial', 14), background='dark red', foreground='white')

scale_options = tk.StringVar()
scale_options.set(available_scale[4])
drop_menu_scale = tk.OptionMenu(app, scale_options , *available_scale)
drop_menu_scale.place(x = 28, y = 245)
drop_menu_scale.config(font=('Arial', 14), background='#1e1e1e', foreground='#3fdc44')

padding_options = tk.StringVar()
padding_options.set(available_scale[9])
drop_menu_padding = tk.OptionMenu(app, padding_options , *available_padding)
drop_menu_padding.place(x = 118, y = 245)
drop_menu_padding.config(font=('Arial', 14), background='#1e1e1e', foreground='#3fdc44')

foregroundColor = tk.Button(app, text='Foreground color', font=('Arial', 12), background='black', foreground='white', command=color_foreground)
foregroundColor.place(x = 20, y = 160)

backgroundColor = tk.Button(app, text='Background color', font=('Arial', 12), background='white', command=color_background)
backgroundColor.place(x = 160, y = 160)

borderColor = tk.Button(app, text='Border color', font=('Arial', 12), background='white', foreground='black', command=color_boarder)
borderColor.place(x = 305, y = 160)

qrtext = tk.Text(app, height=2, width=30, font=('Arial', 12), background='#1e1e1e', foreground='#3fdc44', borderwidth=3)
qrtext.place(x = 270, y = 225)
qrtext.insert("1.0", text)

qrtext_x = tk.Text(app, height=1, width=5, font=('Arial', 14), background='#1e1e1e', foreground='#3fdc44', borderwidth=3)
qrtext_x.place(x = 287, y = 360)
qrtext_x.insert("1.0", '10')

qrtext_y = tk.Text(app, height=1, width=5, font=('Arial', 14), background='#1e1e1e', foreground='#3fdc44', borderwidth=3)
qrtext_y.place(x = 382, y = 360)
qrtext_y.insert("1.0", '5')

qrtext_size = tk.Text(app, height=1, width=5, font=('Arial', 14), background='#1e1e1e', foreground='#3fdc44', borderwidth=3)
qrtext_size.place(x = 477, y = 360)
qrtext_size.insert("1.0", '15')

qrtext_color = tk.Button(app, text='Text color', font=('Arial', 12), background='white', command=color_qrtext)
qrtext_color.place(x = 370, y = 280)

app.mainloop()
