from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), nullable=True)
    content = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

@app.route("/<username>", methods=['GET', 'POST'])
def start_page(username):
    if request.method == 'POST':
        new_message = Message(
            user = username,
            content = request.form['content']
        )
        print(new_message.user, new_message.content)
        db.session.add(new_message)
        db.session.commit()

    messages = Message.query.order_by(Message.created_at).all()
    return render_template('index.html.j2', messages=messages, name=username)

try:
    messages = Message.query.order_by(Message.created_at).all()
except:
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)