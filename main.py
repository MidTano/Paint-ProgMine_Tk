from tkinter import messagebox
import tkinter as tk
from PIL import Image
import io
from converter import convert_png_to_code

global COLOR

LIST_COLOR = ["red", "green", "blue", "black"]
COLOR = LIST_COLOR[3]

IMAGE_NAME = "sourse\\126x126.png"
Y_ART=120

WEIGHT = 600
HEIGHT = 800

BTN_WIDTH = 10
BTN_HEIGHT = 2

root = tk.Tk()
root.title("Paint-ProgMine")
root.option_add("*Font", "consolas 11")
root.option_add("*Label.Font", "consolas 11")
root.iconbitmap("sourse\main.ico")

root.resizable(False, False)
root.geometry(str(WEIGHT) + "x" + str(HEIGHT))

Low_Res_Canvas = tk.Canvas(root, width=162, height=162, bg="white")
Low_Res_Canvas.pack()

Low_Res_Canvas.place(x=WEIGHT, y=HEIGHT)

High_Res_Canvas = tk.Canvas(root, width=538, height=538, bg="white")
High_Res_Canvas.pack()


def paint(event):
    x, y = (event.x), (event.y)
    High_Res_Canvas.create_rectangle(x, y, x + 4, y + 4, fill=COLOR, width=0)
    Low_Res_Canvas.create_rectangle(x / 4, y / 4, x / 4, y / 4, fill=COLOR, width=0)


def erase(event):
    x, y = (event.x), (event.y)
    High_Res_Canvas.create_rectangle(x-16, y-16, x +16, y + 16, fill="white", width=0,outline="white")
    Low_Res_Canvas.create_rectangle((x / 4)-4, (y / 4)-4, (x / 4)+4, (y / 4)+4, fill="white", width=0,outline="white")


def cursor(event):
    x, y = (event.x), (event.y)
    High_Res_Canvas.config(cursor="dot")


def save_code(window):
    with open("code.txt", "w") as f:
        f.write("".join(convert_png_to_code(IMAGE_NAME, Y_ART)))
    window.destroy()
    messagebox.showinfo("Code saved", "Код сохранен в code.txt")



def save():
    root.config(cursor="watch")
    High_Res_Canvas.config(cursor="watch")

    ps = Low_Res_Canvas.postscript(colormode='color')
    img = Image.open(io.BytesIO(ps.encode('utf-8')))
    img.save(IMAGE_NAME)

    Code_Window = tk.Toplevel(root)
    Code_Window.title("Code")
    Code_Window.geometry("300x400")
    Code_Window.iconbitmap("sourse\code.ico")
    Code_Window.resizable(False, False)

    Save_Button = tk.Button(Code_Window, text="Save", command=lambda: save_code(Code_Window))
    Save_Button.pack()

    Code_Area = tk.Text(Code_Window, width=80, height=40)
    Code_Area.pack()

    for line in convert_png_to_code(IMAGE_NAME, Y_ART):
        Code_Area.insert("end", line)

    root.config(cursor="arrow")
    High_Res_Canvas.config(cursor="dot")


def change_color():
    Color_Canvas.config(bg=COLOR)
    root.after(300, change_color)


#####################
def red():
    global COLOR
    COLOR = LIST_COLOR[0]
def green():
    global COLOR
    COLOR = LIST_COLOR[1]
def blue():
    global COLOR
    COLOR = LIST_COLOR[2]
def black():
    global COLOR
    COLOR = LIST_COLOR[3]
#####################


for _ in range(4):
    btn = tk.Button(root, command=eval(LIST_COLOR[_]), width=BTN_WIDTH, height=BTN_HEIGHT, bg=LIST_COLOR[_])
    btn.pack()
    btn.place(x=WEIGHT / 4 * _ + BTN_WIDTH * (WEIGHT / 200), y=HEIGHT - HEIGHT / 6)

Color_Text = tk.Label(root, text="Цвет сейчас")
Color_Text.pack()
Color_Text.place(x=WEIGHT / 8 * 3 + BTN_WIDTH * (WEIGHT / 200), y=HEIGHT - HEIGHT / 3.5 - BTN_HEIGHT * HEIGHT / 200)

Color_Canvas = tk.Canvas(root, width=BTN_WIDTH * WEIGHT / 200, height=BTN_HEIGHT * HEIGHT / 200, bg=COLOR)
Color_Canvas.pack()
Color_Canvas.place(x=WEIGHT / 7 * 3 + BTN_WIDTH * (WEIGHT / 200), y=HEIGHT - HEIGHT / 4)

root.bind("s", lambda x: save())

messagebox.showinfo("Подсказка", "Нажмите S, чтобы сохранить картинку")

High_Res_Canvas.bind("<B1-Motion>", paint)
High_Res_Canvas.bind("<B3-Motion>", erase)
High_Res_Canvas.bind("<Motion>", cursor)

change_color()

if __name__ == "__main__":
    root.mainloop()
