from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://aftqclexuoqfdn:8cd43090a0ff5e5f7435aa3f2b82624a496f96983952f5b45dec822e5458f82b@ec2-54-236-137-173.compute-1.amazonaws.com:5432/d4meqodolojqtn'
db = SQLAlchemy(app)


class TODO(db.Model):
    num = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.Text, nullable=False)
    start = db.Column(db.Text, nullable=False, default=str(datetime.utcnow))
    end = db.Column(db.Text, nullable=False, default=str(datetime.utcnow))
    complete = db.Column(db.Boolean)

    def __repr__(self):
        return "NUM : "+str(self.num)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        post_todo = request.form['todo']
        post_start = request.form['start']
        post_end = request.form['end']
        db.session.add(TODO(todo=post_todo, start=post_start,
                            end=post_end, complete=False))
        db.session.commit()
        return redirect('/')
    else:
        todo1 = TODO.query.all()
        return render_template("home.html", Todo=todo1)


@app.route('/update/<int:num>')
def update(num):
    todo = TODO.query.filter_by(num=num).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect('/')


@app.route('/delete/<int:num>')
def delete(num):
    post_delete = TODO.query.get_or_404(num)
    db.session.delete(post_delete)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
