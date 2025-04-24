from flask import render_template
from app import app, db 


@app.errorhandler(404)
def page_not_found(error):
    """Handler function for page not found"""
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    """Handler function for internal server error"""
    db.session.rollback()
    return render_template("500.html"), 500