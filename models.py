from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):
    __tablename__ = 'post'
    column_1 = db.Column(db.Integer, primary_key=True)
    column_2 = db.Column(db.String(100), nullable=False)
    column_3 = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>'


class CompositeKeyTable(db.Model):
    __tablename__ = 'composite_key_table'
    column_1 = db.Column(db.Integer, primary_key=True)
    column_2 = db.Column(db.String(100), nullable=False)
    column_3 = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>'