from Gui import Main_window
import customtkinter
import tkinter
import os

def create_font():
    font_family = "Hikasami-Bold.ttf"
    project_path = "~/Документы/Учеба/3 семестр/Open Source/GitUpdChecky/UpdChecky"
    font_path = os.path.join(project_path, font_family)
    font_size = 36,
    font_weight= "Bold"
    try:
        title_font = customtkinter.CTkFont(
            family = font_family,
            size = font_size,
            weight=font_weight,
            file = font_path)
    except Exception as ex:
        print("Ошибка загрузки шрифта")
    return title_font

window_resolution = "800x600"

main_windows = Main_window(window_resolution)
main_windows.title("")

title_text = "Welcome to UpdChecky"
text_color = "#a564df"

title = customtkinter.CTkLabel(
    master=main_windows,
    text=title_text,
    text_color=text_color,
    font= create_font())
title.place(anchor = "c", relx = 0.5, rely = 0.3)

main_windows.mainloop()