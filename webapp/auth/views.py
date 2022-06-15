from flask import (render_template, request,
                   Blueprint,
                   redirect,
                   url_for,
                   flash, session)
from flask_login import login_required, logout_user, login_user, current_user
from .forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from .models import User, db, Referrer, current_app
from ..email import send_email, send_password_reset_email, send_confirmation_email
# from flask_babel import _


auth_blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='../templates/auth',
    url_prefix="/auth"
)


@auth_blueprint.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth_blueprint.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)

            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)

        flash('Invalid username or password.')

    return render_template('auth/login.html', form=form, remember=True)


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, account_balance=int(20), total_deposit=int(0)
                    , total_payouts=int(0))
        user.set_password(password=form.password.data)

        user.generate_ref()

        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # send_email(user.email, 'Confirm Your Account',
        #            'auth/email/confirm', user=user, token=token)
        send_confirmation_email(user)


        if 'h_ecns' in session:
            referral_code = session['h_ecns']
            # collect details for Referrer

            collect = Referrer(user_referred=form.email.data, code=referral_code)
            db.session.add(collect)
            db.session.commit()

            try:
                referring_user = User.query.filter_by(referral_code=referral_code).first()
                if referring_user:
                    # increment referring users count
                    referring_user.referrals += 1
                    db.session.commit()

                    # get or create referral codes in db
                    refer = Referrer.query.filter_by(referral_code=referral_code).first()
                    if refer:
                        user.referrer = refer.id
                        db.session.commit()
                    else:
                        referrer = Referrer(referral_code=referral_code)
                        db.session.add(referrer)
                        db.session.commit()
            except Exception as e:
                print(e)
                session.pop('h_ecns', None)
            return redirect(url_for('auth.login'))

        flash('A confirmation email has been sent to you by email. Due to Google policy update Check [spam mail] if mail does not appear in [inbox] and click on [not spam] to get Earncoins updates')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_blueprint.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
        return redirect(url_for('auth.login'))
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth_blueprint.route('/confirm')
@login_required
def resend_confirmation():
    # token = current_user.generate_confirmation_token()
    user = current_user
    send_confirmation_email(user)
    # send_email(current_user.email, 'Confirm Your Account',
    #            'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth_blueprint.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            ('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=('Reset Password'), form=form)


@auth_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', token=token, form=form)


