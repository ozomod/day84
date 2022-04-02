import tkinter.filedialog
from PIL import Image as Image_PIL
from PIL import ImageOps, ImageDraw, ImageFont, ImageTk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd


window = Tk()
window.title("Добро пожаловать в приложение PythonRu")


def confirm_text():
    global im, im_draw
    im = im_draw.copy()

def confirm_logo():
    global im, decreased_merged
    im = decreased_merged.copy()



def change_text(event):

    global tk_im_draw, im_draw

    im_draw = im.copy()
    draw = ImageDraw.Draw(im_draw)
    font = ImageFont.truetype("arial.ttf", text_size.get())
    some_text = text_on_image.get()
    x_axis = text_x.get()
    y_axis = text_y.get()
    current_color = colors[-(color_box.curselection()[0])]
    # print(current_color)
    print(text_size.get())
    draw.text((x_axis, y_axis), some_text, font=font, fill=current_color)

    tk_im_draw = ImageTk.PhotoImage(im_draw)
    label['image'] = tk_im_draw


def create_text():
    global tk_im_draw, im_draw
    # default color listbox
    color_box.selection_set(0)
    current_color = colors[-(color_box.curselection()[0])]

    im_draw = im.copy()
    draw = ImageDraw.Draw(im_draw)
    default_text = "Я вас не звал"
    default_font_size = 55
    font = ImageFont.truetype("arial.ttf", default_font_size)
    # размеры текста для центровки
    w, h = draw.textsize(text=default_text, font=font)
    x_axis = (im.size[0] - w)/2
    y_axis = (im.size[1] - h)/2
    #задаю дефолтные значения для текста
    text_x.set(x_axis)
    text_y.set(y_axis)
    text_size.set(default_font_size)

    draw.text((x_axis, y_axis), default_text, font=font, fill=current_color)
    tk_im_draw = ImageTk.PhotoImage(im_draw)
    label['image'] = tk_im_draw


def set_size(event):
    global tk_merged_decreased, decreased_merged

    percentage = (scale_size.get()/100)
    width = round(logo.size[0] * percentage)
    height = round(logo.size[1] * percentage)
    resized_logo = logo.resize((width, height))

    decreased_merged = im.copy()

    decreased_merged.paste(resized_logo, (position_x.get(), position_y.get()), mask=resized_logo)

    tk_merged_decreased = ImageTk.PhotoImage(decreased_merged)
    label.config(image=tk_merged_decreased)


def select_logo():
    global tk_merged, logo, merged
    logo = Image_PIL.open('watermark.png')
    merged = im.copy()

    x_axis = round(((im.size[0]) - (logo.size[0])*0.55)/2)
    y_axis = round(((im.size[1]) - (logo.size[1])*0.55)/2)

    print(x_axis)
    print(y_axis)
    merged.paste(logo, (x_axis, y_axis), mask=logo)
    tk_merged = ImageTk.PhotoImage(merged)

    label.config(image=tk_merged)

    scale_size.set(55)
    position_x.set(x_axis)
    position_y.set(y_axis)



def select_file():
    global tkimage, im, label
    path = fd.askopenfilename(title='open A file', initialdir='/')

    im = Image_PIL.open(path)
    tkimage = ImageTk.PhotoImage(im)

    label = Label(window, image=tkimage)
    label.grid(row=1, column=1, rowspan=8, columnspan=3)

    position_x['to'] = im.size[0]
    position_y['to'] = im.size[1]

    position_x['from'] = -im.size[0]
    position_y['from'] = -im.size[0]

    text_x['to'] = im.size[0]
    text_y['to'] = im.size[1]


window.minsize(500, 500)

open_button = Button(window, text='open a FILE', command=select_file)
open_button.grid(row=0, column=1)

logo_button = Button(window, text='open a LOGO', command=select_logo)
logo_button.grid(row=0, column=2)

text_on_image = Entry(window)
text_on_image.insert(END, "Я вас не звал")
text_on_image.grid(row=7, column=4)
text_on_image.bind('<KeyRelease>', change_text)

