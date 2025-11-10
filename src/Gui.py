import tkinter
import customtkinter

class Welcome_window(customtkinter.CTk):
    def __init__(self,window_resolution):
        super().__init__()
        self.__window_resolution = self.set_resolution(window_resolution)
        self.geometry(self.__window_resolution)
        self.minsize(640,480)
        self.maxsize(1920,1080)


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

    def get_resolution(self):
        return self.__window_resolution