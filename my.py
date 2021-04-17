from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MAX_CONTENT_LENGTH = 1024 * 1024
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text, nullable=False)
    data = db.Column(db.LargeBinary)

    def __repr__(self):
        return self.title


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/buy/<int:id>')
def buy_item(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/do1500')
def do1500():
    items = Item.query.order_by(Item.price).all()
    return render_template('do1500.html', data=items)


@app.route('/vse')
def vse():
    items = Item.query.order_by(Item.price).all()
    return render_template('vse.html', data=items)


@app.route('/do1000')
def do1000():
    items = Item.query.order_by(Item.price).all()
    return render_template('do1000.html', data=items)


@app.route('/do500')
def do500():
    items = Item.query.order_by(Item.price).all()
    return render_template('do500.html', data=items)


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']

        item = Item(title=title, price=price, description=description)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except Exception:
            return "404 error"
    else:
        return render_template('admin.html')


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
