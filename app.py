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
# rotas para as imagens dos produtos
produtos_img = [
    {'imagem': 'imagens/whey.png'},
    {'imagem': 'imagens/creatina.png'},
    {'imagem': 'imagens/pre_treino.png'},
    {'imagem': 'imagens/creatina.png'},
    {'imagem': 'imagens/cafeina.png'},
    {'imagem': 'imagens/whey.png'},
    {'imagem': 'imagens/cafeina.png'},
    {'imagem': 'imagens/creatina.png'},
    {'imagem': 'imagens/whey.png'}
]


produtos_db = [
    ['Whey Protein - 1kg', 100],
    ['Creatina - 800g', 80],
    ['Pré-treino - 300g', 70],
    ['Creatina - 1kg', 90],
    ['Cafeína 200mg', 50],
    ['Whey Protein - 1kg', 100],
    ['Cafeína 400mg', 70],
    ['Creatina - 1,2kg', 100],
    ['Whey Protein - 1kg', 100]
] # Lista de produtos iniciais para popular o banco de dados

#Função para conectar ao banco
def conectar():
    return sqlite3.connect(database)

# Classe de usuário que o Flask-Login utiliza para gerenciar sessão11
class Usuario(UserMixin):
    def __init__(self, id, nome, senha_hash):
        self.id = id  # ID do usuário, usado internamente pelo Flask-Login
        self.nome = nome  
        self.senha_hash = senha_hash

# Função para adicionar produtos ao banco de dados (usada apenas na inicialização)
def adicionar_prod():
    db = conectar()
    cursor = db.execute('SELECT COUNT(*) FROM produtos')
    if cursor.fetchone()[0] == 0:  # Se não houver produtos, adiciona os iniciais
        for prod in produtos_db:
            cursor = db.execute ('INSERT INTO produtos(prod_nome, prod_valor) VALUES(?, ?)', (prod[0], prod[1])) 
            db.commit()
    db.close()
adicionar_prod()  # Chama a função para adicionar produtos ao banco

# Função para apagar os dados do carrinho do usuário
def apagar_carrinho():
    db = conectar()
    db.execute('DELETE FROM carrinho WHERE user_id = ?', (current_user.id,))
    db.commit() 
    db.close()

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

        # Salva o usuário no banco de dados caso não exista
        db.execute('INSERT INTO usuarios(nome, email, senha) VALUES(?, ?, ?)', (nome, email, senha_hash))
        db.commit()
        #fechar a conexão
        db.close()
    
        return redirect(url_for('login'))

    return render_template('cadastro.html')  

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  
        senha = request.form.get('senha') 

        #conectar e fazer a consulta no banco
        db = conectar() 
        cursor = db.execute('SELECT id, nome, email, senha FROM usuarios WHERE email = ?', (email, )) # Busca o usuário no banco
        resultados = cursor.fetchone()
        db.close()
        if resultados and check_password_hash(resultados[3], senha):
            user = Usuario(resultados[0], resultados[1], resultados[3])# Cria objeto usuário
            login_user(user)  # Realiza o login (cria sessão)
            
            return redirect(url_for('produto'))  # Redireciona após login
        else:
            flash('Senha ou email incorretos!', category = 'error')
            return redirect(url_for('login'))


    return render_template('login.html')  # Mostra formulário de login

@app.route('/logout')   
@login_required
def logout():
    logout_user()  # Remove sessão do usuário
    #apagar_carrinho()  # Limpa o carrinho do usuário ao fazer logout
    return redirect(url_for('login'))  # Redireciona para a página de login

@app.route('/produto')
def produto():
    db = conectar()
    cursor = db.execute('SELECT prod_id, prod_nome, prod_valor FROM produtos')  # Consulta os produtos no banco
    resultado = cursor.fetchall()
    produtos = []
    for item in resultado:
        produtos.append({
            'id': item[0],
            'nome': item[1],
            'preco': item[2],
            'imagem': produtos_img[item[0] - 1]['imagem']  # Associa a imagem ao produto
        })
    return render_template('produto.html', produtos=produtos)

@app.route('/adicionar_ao_carrinho/<int:id_produto>') 
@login_required
def adicionar_ao_carrinho(id_produto):
    db = conectar()
    cursor = db.execute('SELECT * FROM carrinho WHERE prod_id = ? AND user_id = ?', (id_produto, current_user.id))

    if cursor.fetchone():  # Verifica se o produto existe
        cursor = db.execute('UPDATE carrinho SET quantidade = quantidade + 1 WHERE prod_id = ? and user_id = ?', (id_produto, current_user.id))
        db.commit()
    else:
        cursor = db.execute('INSERT INTO carrinho (user_id, prod_id) VALUES (?, ?)', (current_user.id, id_produto))
        db.commit()
    db.close()
    return redirect(url_for('produto'))  

@app.route('/carrinho')
def carrinho():
    db = conectar()
    cursor = db.execute('''
        SELECT p.prod_id, p.prod_nome, p.prod_valor, c.quantidade
        FROM carrinho AS c
        INNER JOIN produtos AS p
        ON c.prod_id = p.prod_id
        WHERE c.user_id = ?
    ''', (current_user.id,))
    resultado = cursor.fetchall()
    carrinho_produtos = []  # Lista para armazenar os detalhes do produto 
    if resultado:
        for produto in resultado:
            carrinho_produtos.append({
                'id': produto[0],
                'nome': produto[1],
                'preco': produto[2],
                'quantidade': produto[3],
                'subtotal': produto[2] * produto[3]  # Calcula o subtotal
            })
    total = sum(produto['preco'] * produto['quantidade'] for produto in carrinho_produtos)
    return render_template('carrinho.html', carrinho=carrinho_produtos, total=total)

@app.route('/remover', methods = ['POST','GET'])
def remover():
    produto_remover = request.form.get('produto')
    db = conectar()
    cursor = db.execute('''
        SELECT p.prod_nome, p.prod_valor, c.quantidade
        FROM carrinho AS c
        INNER JOIN produtos AS p
        ON c.prod_id = p.prod_id
        WHERE c.user_id = ?
    ''', (current_user.id,))
    resultado = cursor.fetchone()
    if resultado:
        if resultado[2] < 1:
            db.execute('DELETE FROM carrinho WHERE prod_id = ? AND user_id = ?', (produto_remover, current_user.id))
        else:
            db.execute('UPDATE carrinho SET quantidade = quantidade - 1 WHERE prod_id = ? AND user_id = ?', (produto_remover, current_user.id))
        db.commit()
        db.close()
    return redirect(url_for('carrinho'))

@app.route('/limpar_carrinho')
def limpar_carrinho():
    apagar_carrinho()
    return redirect(url_for('carrinho'))

#Tratamento dos erros das páginas 404 e 500
@app.errorhandler(404)
def erro_404(e):
    return render_template('erros/404.html'), 404

@app.errorhandler(500)
def erro_500(e):
    return render_template('erros/500.html'), 500



if __name__ == '__main__': 
    app.run(debug=True)
