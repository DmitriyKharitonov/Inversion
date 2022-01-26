from tkinter import *
from inversion_v2 import *
from PIL import ImageTk, Image
from tkinter import filedialog
import os


class App:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("840x840")
        self.root.resizable(width=True, height=True)
        self.btn = Button(self.root, text='open image',
                          command=self.open_img).place(x = 340, y = 0)
        self.btn2 = Button(self.root, text='inversion',
                           command=self.inv).place(x = 460, y = 0)
        self.res = 0
        self.root.mainloop()

    def openfn(self):
        filename = filedialog.askopenfilename(title='open')
        return filename

    def open_img(self):
        x = self.openfn()
        self.res = plt.imread(x)
        self.img = Image.open(x)
        self.img = self.img.resize((720, 720), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        panel = Label(self.root, image=self.img)
        panel.image = self.img
        panel.place(x = 60, y = 30)

    def inv(self):
        new_res = self.res.copy()
        wigth = new_res.shape[0]
        higth = new_res.shape[1]
        new_res = inversion(new_res, self.res, wigth, higth, 200, wigth/2, higth/2)
        self.res = new_res

        new_image = Image.fromarray(new_res)
        self.img = ImageTk.PhotoImage(new_image)
        panel = Label(self.root, image=self.img)
        panel.image = self.img
        panel.place(x = 60, y = 30)


app = App()
