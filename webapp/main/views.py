from flask import Blueprint, redirect, url_for, flash, request, render_template, current_app, session
from flask_login import login_required, logout_user, login_user, current_user
from .forms import EditProfileForm, FundForm, WithdrawalForm, InvestForm, TransferForm
from .. import db, admin
# from werkzeug import security
from ..email import send_deposit_email, send_invest_email, send_share_email, send_withdrawal_email
from ..auth.models import User, Transactions, Investments, Referrer, Share
from ..decorators import has_role
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from datetime import datetime, timedelta
from time import time
from flask_admin import Admin, expose, BaseView, AdminIndexView, helpers



main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='../templates/main'
)



@main_blueprint.route('/')
def index():

    return redirect(url_for('earncoins.home'))


@main_blueprint.route('/dashboard/<username>', methods=["GET", "POST"])
@login_required
def dashboard(username):
    user = User.query.filter_by(username=current_user.username).first()
    invest_history = Investments.query.order_by(Investments.id.desc()).filter_by(user=current_user).limit(3).all()

    return render_template('dashboard.html', user=user, invest_history=invest_history)


@main_blueprint.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=current_user.username).first()

    return render_template(
        'main/profile.html', user=user, username=current_user.username)


@main_blueprint.route('/edit_profile/<username>', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    form = EditProfileForm()
    user = User.query.filter_by(username=current_user.username).first()
    if request.method == "POST":
        user.email = request.form['email']
        user.username = request.form['username']
        user.country = request.form['country']
        user.phone = request.form['phone']
        user.coin = request.form['coin']
        user.wallet_address = request.form['wallet_address']
        # Check for profile pic
        if request.files['profile_pic']:
            user.profile_pic = request.files['profile_pic']

            # Grab Image Name
            pic_filename = secure_filename(user.profile_pic.filename)
            # Set UUID
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            # Save That Image
            saver = request.files['profile_pic']

            # Change it to a string to save to db
            user.profile_pic = pic_name

            try:
                db.session.add(user)
                db.session.commit()
                saver.save(os.path.join(current_app.config['UPLOAD_FOLDER'], pic_name))
                flash("Your Profile has been Updated Successfully!")
                return redirect(url_for('.profile', username=current_user.username))

            except Exception as e:
                print(e)
                if current_user.email == user.email and current_user.username == user.username:
                    flash("Your Profile has been Updated Successfully!")
                    return redirect(url_for('.profile', username=current_user.username))
                else:
                    db.session.rollback(user)
                    flash("Error! Looks like Username or Email is already in use.!")
                    return redirect(url_for('.edit_profile', username=current_user.username))
                    # return render_template("edit_profile.html",
                    #                         form=form,
                    #                         user=user,
                    #                         id=id)
        else:
            db.session.commit()
            flash("User Updated Successfully!")
            return redirect(url_for('.profile', username=current_user.username))

    return render_template("edit_profile.html", form=form, user=user, username=current_user.username)


@main_blueprint.route('/investment/<username>', methods=['GET', 'POST'])
@login_required
def investment(username):
    user = User.query.filter_by(username=username).first()
    form = InvestForm()
    invest_history = Investments.query.order_by(Investments.id.desc()).filter_by(user=current_user)

    if form.validate_on_submit():
        plan = form.investment_plan.data
        investment_amount = form.investment_amount.data
        amount = int(investment_amount)
        try:
            if amount >= (current_user.account_balance - 20):
                flash('Insufficient Balance [ FUND your account ]', category='alert')
                return redirect(url_for('main.investment', username=current_user.username))

            elif (amount >= 100) and (amount <= 499):
                invest = Investments(investment_time=datetime.utcnow(), investment_id=current_user.id, investment_plan='BEGINNER', investment_amount=amount, investment_status='Active')
                current_user.account_balance -= amount
                db.session.add(invest)
                db.session.add(current_user)
                db.session.commit()
                send_invest_email(user)
                flash('[ BEGINNER PLAN ] Activated', category='alert')
                return redirect(url_for('main.investment', username=current_user.username))

            elif (amount >= 500) and (amount <= 1999):
                invest = Investments(investment_time=datetime.utcnow(), investment_id=current_user.id, investment_plan='INTERMEDIATE', investment_amount=amount, investment_status='Active')
                current_user.account_balance -= amount
                db.session.add(invest)
                db.session.add(current_user)
                db.session.commit()
                send_invest_email(user)
                flash('[ INTERMEDIATE PLAN ] Activated', category='alert')
                return redirect(url_for('main.investment', username=current_user.username))

            elif (amount >= 2000) and (amount <= 4999):
                invest = Investments(investment_time=datetime.utcnow(), investment_id=current_user.id, investment_plan='ADVANCED', investment_amount=amount, investment_status='Active')
                current_user.account_balance -= amount
                db.session.add(invest)
                db.session.add(current_user)
                db.session.commit()
                send_invest_email(user)
                flash('[ ADVANCED PLAN ] Activated', category='alert')
                return redirect(url_for('main.investment', username=current_user.username))
#            datetime.datetime.now().date()
            elif amount >= 5000:
                invest = Investments(investment_time=datetime.utcnow(), investment_id=current_user.id, investment_plan='ENTERPRISE', investment_amount=amount, investment_status='Active')
                current_user.account_balance -= amount
                db.session.add(invest)
                db.session.add(current_user)
                db.session.commit()
                send_invest_email(user)
                flash('[ ENTERPRISE PLAN ] Activated', category='alert')
                return redirect(url_for('main.investment', username=current_user.username))

        except Exception as e:
            print(e)

    return render_template(
        'main/investment.html', user=user, form=form, invest_history=invest_history)


@main_blueprint.route('/trans_history/<username>')
@login_required
def history(username):

    user = User.query.filter_by(username=username).first()
    trans_history = Transactions.query.order_by(Transactions.id.desc()).filter_by(user=current_user)
#    share_history = Share.query.order_by(Share.id.desc()).filter_by(share_email=share_email)

    return render_template('main/history.html', user=user, trans_history=trans_history)


@main_blueprint.route('/referrals/<username>')
@login_required
def referrals(username):
    user = User.query.filter_by(username=username).first()
    refs = Referrer.query.filter_by(code=current_user.username).all()
    ref_transactions = Transactions.query.all()

    return render_template('main/referrals.html', user=user, ref_transactions=ref_transactions, refs=refs)


@main_blueprint.route('/fund_acct/<username>', methods=['GET', 'POST'])
@login_required
def funding(username):
    form = FundForm()
    user = User.query.filter_by(username=current_user.username).first()
    if form.validate_on_submit():
        user.deposit_amount = request.form['deposit_amount']
        new_amount = int(user.deposit_amount)
        # Check for profile pic
        if request.files['transaction_image']:
            user.transaction_image = request.files['transaction_image']
            # Grab Image Name
            pic_filename = secure_filename(user.transaction_image.filename)
            # Set UUID
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            # Save That Image
            saver = request.files['transaction_image']

            # Change it to a string to save to db
            user.transaction_image = pic_name

            try:
                trans = Transactions(transaction_time=datetime.utcnow(), transaction_id=current_user.id,
                                     transaction_amount=new_amount, transaction_imgs=pic_name,
                                     transaction_type='DEPOSIT', transaction_status='PENDING',
                                     transaction_email=current_user.email, receiver_email='')
                current_user.referred_deposit = new_amount
                current_user.account_balance += 0
                current_user.total_deposit += new_amount

                db.session.add(trans)
                db.session.add(user)
                db.session.commit()
                saver.save(os.path.join(current_app.config['UPLOAD_FOLDER'], pic_name))

                send_deposit_email(user)
                flash("Transaction processing... ", category='alert')
                return redirect(url_for('.funding', username=current_user.username))

            except Exception as e:
                print(e)
                if new_amount <= 99:
                    flash("Transaction failed", category='alert')



        #return redirect(url_for('main.dashboard', id=current_user.id))
    #transact = Transactions.query.order_by(Transactions.timestamp.desc()).all()
    return render_template('main/funding.html', form=form, user=user)


@main_blueprint.route('/withdrawal/<username>', methods=['GET', 'POST'])
@login_required
def withdrawal(username):
    user = User.query.filter_by(username=current_user.username).first()
    form = WithdrawalForm()
    if form.validate_on_submit():
        withdrawal_amount = form.withdrawal_amount.data
        withdrawal_amount = int(withdrawal_amount)

        if withdrawal_amount <= 99:
            flash("Try again or Top up available balance... ", category='alert')
            return redirect(url_for('.withdrawal', username=current_user.username))
        elif current_user.account_balance <= withdrawal_amount:
            flash("Insufficient balance... ", category='alert')
            return redirect(url_for('.withdrawal', username=current_user.username))
        else:
            trans = Transactions(transaction_time=datetime.utcnow(), transaction_id=current_user.id,
                                 transaction_type='WITHDRAWAL', transaction_amount=withdrawal_amount,
                                 transaction_imgs='', transaction_status='PENDING'
                                 , transaction_email=current_user.email, receiver_email='')
            current_user.account_balance -= withdrawal_amount
            current_user.total_payouts += withdrawal_amount

            db.session.add(trans)
            db.session.commit()
            send_withdrawal_email(user)
            flash("Transaction processing... ", category='alert')
            return redirect(url_for('.withdrawal', username=current_user.username))

        #return redirect(url_for('main.dashboard', id=current_user.id))
    #transact = Transactions.query.order_by(Transactions.timestamp.desc()).all()
    return render_template('main/withdrawal.html', user=user, form=form)


@main_blueprint.route('/share_balance/<username>', methods=['GET', 'POST'])
@login_required
def share_balance(username):
    user = User.query.filter_by(username=username).first()
    form = TransferForm()

    if form.validate_on_submit():
        receiver_email = form.receiver_email.data
        receiver_amount = form.receiver_amount.data
        receiver_amount = int(receiver_amount)

        try:
            if receiver_amount <= (current_user.account_balance - 20):

                credit = User.query.filter_by(email=receiver_email).first()
                credit.account_balance += receiver_amount
                user.account_balance -= receiver_amount
                trans = Transactions(transaction_time=datetime.utcnow(), transaction_id=current_user.id,
                                     transaction_type='SHARE', transaction_amount=receiver_amount,
                                     transaction_imgs='', transaction_status='SUCCESSFUL',
                                     transaction_email=current_user.email)
                received = Share(share_time=datetime.utcnow(), share_id=current_user.id, share_amount=receiver_amount,
                                  share_type='SHARED', share_email=receiver_email)

                db.session.add(received)
                db.session.add(user)
                db.session.add(credit)
                db.session.add(trans)
                db.session.commit()
                send_share_email(user)
                flash(f"You shared ${receiver_amount} successfully to {receiver_email} ", category='alert')
                return redirect(url_for('main.share_balance', username=current_user.username))
        except Exception as e:
            print(e)
            if receiver_amount > current_user.account_balance:
                db.session.rollback()
                flash("Transaction failed [ Fund your account] ", category='alert')

    return render_template('main/transfer_funds.html', user=user, form=form)

