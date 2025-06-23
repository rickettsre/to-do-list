from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to-do-list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)

class TaskAdd(FlaskForm):
    title = StringField('Your task description', validators=[DataRequired()])
    submit = SubmitField('Add Task')

class TaskEdit(FlaskForm):
    title = StringField('Your task description', validators=[DataRequired()])
    complete = StringField('Complete?', validators=[DataRequired()])
    submit = SubmitField('Submit Changes')

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    
    
@app.route("/")
def home():
    task_data = Task.query.all()
    for task in task_data:
        print(task.title, task.complete, type(task.complete))
    return render_template("index.html", task_data=task_data)

@app.route("/add_task", methods=['GET', 'POST'])    
def add_task():
    form = TaskAdd()
    if form.validate_on_submit():
        task = Task(title=form.title.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form=form)

@app.route("/edit/<int:task_id>", methods=['GET', 'POST'])
def edit(task_id):
    task_to_edit = Task.query.get(task_id)
    form = TaskEdit(obj=task_to_edit)
    if form.validate_on_submit():
        task_to_edit.title = form.title.data
        task_to_edit.complete = form.complete.data
        task_to_edit.complete = form.complete.data.lower() in ['true', '1', 'yes', 'on']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form, task=task_to_edit)


@app.route("/delete/<int:task_id>", methods=['GET', 'POST'])
def delete(task_id):
    task_to_delete = Task.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
     with app.app_context():
        db.create_all()  # ✅ Now runs inside app context  
     app.run(debug=True)
