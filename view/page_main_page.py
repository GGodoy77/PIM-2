from customtkinter import *
import view.Acreate.page_acreate as tela_criar
import view.Login.page_login as tela_login
class MainPage(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.navbar = CTkFrame(self, height=60, fg_color="gray")
        self.navbar.pack(fill="x", side="top")

        CTkLabel(self.navbar, text="Plataforma de interação - Crie sua conta e se junte á comunidade!", font=CTkFont(size=20, weight="bold"), text_color="white").pack(pady=15)

        CTkLabel(self, text="Página Inicial", font=CTkFont(size=50, weight="bold")).pack(pady=(150, 20))
        CTkLabel(self, text="Bem-vindo!", font=CTkFont(size=20)).pack(pady=(40,10))

        form = CTkFrame(self, corner_radius=10, width=350, height=320)
        form.pack(pady=(50,80))
        form.pack_propagate(False)

        CTkLabel(form, text="Escolha uma opção", font=CTkFont(size=24, weight="bold")).pack(pady=(40, 30))

        CTkButton(form, text="Criar conta", font=CTkFont(size=18), width=200, height=40, fg_color='black',command=self.abriar_criar_conta).pack(pady=10)
        CTkButton(form, text="Login", font=CTkFont(size=18), width=200, height=40, fg_color='black', command=self.abrir_logar_conta).pack(pady=10)
        CTkButton(form, text="Sair", font=CTkFont(size=18), width=150, height=35, fg_color='red', command=exit).pack(pady=(20,10))

    def abriar_criar_conta(self):
        self.destroy()
        tela_criar.Acreate(self.master).pack(fill='both', expand=True)
    
    def abrir_logar_conta(self):
        self.destroy()
        tela_login.Login(self.master).pack(fill='both', expand=True)