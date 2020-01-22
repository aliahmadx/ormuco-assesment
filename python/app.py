from flask import Flask, render_template, flash, request
from flaskext.mysql import MySQL
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'ormuco'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_SOCKET'] = None

mysql.init_app(app)

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    favcolor = TextField('Email:', validators=[validators.required()])
    catdog = TextField('Password:', validators=[validators.required()])

    @app.route("/", methods=['GET', 'POST'])
    def hello():
        form = ReusableForm(request.form)

        print form.errors
        if request.method == 'POST':
            name=request.form['name']
            favcolor=request.form['favcolor']
            catdog=request.form['catdog']



        return render_template('hello.html', form=form)

    @app.route("/result", methods=['GET', 'POST'])
    def result():
        if request.method == 'POST':
            result = request.form
            name=request.form['name']
            favcolor=request.form['favcolor']
            catdog=request.form['catdog']


            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * from MyUsers where Name = %s", name)
            data = cursor.fetchone()

            if data:
                cursor.close()
                return '<html><body>Name already Exists!</body></html>'
            else:
                cursor.execute("INSERT INTO MyUsers(name, favcolor, catdog) VALUES (%s, %s, %s)", (name, favcolor, catdog))
                conn.commit()
                cursor.close()
                return render_template("result.html",result = result)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

