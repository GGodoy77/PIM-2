from customtkinter import *
import view.Login.page_login as tela_login
import view.Account_Pages.page_scout_mainpage as tela_scout
from tkinter import messagebox
import json
import os
import service.security as security

class ScoutLogin(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        CTkLabel(self, text="Entre na sua conta", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        form = CTkFrame(self, corner_radius=10, width=350, height=370)
        form.pack(pady=(50,80))
        form.pack_propagate(False)

        CTkLabel(form, text='Email', font=CTkFont(size=16)).pack(pady=(30, 1))
        self.entry_email = CTkEntry(form, placeholder_text="Digite seu Email", fg_color='white',text_color='black',width=250)
        self.entry_email.pack(pady=10)

        CTkLabel(form, text='Senha', font=CTkFont(size=16)).pack(pady=(10, 1))

        senha_frame = CTkFrame(form, fg_color="transparent")
        senha_frame.pack(pady=10)

        self.entry_senha = CTkEntry(senha_frame, placeholder_text="Digite sua senha", fg_color='white',text_color='black',width=210, show='*') 
        self.entry_senha.pack(side="left", padx=(0, 5))

        btn_ver_senha = CTkButton(senha_frame, text="👁️", width=30, height=30, command=self.senha_ver)
        btn_ver_senha.pack(side="right", padx=(5, 0))

        CTkButton(form, text='Entrar', font=CTkFont(size=18), width=200, height=40, fg_color='black', command=self.validar).pack(pady=20)
        CTkButton(form, text='Voltar', font=CTkFont(size=18), width=200, height=40, fg_color='red', command=self.voltar_login).pack(pady=10)

    def senha_ver(self):
        if self.entry_senha:
            current_show = self.entry_senha.cget("show")
            if current_show == "*":
                self.entry_senha.configure(show="")
            else:
                self.entry_senha.configure(show="*")

    def voltar_login(self):
        self.destroy()
        tela_login.Login(self.master).pack(fill='both',expand=True)

    def conta_scout(self, dados_usuario):
        self.destroy()
        tela_scout.ScoutMainpage(self.master, dados_usuario).pack(fill='both',expand=True)

    def validar(self):
        self.email=self.entry_email.get()
        self.senha=self.entry_senha.get()

        if not self.email or not self.senha:
            messagebox.showerror("Erro", "Preenhcha todos os campos")
            return
        
        if os.path.exists("scouts.json"):
            with open("scouts.json", "r") as f:
                self.dados = json.load(f)

            self.user_found = False
            for scout_id, info in self.dados.items():
                try:
                    email_decrip = security.descriptografar_dados(info['email'])
                except Exception:
                    email_decrip = info['email'] 

                if email_decrip == self.email and security.verificar_senha(self.senha, info['senha']):
                    
                    dados_sessao = {
                        "nome": info['nome'],
                        "email": email_decrip,
                        "scout_id": scout_id
                    }
                    messagebox.showinfo("Aviso", "Login bem Sucedido!")
                    self.conta_scout(dados_sessao)
                    self.user_found = True
                    break
                
            if not self.user_found:
                messagebox.showerror("Erro", "Usuário ou senha incorretos!")
                
        else:
            messagebox.showerror("Erro", "Nenhum usuário cadasrado no momento")
