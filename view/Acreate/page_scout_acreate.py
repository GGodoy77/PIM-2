from customtkinter import *
import view.Acreate.page_acreate as tela_criar
import view.Login.page_login as tela_login
from tkinter import messagebox
import re
import json
import os
import service.security as security
import uuid

class PoliticaPrivacidade(CTkToplevel):
    def __init__(self, master, filename, title):
        super().__init__(master)
        self.title(title)
        self.geometry("600x500")
        self.transient(master) 
        self.grab_set() 

        CTkLabel(self, text=title, font=CTkFont(size=20, weight="bold")).pack(pady=10)
        self.text_area = CTkTextbox(self, wrap="word", width=550, height=350,state="disabled",fg_color="gray20",text_color="white",font=CTkFont(size=14))
        self.text_area.pack(pady=10)

        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_area.configure(state="normal")
            self.text_area.insert("end", content)
            self.text_area.configure(state="disabled")
        except FileNotFoundError:
            self.text_area.configure(state="normal")
            self.text_area.insert("end", f"Erro: Arquivo '{filename}' não encontrado.")
            self.text_area.configure(state="disabled")
        except Exception as e:
            self.text_area.configure(state="normal")
            self.text_area.insert("end", f"Erro ao carregar o arquivo: {e}")
            self.text_area.configure(state="disabled")

        CTkButton(self, text="Fechar", command=self.destroy, fg_color='black', width=100).pack(pady=10)

class TermosCondicoes(CTkToplevel):
    def __init__(self, master, filename, title):
        super().__init__(master)
        self.title(title)
        self.geometry("600x500")
        self.transient(master) 
        self.grab_set() 

        CTkLabel(self, text=title, font=CTkFont(size=20, weight="bold")).pack(pady=10)
        self.text_area = CTkTextbox(self, wrap="word", width=550, height=350,state="disabled",fg_color="gray20",text_color="white",font=CTkFont(size=14))
        self.text_area.pack(pady=10)

        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_area.configure(state="normal")
            self.text_area.insert("end", content)
            self.text_area.configure(state="disabled")
        except FileNotFoundError:
            self.text_area.configure(state="normal")
            self.text_area.insert("end", f"Erro: Arquivo '{filename}' não encontrado.")
            self.text_area.configure(state="disabled")
        except Exception as e:
            self.text_area.configure(state="normal")
            self.text_area.insert("end", f"Erro ao carregar o arquivo: {e}")
            self.text_area.configure(state="disabled")

        CTkButton(self, text="Fechar", command=self.destroy, fg_color='black', width=100).pack(pady=10)

