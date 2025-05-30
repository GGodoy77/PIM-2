from customtkinter import *
import view.Account_Pages.page_scout_logout_confirmation as tela_deslogar
import view.Login.page_login as tela_login
from tkinter import messagebox
import os
import json
import re
import service.security as security
import datetime

class ScoutMainpage(CTkFrame):
    def __init__(self, master, dados_usuario):
        super().__init__(master)
        self.dados_usuario = dados_usuario

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        menu_lateral = CTkFrame(self, width=900, fg_color="#3f3f3f")
        menu_lateral.grid(row=0, column=0, sticky="ns")
        menu_lateral.grid_propagate(False)

        CTkLabel(menu_lateral, text="Menu", font=CTkFont(size=20, weight="bold")).pack(pady=(150, 150))

        CTkButton(menu_lateral, text="Informações", command=self.mostrar_informacoes, fg_color='black', width=100, height=50).pack(pady=20, fill='x', padx=10)
        CTkButton(menu_lateral, text="Editar Perfil", command=self.mostrar_editar, fg_color='black', width=100, height=50).pack(pady=20, fill='x', padx=10)
        CTkButton(menu_lateral, text="Entrar em um Time", command=self.entrar_em_time, fg_color='black', width=100, height=50).pack(pady=20, fill='x', padx=10)
        CTkButton(menu_lateral, text="Pesquisar Jogadores", command=self.pesquisar_jogadores_globais, fg_color='black', width=100, height=50).pack(pady=20, fill='x', padx=10)
        CTkButton(menu_lateral, text="Sair da Conta", command=self.deslogar, fg_color='red', width=60, height=30).pack(pady=20, fill='x', padx=10)

        self.area_conteudo = CTkScrollableFrame(self)
        self.area_conteudo.grid(row=0, column=1, sticky="nsew")

        self.mostrar_informacoes()

    def limpar_conteudo(self):
        for widget in self.area_conteudo.winfo_children():
            widget.destroy()

    def mostrar_informacoes(self):
        self.limpar_conteudo()

        CTkLabel(self.area_conteudo, text=f"Bem-vindo, {self.dados_usuario.get('nome')}", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        frame_info = CTkScrollableFrame(self.area_conteudo, corner_radius=10, width=500, height=500)
        frame_info.pack(pady=20)

        CTkLabel(frame_info, text="Informações do Recrutador", font=CTkFont(size=20)).pack(pady=20)
        CTkLabel(frame_info, text=f"Email: {self.dados_usuario.get('email')}", font=CTkFont(size=16)).pack(pady=5)

        CTkLabel(frame_info, text="Times em que você está:", font=CTkFont(size=16)).pack(pady=(20, 5))

        id_sessao = self.dados_usuario.get('scout_id')
        if not id_sessao:
            CTkLabel(frame_info, text="Erro: ID do recrutador não encontrado nos dados da sessão.", text_color="red").pack()
            return

        if not os.path.exists("teams.json"):
            CTkLabel(frame_info, text="Nenhum time cadastrado no sistema (teams.json não encontrado).", text_color="gray").pack()
            return

        with open("teams.json", "r") as f:
            times = json.load(f)

        time = False
        for team_id, team_info in times.items(): 
            if "recrutadores" in team_info:
                if id_sessao in team_info["recrutadores"]:
                    team_name = team_info.get("nome", "Nome Desconhecido") 
                    CTkLabel(frame_info, text=f"- {team_name}").pack(pady=2)
                    time = True
        if not time:
            CTkLabel(frame_info, text="Você não está em nenhum time.", text_color="gray").pack()

    def mostrar_editar(self):
        self.limpar_conteudo()
        CTkLabel(self.area_conteudo, text="Editar Perfil", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        frame_editar = CTkFrame(self.area_conteudo, corner_radius=10, width=500, height=300)
        frame_editar.pack(pady=20)
        frame_editar.pack_propagate(False)

        CTkLabel(frame_editar, text="Escolha uma opção para editar", font=CTkFont(size=18)).pack(pady=20)

        CTkButton(frame_editar, text='Mudar Nome', command=self.mostrar_mudar_nome, font=CTkFont(size=16), fg_color='black').pack(pady=10)
        CTkButton(frame_editar, text='Mudar Email', command=self.mostrar_mudar_email, font=CTkFont(size=16), fg_color='black').pack(pady=10)
        CTkButton(frame_editar, text='Mudar Senha', command=self.mostrar_mudar_senha, font=CTkFont(size=16), fg_color='black').pack(pady=10)
        CTkButton(frame_editar, text='Excluir Conta', font=CTkFont(size=16), fg_color='black', command=self.mostrar_excluir_conta).pack(pady=10)

    def entrar_em_time(self):
        self.limpar_conteudo()
        CTkLabel(self.area_conteudo, text="Entrar em um Time", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        frame_entrar_time = CTkFrame(self.area_conteudo, corner_radius=10, width=500, height=300)
        frame_entrar_time.pack(pady=20)
        frame_entrar_time.pack_propagate(False)

        CTkLabel(frame_entrar_time, text='Digite o token do time:', font=CTkFont(size=16)).pack(pady=(60, 1))
        self.entry_token_time = CTkEntry(frame_entrar_time, placeholder_text="Token do Time", fg_color='white', text_color='black', width=250)
        self.entry_token_time.pack(pady=10)

        CTkButton(frame_entrar_time, text='Entrar no Time', font=CTkFont(size=18), width=200, height=40, fg_color='black', command=self.adicionar_ao_time).pack(pady=20)

    def adicionar_ao_time(self):
        token_digitado = self.entry_token_time.get().strip()
        email_recrutador = self.dados_usuario.get('email')
        nome_recrutador = self.dados_usuario.get('nome')
        id_recrutador = self.dados_usuario.get('scout_id')

        if not id_recrutador:
            messagebox.showerror("Erro", "ID do recrutador não encontrado nos dados da sessão. Faça login novamente.")
            return

        if not token_digitado:
            messagebox.showerror("Erro", "Por favor, digite o token do time.")
            return

        if not os.path.exists("teams.json"):
            messagebox.showerror("Erro", "Arquivo teams.json não encontrado.")
            return

        with open("teams.json", "r") as f:
            dados_times = json.load(f)

        time_encontrado = False
        for team_id, team_info in dados_times.items():
            if "token_recrutadores" in team_info:
                try:
                    token_decrip = security.descriptografar_dados(team_info["token_recrutadores"])
                except Exception:
                    token_decrip = team_info["token_recrutadores"]

                if token_decrip == token_digitado:
                    time_encontrado = True
                    if "recrutadores" not in team_info:
                        team_info["recrutadores"] = {}

                    if id_recrutador in team_info["recrutadores"]:
                        messagebox.showinfo("Aviso", f"Você já está no time '{team_info['nome']}'.")
                        return

                    team_info["recrutadores"][id_recrutador] = {
                        "nome": nome_recrutador,
                        "email": security.criptografar_dados(email_recrutador)
                    }
                    messagebox.showinfo("Sucesso", f"Você entrou para o time '{team_info['nome']}'!")
                    break 
        if not time_encontrado:
            messagebox.showerror("Erro", "Token de time inválido ou time não encontrado.")
            return

        with open("teams.json", "w") as f:
            json.dump(dados_times, f, indent=4)

        self.mostrar_informacoes()

    def confirmar_sair_time(self):
        token_digitado = self.entry_token_sair.get().strip()
        scout_id = self.dados_usuario.get('scout_id')
        email_recrutador = self.dados_usuario.get('email')

        if not scout_id:
            messagebox.showerror("Erro", "ID do recrutador não encontrado nos dados da sessão. Faça login novamente.")
            return

        if not token_digitado:
            messagebox.showerror("Erro", "Por favor, digite o token do time.")
            return

        if not os.path.exists("teams.json"):
            messagebox.showerror("Erro", "Arquivo teams.json não encontrado.")
            return

        with open("teams.json", "r") as f:
            dados_times = json.load(f)

        time_encontrado = False
        recrutador_removido = False
        for team_id, team_info in dados_times.items():
            if "token" in team_info:
                try:
                    token_decrip = security.descriptografar_dados(team_info["token"])
                except Exception:
                    token_decrip = team_info["token"]

                if token_decrip == token_digitado:
                    time_encontrado = True
                    if "recrutadores" in team_info:
                        if scout_id in team_info["recrutadores"]:
                            del team_info["recrutadores"][scout_id]
                            messagebox.showinfo("Sucesso", f"Você foi removido do time '{team_info['nome']}'.")
                            recrutador_removido = True
                        else:
                            messagebox.showinfo("Aviso", f"Você não está no time '{team_info['nome']}'.")
                        break

        if not time_encontrado:
            messagebox.showerror("Erro", "Token de time inválido ou time não encontrado.")
        elif not recrutador_removido and time_encontrado:
            messagebox.showinfo("Aviso", "Você não estava neste time.")

        with open("teams.json", "w") as f:
            json.dump(dados_times, f, indent=4)

        self.mostrar_informacoes()

    def mostrar_excluir_conta(self):
        self.limpar_conteudo()
        CTkLabel(self.area_conteudo, text="Excluir Perfil do Recrutador", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        frame_excluir = CTkFrame(self.area_conteudo, corner_radius=10, width=500, height=300)
        frame_excluir.pack(pady=20)
        frame_excluir.pack_propagate(False)

        CTkLabel(frame_excluir, text="Deseja mesmo excluir sua conta?", font=CTkFont(size=18)).pack(pady=(80, 20))

        botoes_frame = CTkFrame(frame_excluir, fg_color="transparent")
        botoes_frame.pack(pady=30)

        CTkButton(botoes_frame, text='Sim', width=120, command=self.confirmar_exclusao).pack(side="left", padx=20)
        CTkButton(botoes_frame, text='Não', width=120, command=self.mostrar_informacoes).pack(side="left", padx=20)

    def confirmar_exclusao(self):
        id_recrutador_deletar = self.dados_usuario.get('scout_id')
        if not id_recrutador_deletar:
            messagebox.showerror("Erro", "Erro ao excluir: ID do recrutador não encontrado nos dados da sessão.")
            return

        if os.path.exists("scouts.json"):
            with open("scouts.json", "r") as f:
                dados_recrutadores = json.load(f)

            if id_recrutador_deletar in dados_recrutadores:
                del dados_recrutadores[id_recrutador_deletar]
                with open("scouts.json", "w") as f:
                    json.dump(dados_recrutadores, f, indent=4)
                messagebox.showinfo("Sucesso", "Sua conta foi excluída.")
            else:
                messagebox.showerror("Erro", "Sua conta não foi encontrada no arquivo de recrutadores.")
                return
        else:
            messagebox.showerror("Erro", "Arquivo players.json não encontrado.")
            return

        if os.path.exists("teams.json"):
            with open("teams.json", "r") as f:
                dados_teams = json.load(f)

            for id_time, time_info in dados_teams.items():
                if "recrutadores" in time_info and id_recrutador_deletar in time_info["recrutadores"]:
                    del time_info["recrutadores"][id_recrutador_deletar]

            with open("teams.json", "w") as f:
                json.dump(dados_teams, f, indent=4)

        self.destroy()
        tela_login.Login(self.master).pack(fill='both', expand=True)

    def mostrar_mudar_nome(self):
        self.limpar_conteudo()
        CTkLabel(self.area_conteudo, text="Mudar Nome", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        frame_mudar_nome = CTkFrame(self.area_conteudo, corner_radius=10, width=500, height=300)
        frame_mudar_nome.pack(pady=20)
        frame_mudar_nome.pack_propagate(False)

        CTkLabel(frame_mudar_nome, text='Novo Nome:', font=CTkFont(size=16)).pack(pady=(30, 1))
        self.entry_novo_nome = CTkEntry(frame_mudar_nome, placeholder_text="Digite o novo nome de usuário", fg_color='white', text_color='black', width=250)
        self.entry_novo_nome.pack(pady=10)
        self.entry_novo_nome.insert(0, self.dados_usuario.get('nome', ''))

        CTkButton(frame_mudar_nome, text='Salvar Nome', font=CTkFont(size=18), width=200, height=40, fg_color='black', command=self.confirmar_mudar_nome).pack(pady=20)
        CTkButton(frame_mudar_nome, text='Voltar', font=CTkFont(size=18), width=200, height=40, fg_color='black', command=self.mostrar_editar).pack(pady=10)

    def confirmar_mudar_nome(self):
        novo_nome = self.entry_novo_nome.get().strip()
        id_recrutador = self.dados_usuario.get('scout_id')

        if not id_recrutador:
            messagebox.showerror("Erro", "ID do recrutador não encontrado nos dados da sessão. Faça login novamente.")
            return
        if not novo_nome:
            messagebox.showerror("Erro", "Por favor, digite um nome válido.")
            return
        if novo_nome == self.dados_usuario.get('nome'):
            messagebox.showinfo("Informação", "O novo nome é igual ao nome atual.")
            return

        if os.path.exists("scouts.json"):
            with open("scouts.json", "r") as f:
                dados_recrutador = json.load(f)

            for r_id, r_info in dados_recrutador.items():
                if r_id != id_recrutador and r_info.get('nome') == novo_nome:
                    messagebox.showerror("Erro", "Este nome de usuário já está em uso.")
                    return
        else:
            messagebox.showerror("Erro", "Arquivo scouts.json não encontrado.")
            return

        if id_recrutador in dados_recrutador:
            dados_recrutador[id_recrutador]['nome'] = novo_nome
            with open("scouts.json", "w") as f:
                json.dump(dados_recrutador, f, indent=4)
        else:
            messagebox.showerror("Erro", "Dados do jogador não encontrados em scouts.json.")
            return

        self.dados_usuario['nome'] = novo_nome

        if os.path.exists("teams.json"):
            with open("teams.json", "r") as f:
                dados_time = json.load(f)

            for id_time, time_info in dados_time.items():
                if "recrutadores" in time_info and id_recrutador in time_info["recrutadores"]:
                    time_info["recrutadores"][id_recrutador]["nome"] = novo_nome 
            
            with open("teams.json", "w") as f:
                json.dump(dados_time, f, indent=4)

        messagebox.showinfo("Sucesso", "Nome atualizado com sucesso!")
        self.mostrar_informacoes()

    def mostrar_mudar_email(self):
        self.limpar_conteudo()
        CTkLabel(self.area_conteudo, text="Mudar Email", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        frame_mudar_email = CTkFrame(self.area_conteudo, corner_radius=10, width=500, height=400)
        frame_mudar_email.pack(pady=20)
        frame_mudar_email.pack_propagate(False)

        CTkLabel(frame_mudar_email, text='Novo Email:', font=CTkFont(size=16)).pack(pady=(30, 1))
        self.entry_novo_email = CTkEntry(frame_mudar_email, placeholder_text="Digite o novo email", fg_color='white', text_color='black', width=250)
        self.entry_novo_email.pack(pady=10)
        self.entry_novo_email.insert(0, self.dados_usuario.get('email', ''))

        CTkLabel(frame_mudar_email, text='Confirme sua Senha:', font=CTkFont(size=16)).pack(pady=(10, 1))
        self.entry_senha_confirmacao = CTkEntry(frame_mudar_email, placeholder_text="Digite sua senha atual", show="*", fg_color='white', text_color='black', width=250)
        self.entry_senha_confirmacao.pack(pady=10)

        CTkButton(frame_mudar_email, text='Salvar Email', font=CTkFont(size=18), width=200, height=40, fg_color='black', command=self.confirmar_mudar_email).pack(pady=20)
        CTkButton(frame_mudar_email, text='Voltar', font=CTkFont(size=18), width=200, height=40, fg_color='black', command=self.mostrar_editar).pack(pady=10)

    def confirmar_mudar_email(self):
        novo_email = self.entry_novo_email.get().strip()
        senha_confirmacao = self.entry_senha_confirmacao.get().strip()
        id_recrutador = self.dados_usuario.get('scout_id')
        email_sessao = self.dados_usuario.get('email')

        if not id_recrutador:
            messagebox.showerror("Erro", "ID do recrutador não encontrado nos dados da sessão. Faça login novamente.")
            return
        if not novo_email or not senha_confirmacao:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
        if novo_email == email_sessao:
            messagebox.showinfo("Informação", "O novo email é igual ao email atual.")
            return
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", novo_email):
            messagebox.showerror("Erro", "Formato de email inválido.")
            return

        if not os.path.exists("players.json"):
            messagebox.showerror("Erro", "Arquivo players.json não encontrado.")
            return

        with open("players.json", "r") as f:
            dados_recrutador = json.load(f)

        recrutador_info = dados_recrutador.get(id_recrutador)
        if not recrutador_info:
            messagebox.showerror("Erro", "Dados do jogador não encontrados em players.json.")
            return

        if not security.verificar_senha(senha_confirmacao, recrutador_info.get('senha')):
            messagebox.showerror("Erro", "Senha atual incorreta.")
            return

        for p_id, p_info in dados_recrutador.items():
            try:
                p_email_decrip = security.descriptografar_dados(p_info.get('email'))
            except Exception:
                p_email_decrip = p_info.get('email')

            if p_id != id_recrutador and p_email_decrip == novo_email:
                messagebox.showerror("Erro", "Este email já está cadastrado para outro jogador.")
                return

        if os.path.exists("teams.json"):
            with open("teams.json", "r") as f:
                teams_data = json.load(f)
            for team_id_iter, team_info_iter in teams_data.items():
                try:
                    team_email_decrip = security.descriptografar_dados(team_info_iter.get('email'))
                except Exception:
                    team_email_decrip = team_info_iter.get('email')
                if team_email_decrip == novo_email:
                    messagebox.showerror("Erro", "Este email já está cadastrado para um time.")
                    return


        dados_recrutador[id_recrutador]['email'] = security.criptografar_dados(novo_email)
        with open("players.json", "w") as f:
            json.dump(dados_recrutador, f, indent=4)

        self.dados_usuario['email'] = novo_email

        if os.path.exists("teams.json"):
            with open("teams.json", "r") as f:
                teams_data_for_update = json.load(f)

            for team_id_update, team_info_update in teams_data_for_update.items():
                if "recrutadores" in team_info_update and id_recrutador in team_info_update["recrutadores"]:
                    team_info_update["recrutadores"][id_recrutador]["email"] = security.criptografar_dados(novo_email)
            
            with open("teams.json", "w") as f:
                json.dump(teams_data_for_update, f, indent=4)

        messagebox.showinfo("Sucesso", "Email atualizado com sucesso!")
        self.mostrar_informacoes()

    def mostrar_mudar_senha(self):
        self.limpar_conteudo()
        CTkLabel(self.area_conteudo, text="Mudar Senha", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        frame_mudar_senha = CTkFrame(self.area_conteudo, corner_radius=10, width=500, height=450)
        frame_mudar_senha.pack(pady=20)
        frame_mudar_senha.pack_propagate(False)

        CTkLabel(frame_mudar_senha, text='Senha Atual:', font=CTkFont(size=16)).pack(pady=(30, 1))
        self.entry_senha_atual = CTkEntry(frame_mudar_senha, placeholder_text="Digite sua senha atual", show="*", fg_color='white', text_color='black', width=250)
        self.entry_senha_atual.pack(pady=10)

        CTkLabel(frame_mudar_senha, text='Nova Senha:', font=CTkFont(size=16)).pack(pady=(10, 1))
        self.entry_nova_senha = CTkEntry(frame_mudar_senha, placeholder_text="Digite sua nova senha", show="*", fg_color='white', text_color='black', width=250)
        self.entry_nova_senha.pack(pady=10)

        CTkLabel(frame_mudar_senha, text='Confirmar Nova Senha:', font=CTkFont(size=16)).pack(pady=(10, 1))
        self.entry_confirmar_nova_senha = CTkEntry(frame_mudar_senha, placeholder_text="Confirme sua nova senha", show="*", fg_color='white', text_color='black', width=250)
        self.entry_confirmar_nova_senha.pack(pady=10)

        CTkButton(frame_mudar_senha, text='Confirmar Mudança', font=CTkFont(size=18), width=200, height=40, fg_color='black', command=self.confirmar_mudar_senha).pack(pady=20)
        CTkButton(frame_mudar_senha, text='Voltar', font=CTkFont(size=18), width=200, height=40, fg_color='black', command=self.mostrar_informacoes).pack(pady=10)

    def confirmar_mudar_senha(self):
        senha_atual = self.entry_senha_atual.get().strip()
        nova_senha = self.entry_nova_senha.get().strip()
        confirmar_nova_senha = self.entry_confirmar_nova_senha.get().strip()
        id_recrutador = self.dados_usuario.get("scout_id")

        if not senha_atual or not nova_senha or not confirmar_nova_senha:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        if nova_senha != confirmar_nova_senha:
            messagebox.showerror("Erro", "A nova senha e a confirmação não coincidem.")
            return

        if len(nova_senha) < 4:
            messagebox.showerror("Erro", "A nova senha deve ter no mínimo 4 caracteres.")
            return
        if not re.search(r"[a-z]", nova_senha):
            messagebox.showerror("Erro", "A nova senha deve conter pelo menos uma letra minúscula.")
            return
        if not re.search(r"[A-Z]", nova_senha):
            messagebox.showerror("Erro", "A nova senha deve conter pelo menos uma letra maiúscula.")
            return
        if not re.search(r"[0-9]", nova_senha):
            messagebox.showerror("Erro", "A nova senha deve conter pelo menos um número.")
            return
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", nova_senha):
            messagebox.showerror("Erro", "A nova senha deve conter pelo menos um caractere especial.")
            return

        if not id_recrutador:
            messagebox.showerror("Erro", "ID do jogador não encontrado na sessão. Faça login novamente.")
            return

        if not os.path.exists("scouts.json"):
            messagebox.showerror("Erro", "Arquivo scouts.json não encontrado.")
            return

        with open("scouts.json", "r") as f:
            dados_recrutador = json.load(f)

        dados_recrutador_atual = dados_recrutador.get(id_recrutador)
        if not dados_recrutador_atual:
            messagebox.showerror("Erro", "Seu jogador não foi encontrado no arquivo de recrutadores.")
            return

        senha_hash_armazenada = dados_recrutador_atual.get("senha")
        if not security.verificar_senha(senha_atual, senha_hash_armazenada):
            messagebox.showerror("Erro", "Senha atual incorreta.")
            return
        
        nova_senha_hash = security.hash_senha(nova_senha)
        dados_recrutador[id_recrutador]["senha"] = nova_senha_hash

        with open("scouts.json", "w") as f:
            json.dump(dados_recrutador, f, indent=4)
        
        messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")
        self.mostrar_informacoes()

    def convidar_jogador(self, id_jogador, nome_jogador):
        id_recrutador = self.dados_usuario.get("scout_id")
        nome_recrutador = self.dados_usuario.get("nome")

        if not id_recrutador or not nome_recrutador:
            messagebox.showerror("Erro", "Dados do recrutador não encontrados na sessão. Faça login novamente.")
            return

        if not os.path.exists("players.json"):
            messagebox.showerror("Erro", "Arquivo players.json não encontrado.")
            return

        try:
            with open("players.json", "r") as f:
                dados_jogadores = json.load(f)

            if id_jogador not in dados_jogadores:
                messagebox.showerror("Erro", "Jogador não encontrado.")
                return

            info_jogadores = dados_jogadores[id_jogador]

            if "convites" not in info_jogadores:
                info_jogadores["convites"] = {}

            if id_recrutador in info_jogadores["convites"] and info_jogadores["convites"][id_recrutador].get("tipo") == "recrutador" and info_jogadores["convites"][id_recrutador].get("status") == "pendente":
                messagebox.showinfo("Informação", f"Convite de recrutador para {nome_jogador} já foi enviado e está pendente.")
                return

            tempo_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            info_jogadores["convites"][id_recrutador] = {
                "tipo": "recrutador",
                "remetente": nome_recrutador,
                "status": "pendente",
                "data": tempo_atual
            }

            with open("players.json", "w") as f:
                json.dump(dados_jogadores, f, indent=4)

            messagebox.showinfo("Sucesso", f"Convite de recrutador enviado para {nome_jogador}!")
            self.executar_pesquisa_global()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao enviar convite: {e}")

    def pesquisar_jogadores_globais(self):
        self.limpar_conteudo()

        CTkLabel(self.area_conteudo, text="Pesquisar Jogadores (Global)", font=CTkFont(size=50, weight="bold")).pack(
            pady=(200, 20))

        frame_procurar = CTkFrame(self.area_conteudo, width=500, height=500, corner_radius=10)
        frame_procurar.pack(pady=20)
        frame_procurar.pack_propagate(False)

        CTkLabel(frame_procurar, text="Buscar Todos os Jogadores da Plataforma", font=CTkFont(size=20, weight="bold")).pack(pady=(20, 10))

        CTkLabel(frame_procurar, text="Digite o nome ou e-mail do jogador:").pack(pady=5)
        self.entry_busca_global = CTkEntry(frame_procurar, placeholder_text="Buscar jogador...", width=250)
        self.entry_busca_global.pack(pady=5)

        CTkButton(frame_procurar, text="Pesquisar", command=self.executar_pesquisa_global, fg_color='black').pack(pady=10)

        self.resultados_frame_global = CTkFrame(frame_procurar, corner_radius=10, width=400, height=280)
        self.resultados_frame_global.pack(pady=10)
        self.resultados_frame_global.pack_propagate(False)

    def executar_pesquisa_global(self):
        termo = self.entry_busca_global.get().strip().lower()

        for widget in self.resultados_frame_global.winfo_children():
            widget.destroy()

        if not termo:
            CTkLabel(self.resultados_frame_global, text="Digite algo para buscar.", text_color="red").pack()
            return

        if not os.path.exists("players.json"):
            CTkLabel(self.resultados_frame_global, text="Arquivo players.json não encontrado.", text_color="red").pack()
            return

        id_recrutador = self.dados_usuario.get("scout_id")
        nome_recrutador = self.dados_usuario.get("nome")
        if not id_recrutador or not nome_recrutador:
            messagebox.showerror("Erro", "Dados do recrutador não encontrados na sessão. Faça login novamente.")
            return

        # Determine o id_time e nome_time do recrutador atual, se houver
        self.id_time_do_recrutador = None
        self.nome_time_do_recrutador = None
        if os.path.exists("teams.json"):
            with open("teams.json", "r") as tf:
                dados_times = json.load(tf)
            for id_time, info_time in dados_times.items():
                if "recrutadores" in info_time and id_recrutador in info_time["recrutadores"]:
                    self.id_time_do_recrutador = id_time
                    self.nome_time_do_recrutador = info_time.get("nome", "Time Desconhecido")
                    break

        with open("players.json", "r") as f:
            dados_jogadores = json.load(f)

        encontrados = []
        for id_jogador, info in dados_jogadores.items():
            nome_jogador = info.get("nome", "").lower()
            try:
                email_jogador = security.descriptografar_dados(info.get("email")).lower()
            except Exception:
                email_jogador = info.get("email", "").lower()

            if termo in nome_jogador or termo in email_jogador:
                status_convite = "nenhum"
                # Verifica se há um convite pendente deste recrutador
                if "convites" in info and id_recrutador in info["convites"]:
                    if info["convites"][id_recrutador].get("tipo") == "convite_recrutador_time": # Tipo de convite de recrutador para time
                        status_convite = info["convites"][id_recrutador].get("status", "pendente")

                encontrados.append({
                    "id": id_jogador,
                    "nome": info.get("nome"),
                    "email": email_jogador,
                    "status_convite": status_convite,
                    "id_time_jogador": info.get("time_id") # Pega o time atual do jogador
                })

        if encontrados:
            for jogador in encontrados:
                frame_jogador = CTkFrame(self.resultados_frame_global, fg_color="transparent")
                frame_jogador.pack(pady=5, fill='x', padx=10)
                
                texto_jogador = f"Nome: {jogador['nome']}\nEmail: {jogador['email']}"
                # Opcionalmente, você pode exibir o time atual do jogador aqui
                # if jogador['id_time_jogador']:
                #     texto_jogador += f"\nTime: {jogador['id_time_jogador']}" 

                CTkLabel(frame_jogador, text=texto_jogador).pack(side='left', padx=5)

                if jogador['status_convite'] == "pendente":
                    CTkLabel(frame_jogador, text="Convite Pendente", text_color="orange").pack(side='right', padx=5)
                elif jogador['id_time_jogador'] is not None:
                    CTkLabel(frame_jogador, text="Já está em um time", text_color="gray").pack(side='right', padx=5)
                elif self.id_time_do_recrutador: # Mostra o botão de convite APENAS se o recrutador estiver em um time
                    CTkButton(frame_jogador, text="Convidar para o Time", fg_color='blue',
                               command=lambda p=jogador: self.convidar_jogador_scout(p['id'], p['nome'])).pack(side='right', padx=5)
                else:
                    CTkLabel(frame_jogador, text="Não pode convidar (não em time)", text_color="gray").pack(side='right', padx=5)
        else:
            CTkLabel(self.resultados_frame_global, text="Nenhum jogador encontrado.", text_color="gray").pack()

    def convidar_jogador_scout(self, id_jogador, nome_jogador):
        id_recrutador = self.dados_usuario.get("scout_id")
        nome_recrutador = self.dados_usuario.get("nome")

        if not id_recrutador or not nome_recrutador:
            messagebox.showerror("Erro", "Dados do recrutador não encontrados na sessão. Faça login novamente.")
            return
        
        id_time_do_recrutador = self.id_time_do_recrutador
        nome_time_do_recrutador = self.nome_time_do_recrutador

        if not id_time_do_recrutador: 
            messagebox.showerror("Permissão Negada", "Você só pode enviar convites de recrutador se estiver associado a um time.")
            self.executar_pesquisa_global() 
            return

        if not os.path.exists("players.json"):
            messagebox.showerror("Erro", "Arquivo players.json não encontrado.")
            return
        
        try:
            with open("players.json", "r") as f:
                dados_jogadores = json.load(f)
            with open("teams.json", "r") as tf:
                dados_times = json.load(tf)
        except FileNotFoundError:
            messagebox.showerror("Erro", "Um dos arquivos de dados (players.json ou teams.json) não foi encontrado.")
            return
        except json.JSONDecodeError:
            messagebox.showerror("Erro", "Erro ao ler dados dos arquivos JSON. Verifique a formatação.")
            return

        info_jogador = dados_jogadores.get(id_jogador)
        if not info_jogador:
            messagebox.showerror("Erro", "Jogador não encontrado.")
            return
        
        # Verifica se o jogador já está em um time
        if info_jogador.get("time_id") is not None:
            messagebox.showinfo("Informação", f"{nome_jogador} já está em um time. Não é possível enviar convite.")
            return
        
        # Verifica se o jogador já possui um convite pendente DESTE recrutador
        if "convites" not in info_jogador:
            info_jogador["convites"] = {}


        convite_existente_deste_time = False
        for id_convite_existente, detalhes_convite_existente in info_jogador["convites"].items():
            if (detalhes_convite_existente.get("tipo") == "time" and id_convite_existente == id_time_do_recrutador and detalhes_convite_existente.get("status") == "pendente") or \
               (detalhes_convite_existente.get("tipo") == "convite_recrutador_time" and detalhes_convite_existente.get("id_time") == id_time_do_recrutador and detalhes_convite_existente.get("status") == "pendente"):
                convite_existente_deste_time = True
                break

        if convite_existente_deste_time:
            messagebox.showinfo("Informação", f"Já existe um convite pendente para {nome_jogador} deste time.")
            return

        data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        info_jogador["convites"][id_recrutador] = {
            "tipo": "convite_recrutador_time",
            "remetente": nome_recrutador,
            "status": "pendente",
            "data": data_atual,
            "id_time": id_time_do_recrutador, 
            "nome_time": nome_time_do_recrutador 
        }

        with open("players.json", "w") as f:
            json.dump(dados_jogadores, f, indent=4)

        messagebox.showinfo("Sucesso", f"Convite enviado para {nome_jogador} para ingressar no time {nome_time_do_recrutador}!")
        self.executar_pesquisa_global()

    def deslogar(self):
        self.destroy()
        tela_deslogar.Logout(self.master, self.dados_usuario).pack(fill='both', expand=True)