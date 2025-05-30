from customtkinter import *
import view.page_main_page as tela_inical
import view.Account_Pages.page_player_mainpage as tela_voltar

class Logout(CTkFrame):
    def __init__(self, master, dados_usuario):
        super().__init__(master)
        self.dados_usuario= dados_usuario

        CTkLabel(self, text="Deseja Mesmo sair da Conta?", font=CTkFont(size=50, weight="bold")).pack(pady=(400, 20))

        botoes_frame = CTkFrame(self, fg_color="transparent")
        botoes_frame.pack(pady=30) 

        CTkButton(botoes_frame, text='Sim', command=self.sim, width=120, fg_color='green').pack(side="left", padx=20)
        CTkButton(botoes_frame, text='Não', command=self.nao, width=120, fg_color='red').pack(side="left", padx=20)

    def sim(self):
        self.destroy()
        tela_inical.MainPage(self.master).pack(fill='both', expand=True)

    def nao(self):
        self.destroy()
        tela_voltar.PlayerMainpage(self.master, self.dados_usuario).pack(fill='both', expand=True)
