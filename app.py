from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Post, CompositeKeyTable
from sqlalchemy.sql import text
from datetime import datetime, date
from flask.json.provider import DefaultJSONProvider


class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, date):
            # Format the datetime object as a string
            return obj.isoformat()
        # Call the base class method for other types
        return super().default(obj)


app = Flask(__name__)

# PostgreSQL 연결 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1q2w3e@localhost/board_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'max_overflow': 20,
    'pool_timeout': 30,
    'pool_recycle': 1800,
    'pool_pre_ping': True
}

db.init_app(app)
app.json = CustomJSONProvider(app)


@app.route('/date-format')
def date_format():
    d = date(2021, 1, 1)
    return jsonify({"date": d})


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


@app.route('/page', methods=['GET'])
def page():
    page = 1
    per_page = 2

    posts = Post.query.offset((page - 1) * per_page).limit(per_page).all()

    total = Post.query.count()
    result = {
        "total": total,
        "page": page,
        "per_page": per_page,
        "items": [
            {"id": post.column_1, "title": post.column_2, "content": post.column_3}
            for post in posts
        ]
    }

    return result


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


@app.route('/composite-key-table', methods=['POST'])
def post_composite_key_table():
    c1 = request.json.get('c1')
    c2 = request.json.get('c2')
    c3 = request.json.get('c3')

    composite_key_tables = CompositeKeyTable(column_1=c1, column_2=c2, column_3=c3)

    db.session.add(composite_key_tables)
    db.session.commit()

    return jsonify({})


@app.route('/composite-key-table', methods=['GET'])
def get_composite_key_table():
    composite_key_tables = CompositeKeyTable.query.all()

    composite_key_table_json = [
        {"c1": c.column_1, "c2": c.column_2, "c3": c.column_3}
        for c in composite_key_tables
    ]

    return jsonify(composite_key_table_json)


if __name__ == '__main__':
    app.run(debug=True)
