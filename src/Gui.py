import customtkinter
import os

class Main_Window(customtkinter.CTk):
    def __init__(self,window_resolution, ):
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
        
class SourceList_Menu(Main_Window):
    def __init__(self, window_resolution):
        super().__init__(window_resolution=window_resolution)
        self.__window_resolution = window_resolution
        self.__main_color = "#a564df"
        self.__second_color = "#625b9f"
        self.__backgrouund_color = "#0e0f11"
        self.__fonts_path ="~/Документы/Учеба/3 семестр/Open Source/GitUpdChecky/UpdChecky/ttf-fonts"
        
        __title_text = "Welcome to UpdChecky"
        self.title = customtkinter.CTkLabel(
        master=self,
        text=__title_text,
        text_color=self.__main_color,
        fg_color=self.__backgrouund_color,
        font=self.create_font("Hikasami-Bold.ttf", "Hikasami", 36, "bold"))
        self.title.place(anchor = "c", relx = 0.5, rely = 0.3)

        __explane_text = "Select source from that you downloaded programs."
        self.explane = customtkinter.CTkLabel(
        master=self,
        text=__explane_text,
        text_color=self.__second_color,
        fg_color=self.__backgrouund_color,
        font=self.create_font("Hikasami-Regular.ttf", "Hikasami", 14, "bold"))
        self.explane.place(anchor = "c", relx = 0.5, rely = 0.45)

    def get_fonts_path(self):
        return self.__fonts_path
        
    def create_font(self, font_family_file, font_family, font_size, font_weight = "normal"):
        """Импортирует шрифт из файла ttf или otf в проект.
            font_family_file - название файла шрифта
            font_family -название шрифта в программе
            font_size - размер кегля шрифта
            font_weight - жирность шрифта (Bold, Normal)
        """
        font = os.path.expanduser(self.get_fonts_path())
        font = os.path.join(font, font_family_file)
            
        try:
            customtkinter.FontManager.load_font(font)

            title_font = customtkinter.CTkFont(
                family = font_family,
                size = font_size,
                weight=font_weight)
            return title_font
        except Exception as ex:
            print(f"Предупреждение: Не удалось загрузить шрифт {font_family_file} с помощью FontManager: {ex}")
            return customtkinter.CTkFont(family="Arial", size=font_size, weight=font_weight)