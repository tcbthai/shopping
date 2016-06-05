from app.models_sqldb import Product
from app import db


class Cart:
    def __init__(self, session):
        self.session = session

    def add_to_cart(self, request, product_id):
        product = Product.query.get(product_id)
        if 'cart' in self.session:
            for d in self.session['cart']:
                if not d.items():
                    self.clear_cart()
        if 'cart' in self.session:
            if any(product.product_code in d for d in self.session['cart']):
                for d in self.session['cart']:
                    d.update((k, request.form['quantity']) for k, v in d.items() if k == product.product_code)
            else:
                self.session['cart'].append({product.product_code: request.form['quantity']})
        else:
            self.session['cart'] = [{product.product_code: request.form['quantity']}]

        for d in self.session['cart']:
            for k, v in d.items():
                if int(v) == 0:
                    d.clear()

    def total(self):
        total = 0
        if self.get_cart():
            for product in self.get_cart():
                for k, v in product.items():
                    total = total + k.price * int(v) // 1000
        return total

    def get_cart(self):
        buying = []
        if 'cart' in self.session:
            for d in self.session['cart']:
                for k, v in d.items():
                    products = Product.query.filter_by(product_code=k).first()
                    quantity = products.stock if products.stock < int(v) else int(v)
                    buying.append({products: quantity})
        return buying

    def clear_cart(self):
        self.session.pop('cart', None)

    def remove(self, product_code):
        if self.session['cart']:
            for d in self.session['cart']:
                for k, v in d.items():
                    if k == product_code:
                        d.clear()

    def remove_stock(self):
        buying = self.get_cart()
        for d in buying:
            for k, v in d.items():
                k.stock = k.stock - int(v)
                db.session.add(k)
            db.session.commit()
