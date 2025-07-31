from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'uma-chave-secreta-segura'  # Chave usada para proteger sessões e cookies

login_manager = LoginManager(app)  # Inicializa o Flask-Login no app Flask
login_manager.login_view = 'login'  # Define a rota de login para redirecionar usuários não autenticados

# Banco de dados para armazenar usuários
database = 'banco.db'
#produtos, inicalmente esse será o modelo armazenado
produtos = [
    {'id': 1, 'nome': 'Whey Protein - 1kg', 'preco': 100, 'imagem': 'imagens/whey.png'},
    {'id': 2, 'nome': 'Creatina - 800g', 'preco': 80, 'imagem': 'imagens/creatina.png'},
    {'id': 3, 'nome': 'Pré-treino - 300g', 'preco': 70, 'imagem': 'imagens/pre_treino.png'},
    {'id': 4, 'nome': 'Creatina - 1kg', 'preco': 90, 'imagem': 'imagens/creatina.png'},
    {'id': 5, 'nome': 'Cafeína 200mg', 'preco': 50, 'imagem': 'imagens/cafeina.png'},
    {'id': 6, 'nome': 'Whey Protein - 1kg', 'preco': 100, 'imagem': 'imagens/whey.png'},
    {'id': 7, 'nome': 'Cafeína 400mg', 'preco': 70, 'imagem': 'imagens/cafeina.png'},
    {'id': 8, 'nome': 'Creatina - 1,2kg', 'preco': 100, 'imagem': 'imagens/creatina.png'},
    {'id': 9, 'nome': 'Whey Protein - 1kg', 'preco': 100, 'imagem': 'imagens/whey.png'}
]


produtos_ = [
    ['Whey Protein - 1kg', 100],
    ['Creatina - 800g', 80],
    ['Pré-treino - 300g', 70],
    ['Creatina - 1kg', 90],
    ['Cafeína 200mg', 50],
    ['Cafeína 400mg', 70],
    ['Creatina - 1,2kg', 100],
    ['Whey Protein - 1kg', 100]
]

#Função para conectar ao banco
def conectar():
    return sqlite3.connect(database)

# Classe de usuário que o Flask-Login utiliza para gerenciar sessão
class Usuario(UserMixin):
    def __init__(self, id, nome, senha_hash):
        self.id = id  # ID do usuário, usado internamente pelo Flask-Login
        self.nome = nome  
        self.senha_hash = senha_hash 

# Função para adicionar produtos ao banco de dados
def adicionar_prod():
    db = conectar()
    cursor = db.execute('SELECT COUNT(*) FROM produtos')
    if cursor.fetchone()[0] == 0:  # Se não houver produtos, adiciona os iniciais
        for prod in produtos_:
            cursor = db.execute ('INSERT INTO produtos(prod_nome, prod_valor) VALUES(?, ?)', (prod[0], prod[1])) 
            db.commit()
    db.close()
adicionar_prod()  # Chama a função para adicionar produtos ao banco

@login_manager.user_loader 
def load_user(user_id):
    db = conectar()
    cursor = db.execute('SELECT id, nome, senha FROM usuarios WHERE id = ?', (user_id, ))  # Busca usuário no banco pelo ID 
    dados = cursor.fetchone()
    db.close()
    if dados:
        return Usuario(dados[0], dados[1], dados[2])  # Cria objeto usuário para sessão
    return None  # Retorna None se usuário não encontrado


@app.route('/')
def index():
     return render_template('index.html', nome=None)

@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        #conectar ao banco
        db = conectar()
        # Captura os dados do formulário de forma segura
        email = request.form.get('email')
        senha = request.form.get('senha')
        nome = request.form.get('nome')
       

        # Verifica se algum campo está vazio
        if not email or not nome or not senha:
            return redirect(url_for('cadastro'))

        # Verifica se o usuário já existe
        cursor = db.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user:
            flash('Usuário já existe! Escolha outro email.')
            return redirect(url_for('cadastro'))

        # Gera hash seguro da senha
        senha_hash = generate_password_hash(senha)

        # Salva o usuário no banco de dados
        db.execute('INSERT INTO usuarios(nome, email, senha) VALUES(?, ?, ?)', (nome, email, senha_hash))
        db.commit()
        #fechar a conexão
        db.close()
    
        return redirect(url_for('login'))

    return render_template('cadastro.html')  

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  # email do usuário do formulário
        senha = request.form.get('senha')      # Senha digitada

        #conectar e fazer a consulta no banco
        db = conectar() 
        cursor = db.execute('SELECT id, nome, email, senha FROM usuarios WHERE email = ?', (email, )) # Busca o usuário no banco
        resultados = cursor.fetchone()
        #usuarios = [{'id': row[0], 'nome': row[1], 'email': row[2], 'senha': row[3]} for row in resultados] #lista de usuários

        if resultados and check_password_hash(resultados[3], senha):
            user = Usuario(resultados[0], resultados[1], resultados[3])# Cria objeto usuário
            login_user(user)  # Realiza o login (cria sessão)
            
            return redirect(url_for('produto'))  # Redireciona após login
        
        db.close()

        return redirect(url_for('login'))

    return render_template('login.html')  # Mostra formulário de login


@app.route('/logout')
@login_required
def logout():
    logout_user()  # Remove sessão do usuário

    return redirect(url_for('login'))  # Redireciona para a página de login


@app.route('/produto')

def produto():
  
    return render_template('produto.html', produtos=produtos)


@app.route('/adicionar_ao_carrinho/<int:id_produto>')

def adicionar_ao_carrinho(id_produto):
    carrinho = session.get('carrinho', [])
    carrinho.append(id_produto)
    session['carrinho'] = carrinho
    return redirect(url_for('produto'))

@app.route('/carrinho')

def carrinho():
    carrinho_ids = session.get('carrinho', [])
     # Conta quantas vezes cada ID aparece → quantidades por produto
    quantidades = {}
    for pid in carrinho_ids:
        quantidades[pid] = quantidades.get(pid, 0) + 1

    carrinho_produtos = []
    total = 0  
    # Para cada produto da loja, se estiver no carrinho, monta o item
    #'pid' representa o id do produto

    for produto in produtos:
        pid = produto['id']
        if pid in quantidades:
            item = produto.copy()
            item['quantidade'] = quantidades[pid]
            item['subtotal'] = produto['preco'] * quantidades[pid]
            total += item['subtotal']            
            carrinho_produtos.append(item)

    return render_template('carrinho.html', carrinho=carrinho_produtos, total=total)

@app.route('/remover',methods = ['POST','GET'])
def remover():
    produto_remover = int(request.form.get('produto'))
    carrinho = session.get('carrinho', [])
    if produto_remover in carrinho:
        carrinho.remove(produto_remover)
        session['carrinho'] = carrinho
    return redirect(url_for('carrinho'))
    

if __name__ == '__main__': 
    app.run(debug=True)
