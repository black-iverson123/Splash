from app import create_app, socketio, db
from app.extensions.models import User


app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User':User}

if __name__=='__main__':
    app.app_context().push()
    db.create_all()
    socketio.run(app, host="0.0.0.0", port=int("5000"), debug=True, allow_unsafe_werkzeug=True)

