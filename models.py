from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author name is required.")
        # Ensure name is unique in the database
        existing_author = Author.query.filter(Author.name == name).first()
        if existing_author:
            raise ValueError(f"Author name '{name}' must be unique.")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone_number

    def __repr__(self):
        return f'<Author(id={self.id}, name={self.name})>'


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
    def validate_content_length(self, key, content):
        if not content or len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return content

    @validates('summary')
    def validate_summary_length(self, key, summary):
        if not summary or len(summary) > 250:
            raise ValueError("Post summary cannot exceed 250 characters.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ["Fiction", "Non-Fiction"]
        if category not in valid_categories:
            raise ValueError(f"Post category must be one of {valid_categories}.")
        return category

    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError(
                "Post title must include one of the following clickbait phrases: "
                "'Won't Believe', 'Secret', 'Top', or 'Guess'."
            )
        return title

    def __repr__(self):
        return f'<Post(id={self.id}, title={self.title})>'
