import customtkinter
import tkinter
from tkinter import ttk

class Main_window(customtkinter.CTk):
    def __init__(self,window_resolution):
        super().__init__()
        self.__window_resolution = self.set_resolution(window_resolution)
        self.geometry(self.__window_resolution)
        self.configure(fg_color = "#a564df")
        self.minsize(640,480)
        self.maxsize(1920,1080)

        self.add_background(self, 1000, 500, "#0e0f11",8, "#625b9f", 6)
    @staticmethod
    def is_resolution(resolution):
        parts = resolution.split('x')
        if len(parts) != 2:
            return False
        try:
            x = int(parts[0].strip())
            y = int(parts[1].strip())
            return True
        except ValueError:
            return False

    def set_resolution(self, window_resolution):
        if self.is_resolution(window_resolution):
            self.__window_resolution = window_resolution
        else :
            print("This is not resolution")
    
    def add_background(self,node, width, height, color, border_width, border_color, corner_radius):
        background = customtkinter.CTkFrame(
            master = node,
            width=width,
            height= height,
            fg_color=color,
            border_width=border_width,
            border_color=border_color,
            corner_radius=corner_radius)
        background.place(
            anchor = "c",
            relx =.5,
            rely =.5,
            relwidth = 1.1,
            relheight = .85)