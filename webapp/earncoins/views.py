from flask import render_template, Blueprint, flash, redirect, url_for, session, request
from flask_login import login_required, current_user
from ..auth.models import Referrer, User
#from ..decorators import admin_required, permission_required
from .forms import CalculatorForm
import decimal
import random


earncoins_blueprint = Blueprint(
    'earncoins',
    __name__,
    template_folder='../templates/earncoins',
    url_prefix="/earncoins",
    static_url_path='',
    static_folder='webapp/static',
)


@earncoins_blueprint.route('/ecns/<string:referral_code>')
def new_referral(referral_code):
    #if its a new user, get the user that referred them. Save referrer in a cookie. Redirect to signup
    if referral_code:
        try:
            user = User.query.filter_by(referral_code=referral_code).first()
            if user:
                session['h_ecns'] = user.referral_code
        except:
            pass

    return redirect(url_for('auth.register'))


@earncoins_blueprint.route('ecns', methods=['GET'])
def refer():

    if 'h_email' in session:
        try:
            email = session['h_email']
            user = User.query.filter_by(email=email).first_or_404()
            if user:
                referral_code = user.referral_code
                referrals = user.referrals

        except:
            session.pop('h_email', None)
            redirect(url_for('earncoins.home'))
    else:
        return redirect(url_for('earncoins.home'))

    return render_template('refer.html', referral_code=referral_code, referrals=referrals)


@earncoins_blueprint.route('/home', methods=["GET", "POST"])
def home():
    action = ['DEPOSIT', 'WITHDRAWAL']
    coin = ['Bitcoin', 'Ethereum', 'Litecoin']
    time = ['Less than a', '2', '4', '5', '11', '10', '20', '30', '3', '7', '14', '6', '19', '1', '9', '16', '17', '23', '35', '65']
    country = ['New Zealand ', 'Singapore ', 'Hong Kong ', 'Denmark ', 'South Korea ','United States ','Georgia ','United Kingdom ','Norway ','Sweden ','Lithuania ','Malaysia ','Mauritius ','Australia ','Taiwan ','United Arab Emirates ','Macedonia ','Estonia ',
               'Latvia ', 'Finland ', 'Thailand ', 'Germany ', 'Canada ', 'Ireland ', 'Kazakhstan ', 'Iceland ', 'Austria ', 'Russia ', 'Japan ','Spain ','China ','France ','Turkey ','Azerbaijan ','Israel ','Switzerland ','Slovenia ','Rwanda ','Portugal ','Poland ','Czech Republic ','Netherlands ','Bahrain ','Serbia ','Slovakia '
                , 'Belgium ', 'Armenia ', 'Moldova ', 'Belarus', 'Croatia ']
    names = ['Kendall ','Kinsley ','Madison','Willow ','Graham ','Huxley ','Carter ','Sawyer ','Araminta ','Winston ','Birch ','Arden ','Huffington ','Dane ','Clover ','Wang ','Li ','Zhang ','Chen ','Yang ','Asad ','Islam ','Faheem ','Ekram ','Dawoud ','Habib','Hafizullah ','Kamil ','Kazem ','Ahmad ','Aleksy ','Alina ','Andnej ','Apoloniusz',' Daniela ','Leon ','Luka '
             , 'Tobias', 'Elias', ' Anne', 'Ania', 'Oliver ', 'Harry ','George ','Sophia ','Emily ','Amelia ','Isabella ','Anwen ','Nora ']
    amount = ['175','300','500','268','1,000','2,100','760','4,000','5,620','465','890','7,100','256','543','190','208','645','7,900','1,500','9,000','14,500','550','195','330','410','698','33,000','712','9,856','937','345','2,345','70,000','867','5,887','895','345','5,643','853','1,246','3,000','429','643','5,867','6,465','560','290','308','746','7,646','6452','747']

    form = CalculatorForm()
    if request.method == "POST" and form.validate_on_submit():
        plan = request.form['plan']
        invest = request.form['amount']
        invest_amt = float(invest)
        plan_select = float(plan)
        if invest_amt and plan_select:
            min_daily = invest_amt * plan_select
            max_daily = invest_amt * (plan_select + float(0.05))
            min_days = (invest_amt * plan_select) * 4
            max_days = (invest_amt * (plan_select + float(0.05))) * 4
            min_balance = invest_amt + min_days
            max_balance = invest_amt + max_days
            flash(f" Daily: ${min_daily} - ${max_daily}   *   4 Days: ${min_days} - ${max_days}"
                  f"   *   Total: ${min_balance} - ${max_balance} ", category='success')
        else:
            pass

    return render_template(
        'home.html', form=form, coin=coin, time=time, country=country, names=names, amount=amount, action=action)


@earncoins_blueprint.route('/pricing')
def pricing():

    return render_template(
        'pricing.html'
    )


@earncoins_blueprint.route('/FAQs')
def faqs():

    return render_template(
        'faqs.html'
    )


@earncoins_blueprint.route('/terms')
def terms():

    return render_template(
        'terms.html'
    )


@earncoins_blueprint.route('/About')
def about():

    return render_template(
        'about.html'
    )


@earncoins_blueprint.route('/referrals')
@login_required
#@permission_required(Permission.BASIC)
def ref():

    return render_template(
        'referrals.html'
    )


@earncoins_blueprint.route('/privacy')
def privacy():

    return render_template(
        'privacy.html'
    )

@earncoins_blueprint.route('/leaderboard')
#@admin_required
def leaderboard():
    leaders = Referrer.query.order_by(Referrer.entries.desc()).all()
    print(leaders)
    return render_template('leaderboard.html', leaders=leaders)

