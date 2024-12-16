from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Post
from sqlalchemy.sql import text

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
    posts_json = [
        {"id": post.column_1, "title": post.column_2, "content": post.column_3}
        for post in posts
    ]
    return jsonify(posts_json)


# 게시글 생성
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.json.get('title')
        content = request.json.get('content')
        new_post = Post(column_2=title, column_3=content)
        db.session.add(new_post)
        db.session.commit()

    return jsonify({})


# 게시글 수정
@app.route('/update/<int:post_id>', methods=['GET', 'PATCH'])
def update(post_id):
    post = Post.query.get_or_404(post_id)

    post.column_2 = request.json.get('title')
    post.column_3 = request.json.get('content')
    db.session.commit()

    return jsonify({})


@app.route('/raw-query', methods=['GET'])
def raw_query():
    query = """
        SELECT *
        FROM public.post 
    """

    result = db.session.execute(text(query), )
    all = result.mappings().all()

    r = [{"title": a.get("column_1"), "content": a.get("column_2")}
         for a in all]

    return jsonify(r)


@app.route('/raw-query-params', methods=['GET'])
def raw_query_params():
    query = """
        SELECT *
        FROM public.post 
        WHERE column_1 = :post_id
    """

    params = {
        "post_id": 2
    }

    result = db.session.execute(text(query), params)
    all = result.mappings().all()

    r = [{"title": a.get("column_1"), "content": a.get("column_2")}
         for a in all]

    return jsonify(r)


if __name__ == '__main__':
    app.run(debug=True)
