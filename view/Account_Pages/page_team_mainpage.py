from customtkinter import *
import view.Account_Pages.page_team_logout_confirmation as tela_voltar
import view.Login.page_login as tela_login
from tkinter import messagebox
import json
import re
import os
import datetime
import service.security as security
import uuid

class TeamMainpage(CTkFrame):
    def __init__(self, master, dados_usuario):
        super().__init__(master)
        self.dados_usuario=dados_usuario

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        menu_lateral = CTkFrame(self, width=700, fg_color="#3f3f3f")  
        menu_lateral.grid(row=0, column=0, sticky="ns")
        menu_lateral.grid_propagate(False)

        CTkLabel(menu_lateral, text="Menu", font=CTkFont(size=20, weight="bold")).pack(pady=(150, 150))

        CTkButton(menu_lateral, text="Informações", command=self.mostrar_informacoes, fg_color='black', width=100, height=50).pack(pady=10, fill='x', padx=10)
        CTkButton(menu_lateral, text="Token Recrutador", command=self.mostrar_token_recrutador, fg_color='black', width=100, height=50).pack(pady=10, fill='x', padx=10)
        CTkButton(menu_lateral, text="Pesquisar Time", command=self.pesquisar_jogador_time, fg_color='black', width=100, height=50).pack(pady=10, fill='x', padx=10)
        CTkButton(menu_lateral, text="Pesquisar Plataforma", command=self.pesquisar_jogadores_globais, fg_color='black', width=100, height=50).pack(pady=10, fill='x', padx=10)
        CTkButton(menu_lateral, text="Editar Perfil", command=self.mostrar_editar, fg_color='black', width=100, height=50).pack(pady=(10,20), fill='x', padx=10)
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

            CTkLabel(frame_info, text="Informações do Time", font=CTkFont(size=20)).pack(pady=20)
            CTkLabel(frame_info, text="Jogadores do time:", font=CTkFont(size=16)).pack(pady=(20, 5))

            team_id = self.dados_usuario.get("team_id")

            if not os.path.exists("teams.json"):
                CTkLabel(frame_info, text="Arquivo teams.json não encontrado.", text_color="red").pack()
                return

            with open("teams.json", "r") as f:
                teams = json.load(f)

            dados_time = teams.get(team_id)
            if not dados_time:
                CTkLabel(frame_info, text="Time não encontrado nos dados.", text_color="red").pack()
                return

            jogadores = dados_time.get("jogadores", {})

            if not jogadores:
                CTkLabel(frame_info, text="Nenhum jogador cadastrado no time.", text_color="gray").pack()
                return

            for jogador_nome, info in jogadores.items():
                try:
                    email_decrip = security.descriptografar_dados(info.get('email'))
                except Exception:
                    email_decrip = info.get('email')

                CTkLabel(frame_info, text=f"Nome: {info.get('nome')}").pack(pady=(10, 0))
                CTkLabel(frame_info, text=f"E-mail: {email_decrip}").pack(pady=(0, 10))

    def mostrar_editar(self):
        self.limpar_conteudo()
        CTkLabel(self.area_conteudo, text="Editar Perfil", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        frame_editar = CTkFrame(self.area_conteudo, corner_radius=10, width=500, height=300)
        frame_editar.pack(pady=20)
        frame_editar.pack_propagate(False)

        CTkLabel(frame_editar, text="Escolha uma opção para editar", font=CTkFont(size=18)).pack(pady=20)

        CTkButton(frame_editar, text='Mudar Nome', command=self.mostrar_mudar_nome, font=CTkFont(size=16), fg_color='black').pack(pady=10)
        CTkButton(frame_editar, text='Excluir Conta', font=CTkFont(size=16), fg_color='black', command=self.excluir_conta).pack(pady=10)

    def excluir_conta(self):
        self.limpar_conteudo()
        CTkLabel(self.area_conteudo, text="Excluir Perfil do Time", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        frame_excluir = CTkFrame(self.area_conteudo, corner_radius=10, width=500, height=300)
        frame_excluir.pack(pady=20)
        frame_excluir.pack_propagate(False)

        CTkLabel(frame_excluir, text="Deseja mesmo excluir a conta do seu time?", font=CTkFont(size=18)).pack(pady=(80, 20))

        botoes_frame = CTkFrame(frame_excluir, fg_color="transparent")
        botoes_frame.pack(pady=30)

        CTkButton(botoes_frame, text='Sim', width=120, command=self.confirmar_exclusao).pack(side="left", padx=20)
        CTkButton(botoes_frame, text='Não', width=120, command=self.mostrar_informacoes).pack(side="left", padx=20)

    def confirmar_exclusao(self):
        nome_time = self.dados_usuario.get('nome')

        if os.path.exists("teams.json"):
            with open("teams.json", "r") as f:
                dados_time = json.load(f)

            if nome_time in dados_time:
                del dados_time[nome_time]
                with open("teams.json", "w") as f:
                    json.dump(dados_time, f, indent=4)
                messagebox.showinfo("Sucesso", "A conta do time foi excluída.")
            else:
                messagebox.showerror("Erro", "Conta do time não encontrada.")
                return
        
        self.destroy()
        tela_login.Login(self.master).pack(fill='both', expand=True)

    def mostrar_token_recrutador(self):
        self.limpar_conteudo()

        CTkLabel(self.area_conteudo, text="Token do Recrutador", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        frame_token = CTkFrame(self.area_conteudo, corner_radius=10, width=500, height=300)
        frame_token.pack(pady=20)
        frame_token.pack_propagate(False)

        CTkLabel(frame_token, text='Mude o token do seu time', font=CTkFont(size=24)).pack(pady=(40, 10))
        CTkLabel(frame_token, text='Token', font=CTkFont(size=16)).pack(pady=10)
        self.entry_token=CTkEntry(frame_token, placeholder_text="Escreva o token do seu time", fg_color='white',text_color='black',width=250)
        self.entry_token.pack(pady=10)

        team_id = self.dados_usuario.get('team_id')

        if not team_id:
            CTkLabel(frame_token, text="Erro: ID do time não encontrado nos dados da sessão. Faça login novamente.", text_color="red").pack(pady=5)
            return

        if not os.path.exists("teams.json"):
            CTkLabel(frame_token, text="Arquivo teams.json não encontrado.", text_color="red").pack(pady=5)
            return

        with open("teams.json", "r") as f:
            teams = json.load(f)

        dados_time = teams.get(team_id)
        if not dados_time:
            CTkLabel(frame_token, text="Time não encontrado no arquivo de dados. Verifique o ID da sessão.", text_color="red").pack(pady=5)
            return

        if "token_recrutadores" in dados_time and dados_time["token_recrutadores"]:
            try:
                token_decrip = security.descriptografar_dados(dados_time["token_recrutadores"])
                self.entry_token.insert(0, token_decrip) 
                CTkLabel(frame_token, text=f"Token atual: {token_decrip}", font=CTkFont(size=14), text_color='gray').pack(pady=5)
            except Exception as e:
                CTkLabel(frame_token, text="Erro ao carregar token (formato inválido ou erro de descriptografia).", font=CTkFont(size=14), text_color='red').pack(pady=5)
        else:
            CTkLabel(frame_token, text="Nenhum token definido ainda.", font=CTkFont(size=14), text_color='gray').pack(pady=5)


        CTkButton(frame_token, text="Gerar Token", font=CTkFont(size=18), width=200, height=40, fg_color='black',command=self.cadastrar_token_recrutador).pack(pady=20)

    def cadastrar_token_recrutador(self):
        team_id = self.dados_usuario.get("team_id")
        if not team_id:
            messagebox.showerror("Erro", "ID do time não encontrado. Faça login novamente.")
            return

        if not os.path.exists("teams.json"):
            messagebox.showerror("Erro", "Arquivo teams.json não encontrado.")
            return

        try:
            with open("teams.json", "r") as f:
                teams_data = json.load(f)

            if team_id not in teams_data:
                messagebox.showerror("Erro", "Seu time não foi encontrado nos registros.")
                return

            novo_token_uuid = str(uuid.uuid4())
            novo_token_crip = security.criptografar_dados(novo_token_uuid)

            teams_data[team_id]["token_recrutadores"] = novo_token_crip

            with open("teams.json", "w") as f:
                json.dump(teams_data, f, indent=4)
            
            messagebox.showinfo("Sucesso", f"Novo token gerado e salvo com sucesso!\nCompartilhe este token com seus recrutadores:\n{novo_token_uuid}")
            self.mostrar_token_recrutador()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar novo token: {e}")

    def listar_jogadores_do_time(email_time, teams):
        for dados_time in teams.values():
            try:
                email_time_decrip = security.descriptografar_dados(dados_time.get("email"))
            except Exception:
                email_time_decrip = dados_time.get("email")

            if email_time_decrip == email_time:
                jogadores = dados_time.get("jogadores", {})
                return [
                    {
                        "nome": jogador.get("nome"),
                        "email": security.descriptografar_dados(jogador.get("email", ""))
                    } for jogador in jogadores.values()
                ]
        return []

    def pesquisar_jogador_time(self):
        self.limpar_conteudo()

        CTkLabel(self.area_conteudo, text="Pesquisar Jogadores", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        frame_procurar = CTkFrame(self.area_conteudo, width=500, height=500, corner_radius=10)
        frame_procurar.pack(pady=20)
        frame_procurar.pack_propagate(False) 

        CTkLabel(frame_procurar, text="Buscar Jogadores", font=CTkFont(size=20, weight="bold")).pack(pady=(20, 10))

        CTkLabel(frame_procurar, text="Digite o nome ou e-mail do jogador:").pack(pady=5)
        self.entry_busca = CTkEntry(frame_procurar, placeholder_text="Buscar jogador...")
        self.entry_busca.pack(pady=5)

        CTkButton(frame_procurar, text="Pesquisar", command=self.executar_pesquisa_time, fg_color='black').pack(pady=10)

        self.resultados_frame = CTkFrame(frame_procurar, corner_radius=10, width=400, height=280)
        self.resultados_frame.pack(pady=10)
        self.resultados_frame.pack_propagate(False)

    def executar_pesquisa_time(self):
        termo = self.entry_busca.get().strip().lower()

        for widget in self.resultados_frame.winfo_children():
            widget.destroy()

        if not termo:
            CTkLabel(self.resultados_frame, text="Digite algo para buscar.", text_color="red").pack()
            return
        
        team_id = self.dados_usuario.get("team_id")
        if not team_id:
            messagebox.showerror("Erro", "ID do time não encontrado na sessão. Faça login novamente.")
            return

        if not os.path.exists("teams.json"):
            CTkLabel(self.resultados_frame, text="Arquivo teams.json não encontrado.", text_color="red").pack()
            return

        with open("teams.json", "r") as f:
            teams = json.load(f)

        dados_time = teams.get(team_id)

        if not dados_time:
            CTkLabel(self.resultados_frame, text="Time não encontrado.", text_color="red").pack()
            return

        jogadores = dados_time.get("jogadores", {})

        encontrados = []
        for jogador_id, info in jogadores.items(): 
            nome_jogador = info.get("nome", "").lower()

            try:
                email_jogador = security.descriptografar_dados(info.get("email")).lower()
            except Exception:
                email_jogador = info.get("email", "").lower()

            if termo in nome_jogador or termo in email_jogador:
                encontrados.append({"id": jogador_id, "nome": info.get("nome"), "email": email_jogador}) 

        if encontrados:
            for jogador in encontrados:
                frame_jogador = CTkFrame(self.resultados_frame, fg_color="transparent")
                frame_jogador.pack(pady=5, fill='x', padx=10)
                CTkLabel(frame_jogador, text=f"Nome: {jogador['nome']}\nEmail: {jogador['email']}").pack(side='left', padx=5)
                CTkButton(frame_jogador, text="Ver Perfil", fg_color='black',
                           command=lambda j=jogador: self.mostrar_perfil_jogador(j['id'], j['nome'], j['email'])).pack(side='right', padx=5)
        else:
            CTkLabel(self.resultados_frame, text="Nenhum jogador encontrado no seu time.", text_color="gray").pack()

    def mostrar_perfil_jogador(self, id_jogador, nome_jogador, email_jogador):
        self.limpar_conteudo()
        CTkLabel(self.area_conteudo, text="Perfil do Jogador", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        frame_perfil = CTkFrame(self.area_conteudo, corner_radius=10, width=500, height=300)
        frame_perfil.pack(pady=20)
        frame_perfil.pack_propagate(False)

        CTkLabel(frame_perfil, text=f"Nome: {nome_jogador}", font=CTkFont(size=20)).pack(pady=(30, 5))
        CTkLabel(frame_perfil, text=f"Email: {email_jogador}", font=CTkFont(size=16)).pack(pady=(0, 20))

        CTkButton(frame_perfil, text="Remover do Time", font=CTkFont(size=18), width=200, height=40, fg_color='red',
                   command=lambda: self.confirmar_remover_jogador(id_jogador, nome_jogador)).pack(pady=20)
        CTkButton(frame_perfil, text="Voltar para Pesquisa", font=CTkFont(size=18), width=200, height=40, fg_color='black',
                   command=self.pesquisar_jogador_time).pack(pady=10)

    def confirmar_remover_jogador(self, id_jogador, nome_jogador):
        resposta = messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover {nome_jogador} do seu time?")
        if resposta:
            self.remover_jogador_do_time(id_jogador)

    def remover_jogador_do_time(self, id_jogador):
        time_id = self.dados_usuario.get("team_id")

        if not time_id:
            messagebox.showerror("Erro", "ID do time não encontrado na sessão. Faça login novamente.")
            return

        if not os.path.exists("teams.json"):
            messagebox.showerror("Erro", "Arquivo teams.json não encontrado.")
            return

        try:
            with open("teams.json", "r") as f:
                teams_data = json.load(f)

            if time_id not in teams_data:
                messagebox.showerror("Erro", "Seu time não foi encontrado nos registros.")
                return

            if "jogadores" in teams_data[time_id] and id_jogador in teams_data[time_id]["jogadores"]:
                player_name = teams_data[time_id]["jogadores"][id_jogador].get("nome", "este jogador")
                del teams_data[time_id]["jogadores"][id_jogador]

                with open("teams.json", "w") as f:
                    json.dump(teams_data, f, indent=4)

                messagebox.showinfo("Sucesso", f"{player_name} foi removido do seu time com sucesso!")
                self.pesquisar_jogador_time()
            else:
                messagebox.showerror("Erro", "Jogador não encontrado neste time.")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover jogador: {e}")

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

        id_time = self.dados_usuario.get("team_id")
        nome_time = self.dados_usuario.get("nome")
        if not id_time or not nome_time:
            messagebox.showerror("Erro", "Dados do time não encontrados na sessão. Faça login novamente.")
            return

        with open("players.json", "r") as f:
            dados_jogador = json.load(f)

        encontrados = []
        for id_jogador, info in dados_jogador.items():
            nome_jogador = info.get("nome", "").lower()
            try:
                email_jogador = security.descriptografar_dados(info.get("email")).lower()
            except Exception:
                email_jogador = info.get("email", "").lower()

            if termo in nome_jogador or termo in email_jogador:
                status_convite = "none"
                if "convites" in info and id_time in info["convites"]:
                    if info["convites"][id_time].get("tipo") == "time":
                        status_convite = info["convites"][id_time].get("status", "pendente")

                encontrados.append({
                    "id": id_jogador,
                    "nome": info.get("nome"),
                    "email": email_jogador,
                    "id_time_atual": info.get("time_id"),
                    "status_convite": status_convite
                })

        if encontrados:
            for jogador in encontrados:
                frame_player = CTkFrame(self.resultados_frame_global, fg_color="transparent")
                frame_player.pack(pady=5, fill='x', padx=10)
                CTkLabel(frame_player, text=f"Nome: {jogador['nome']}\nEmail: {jogador['email']}").pack(side='left', padx=5)

                if jogador['id_time_atual'] == id_time:
                     CTkLabel(frame_player, text="Já está no seu time", text_color="green").pack(side='right', padx=5)
                elif jogador['status_convite'] == "pendente":
                    CTkLabel(frame_player, text="Convite Pendente", text_color="orange").pack(side='right', padx=5)
                else:
                    CTkButton(frame_player, text="Convidar para o Time", fg_color='green',
                               command=lambda p=jogador: self.convidar_jogador_para_time(p['id'], p['nome'])).pack(side='right', padx=5)
        else:
            CTkLabel(self.resultados_frame_global, text="Nenhum jogador encontrado.", text_color="gray").pack()

    def convidar_jogador_para_time(self, id_jogador, nome_jogador):
        id_time = self.dados_usuario.get("team_id")
        nome_time = self.dados_usuario.get("nome")

        if not id_time or not nome_time:
            messagebox.showerror("Erro", "Dados do time não encontrados. Faça login novamente.")
            return

        if not id_jogador:
            messagebox.showerror("Erro", "Jogador não encontrado.")
            return

        if not os.path.exists("players.json"):
            messagebox.showerror("Erro", "Arquivo players.json não encontrado.")
            return

        try:
            with open("players.json", "r") as pf:
                players_data = json.load(pf)
        except json.JSONDecodeError:
            messagebox.showerror("Erro", "Erro ao ler players.json. Arquivo corrompido.")
            return

        info_jogador = players_data.get(id_jogador)
        if not info_jogador:
            messagebox.showerror("Erro", "Informações do jogador não encontradas.")
            return

        if "convites" not in info_jogador:
            info_jogador["convites"] = {}

        if id_time in info_jogador["convites"]:
            existing_invite = info_jogador["convites"][id_time]
            if existing_invite.get("status") == "pendente":
                messagebox.showinfo("Informação", "Convite para este jogador já foi enviado e está pendente.")
                return
            elif existing_invite.get("status") == "aceito":
                messagebox.showinfo("Informação", "Este jogador já está no seu time.")
                return

        tempo_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info_jogador["convites"][id_time] = {
            "tipo": "time",
            "remetente": nome_time,
            "status": "pendente",
            "data": tempo_atual,
            "id_time": id_time,
            "nome_time": nome_time
        }

        try:
            with open("players.json", "w") as pf:
                json.dump(players_data, pf, indent=4)
            messagebox.showinfo("Sucesso", f"Convite enviado para {nome_jogador}!")

            self.executar_pesquisa_global()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar convite: {e}")

    def mostrar_mudar_nome(self):
        self.limpar_conteudo()
        CTkLabel(self.area_conteudo, text="Mudar Nome do Time", font=CTkFont(size=50, weight="bold")).pack(pady=(200, 20))

        frame_mudar_nome = CTkFrame(self.area_conteudo, corner_radius=10, width=500, height=300)
        frame_mudar_nome.pack(pady=20)
        frame_mudar_nome.pack_propagate(False)

        CTkLabel(frame_mudar_nome, text='Novo Nome do Time:', font=CTkFont(size=16)).pack(pady=(30, 1))
        self.entry_novo_nome_time = CTkEntry(frame_mudar_nome, placeholder_text="Digite o novo nome", fg_color='white', text_color='black', width=250)
        self.entry_novo_nome_time.pack(pady=10)

        CTkButton(frame_mudar_nome, text='Confirmar Mudança', font=CTkFont(size=18), width=200, height=40, fg_color='black', command=self.confirmar_mudar_nome).pack(pady=20)
        CTkButton(frame_mudar_nome, text='Cancelar', font=CTkFont(size=18), width=200, height=40, fg_color='black', command=self.mostrar_informacoes).pack(pady=10)

    def confirmar_mudar_nome(self):
        novo_nome = self.entry_novo_nome_time.get().strip()
        id_time = self.dados_usuario.get("team_id")

        if not novo_nome:
            messagebox.showerror("Erro", "O novo nome não pode estar vazio.")
            return
        
        if not re.match(r"^[a-zA-Z0-9_]+$", novo_nome):
            messagebox.showerror("Erro", "O nome do time deve conter apenas letras, números e '_'.")
            return

        if not id_time:
            messagebox.showerror("Erro", "ID do time não encontrado na sessão. Faça login novamente.")
            return

        if not os.path.exists("teams.json"):
            messagebox.showerror("Erro", "Arquivo teams.json não encontrado.")
            return

        with open("teams.json", "r") as f:
            dados_time = json.load(f)

        for t_id, t_info in dados_time.items():
            if t_id != id_time and t_info.get("nome", "").lower() == novo_nome.lower():
                messagebox.showerror("Erro", "Este nome de time já está em uso.")
                return

        if id_time in dados_time:
            dados_time[id_time]["nome"] = novo_nome
            
            with open("teams.json", "w") as f:
                json.dump(dados_time, f, indent=4)
            
            self.dados_usuario["nome"] = novo_nome 
            messagebox.showinfo("Sucesso", f"Nome do time alterado para '{novo_nome}'.")
            self.mostrar_informacoes()
        else:
            messagebox.showerror("Erro", "Seu time não foi encontrado no arquivo de times.")

    def deslogar(self):
        self.destroy()
        tela_voltar.Logout(self.master, self.dados_usuario).pack(fill='both', expand=True)