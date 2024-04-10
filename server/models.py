import re
from flask_sqlalchemy import SQLAlchemy
import requests

from sqlalchemy.orm import validates
db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Author name is required")
        return value
    
    def requires_unique_name(self):
        with app.app_context():
            author_a = Author(name='Ben', phone_number='1231144321')
            db.session.add(author_a)
            db.session.commit()
            with pytest.raises(ValueError):
                    author_b = Author(name='Ben', phone_number='1231144321')
                    db.session.query(Author).delete()
                    db.session.commit()



    @validates('phone_number')
    def validate_phonenumber(self, key, number):
        if len(number) != 10:
            raise ValueError("Phone number has to be exactly 10 digits")

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # __table_args__ = (
    #     UniqueConstraint('title', name='unique_title'),
    # )

    @validates('title')
    def validate_post_title(self, key, value):
        if not value:
            raise ValueError("Post title is required")
        return value

    @validates('content')
    def validate_post_content(self, key, value):
        if value and len(value) < 250:
            raise ValueError(
                "Post content must be at least 250 characters long")
        return value

    @validates('summary')
    def validate_post_summary(self, key, value):
        if value and len(value) >= 250:
            raise ValueError(
                "Post summary must be a maximum of 250 characters")
        return value

    @validates('category')
    def validate_post_category(self, key, value):
        if value not in ["Fiction", "Non-Fiction"]:
            raise ValueError(
                "Post category must be either Fiction or Non-Fiction")
        return value
    

    @validates('clickbait_validator')
    def validate_clickbait(self, key, value):
        if value:
            if not any(word in value.lower() for word in ['amazing', 'incredible', '10x', 'secret', 'one weird trick']):
                return value
            else:
                raise ValueError("Post content contains clickbait language")
            return value
    




    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'