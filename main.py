# main.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/document_repository'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)

@app.route('/documents', methods=['GET', 'POST'])
def documents():
    if request.method == 'POST':
        data = request.json
        new_document = Document(title=data['title'], content=data['content'], status=data['status'])
        db.session.add(new_document)
        db.session.commit()
        return jsonify({'message': 'Document created successfully'}), 201
    elif request.method == 'GET':
        documents = Document.query.all()
        result = [{'id': document.id, 'title': document.title, 'content': document.content, 'status': document.status} for document in documents]
        return jsonify(result)

@app.route('/documents/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def document(id):
    document = Document.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({'id': document.id, 'title': document.title, 'content': document.content, 'status': document.status})
    elif request.method == 'PUT':
        data = request.json
        document.title = data['title']
        document.content = data['content']
        document.status = data['status']
        db.session.commit()
        return jsonify({'message': 'Document updated successfully'})
    elif request.method == 'DELETE':
        db.session.delete(document)
        db.session.commit()
        return jsonify({'message': 'Document deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
