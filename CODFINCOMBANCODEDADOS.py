# Importando tkinter forma gráfica da janela
from tkinter import *
from tkinter import ttk, messagebox
import firebirdsql
from PIL import Image, ImageTk  # Importando Pillow para manipulação de imagens

# Janela organizada com a função dentro
janela = Tk()

# Funções dos botões editar/salvar
class Funcao:
    def editar(self):
        # Obtém o item selecionado na Treeview
        selected_item = self.caixa.selection()
        if selected_item:
            # Obtém os dados do item selecionado
            item_data = self.caixa.item(selected_item)
            # Preenche os campos de entrada com os dados do item
            self.caixa_entry.delete(0, END)
            self.caixa_entry.insert(0, item_data['values'][0])  # CAIXA
            self.tipo_entry.delete(0, END)
            self.tipo_entry.insert(0, item_data['values'][1])  # TIPO
            self.id_entry.delete(0, END)
            self.id_entry.insert(0, item_data['values'][2])  # ID
            self.valor_entry.delete(0, END)
            self.valor_entry.insert(0, item_data['values'][3])  # VALOR
            self.obs_entry.delete(0, END)
            self.obs_entry.insert(0, item_data['values'][4])  # OBS

            # Desabilita os campos ID e OBS para edição
            self.id_entry.config(state='readonly')
            self.obs_entry.config(state='readonly')
        else:
            messagebox.showwarning("Seleção", "Por favor, selecione um item para editar.")

    def salvar(self):
        # Obtém os dados dos campos de entrada
        caixa = self.caixa_entry.get()
        tipo = self.tipo_entry.get()
        id_ = self.id_entry.get()  # O ID não pode ser alterado
        valor = self.valor_entry.get()
        obs = self.obs_entry.get()  # O OBS não pode ser alterado

        if not id_:
            messagebox.showerror("Erro", "Nenhum item selecionado para salvar.")
            return

        self.banco.atualizar_dados(caixa, tipo, id_, valor, obs)

        # Limpa os campos e desbloqueia
        self.limpar_campos()

        # Limpa a tabela para mantê-la em branco após salvar
        self.limpar_tabela()
        messagebox.showinfo("Sucesso", "Dados atualizados com sucesso.")

    def limpar_campos(self):
        # Limpa os campos de entrada e desbloqueia todos
        self.caixa_entry.delete(0, END)
        self.tipo_entry.delete(0, END)
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, END)
        self.valor_entry.delete(0, END)
        self.obs_entry.config(state='normal')
        self.obs_entry.delete(0, END)

    def limpar_tabela(self):
        # Remove todos os itens da Treeview
        for item in self.caixa.get_children():
            self.caixa.delete(item)

class MeuBancoDeDados:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def conectabd(self, banco):
        try:
            self.conn = firebirdsql.connect(
                host="localhost",
                database=banco,  # Usando o banco informado
                user="SYSDBA",
                password="masterkey"
            )
            self.cursor = self.conn.cursor()
            print("Conectado com Sucesso")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")

    def desconectabd(self):
        if self.conn:
            self.conn.close()
            print("Conexão fechada.")

    def consulta_tabela(self):
        if self.conn:
            try:
                self.cursor.execute("SELECT caixa, tipo, id, valor, obs FROM caixas_creditos;")
                resultados = self.cursor.fetchall()
                return resultados
            except Exception as e:
                print(f"Erro ao consultar tabela: {e}")
                return []
        return []

    def consulta_por_caixa(self, caixa):
        if self.conn:
            try:
                self.cursor.execute("SELECT caixa, tipo, id, valor, obs FROM caixas_creditos WHERE caixa = ?;", (caixa,))
                resultados = self.cursor.fetchall()
                return resultados
            except Exception as e:
                print(f"Erro ao consultar por caixa: {e}")
                return []
        return []

    def atualizar_dados(self, caixa, tipo, id_, valor, obs):
        if self.conn:
            try:
                self.cursor.execute("""
                    UPDATE caixas_creditos
                    SET caixa = ?, tipo = ?, valor = ?, obs = ?
                    WHERE id = ?;
                """, (caixa, tipo, valor, obs, id_))
                self.conn.commit()
                print("Dados atualizados com sucesso.")
            except Exception as e:
                print(f"Erro ao atualizar dados: {e}")
        else:
            print("Não há conexão com o banco de dados.")
            messagebox.showerror("Erro", "Não há conexão com o banco de dados.")
            
