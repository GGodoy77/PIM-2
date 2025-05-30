from customtkinter import *
import view.page_main_page as tela_inicial
import view.Acreate.page_player_acreate as tela_jogador
import view.Acreate.page_team_acreate as tela_time
import view.Acreate.page_scout_acreate as tela_recrutador

class Acreate(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        CTkLabel(self, text="Crie a sua conta", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        form = CTkFrame(self, corner_radius=10, width=350, height=375)
        form.pack(pady=(50,80))
        form.pack_propagate(False)

        CTkLabel(form, text="Escolha uma opção", font=CTkFont(size=24, weight="bold")).pack(pady=30)

        CTkButton(form, text="Sou Jogador", font=CTkFont(size=18), width=200, height=40, fg_color='black',command=self.abrir_criar_conta_player).pack(pady=10)
        CTkButton(form, text="Sou dono do time", font=CTkFont(size=18), width=200, height=40, fg_color='black',command=self.abrir_conta_time).pack(pady=10)
        CTkButton(form, text="Sou recrutador", font=CTkFont(size=18), width=200, height=40, fg_color='black',command=self.abrir_conta_recrutador).pack(pady=10)
        CTkButton(form, text="Voltar", font=CTkFont(size=18), width=150, height=35, fg_color='red',command=self.voltar).pack(pady=(20, 10))

    def voltar(self):
        self.destroy()
        tela_inicial.MainPage(self.master).pack(fill='both', expand=True)

    def abrir_criar_conta_player(self):
        self.destroy()
        tela_jogador.PlayerAcreate(self.master).pack(fill='both', expand=True)

    def abrir_conta_time(self):
        self.destroy()
        tela_time.TeamAcreate(self.master).pack(fill='both', expand=True)

    def abrir_conta_recrutador(self):
        self.destroy()
        tela_recrutador.ScoutAcreate(self.master).pack(fill='both', expand=True)