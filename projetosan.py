from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Cadastro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.Integer)
    email = db.Column(db.String(100),nullable=False)

    # tive que retirar o data_criada pq dizia que o db não possuía propriedade Datetime(??)
    # data_criada = db.Column(db.Datetime, default=datetime.utcnow)


    def __repr__(self):
        return '<Task %r>' % self.id




@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        #Código do nome
        nome_form = request.form['nome']

        #Código do endereço
        endereco_form = request.form['endereco']

        #Código do telefone
        telefone_form = request.form['telefone']

        #Código do email
        email_form = request.form['email']

        cadastro = Cadastro(nome=nome_form, endereco=endereco_form, telefone=telefone_form, email=email_form)

        try:
        #adicionando as informações à database:
            db.session.add(cadastro)
            db.session.commit()

            return redirect('/')
        except:

            return 'Houve um erro ao adicionar seu cadastro à nossa base de dados '
    else:
        tasks = Cadastro.query.all()
        return render_template("index.html", tasks=tasks)

@app.route('/deletar/<int:id>')
def deletar(id):
    inf_deletada= Cadastro.query.get_or_404(id)

    try:
        db.session.delete(inf_deletada)
        db.session.commit()
        return redirect('/')
    except:
        return 'Houve um problema ao tentar deletar o seu cadastro :/'


@app.route('/atualizar/<int:id>', methods=['POST', 'GET'])
def atualizar(id):
    task = Cadastro.query.get_or_404(id)

    if request.method == "POST":
        task.nome = request.form['nome']
        task.endereco = request.form['endereco']
        task.telefone = request.form['telefone']
        task.email = request.form['email']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Houve um problema ao atualizar o seu cadastro :/'

    else:
        return render_template('atualizar.html', task=task)


if(__name__)== '__main__':
    app.run(debug=True)