class DentroJanela(Funcao):
    def __init__(self):
        self.janela = janela
        self.banco = MeuBancoDeDados()
        self.divisaotela()
        self.botao()
        self.titulojanela()
        self.crudbanco()
        janela.mainloop()

    def titulojanela(self):
        self.janela.title("Troca de Creditos Diversos")
        self.janela.configure(background='#e68a00')
        self.janela.geometry("800x600")
        self.janela.resizable(True, True)
        self.janela.maxsize(width=900, height=700)
        self.janela.minsize(width=900, height=700)
        # Troca o ícone (usando arquivo .ico ou .png)
        self.janela.iconbitmap("C:\\Users\\Pichau\\Desktop\\cdiversos\\images\\em.ico")  # Para .ico
        # Ou se for uma imagem .png
        # self.janela.iconphoto(False, PhotoImage(file="caminho/do/arquivo.png"))

    def divisaotela(self):
        self.divisao1 = Frame(self.janela, bd=4, bg='white', highlightbackground='#0066cc', highlightthickness=6)
        self.divisao1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.divisao2 = Frame(self.janela, bd=4, bg='white', highlightbackground='#0066cc', highlightthickness=6)
        self.divisao2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

        try:
            self.imagem = Image.open("C:\\Users\\Pichau\\Desktop\\cdiversos\\images\\emsoft.png")
            self.imagem_tk = ImageTk.PhotoImage(self.imagem)
            self.label_imagem = Label(self.divisao1, image=self.imagem_tk)
            self.label_imagem.place(relx=0.5, rely=0.4, anchor='center')
            self.label_imagem.image = self.imagem_tk
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")

    def botao(self):
        self.btalterar = Button(self.divisao1, text='Editar', bd=2, bg='white', fg='black', font=('verdana'), command=self.editar)
        self.btalterar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)
        self.btsalvar = Button(self.divisao1, text='Salvar', bd=2, bg='white', fg='black', font=('verdana'), command=self.salvar)
        self.btsalvar.place(relx=0.8, rely=0.3, relwidth=0.1, relheight=0.15)

        # Label para Caixa
        self.caixa_label = Label(self.divisao1, text="CAIXA:", bg='white', fg='black', font=('verdana', 10))
        self.caixa_label.place(relx=0.01, rely=0.1)

        # Campos de entrada
        self.caixa_entry = Entry(self.divisao1)
        self.caixa_entry.place(relx=0.1, rely=0.1, relwidth=0.1, relheight=0.1)

        self.tipo_entry = Entry(self.divisao1)
        self.tipo_entry.place(relx=0.1, rely=0.25, relwidth=0.1, relheight=0.1)

        self.id_entry = Entry(self.divisao1)
        self.id_entry.place(relx=0.1, rely=0.4, relwidth=0.1, relheight=0.1)

        self.valor_entry = Entry(self.divisao1)
        self.valor_entry.place(relx=0.1, rely=0.55, relwidth=0.1, relheight=0.1)

        self.obs_entry = Entry(self.divisao1)
        self.obs_entry.place(relx=0.1, rely=0.7, relwidth=0.1, relheight=0.1)

        # Botão para buscar dados
        self.btbuscar = Button(self.divisao1, text='Buscar', bd=2, bg='white', fg='black', font=('verdana'), command=self.buscar_por_caixa)
        self.btbuscar.place(relx=0.8, rely=0.5, relwidth=0.1, relheight=0.15)

        # Novo botão para Conectar ao banco
        self.btconectar = Button(self.divisao1, text='Conectar', bd=2, bg='white', fg='black', font=('verdana'), command=self.conectar)
        self.btconectar.place(relx=0.8, rely=0.7, relwidth=0.1, relheight=0.15)

        # Adiciona a entry para o banco de dados
        self.banco_label = Label(self.divisao1, text="Banco de Dados:", bg='white', fg='black', font=('verdana', 10))
        self.banco_label.place(relx=0.01, rely=0.85)

        self.banco_entry = Entry(self.divisao1)
        self.banco_entry.place(relx=0.16, rely=0.85, relwidth=0.5, relheight=0.1)

    def conectar(self):
        banco_informado = self.banco_entry.get()  # Pega o banco informado pelo usuário
        if not banco_informado:
            messagebox.showerror("Erro", "Por favor, insira o caminho do banco de dados.")
            return

        self.banco.conectabd(banco_informado)  # Passa o banco para a função de conexão
        messagebox.showinfo("Sucesso", "Conexão estabelecida com sucesso!")

    def crudbanco(self):
        self.caixa = ttk.Treeview(self.divisao2, columns=('Caixa', 'Tipo', 'ID', 'Valor', 'Obs'), show='headings')
        self.caixa.heading('Caixa', text='Caixa')
        self.caixa.heading('Tipo', text='Tipo')
        self.caixa.heading('ID', text='ID')
        self.caixa.heading('Valor', text='Valor')
        self.caixa.heading('Obs', text='Observação')

        self.caixa.column('Caixa', width=150)
        self.caixa.column('Tipo', width=100)
        self.caixa.column('ID', width=50)
        self.caixa.column('Valor', width=100)
        self.caixa.column('Obs', width=100)

        # Centraliza o texto nas colunas
        for col in self.caixa['columns']:
            self.caixa.column(col, anchor='center', width=100)  # Define a largura e centraliza o texto
        self.caixa.pack(fill=BOTH, expand=True)

        self.caixa.pack(fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self.divisao2, orient='vertical', command=self.caixa.yview)
        self.caixa.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)

    def carregar_dados(self):
        for item in self.caixa.get_children():
            self.caixa.delete(item)
        dados = self.banco.consulta_tabela()
        for linha in dados:
            self.caixa.insert('', 'end', values=linha)

    def buscar_por_caixa(self):
        caixa = self.caixa_entry.get()
        if not caixa:
            messagebox.showerror("Erro", "Por favor, insira o valor do caixa para a busca.")
            return

        for item in self.caixa.get_children():
            self.caixa.delete(item)

        dados = self.banco.consulta_por_caixa(caixa)
        if dados:
            for linha in dados:
                self.caixa.insert('', 'end', values=linha)
        else:
            messagebox.showinfo("Resultado", "Nenhum registro encontrado para o caixa informado.")

# Inicializa a aplicação
if __name__ == "__main__":
    DentroJanela()
