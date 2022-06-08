from asyncio import tasks
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)#webサーバーインスタンス化
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo_Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/', methods=['GET','POST'])
def index():
  if request.method == 'POST':
    take_content = request.form.get('content')
    new_task = Todo_Post(content=take_content)
    try:
      db.session.add(new_task)
      db.session.commit()
      task = Todo_Post.query.order_by(Todo_Post.date_created).all()
      return render_template('index.html', tasks=task, length=len(task))
    except:
       return "フォームの送信中に問題が発生しました"

  else:
    tasks = Todo_Post.query.order_by(Todo_Post.date_created).all()
    return render_template('index.html', tasks=tasks)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
  task = Todo_Post.query.get(id)
  if request.method == 'GET':
    return render_template('edit.html', task=task)
  else:
    task.content = request.form.get('content')
    try:
       db.session.commit()
       return redirect('/')
    except:
      return "タスクの編集中に問題が発生しました"


@app.route('/delete/<int:id>')#デフォルトがGETなので記載する必要なし
def delete(id):
  task = Todo_Post.query.get(id)
  db.session.delete(task)
  db.session.commit()
  return redirect('/')

if __name__ == "__main__":
    # モデルからテーブルを作成(データベースファイルを最初に作るときだけ実行)
    db.create_all()
    
    # アプリを起動(データベースファイルを最初に作るときはコメントアウトして実行しない)
    app.run(host="127.0.0.1", port=5000)













