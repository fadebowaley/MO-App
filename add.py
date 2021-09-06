import random
from select import select
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property

app = Flask(__name__)

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    servers = db.relationship('Server', backref='owner', lazy='dynamic')

    @hybrid_property
    def server_slot_count(self):
        return sum(server.server_slot for server in self.servers)

    @server_slot_count.expression
    def server_slot_count(cls):
        return (
            select([func.sum(Server.server_slot)]).
            where(Server.server_admin == cls.user_id).
            label('server_slot_count')
        )


class Server(db.Model):
    __tablename__ = "server"
    server_id = db.Column(db.Integer, primary_key=True)
    server_admin = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    server_slot = db.Column(db.Integer, unique=False, nullable=False, server_default="32")


@app.route('/')
def index():
    html = []
    for user in User.query.all():
        html.append('User :{user}; Server Count:{count}'.format(user=user.username, count=user.server_slot_count))

    return '<br>'.join(html)


def build_sample_db():
    db.drop_all()
    db.create_all()

    for username in ['DarkSuniuM', 'pjcunningham']:

        user = User(
            username=username,
        )
        db.session.add(user)
        db.session.commit()
        for slot in random.sample(range(1, 100), 5):
            server = Server(
                server_admin=user.user_id,
                server_slot=slot
            )
            db.session.add(server)

        db.session.commit()


if __name__ == '__main__':
    build_sample_db()
    app.run(port=5000, debug=True)