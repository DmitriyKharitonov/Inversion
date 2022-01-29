from tkinter import *
from inversion_v2 import *
from PIL import ImageTk, Image
from tkinter import filedialog
import os
import datetime

class App:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("840x840")
        self.root.resizable(width=True, height=True)
        self.btn = Button(self.root, text='open image',
                          command=self.open_img).place(x=200, y=0)
        self.btn2 = Button(self.root, text='inversion',
                           command=self.inv).place(x=320, y=0)
        self.btn3 = Button(self.root, text = 'reset_photo',
                           command = self.reset_photo).place(x=420, y = 0)
        self.btn4 = Button(self.root, text = 'save_photo',
                           command = self.save_photo).place(x=520, y = 0)
        self.res = 0
        self.radius = 50
        self.inversion_radius = self.radius
        self.canvas = Canvas(self.root)
        self.canvas.place(x=60, y=30, height=720, width=720)
        self.canvas.bind("<Motion>", self.motion)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<MouseWheel>", self.change_inversion_radius)
        self.circle = 0
        self.x_coordinate = 420
        self.y_coordinate = 420
        self.root.mainloop()

    def openfn(self):
        filename = filedialog.askopenfilename(title='open')
        return filename


    def open_img(self):
        x = self.openfn()
        self.res = plt.imread(x)
        self.img = Image.open(x)
        self.img = self.img.resize((720, 720), Image.ANTIALIAS)
        self.img.save("Photo.jpg")
        self.res = plt.imread("Photo.jpg")
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)
        # panel = Label(self.root, image=self.img)
        # panel.image = self.img
        # panel.place(x = 60, y = 30)

    def inv(self):
        new_res = self.res.copy()
        img_wigth = new_res.shape[0]
        img_higth = new_res.shape[1]
        new_res = inversion(new_res, self.res, img_wigth, img_higth,
                            self.inversion_radius, self.x_coordinate, self.y_coordinate)
        self.res = new_res

        new_image = Image.fromarray(new_res)
        self.img = ImageTk.PhotoImage(new_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)

    def motion(self, event):
        x, y = event.x + 3, event.y + 7
        self.canvas.delete(self.circle)

        x_max = x + self.radius
        x_min = x - self.radius
        y_max = y + self.radius
        y_min = y - self.radius
        self.circle = self.canvas.create_oval(
            x_max, y_max, x_min, y_min, outline="black")

    def on_click(self, event):
        try:
            self.canvas.delete(point)
        except:
            pass

        self.x_coordinate = event.y
        self.y_coordinate = event.x

        self.inv()

        point = self.canvas.create_oval(
            event.x+2, event.y+2, event.x-2, event.y-2, outline="#8B0000", fill="#8B0000")

    def change_inversion_radius(self, event):
        if event.delta == 120:
            self.radius = self.radius + 20
            self.inversion_radius = self.radius
            self.motion(event)
        if event.delta == -120:
            self.radius = self.radius - 20
            self.inversion_radius = self.radius
            self.motion(event)

    def reset_photo(self):
        self.img = Image.open("Photo.jpg")
        self.res = plt.imread("Photo.jpg")
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)

    def save_photo(self):
        img_to_save = Image.fromarray(self.res)
        img_to_save.save("Photo_" + str(datetime.datetime.now().time()).split(".")[0].replace(":", "_")+".jpg")

app = App()
