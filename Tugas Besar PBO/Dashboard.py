import tkinter as tk
from tkinter import Menu, messagebox, NONE
from PIL import Image, ImageTk
from frmlogin import *
from frmmhs import *

class Dashboard:
    def __init__(self):
        # root window
        self.root = tk.Tk()
        self.root.title('Menu Demo')
        self.root.geometry("900x400")
        self.__data = None
        self.__level = None

        # Menambahkan gambar ke background
        image = Image.open("gambar/download.jpg")  # Ganti path dengan path file gambar Anda

        # Menyesuaikan ukuran gambar
        width, height = 900, 500  # Ganti sesuai dengan ukuran yang Anda inginkan
        image = image.resize((width, height))

        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.root, image=photo)
        label.image = photo
        label.pack()

        # Menyesuaikan desain warna
        self.root.configure(bg='yellow')  # Warna latar belakang

        # create a menubar
        self.menubar = Menu(self.root, bg='#4CAF50', fg='white')  # Warna latar belakang dan teks
        self.root.config(menu=self.menubar)

        # create menus
        self.file_menu = Menu(self.menubar, tearoff=0, bg='#4CAF50', fg='white')  # Warna latar belakang dan teks
        self.guest_menu = Menu(self.menubar, tearoff=0, bg='#4CAF50', fg='white')  # Warna latar belakang dan teks
        self.admin_menu = Menu(self.menubar, tearoff=0, bg='#4CAF50', fg='white')  # Warna latar belakang dan teks
        self.mahasiswa_menu = Menu(self.menubar, tearoff=0, bg='#4CAF50', fg='white')  # Warna latar belakang dan teks
        self.dosen_menu = Menu(self.menubar, tearoff=0, bg='#4CAF50', fg='white')  # Warna latar belakang dan teks

        # add menu items to File menu
        self.file_menu.add_command(label='Sign Up', command=lambda: self.new_window("Log Me In"))
        self.file_menu.add_command(label='Login', command=lambda: self.new_window("Log Me In", FormLogin))
        self.file_menu.add_command(label='Exit', command=self.root.destroy)

        # add menu items to menu Dosen
        self.dosen_menu.add_command(label='Dosen', command=lambda: self.new_window("Data Mahasiswa dan Matakuliah", Formmatakuliah))

        # add menus to the menubar
        self.menubar.add_cascade(label="File", menu=self.file_menu)

    def new_window(self, number, _class):
        new = tk.Toplevel(self.root)
        new.transient()
        new.grab_set()
        _class(new, number, self.update_main_window)

    def update_main_window(self, data):
        # Method to receive data from child windows
        self.__data = data
        level = self.__data[0]
        loginvalid = self.__data[1]
        if(loginvalid==True):
            index = self.file_menu.index('Login')
            # hapus menu login
            self.file_menu.delete(index)
            self.file_menu.add_command(label='Logout', command=self.Logout)

            # tambahkan menu sesuai level
            if(level=='admin'): 
                self.menubar.add_cascade(label="Admin", menu=self.admin_menu)
                self.__level = 'Admin'
            elif(level=='mahasiswa'): 
                self.menubar.add_cascade(label="Mahasiswa", menu=self.mahasiswa_menu)
                self.__level = 'Mahasiswa'
            elif(level=='dosen'):
                self.menubar.add_cascade(label="Dosen", menu=self.dosen_menu)
                self.__level = 'Dosen'
            else:
                pass

    def Logout(self):
        index = self.file_menu.index('Logout')
        self.file_menu.delete(index)
        self.file_menu.add_command(label='Login', command=lambda: self.new_window("Log Me In", FormLogin))
        self.remove_all_menus()

    def remove_all_menus(self):
        index = self.menubar.index(self.__level)
        if index is not None:
            self.menubar.delete(index)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    menu_app = Dashboard()
    menu_app.run()
