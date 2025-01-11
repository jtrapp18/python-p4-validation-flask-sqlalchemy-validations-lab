from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 

    @validates('name')
    def validate_name(self, key, name):

        existing_author = Author.query.filter_by(name=name).first()

        if not name or existing_author:
            raise ValueError("Must have a unique name")

        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone):
        phone_pattern = r"[0-9]{10}"
        phone_regex = re.compile(phone_pattern)

        if not phone_regex.fullmatch(phone):
            raise ValueError("Author phone numbers must be exactly ten digits.")
        return phone

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        category_options = ["Fiction", "Non-Fiction"]
        if category not in category_options:
            raise ValueError("Post category must be either Fiction or Non-Fiction.")
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        title_options = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(option in title for option in title_options):
            raise ValueError("Post title must contain one of the following:", title_options)
        return title
    
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
