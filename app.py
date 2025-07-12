from flask import Flask, render_template, url_for, request, redirect, session, make_response 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

users = {}
app.config['SECRET_KEY'] = 'chave_hiper_mega_secreta'

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
@app.route('/')
def index():
     if 'user_name' in session:
        nome = session['user_name']
        return render_template('index.html', nome=nome)
     return render_template('index.html', nome=None)

@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
     
        if nome in users:
            return render_template('cadastro.html', erro='usuario ja existe')
        
        senha_hash = generate_password_hash(senha)
        users[nome] = senha_hash
        return redirect(url_for('login') )
    
    return render_template('cadastro.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
     if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
    
        if nome in users and check_password_hash(users[nome], senha):
            session['user_name'] = nome
            response = make_response(redirect(url_for('base')))
            response.set_cookie('nome', nome, 7*24*60*60)
            return response
        else: 
            return redirect(url_for('cadastro', user_name=session.get('user_name')))
        
    
     return render_template('login.html')

@app.route('/logout')
def logout():
    if session.get('user_name'):
        session.clear()
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/produto')
def produto():
    nome = session.get('user_name')
    return render_template('produto.html', produtos=produtos, user_name = nome)

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

    # Passa lista de itens e total para o template
    return render_template('carrinho.html',carrinho=carrinho_produtos,total=total)


@app.route('/base')
def base():
    nome = session.get('user_name')
    return render_template('base.html', user_name = nome)

# @app.route('/get')
# def get_session():
#     if session.get('user_name'):
#         usuario = session.get('user_name')  # ou session['usuario'], se tiver certeza que existe
#         return f'Usuário na sessão: {usuario}'
#     else:
#         return 'Não há nenhumusuário logado'



if __name__ == '__main__': 
    app.run(debug=True)
