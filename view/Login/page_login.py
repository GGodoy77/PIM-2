from customtkinter import *
import view.page_main_page as tela_incial
import view.Login.page_player_login as tela_login_player
import view.Login.page_team_login as tela_login_time
import view.Login.page_scout_login as tela_login_recrutador
class Login(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        CTkLabel(self, text="Entre na sua conta", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        form = CTkFrame(self, corner_radius=10, width=350, height=375)
        form.pack(pady=(50,80))
        form.pack_propagate(False)

        CTkLabel(form, text="Escolha uma opção", font=CTkFont(size=24, weight="bold")).pack(pady=30)

        CTkButton(form, text="Sou Jogador", font=CTkFont(size=18), width=200, height=40, fg_color='black',command=self.abrir_logar_player).pack(pady=10)
        CTkButton(form, text="Sou dono do time", font=CTkFont(size=18), width=200, height=40, fg_color='black',command=self.abrir_logar_time).pack(pady=10)
        CTkButton(form, text="Sou recrutador", font=CTkFont(size=18), width=200, height=40, fg_color='black',command=self.abrir_logar_recrutador).pack(pady=10)
        CTkButton(form, text="Voltar", font=CTkFont(size=18), width=150, height=35, fg_color='red',command=self.voltar).pack(pady=(20, 10))

    def voltar(self):
        self.destroy()
        tela_incial.MainPage(self.master).pack(fill='both', expand=True)

    def abrir_logar_player(self):
        self.destroy()
        tela_login_player.PlayerLogin(self.master).pack(fill='both', expand=True)

    def abrir_logar_time(self):
        self.destroy()
        tela_login_time.TeamLogin(self.master).pack(fill='both', expand=True)
    
    def abrir_logar_recrutador(self):
        self.destroy()
        tela_login_recrutador.ScoutLogin(self.master).pack(fill='both', expand=True)