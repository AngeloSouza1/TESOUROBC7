import tkinter as tk
from PIL import Image, ImageTk
from modulo_tesouro import cacar_tesouro


class TreasureHuntApp:
    def __init__(self, root):
        self.root = root
        self.configurar_janela()
        self.carregar_widgets()
        self.campos_visiveis = False

    def configurar_janela(self):
        self.root.title("Caça ao Tesouro dos Programadores 🗺️💎")
        largura_janela = 819
        altura_janela = 819
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x_central = int((largura_tela - largura_janela) / 2)
        y_central = int((altura_janela - largura_janela) / 2)
        self.root.geometry(f"{largura_janela}x{largura_janela}+{x_central}+{y_central}")
        self.root.resizable(False, False)

        # Adicionando o background
        self.background_image = ImageTk.PhotoImage(Image.open("assets/background.png"))
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

    def carregar_widgets(self):
        # Botão principal
        self.botao_imagem = ImageTk.PhotoImage(Image.open("assets/start_button.png").resize((50, 50)))
        self.botao_iniciar = tk.Button(
            self.root,
            image=self.botao_imagem,
            command=self.mostrar_campos,
            bg="#2b2b2b",
            bd=0,
            activebackground="#1E1E1E",
        )
        # Posicionar o botão no canto inferior direito
        self.botao_iniciar.place(relx=0.95, rely=0.95, anchor="se")

    def mostrar_campos(self):
        if not self.campos_visiveis:
            # Campo para inserir ponto de partida
            self.ponto_partida_label = tk.Label(
                self.root,
                text="Ponto de Partida:",
                bg="#2b2b2b",
                fg="#FFD700",
                font=("Helvetica", 12),
            )
            self.ponto_partida_label.place(relx=0.1, rely=0.2, anchor="w")

            self.ponto_partida_entry = tk.Entry(
                self.root, font=("Helvetica", 12), width=10, bg="#1E1E1E", fg="#FFD700", insertbackground="#FFD700"
            )
            self.ponto_partida_entry.place(relx=0.1, rely=0.25, anchor="w")

            # Campo para inserir as pistas
            self.pistas_label = tk.Label(
                self.root,
                text="Pistas (separadas por espaço):",
                bg="#2b2b2b",
                fg="#FFD700",
                font=("Helvetica", 12),
            )
            self.pistas_label.place(relx=0.1, rely=0.35, anchor="w")

            self.pistas_entry = tk.Entry(
                self.root, font=("Helvetica", 12), width=40, bg="#1E1E1E", fg="#FFD700", insertbackground="#FFD700"
            )
            self.pistas_entry.place(relx=0.1, rely=0.4, anchor="w")

            # Botão para calcular a posição final
            self.botao_calcular = tk.Button(
                self.root,
                text="Calcular Posição Final",
                command=self.calcular_posicao,
                bg="#FFD700",
                fg="#2b2b2b",
                font=("Helvetica", 12, "bold"),
            )
            self.botao_calcular.place(relx=0.1, rely=0.5, anchor="w")

            self.campos_visiveis = True

    def calcular_posicao(self):
        try:
            ponto_partida = int(self.ponto_partida_entry.get())
            pistas = list(map(int, self.pistas_entry.get().split()))

            # Validação do ponto de partida
            if not (0 <= ponto_partida <= 10):
                self.exibir_erro("🟡 O ponto de partida deve estar entre 0 e 10.")
                return
        except ValueError:
            self.exibir_erro("🔴 Entrada inválida!\nCertifique-se de que o ponto de partida e as pistas sejam números inteiros.")
            return

        if len(pistas) != 3:
            self.exibir_erro("🟡 Entrada incompleta!\nInsira exatamente 3 pistas separadas por espaço.")
            return

        posicao_final = cacar_tesouro(ponto_partida, pistas)
        self.exibir_saida(ponto_partida, pistas, posicao_final)

    def exibir_saida(self, ponto_partida, pistas, posicao_final):
        if hasattr(self, "output_frame"):
            self.output_frame.destroy()

        self.output_frame = tk.Frame(
            self.root, bg="#333333", highlightthickness=2, highlightbackground="#FFD700", relief="raised"
        )
        self.output_frame.place(relx=0.5, rely=0.6, anchor="center", width=600, height=300)

        self.close_icon = ImageTk.PhotoImage(Image.open("assets/close_icon.png").resize((20, 20)))
        self.close_button = tk.Button(
            self.output_frame,
            image=self.close_icon,
            bg="#333333",
            bd=0,
            activebackground="#444444",
            command=self.resetar_tela,
        )
        self.close_button.place(x=570, y=5)

        ponto_partida_label = tk.Label(
            self.output_frame,
            text=f"Ponto de Partida: {ponto_partida}",
            bg="#333333",
            fg="#FFD700",
            font=("Courier", 12),
        )
        ponto_partida_label.place(x=10, y=30)

        pistas_label = tk.Label(
            self.output_frame,
            text=f"Pistas: {', '.join(map(str, pistas))}",
            bg="#333333",
            fg="#FFD700",
            font=("Courier", 12),
        )
        pistas_label.place(x=10, y=70)

        posicao_final_label = tk.Label(
            self.output_frame,
            text=f"Posição Final: {posicao_final}",
            bg="#333333",
            fg="#00FF00",
            font=("Courier", 14, "bold"),
        )
        posicao_final_label.place(x=10, y=110)

    def exibir_erro(self, mensagem):
        largura_janela = self.root.winfo_width()
        altura_janela = self.root.winfo_height()
        largura_tela = self.root.winfo_x()
        altura_tela = self.root.winfo_y()

        popup = tk.Toplevel(self.root)
        popup.geometry(f"350x150+{largura_tela + largura_janela//2 - 175}+{altura_tela + altura_janela//2 - 75}")
        popup.configure(bg="#2b2b2b")

        popup.title("Aviso ⚠️")
        erro_label = tk.Label(
            popup, 
            text=mensagem, 
            fg="#FFD700", 
            bg="#2b2b2b", 
            font=("Helvetica", 12, "bold"),
            wraplength=300, 
            justify="center"
        )
        erro_label.pack(pady=20)

        tk.Button(
            popup, 
            text="Entendido", 
            command=popup.destroy,
            bg="#FFD700",
            fg="#2b2b2b",
            font=("Helvetica", 10, "bold"),
            activebackground="#444444",
            activeforeground="#FFD700"
        ).pack()

    def resetar_tela(self):
        if hasattr(self, "output_frame"):
            self.output_frame.destroy()
            del self.output_frame
        self.resetar_campos()

    def resetar_campos(self):
        if hasattr(self, "ponto_partida_entry"):
            self.ponto_partida_entry.place_forget()
            self.pistas_entry.place_forget()
            self.botao_calcular.place_forget()
            self.ponto_partida_label.place_forget()
            self.pistas_label.place_forget()
            self.campos_visiveis = False


if __name__ == "__main__":
    root = tk.Tk()
    app = TreasureHuntApp(root)
    root.mainloop()
