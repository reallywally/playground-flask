from flask import Flask, render_template, request, redirect, url_for
from models import db, Post

app = Flask(__name__)

# PostgreSQL 연결 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1q2w3e@localhost/board_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 데이터베이스 초기화
with app.app_context():
    db.create_all()

# 게시판 목록
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

# 게시글 생성
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

# 게시글 수정
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', post=post)

# 게시글 삭제
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
