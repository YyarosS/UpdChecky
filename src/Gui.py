from Settings import Settings  as set
import customtkinter
from tkinter import ttk 
import os

class Background(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        #self.__window_resolution(self.is_resolution(window_resolution))
        #self.geometry(self.__window_resolution)
        self.configure(fg_color = "#a564df")
        self.minsize(800,600)
        self.maxsize(1920,1080)
        self.add_background(self, 1000, 500,"#0e0f11", 8,"#625b9f", 6)
    
    def add_background(self,node, width, height, color, border_width, border_color, corner_radius):
        """Создание заднего фона"""
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
          
class Main_Window(Background):
    def __init__(self):
        super().__init__()
        self.main_color = "#a564df"
        self.second_color = "#625b9f"
        self.background_color = "#0e0f11"
        self.forground_color = "#c89bf3"
        self._set_scaled_min_max()
        self.__fonts_path ="~/Документы/Учеба/3 семестр/Open Source/GitUpdChecky/UpdChecky/ttf-fonts"
        

        __title_text = "Welcome to UpdChecky"
        __title = customtkinter.CTkLabel(
            master=self,
            text=__title_text,
            text_color=self.main_color,
            fg_color=self.background_color,
            font=self.create_font(
                "Hikasami-Bold.ttf",
                "Hikasami",
                36,
                "bold"))
        __title.place(
            anchor = "c",
            relx = 0.5,
            rely = 0.3)

        __explane_text = "Select source from that you downloaded programs."
        __explane = customtkinter.CTkLabel(
            master=self,
            text=__explane_text,
            text_color=self.second_color,
            fg_color=self.background_color,
            font=self.create_font(
                "Hikasami-Regular.ttf",
                "Hikasami",
                15,
                "bold"))
        __explane.place(
            anchor = "c",
            relx = 0.5,
            rely = 0.45)

        source_list = customtkinter.CTkFrame(
            master=self,
            corner_radius=15,
            border_width=6,
            border_color = self.second_color,
            fg_color= self.main_color,
            bg_color= self.background_color)
        source_list.place(
            anchor = 'c',
            relx = 0.5,
            rely = 0.65,
            relwidth = 0.45,
            relheight = 0.3,)
        
        first_name = "From the package manager"
        second_name = "Flatpak"
        third_name = "Snap"
        first_source = Source_Item(self,source_list, first_name, 0.2)
        second_source = Source_Item(self, source_list, second_name, 0.5)
        third_source = Source_Item(self, source_list, third_name,  0.8)
        sources = [first_source, second_source, third_source]

        ok_btn = customtkinter.CTkButton(
            self,
            font= self.create_font("Hikasami-Medium.ttf","Hikasami",18),
            command=lambda: self.change_warframe(sources=sources),
            bg_color= self.background_color,
            border_color= self.main_color,
            text_color= self.second_color,
            fg_color= "transparent",
            corner_radius=20,
            border_width= 1,
            width=115,
            height=40,
            text='ok')
        ok_btn.place(anchor='se', relx= 0.92, rely= 0.885)

    def create_font(self, font_family_file, font_family, font_size, font_weight = "normal"):
        """Импортирует шрифт из файла ttf или otf в проект.
            font_family_file - название файла шрифта
            font_family -название шрифта в программе
            font_size - размер кегля шрифта
            font_weight - жирность шрифта (Bold, Normal)
        """
        font = os.path.expanduser(self.__fonts_path)
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
            return customtkinter.CTkFont(
                family="Arial",
                size=font_size,
                weight=font_weight)
        
    def change_warframe(self, sources):
        """Смена начального окна, на главное"""
        selected_sources= self.check_selected_sources(sources)
        self.save_sources(selected_sources)
        

    def check_selected_sources(self, sources):
        """Проверка, какой источник был выбран и возврат его имени"""
        selected_sources = []
        for source in sources:
            if (source.is_selected()):
                selected_sources.append(source.get_source_text())
        return selected_sources
    
    def save_sources(self, sources):
        if (len(sources) != 0):
            for source in sources:
                set.selected_source_list = source
                set.selected_source_list
        else:
            error_window = customtkinter.CTkToplevel(self)
            error_window.geometry("400x150")
            error_window.title("Ошибка ввода источников")
            error_massage = customtkinter.CTkLabel(
                error_window,
                text="Выбери хотя бы один источник!",
                fg_color= self.background_color,
                text_color= self.second_color,
                font= self.create_font(
                    "Hikasami-Medium.ttf",
                    "Hikasami",
                    22,
                    "bold"))
            error_massage.place(
                anchor= 'c',
                relx=0.5,
                rely=0.4,
                relwidth=1,
                relheight=1)
    
class Source_Item(Main_Window):
    def  __init__(self,main_root,root_item, source_name, height):
        """Это конструктор класса Source_Item, целькоторого добавть на экран пункт для выбора.
        Для создания экземпляра нужны следующие аргументы: 
        - ```main_root```(главный корневой элемент, который создает окно)
        - ```root_item```(корневой элемент списока куда добавляется элемент списка)
        - ```source_name```(текст пункта)
        - ```height```(ширина пункта, сколько места он будет занимать в списке)"""
        self.__checkbox_background = customtkinter.CTkFrame(
            root_item,
            fg_color= main_root.forground_color,
            corner_radius=15)
        self.__checkbox_background.place(
            relwidth= 0.9,
            relheight= 0.25,
            relx= 0.5,
            rely= height,
            anchor= 'c')

        self.__source_name = customtkinter.CTkLabel(
            self.__checkbox_background,
            text=source_name,
            text_color=main_root.background_color,
            fg_color=main_root.forground_color,
            font= main_root.create_font(
                "SUSEMono-Medium.ttf",
                "SUSEMono",
                16,
                "bold"))
        self.__source_name.place(
            anchor='c',
            relx=0.45,
            rely =0.5)

        self.__source_box = customtkinter.CTkCheckBox(
            self.__checkbox_background,
            checkmark_color=main_root.background_color,
            fg_color= main_root.second_color,
            corner_radius= 15,
            offvalue="off",
            onvalue="on",
            text="")
        self.__source_box.place(
            relwidth = 0.1,
            relheight = 0.8,
            relx= 0.95,
            rely= 0.5,
            anchor = 'e')
        
    def is_selected(self):
        """Проверка является ли виджет CTkChcekBox активным"""
        if (self.__source_box.get() == "on"): 
            return True
        else:
            return False
    
    def get_source_text(self):
        """Возвращение значения источника установки программ"""
        return self.__source_name.cget("text")