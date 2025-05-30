from customtkinter import *
import view.Account_Pages.page_player_logout_confirmation as tela_deslogar
import view.Login.page_login as tela_login
from tkinter import messagebox
import os
import json
import re
import service.security as security
import datetime

class PlayerMainpage(CTkFrame):
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
        self.btn_convites = CTkButton(menu_lateral, text="Meus Convites", command=self.mostrar_convites, fg_color='black', width=100, height=50)
        self.btn_convites.pack(pady=20, fill='x', padx=10)
        self.update_notificacao_convite() 
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

        frame_info = CTkScrollableFrame(self.area_conteudo, corner_radius=10, width=500, height=300)
        frame_info.pack(pady=20)

        CTkLabel(frame_info, text="Informações do Jogador", font=CTkFont(size=20)).pack(pady=20)
        CTkLabel(frame_info, text=f"Email: {self.dados_usuario.get('email')}", font=CTkFont(size=16)).pack(pady=5)

        CTkLabel(frame_info, text="Times em que você está:", font=CTkFont(size=16)).pack(pady=(20, 5))

        id_sessao = self.dados_usuario.get('player_id')

        if not id_sessao:
            CTkLabel(frame_info, text="Erro: ID do jogador não encontrado.", text_color="red").pack()
            return

        if not os.path.exists("teams.json"):
            CTkLabel(frame_info, text="Arquivo teams.json não encontrado.", text_color="red").pack()
            return

        with open("teams.json", "r") as f:
            times = json.load(f)

        encontrou_time = False

        for team_id, team_info in times.items():
            jogadores = team_info.get("jogadores", {})
            if id_sessao in jogadores:
                team_name = team_info.get("nome", "Nome Desconhecido")
                CTkLabel(frame_info, text=f"- {team_name}").pack(pady=2)
                encontrou_time = True

        if not encontrou_time:
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

    def mostrar_excluir_conta(self):
        self.limpar_conteudo()
        CTkLabel(self.area_conteudo, text="Excluir Perfil do Jogador", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        frame_excluir = CTkFrame(self.area_conteudo, corner_radius=10, width=500, height=300)
        frame_excluir.pack(pady=20)
        frame_excluir.pack_propagate(False)

        CTkLabel(frame_excluir, text="Deseja mesmo excluir sua conta?", font=CTkFont(size=18)).pack(pady=(80, 20))

        botoes_frame = CTkFrame(frame_excluir, fg_color="transparent")
        botoes_frame.pack(pady=30)

        CTkButton(botoes_frame, text='Sim', width=120, command=self.confirmar_exclusao).pack(side="left", padx=20)
        CTkButton(botoes_frame, text='Não', width=120, command=self.mostrar_informacoes).pack(side="left", padx=20)

    def confirmar_exclusao(self):
        id_jogador_deletar = self.dados_usuario.get('player_id')
        if not id_jogador_deletar:
            messagebox.showerror("Erro", "Erro ao excluir: ID do jogador não encontrado nos dados da sessão.")
            return

        if os.path.exists("players.json"):
            with open("players.json", "r") as f:
                dados_players = json.load(f)

            if id_jogador_deletar in dados_players:
                del dados_players[id_jogador_deletar]
                with open("players.json", "w") as f:
                    json.dump(dados_players, f, indent=4)
                messagebox.showinfo("Sucesso", "Sua conta foi excluída.")
            else:
                messagebox.showerror("Erro", "Sua conta não foi encontrada no arquivo de jogadores.")
                return
        else:
            messagebox.showerror("Erro", "Arquivo players.json não encontrado.")
            return

        if os.path.exists("teams.json"):
            with open("teams.json", "r") as f:
                dados_teams = json.load(f)

            for id_time, time_info in dados_teams.items():
                if "jogadores" in time_info and id_jogador_deletar in time_info["jogadores"]:
                    del time_info["jogadores"][id_jogador_deletar]

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
        id_jogador = self.dados_usuario.get('player_id')

        if not id_jogador:
            messagebox.showerror("Erro", "ID do jogador não encontrado nos dados da sessão. Faça login novamente.")
            return
        if not novo_nome:
            messagebox.showerror("Erro", "Por favor, digite um nome válido.")
            return
        if novo_nome == self.dados_usuario.get('nome'):
            messagebox.showinfo("Informação", "O novo nome é igual ao nome atual.")
            return

        if os.path.exists("players.json"):
            with open("players.json", "r") as f:
                dados_jogador = json.load(f)

            for p_id, p_info in dados_jogador.items():
                if p_id != id_jogador and p_info.get('nome') == novo_nome:
                    messagebox.showerror("Erro", "Este nome de usuário já está em uso.")
                    return
        else:
            messagebox.showerror("Erro", "Arquivo players.json não encontrado.")
            return

        if id_jogador in dados_jogador:
            dados_jogador[id_jogador]['nome'] = novo_nome
            with open("players.json", "w") as f:
                json.dump(dados_jogador, f, indent=4)
        else:
            messagebox.showerror("Erro", "Dados do jogador não encontrados em players.json.")
            return

        self.dados_usuario['nome'] = novo_nome

        if os.path.exists("teams.json"):
            with open("teams.json", "r") as f:
                dados_time = json.load(f)

            for id_time, time_info in dados_time.items():
                if "jogadores" in time_info and id_jogador in time_info["jogadores"]:
                    time_info["jogadores"][id_jogador]["nome"] = novo_nome 
            
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
        id_jogador = self.dados_usuario.get('player_id')
        email_sessao = self.dados_usuario.get('email')

        if not id_jogador:
            messagebox.showerror("Erro", "ID do jogador não encontrado nos dados da sessão. Faça login novamente.")
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
            players_data = json.load(f)

        player_info = players_data.get(id_jogador)
        if not player_info:
            messagebox.showerror("Erro", "Dados do jogador não encontrados em players.json.")
            return

        if not security.verificar_senha(senha_confirmacao, player_info.get('senha')):
            messagebox.showerror("Erro", "Senha atual incorreta.")
            return

        for p_id, p_info in players_data.items():
            try:
                p_email_decrip = security.descriptografar_dados(p_info.get('email'))
            except Exception:
                p_email_decrip = p_info.get('email')

            if p_id != id_jogador and p_email_decrip == novo_email:
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


        players_data[id_jogador]['email'] = security.criptografar_dados(novo_email)
        with open("players.json", "w") as f:
            json.dump(players_data, f, indent=4)

        self.dados_usuario['email'] = novo_email

        if os.path.exists("teams.json"):
            with open("teams.json", "r") as f:
                teams_data_for_update = json.load(f)

            for team_id_update, team_info_update in teams_data_for_update.items():
                if "jogadores" in team_info_update and id_jogador in team_info_update["jogadores"]:
                    team_info_update["jogadores"][id_jogador]["email"] = security.criptografar_dados(novo_email)
            
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

        CTkButton(frame_mudar_senha, text='Salvar senha', font=CTkFont(size=18), width=200, height=40, fg_color='black', command=self.confirmar_mudar_senha).pack(pady=20)
        CTkButton(frame_mudar_senha, text='Voltar', font=CTkFont(size=18), width=200, height=40, fg_color='black', command=self.mostrar_editar).pack(pady=10)

    def confirmar_mudar_senha(self):
        senha_atual = self.entry_senha_atual.get().strip()
        nova_senha = self.entry_nova_senha.get().strip()
        confirmar_nova_senha = self.entry_confirmar_nova_senha.get().strip()
        id_jogador = self.dados_usuario.get("player_id")

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

        if not id_jogador:
            messagebox.showerror("Erro", "ID do jogador não encontrado na sessão. Faça login novamente.")
            return

        if not os.path.exists("players.json"):
            messagebox.showerror("Erro", "Arquivo players.json não encontrado.")
            return

        with open("players.json", "r") as f:
            players_data = json.load(f)

        dados_player_atual = players_data.get(id_jogador)
        if not dados_player_atual:
            messagebox.showerror("Erro", "Seu jogador não foi encontrado no arquivo de jogadores.")
            return

        senha_hash_armazenada = dados_player_atual.get("senha")
        if not security.verificar_senha(senha_atual, senha_hash_armazenada):
            messagebox.showerror("Erro", "Senha atual incorreta.")
            return
        
        nova_senha_hash = security.hash_senha(nova_senha)
        players_data[id_jogador]["senha"] = nova_senha_hash

        with open("players.json", "w") as f:
            json.dump(players_data, f, indent=4)
        
        messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")
        self.mostrar_informacoes()

    def update_notificacao_convite(self):
        id_jogador = self.dados_usuario.get("player_id")
        if not id_jogador:
            return

        if not os.path.exists("players.json"):
            return

        try:
            with open("players.json", "r") as f:
                dados_jogadores = json.load(f)

            info_jogador = dados_jogadores.get(id_jogador)
            if not info_jogador or "convites" not in info_jogador:
                self.btn_convites.configure(text="Meus Convites", fg_color="black")
                return

            convites = info_jogador.get("convites", {})
            pendentes = sum(1 for convite in convites.values() if convite.get("status") == "pendente")

            if pendentes > 0:
                self.btn_convites.configure(text=f"Meus Convites ({pendentes})", fg_color="red")
            else:
                self.btn_convites.configure(text="Meus Convites", fg_color="black")

        except Exception as e:
            print(f"Erro ao atualizar notificação de convites: {e}")

    def mostrar_convites(self):
        for widget in self.area_conteudo.winfo_children():
            widget.destroy()

        CTkLabel(self.area_conteudo, text="Convites", font=CTkFont(size=24, weight="bold")).pack(pady=20)

        player_id = self.dados_usuario.get("player_id")
        if not player_id:
            CTkLabel(self.area_conteudo, text="ID do jogador não encontrado. Faça login novamente.", font=CTkFont(size=14)).pack()
            return

        if not os.path.exists("players.json"):
            CTkLabel(self.area_conteudo, text="Arquivo players.json não encontrado.", font=CTkFont(size=14)).pack()
            return

        try:
            with open("players.json", "r") as pf:
                players_data = json.load(pf)
        except json.JSONDecodeError:
            CTkLabel(self.area_conteudo, text="Erro ao ler players.json. Arquivo corrompido.", font=CTkFont(size=14)).pack()
            return

        player_info = players_data.get(player_id)
        if not player_info:
            CTkLabel(self.area_conteudo, text="Suas informações de jogador não foram encontradas.", font=CTkFont(size=14)).pack()
            return

        convites_pendentes = {
            sender_id: invite_info for sender_id, invite_info in player_info.get("convites", {}).items()
            if invite_info.get("status") == "pendente"
        }

        if not convites_pendentes:
            CTkLabel(self.area_conteudo, text="Nenhum convite pendente.", font=CTkFont(size=16)).pack(pady=20)
            return

        for sender_id, invite_info in convites_pendentes.items():
            # Retrieve the specific fields as stored in players.json
            tipo_convite = invite_info.get("tipo", "desconhecido")
            remetente = invite_info.get("remetente", "Desconhecido")
            data = invite_info.get("data", "Sem data") # Use "data" as primary, no "tempo" fallback if you stick to "data"

            # Specific for team invites
            nome_time_convite = invite_info.get("nome_time", None) # Get the specific team name from the invite data
            id_time_convite = invite_info.get("id_time", sender_id) # Get the specific team ID from the invite data, fallback to sender_id if somehow missing

            invite_frame = CTkFrame(self.area_conteudo, corner_radius=10, width=500)
            invite_frame.pack(pady=10, padx=20, fill='x')

            if tipo_convite == "time":
                # Ensure the sender_id is indeed the team_id
                if id_time_convite != sender_id:
                    # This implies a structural issue in how invites are keyed.
                    # For now, we'll assume sender_id is the team_id.
                    pass 

                display_remetente = nome_time_convite if nome_time_convite else remetente
                texto_convite = f"Convite para o Time: {display_remetente}"
                
                CTkLabel(invite_frame, text=texto_convite, font=CTkFont(size=18, weight="bold")).pack(pady=(10, 5), anchor='w', padx=10)
                CTkLabel(invite_frame, text=f"Enviado em: {data}", font=CTkFont(size=12)).pack(pady=(0, 5), anchor='w', padx=10)
                
                CTkButton(invite_frame, text="Aceitar Convite", fg_color='green',
                          command=lambda s_id=sender_id, t_name=nome_time_convite: self.aceitar_convite_time(s_id, t_name)).pack(pady=5, padx=10)
                CTkButton(invite_frame, text="Recusar Convite", fg_color='red',
                          command=lambda s_id=sender_id: self.recusar_convite(s_id)).pack(pady=5, padx=10)
            
            elif tipo_convite == "recrutador":
                CTkLabel(invite_frame, text=f"Convite de Recrutador: {remetente}", font=CTkFont(size=18, weight="bold")).pack(pady=(10, 5), anchor='w', padx=10)
                CTkLabel(invite_frame, text=f"Enviado em: {data}", font=CTkFont(size=12)).pack(pady=(0, 5), anchor='w', padx=10)
                CTkButton(invite_frame, text="Aceitar Convite (Recrutador)", fg_color='blue',
                          command=lambda s_id=sender_id, s_name=remetente: self.aceitar_convite_scout(s_id, s_name)).pack(pady=5, padx=10)
                CTkButton(invite_frame, text="Recusar Convite", fg_color='red',
                          command=lambda s_id=sender_id: self.recusar_convite(s_id)).pack(pady=5, padx=10)
            else:
                CTkLabel(invite_frame, text=f"Convite Desconhecido de: {remetente}", font=CTkFont(size=18, weight="bold")).pack(pady=(10, 5), anchor='w', padx=10)

        self.update_notificacao_convite()

    def aceitar_convite_time(self, sender_id, team_name):
        player_id = self.dados_usuario.get("player_id")

        if not player_id:
            messagebox.showerror("Erro", "ID do jogador não encontrado na sessão.")
            return

        if not os.path.exists("players.json") or not os.path.exists("teams.json"):
            messagebox.showerror("Erro", "Arquivos players.json ou teams.json não encontrados.")
            return

        try:
            with open("players.json", "r") as pf:
                players_data = json.load(pf)
            with open("teams.json", "r") as tf:
                teams_data = json.load(tf)

            player_info = players_data.get(player_id)
            team_info = teams_data.get(sender_id)

            if not player_info:
                messagebox.showerror("Erro", "Informações do jogador não encontradas.")
                return

            if not team_info:
                messagebox.showerror("Erro", "Time do convite não encontrado.")
                return

            # Verifica se já é membro
            if player_id in team_info.get("jogadores", {}):
                messagebox.showinfo("Informação", "Você já faz parte deste time.")
            else:
                # Adiciona no time
                if "jogadores" not in team_info:
                    team_info["jogadores"] = {}

                team_info["jogadores"][player_id] = {
                    "nome": player_info.get("nome"),
                    "email": player_info.get("email")
                }

                player_info["time_id"] = sender_id
                player_info["nome_time"] = team_info.get("nome")

            # Atualiza convite
            if "convites" in player_info and sender_id in player_info["convites"]:
                player_info["convites"][sender_id]["status"] = "aceito"

            with open("players.json", "w") as pf:
                json.dump(players_data, pf, indent=4)

            with open("teams.json", "w") as tf:
                json.dump(teams_data, tf, indent=4)

            messagebox.showinfo("Sucesso", f"Você entrou no time {team_name}!")
            self.mostrar_convites()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aceitar convite do time: {e}")

    def aceitar_convite_scout(self, scout_id_convite, scout_name):
        player_id = self.dados_usuario.get("player_id")

        if not player_id:
            messagebox.showerror("Erro", "ID do jogador não encontrado na sessão.")
            return

        if not os.path.exists("players.json"):
            messagebox.showerror("Erro", "Arquivo players.json não encontrado.")
            return

        try:
            with open("players.json", "r") as pf:
                players_data = json.load(pf)

            player_info = players_data.get(player_id)
            if not player_info:
                messagebox.showerror("Erro", "Seu jogador não foi encontrado.")
                return

            if "convites" in player_info and scout_id_convite in player_info["convites"]:
                player_info["convites"][scout_id_convite]["status"] = "aceito"
            else:
                messagebox.showerror("Erro", "Convite de recrutador não encontrado ou já aceito/recusado.")
                return

            with open("players.json", "w") as pf:
                json.dump(players_data, pf, indent=4)

            messagebox.showinfo("Sucesso", f"Você aceitou o interesse do recrutador {scout_name}!")
            self.mostrar_convites()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aceitar convite de recrutador: {e}")

    def recusar_convite(self, sender_id):
        player_id = self.dados_usuario.get("player_id")

        if not player_id:
            messagebox.showerror("Erro", "ID do jogador não encontrado na sessão.")
            return

        if not os.path.exists("players.json"):
            messagebox.showerror("Erro", "Arquivo players.json não encontrado.")
            return

        try:
            with open("players.json", "r") as pf:
                players_data = json.load(pf)

            player_info = players_data.get(player_id)
            if not player_info:
                messagebox.showerror("Erro", "Seu jogador não foi encontrado.")
                return

            if "convites" in player_info and sender_id in player_info["convites"]:
                player_info["convites"][sender_id]["status"] = "recusado"
            else:
                messagebox.showerror("Erro", "Convite não encontrado ou já processado.")
                return

            with open("players.json", "w") as pf:
                json.dump(players_data, pf, indent=4)

            messagebox.showinfo("Informação", "Convite recusado.")
            self.mostrar_convites()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao recusar convite: {e}")

    def deslogar(self):
        self.destroy()
        tela_deslogar.Logout(self.master, self.dados_usuario).pack(fill='both', expand=True)