class ScoutAcreate(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        CTkLabel(self, text="Crie a sua conta", font=CTkFont(size=50, weight="bold")).pack(pady=(50, 20))

        form = CTkFrame(self, corner_radius=10, width=350, height=800)
        form.pack(pady=(50,80))
        form.pack_propagate(False)

        CTkLabel(form, text='Usuário', font=CTkFont(size=16)).pack(pady=(30, 1))
        self.entry_usuario=CTkEntry(form, placeholder_text="Digite seu nome de Usuário", fg_color='white', text_color='black',width=250)
        self.entry_usuario.pack(pady=10)

        CTkLabel(form, text='Email', font=CTkFont(size=16)).pack(pady=(10, 1))
        self.entry_email=CTkEntry(form, placeholder_text="Digite seu email", fg_color='white',text_color='black',width=250)
        self.entry_email.pack(pady=10)

        CTkLabel(form, text='Confirmar Email', font=CTkFont(size=16)).pack(pady=(10, 1))
        self.entry_confirmar_email=CTkEntry(form, placeholder_text="Confirme o seu email", fg_color='white',text_color='black',width=250)
        self.entry_confirmar_email.pack(pady=10)

        CTkLabel(form, text='Senha', font=CTkFont(size=16)).pack(pady=(10, 1))
        self.entry_senha=CTkEntry(form, placeholder_text="Digite sua senha", fg_color='white',text_color='black',width=250)
        self.entry_senha.pack(pady=10)

        CTkLabel(form, text='Confirmar Senha', font=CTkFont(size=16)).pack(pady=(10, 1))
        self.entry_confirmar_senha=CTkEntry(form, placeholder_text="Confirme a sua senha", fg_color='white',text_color='black',width=250)
        self.entry_confirmar_senha.pack(pady=10)

        self.checkbox_termos = CTkCheckBox(form, text="Eu li e concordo com os Termos e Condições", font=CTkFont(size=13))
        self.checkbox_termos.pack(pady=(10,0))
        CTkButton(form, text="Leia aqui", font=CTkFont(size=12, underline=True),fg_color="transparent", text_color="white", hover_color="gray", command=lambda: self.abrir_termos_condicoes("terms.txt", "Termos e Condições")).pack(padx=5)

        self.checkbox_politicas = CTkCheckBox(form, text="Eu li e concordo com as Políticas de Privacidade", font=CTkFont(size=13))
        self.checkbox_politicas.pack(pady=(10,0))
        CTkButton(form, text="Leia aqui", font=CTkFont(size=12, underline=True),fg_color="transparent", text_color="white", hover_color="gray", command=lambda: self.abrir_politicas("politica_privacidade.txt", "Políticas de Privacidade")).pack(padx=5)

        CTkButton(form, text="Cadastrar", font=CTkFont(size=18), width=200, height=40, fg_color='black',command=self.cadastrar).pack(pady=20)
        CTkButton(form, text="Voltar", font=CTkFont(size=18), width=150, height=35, fg_color='red',command=self.voltar).pack(pady=(5, 30))

    def voltar(self):
        self.destroy()
        tela_criar.Acreate(self.master).pack(fill='both', expand=True)

    def abrir_termos_condicoes(self, filename, title):
        TermosCondicoes(self.master, filename, title)

    def abrir_politicas(self, filename, title):
        PoliticaPrivacidade(self.master, filename, title)

    def senha_valida(self, senha):
        letras=re.search(r"[a-z]", senha)
        maiusculas=re.search(r"[A-Z]", senha)
        numeros=re.search(r"[0-9]", senha)
        especiais=re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha)

        return (len(senha) >= 4 and letras and maiusculas and numeros and especiais)

    def email_valido(email):
        padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if re.match(padrao, email):
            return True
        else:
            return False

    def gerar_id(self):
        return str(uuid.uuid4())[:8]

    def cadastrar(self):
        self.nome = self.entry_usuario.get()
        self.email = self.entry_email.get()
        self.senha = self.entry_senha.get()
        self.confirmemail = self.entry_confirmar_email.get()
        self.confirmsenha = self.entry_confirmar_senha.get()

        if not self.email or not self.confirmemail or not self.senha or not self.confirmsenha or not self.nome:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        elif not re.match(self.email_valido, self.email):
            messagebox.showerror("Erro", "Formato de E-mail inválido.")
        elif self.email != self.confirmemail:
            messagebox.showerror("Erro", "O seu email não coincide com a confirmação")
        elif self.senha != self.confirmsenha:
            messagebox.showerror("Erro", "A sua senha não coincide com a confirmação")
        elif not self.senha_valida(self.senha):
            messagebox.showerror("Erro", "A senha deve conter pelo menos 4 letras, uma letra maiúscula, um caractere especial, e um número! \nObs:Os caracteres especiais não contarão como letras!")
        elif not self.checkbox_termos.get():
            messagebox.showerror("Erro", "Você deve aceitar os Termos e Condições para criar a conta.")
        elif not self.checkbox_politicas.get():
            messagebox.showerror("Erro", "Você deve aceitar as Políticas de Privacidade para criar a conta.")
        else:
            self.dados={}
            if os.path.exists("scouts.json"):
                with open("scouts.json", "r") as f:
                    self.dados=json.load(f)

            for usuario in self.dados.values():
                try:
                    email_decrip = security.descriptografar_dados(usuario['email'])
                except Exception: 
                    email_decrip = usuario['email'] 
                    
                if usuario['nome']==self.nome: 
                    messagebox.showerror("Erro", "Nome de usuário já existente")
                    return
            
                if email_decrip == self.email:
                    messagebox.showerror("Erro", "Email já cadastrado")
                    return
            
            email_crip = security.criptografar_dados(self.email)
            senha_hash = security.hash_senha(self.senha)

            id_anonimo = self.gerar_id()
            self.dados[id_anonimo] = {
                "nome": self.nome,
                "email": email_crip,
                "senha": senha_hash
            }

            with open("scouts.json", "w") as f:
                json.dump(self.dados, f, indent=4)
            messagebox.showinfo("Aviso", f"Cadastro realizado!\nNome de Usuário: {self.nome}")
            self.destroy()
            tela_login.Login(self.master).pack(fill='both', expand=True)