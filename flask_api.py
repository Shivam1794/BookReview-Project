from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from gensim.downloader import load
import pickle

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<username>:<your_password>@<host>:<port>/<database_name>'
db = SQLAlchemy(app)

# Database Models
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    summary = db.Column(db.Text, nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.String(100), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)


# Load the model components from the pickle file
with open('D:\\BooksReview Project\\recommendation_model.pkl', 'rb') as file:
    model_components = pickle.load(file)

# Extract components from Pickle File
word2vec_model = model_components['word2vec_model']
le = model_components['label_encoder']
scaler = model_components['scaler']
cosine_sim = model_components['cosine_sim']
df = model_components['df']
content_based_df = model_components['books_similarity_matrix']

# API Endpoints

# Add Books to table
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = Books(**data)
    try:
        db.session.add(new_book)
        db.session.commit()
        return jsonify({"message": "Book added"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Error adding book"}), 400

# Get Books detail from table
@app.route('/books', methods=['GET'])
def get_books():
    books = Books.query.all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'genre': book.genre,
        'year_published': book.year_published,
        'summary': book.summary
    } for book in books])

# Get details of a particular book from table
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Books.query.get(id)
    if book:
        return jsonify({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'year_published': book.year_published,
            'summary': book.summary
        })
    return jsonify({"message": "Book not found"}), 404


# Update book details in table
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Books.query.get(id)
    if book:
        data = request.json
        for key, value in data.items():
            setattr(book, key, value)
        db.session.commit()
        return jsonify({"message": "Book updated"})
    return jsonify({"message": "Book not found"}), 404

# Delete a particular book from the table
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Books.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted"})
    return jsonify({"message": "Book not found"}), 404

# Add review about a book in table
@app.route('/books/<int:id>/reviews', methods=['POST'])
def add_review(id):
    book = Books.query.get(id)
    if book:
        data = request.json
        review = Review(book_id=id, **data)
        db.session.add(review)
        db.session.commit()
        return jsonify({"message": "Review added"}), 201
    return jsonify({"message": "Book not found"}), 404

# Get reviews of a particular book from table
@app.route('/books/<int:id>/reviews', methods=['GET'])
def get_reviews(id):
    reviews = Review.query.filter_by(book_id=id).all()
    return jsonify([{
        'id': review.id,
        'user_id': review.user_id,
        'review_text': review.review_text,
        'rating': review.rating
    } for review in reviews])

# Get summary of a particular book from table
@app.route('/books/<int:id>/summary', methods=['GET'])
def get_summary(id):
    book = Books.query.get(id)
    if book:
        reviews = Review.query.filter_by(book_id=id).all()
        avg_rating = sum(review.rating for review in reviews) / len(reviews) if reviews else None
        return jsonify({
            'summary': book.summary,
            'average_rating': avg_rating
        })
    return jsonify({"message": "Book not found"}), 404

# Get recommendations of books
@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    # content_based_df = generate_recommendations_df()
    recommendations = content_based_df.to_dict(orient='records')
    return jsonify(recommendations)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)