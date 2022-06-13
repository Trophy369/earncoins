import os
from webapp import db, migrate, create_app
from webapp.auth.models import User, Referrer, Role, Transactions, Investments


env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())

UPLOAD_FOLDER = 'webapp/static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, migrate=migrate, Referrer=Referrer, Role=Role,
                Transactions=Transactions, Investments=Investments)


if __name__ == '__main__':
    app.run(debug=False)
