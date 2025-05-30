from customtkinter import set_appearance_mode
from view.page_main_page import MainPage
from customtkinter import *

if __name__ == "__main__":
    set_appearance_mode("dark")
    root = CTk()
    root.title("Sistema")
    root.after(0, lambda:root.state('zoomed'))
    MainPage(root).pack(fill='both', expand=True)
    root.mainloop()