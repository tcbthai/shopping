from . import payment
from cart import Cart
from flask import session, render_template, request, redirect, url_for, flash
import braintree
from flask_login import login_required, current_user
from app.models_sqldb import History

cart = Cart(session)

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]


@payment.route('/basket', methods=['GET'])
def basket():
    buying = cart.get_cart()
    total = cart.total()
    return render_template('basket.html', buying=buying, total=total)


@payment.route('/basket/remove/<product_code>')
def remove(product_code):
    cart.remove(product_code)
    return redirect(url_for('.basket'))


@payment.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    transaction = braintree.Transaction.find(transaction_id)
    result = {}
    buying= cart.get_cart()
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
        cart.remove_stock()
        cart.clear_cart()
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('checkout/show.html', transaction=transaction, result=result)


@payment.route('/checkout')
@login_required
def new_checkout():
    client_token = braintree.ClientToken.generate()
    return render_template('checkout/new.html', client_token=client_token)


@payment.route('/checkout', methods=['POST'])
def create_checkout():
    result = braintree.Transaction.sale({
        'amount': cart.total(),
        'payment_method_nonce': request.form['payment_method_nonce'],
    })

    if result.is_success or result.transaction:
        return redirect(url_for('.show_checkout', transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('.new_checkout'))
