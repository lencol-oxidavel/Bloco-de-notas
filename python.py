from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring
import mysql.connector


def salvar():
    global diretorio
    try:
        if diretorio == '':
            diretorio = asksaveasfilename()
        arq = open(diretorio, 'w')
        arq.write(texto.get("1.0", END))
    except:
        pass
    

def abrir():
    global diretorio
    try:
        diretorio = askopenfilename()
        conteudo = []
        arq = open(diretorio, 'r')
        for linha in arq:
            conteudo.append(linha)
        texto.delete("1.0", END)
        texto.insert('insert' ,'\n'.join(conteudo))
    except:
        pass


def abrir_banco_de_dados():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bloco_de_notas"
        )
        
        if conexao.is_connected():
            cursor = conexao.cursor()
            
            # Pega os nomes das notas do banco de dados
            cursor.execute("SELECT nome FROM notas")
            notas = cursor.fetchall()
            
            if not notas:
                print("Nenhuma nota encontrada no banco de dados.")
                return
            
            # Cria uma janela para o usuário escolher a nota
            escolha = Toplevel(root)
            escolha.title("Escolher Nota")
            
            lista_notas = Listbox(escolha)
            for nota in notas:
                lista_notas.insert(END, nota)
            lista_notas.pack()
            
            def carregar_nota():
                nome_nota = lista_notas.get(ACTIVE)
                if nome_nota:
                    nome_nota = nome_nota
                    cursor.execute("SELECT content FROM notas WHERE nome = %s", (nome_nota)) # (nome_nota,)) removi a virgula o que me permitiu de alguma forma que eu carregasse a nota no widget de texto
                    conteudo = cursor.fetchone()
                    
                    if conteudo:
                        conteudo_limpo = conteudo[1:-1] # limpa o texto do primeiro e ultimo caracteres mas não funciona
                        texto.delete("1.0", END)
                        texto.insert(END, conteudo_limpo)
                        print("Nota carregada com sucesso!")
                    else:
                        print("Erro ao carregar a nota.")
                
                escolha.destroy()
                
            
            botao_carregar = Button(escolha, text="Carregar Nota", command=carregar_nota)
            botao_carregar.pack()
            
            # Mantém a janela de seleção aberta até que o usuário escolha uma nota
            escolha.protocol("WM_DELETE_WINDOW", lambda: (cursor.close(), conexao.close(), escolha.destroy()))
            escolha.mainloop()
            
    except mysql.connector.Error as err:
        print("Erro: {}".format(err))
        

def salvar_banco_de_dados():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bloco_de_notas"
        )
        
        if conexao.is_connected():
            cursor = conexao.cursor()
            
            # Cria uma janela para o usuário inserir o nome da nota
            nome = askstring("Salvar Nota", "Digite o nome da nota:")
            if not nome:
                print("Nome da nota não fornecido.")
                return
            
            conteudo = texto.get("1.0", END)
            
            cursor.execute("INSERT INTO notas (nome, content) VALUES (%s, %s)", (nome, conteudo))
            conexao.commit()
            print("Nota salva no banco de dados com sucesso!")
                
            cursor.close()
            conexao.close()
            
    except mysql.connector.Error as err:
        print("Erro: {}".format(err))
    

def sair():
    root.destroy()


def tema(estilo):
    if estilo == 1:
        texto['bg'] = 'black'
        texto['fg'] = 'white'
    if estilo == 2:
        texto['bg'] = 'white'
        texto['fg'] = 'black'


diretorio = ''
tamanho = 12
fonte_estilo = 'arial'

root = Tk()
root['bg'] = 'gray'
root.title('Bloco De Notas')
largura_janela = 800
altura_janela = 400

# Calcula a posição para centralizar a janela
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
pos_x = (largura_tela // 2) - (largura_janela // 2)
pos_y = (altura_tela // 2) - (altura_janela // 2)

# Define a geometria da janela com a posição calculada
root.geometry('{}x{}+{}+{}'.format(largura_janela, altura_janela, pos_x, pos_y))


menu = Menu(root)

arquivo = Menu(menu)
arquivo.add_command(label='Abrir', command = abrir)
arquivo.add_command(label='Salvar', command = salvar)
arquivo.add_command(label = 'abrir no banco de dados', command = abrir_banco_de_dados)
arquivo.add_command(label = 'salvar no banco de dados', command = salvar_banco_de_dados)
arquivo.add_command(label = 'sair', command = sair)
menu.add_cascade(label='Arquivo', menu=arquivo)

estilo = Menu(menu)
estilo.add_command(label = 'escuro', command = lambda : tema(1))
estilo.add_command(label = 'claro', command = lambda : tema(2))
menu.add_cascade(label="tema", menu = estilo)


root.config(menu = menu)

texto = Text(root, width = 180, height = 80, bg = 'white', fg = 'black')
texto.pack(side = TOP)
texto.configure(font=(fonte_estilo, tamanho))

root.mainloop()
