from flask import render_template, request, url_for, redirect, flash, Blueprint
from app import app, db
from app.models.tables import Pessoa, User
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@app.route("/consulta")
@login_required
def index():
    users = User.query.all()  # Select * from users;
    return render_template("users.html", users=users)


@app.route("/user/<int:id>")
@login_required
def unique(id):
    user = User.query.get(id)
    return render_template("user.html", user=user)


@app.route("/user/delete/<int:id>")
@login_required
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()

    return redirect("/consulta")


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user and not check_password_hash(user.password, password):
        flash('Por favor verifique os seus dados de login e tente novamente!.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('O Email informado já existe!.')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name,
                    password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@app.route('/listagem')
@login_required
def listagem():
    pessoas = Pessoa.query.all()
    return render_template('listagem.html', pessoas=pessoas, ordem='id')


@app.route('/selecao/<int:id>')
@login_required
def selecao(id=0):
    pessoas = Pessoa.query.filter_by(id=id).all()
    return render_template('listagem.html', pessoas=pessoas, ordem='id')
    

@app.route('/ordenacao/<campo>/<ordem_anterior>')
@login_required
def ordenacao(campo='id', ordem_anterior=''):
    if campo == 'id':
        if ordem_anterior == campo:
            pessoas = Pessoa.query.order_by(Pessoa.id.desc()).all()
        else:
            pessoas = Pessoa.query.order_by(Pessoa.id).all()
    elif campo == 'nome':
        if ordem_anterior == campo:
            pessoas = Pessoa.query.order_by(Pessoa.nome.desc()).all()
        else:
            pessoas = Pessoa.query.order_by(Pessoa.nome).all()
    elif campo == 'idade':
        if ordem_anterior == campo:
            pessoas = Pessoa.query.order_by(Pessoa.idade.desc()).all()
        else:
            pessoas = Pessoa.query.order_by(Pessoa.idade).all()
    elif campo == 'sexo':
        if ordem_anterior == campo:
            pessoas = Pessoa.query.order_by(Pessoa.sexo.desc()).all()
        else:
            pessoas = Pessoa.query.order_by(Pessoa.sexo).all()
    elif campo == 'salario':
        if ordem_anterior == campo:
            pessoas = Pessoa.query.order_by(Pessoa.salario.desc()).all()
        else:
            pessoas = Pessoa.query.order_by(Pessoa.salario).all()
    else:
        pessoas = Pessoa.query.order_by(Pessoa.id).all()

    return render_template('listagem.html', pessoas=pessoas, ordem=campo)


@app.route('/consulta', methods=['POST'])
@login_required
def consulta():
    consulta = '%'+request.form.get('consulta')+'%'
    campo = request.form.get('campo')

    if campo == 'nome':
        pessoas = Pessoa.query.filter(Pessoa.nome.like(consulta)).all()
    elif campo == 'idade':
        pessoas = Pessoa.query.filter(Pessoa.idade.like(consulta)).all()
    elif campo == 'sexo':
        pessoas = Pessoa.query.filter(Pessoa.sexo.like(consulta)).all()
    elif campo == 'salario':
        pessoas = Pessoa.query.filter(Pessoa.salario.like(consulta)).all()
    else:
        pessoas = Pessoa.query.all()

    return render_template('listagem.html', pessoas=pessoas, ordem='id')


@app.route('/insercao')
@login_required
def insercao():
    return render_template('insercao.html')


@app.route('/salvar_insercao', methods=['POST'])
@login_required
def salvar_insercao():
    Nome = request.form.get('nome')
    Idade = int(request.form.get('idade'))
    Sexo = request.form.get('sexo')
    Salario = float(request.form.get('salario'))

    pessoa = Pessoa(Nome, Idade, Sexo, Salario)

    db.session.add(pessoa)
    db.session.commit()

    pessoas = Pessoa.query.all()
    return render_template('listagem.html', pessoas=pessoas, ordem='id')


@app.route('/edicao/<int:id>')
@login_required
def edicao(id=0):
    pessoa = Pessoa.query.filter_by(id=id).first()
    return render_template('edicao.html', pessoa=pessoa)


@app.route('/salvar_edicao', methods=['POST'])
@login_required
def salvar_edicao():
    Id = int(request.form.get('id'))
    Nome = request.form.get('nome')
    Idade = int(request.form.get('idade'))
    Sexo = request.form.get('sexo')
    Salario = float(request.form.get('salario'))

    pessoa = Pessoa.query.filter_by(id=Id).first()

    pessoa.nome = Nome
    pessoa.idade = Idade
    pessoa.sexo = Sexo
    pessoa.salario = Salario
    db.session.commit()

    pessoas = Pessoa.query.all()
    return render_template('listagem.html', pessoas=pessoas, ordem='id')


@app.route('/delecao/<int:id>')
@login_required
def delecao(id=0):
    pessoa = Pessoa.query.filter_by(id=id).first()
    return render_template('delecao.html', pessoa=pessoa)


@app.route('/salvar_delecao', methods=['POST'])
@login_required
def salvar_delecao():
    Id = int(request.form.get('id'))

    pessoa = Pessoa.query.filter_by(id=Id).first()

    db.session.delete(pessoa)
    db.session.commit()

    pessoas = Pessoa.query.all()
    return render_template('listagem.html', pessoas=pessoas, ordem='id')


@app.route('/graficos')
@login_required
def graficos():
    pessoasM = Pessoa.query.filter_by(sexo='M').all()
    pessoasF = Pessoa.query.filter_by(sexo='F').all()

    salarioM = 0
    for m in pessoasM:
        salarioM += m.salario
    if len(pessoasM) > 0:
        salarioM = salarioM / len(pessoasM)

    salarioF = 0
    for f in pessoasF:
        salarioF += f.salario
    if len(pessoasF) > 0:
        salarioF = salarioF / len(pessoasF)

    idadeM = 0
    for m in pessoasM:
        idadeM += m.idade
    if len(pessoasM) > 0:
        idadeM = idadeM / len(pessoasM)

    idadeF = 0
    for f in pessoasF:
        idadeF += f.idade
    if len(pessoasF) > 0:
        idadeF = idadeF / len(pessoasF)

    return render_template('graficos.html',
                           salarioM=salarioM, salarioF=salarioF, idadeM=idadeM, idadeF=idadeF)
