from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False, unique = True)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    @validates('name')
    def validate_name(self, key, name):
        names = db.session.query(Author.name).all()
        if not name:
             raise ValueError("Name field is required.")
        elif name in names:
            raise ValueError("Name must be unique.")
        return name
            
    @validates('phone_number')
    def validate_phone(self, key, number):
        if len(number) != 10:
            raise ValueError('Phone number must be 10 digits long')
        return number


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True )
    title = db.Column(db.String, nullable = False)
    content = db.Column(db.String, nullable = True)
    category = db.Column(db.String)
    summary = db.Column(db.String, nullable = True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates('content', 'summary')
    def validate_length(self, key, post):
        if (key == 'content'):
            if len(post) <= 250:
                raise ValueError("Post content must be greater than 250 characters.")
        if (key == 'summary'):
            if len(post) >= 250:
                raise ValueError("Post dummer must be less than 250 chatacters")
        return post
    
    @validates('title')
    def validate_title(self, key, title):
        clickbait = ["Won't Belive", "Secret", "Top", "Guess"]
        if not any(substring in title for substring in clickbait):
            raise ValueError('No clickbait found')
        return title

    @validates('category')
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError("Category must be Fiction or Non-Fiction.")
        return category            