color_box = Listbox(width=15, height=7)
color_box.grid(row=8, column=4)
color_box.bind('<<ListboxSelect>>', change_text)
colors = ['red', 'blue', 'green', 'orange', 'black', 'yellow', 'white']
for color in colors:
    color_box.insert(1, color)

confirm_logo_button = Button(window, text='confirm LOGO', command=confirm_logo)
confirm_logo_button.grid(row=7, column=0)

confirm_text_button = Button(window, text='confirm TEXT', command=confirm_text)
confirm_text_button.grid(row=9, column=4)

save_button = Button(window, text='save')
save_button.grid(row=9, column=1)

create_text_button = Button(window, text='Create Text', command=create_text)
create_text_button.grid(row=0, column=3)

logo_size_label = Label(window, text='change logo size')
logo_size_label.grid(row=1, column=0)
scale_size = Scale(window, orient=HORIZONTAL, length=200, from_=5, to=300, tickinterval=30, resolution=10)
scale_size.grid(row=2, column=0)
scale_size.bind("<B1-Motion>", set_size)


logo_x_label = Label(window, text='change logo x-axis ')
logo_x_label.grid(row=3, column=0)
position_x = Scale(window, orient=HORIZONTAL, length=200, from_=0, to=300, tickinterval=100, resolution=10)
position_x.grid(row=4, column=0)
position_x.bind("<B1-Motion>", set_size)


logo_y_label = Label(window, text='change logo y-axis ')
logo_y_label.grid(row=5, column=0)
position_y = Scale(window, orient=HORIZONTAL, length=200, from_=0, to=300, tickinterval=100, resolution=10)
position_y.grid(row=6, column=0)
position_y.bind("<B1-Motion>", set_size)


text_size_label = Label(window, text='change text size')
text_size_label.grid(row=1, column=4)
text_size = Scale(window, orient=HORIZONTAL, length=200, from_=25, to=100, tickinterval=30, resolution=10)
text_size.grid(row=2, column=4)
text_size.bind('<B1-Motion>', change_text)

text_x_label = Label(window, text='change text x-axis')
text_x_label.grid(row=3, column=4)
text_x = Scale(window, orient=HORIZONTAL, length=200, from_=-0, to=300, tickinterval=100, resolution=10)
text_x.grid(row=4, column=4)
text_x.bind("<B1-Motion>", change_text)

text_y_label = Label(window, text='change text y-axis')
text_y_label.grid(row=5, column=4)
text_y = Scale(window, orient=HORIZONTAL, length=200, from_=-0, to=300, tickinterval=100, resolution=10)
text_y.grid(row=6, column=4)
text_y.bind("<B1-Motion>", change_text)


window.mainloop()



# im = Image.open('wojak.jpg')
# ozomod = Image.open('w_watermark.png')
#
# draw = ImageDraw.Draw(im)
# font = ImageFont.truetype("arial.ttf", 25)
# draw.text((100, 25), 'world', font=font, fill=(255,0,0,255))
#
# im.show()
# #
# # size = im.size
# # wm_size = (round(size[0]*0.1), round(size[0]*0.1))
# # resized_watermark = ozomod.resize(wm_size)
# # margin = round(size[0]*0.02)
# # print(margin)
# #
# # im.paste(resized_watermark, (size[0]-wm_size[0]-margin, size[1]-wm_size[1]-margin), mask=resized_watermark)
# #
# # im.show()



# def create_text(event):
#     global tk_im_draw, im_draw
#
#     im_draw = im.copy()
#     draw = ImageDraw.Draw(im_draw)
#     font = ImageFont.truetype("arial.ttf", text_size.get())
#     some_text = text_on_image.get()
#     x_axis = text_x.get()
#     y_axis = text_y.get()
#     current_color = colors[-(color_box.curselection()[0])]
#     print(current_color)
#     draw.text((x_axis, y_axis), some_text, font=font, fill=current_color)
#
#     tk_im_draw = ImageTk.PhotoImage(im_draw)
#     label['image'] = tk_im_draw