"""
Demonstrate using hidden form fields as a way of 
preserving state from one request to the next.  In some 
situations, hidden fields can be a useful alternative to 
using cookies (the session variable). 
"""

import flask
import logging

# Our own modules
import config

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration(proxied=(__name__ != "__main__"))
app.secret_key = CONFIG.SECRET_KEY  # Should allow using session variables


###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    """The main page of the application.
    In this app, we will carry state from screen
    to screen in hidden fields.  Initially we 
    know nothing. 
    """
    flask.g.link_local = flask.url_for("time")
    flask.g.link_external = flask.url_for("time", _external=True)
    app.logger.debug("Links '{}' and '{}'".format(flask.g.link_local, flask.g.link_external))
    return flask.render_template('index.html')

###
# Hijacking this project for an experiment with timezones
###
@app.route("/time")
def time():
    """Time form.  Can I get the local time zone 
    of the user?  
    """
    flask.g.proposed_time = "4-5am on Saturday, because it sounds terrible"
    return flask.render_template('timezone.html')





#######################
# Form handlers.
# At each step, we stash and retrieve information
# from hidden fields 
#######################

@app.route("/_step", methods=["POST"])
def step():
    """
    User has submitted a form.  They may have provided some 
    information, and we may have stashed some information 
    in the form. 
    """
    app.logger.debug("Entering step")

    #
    flask.g.color = flask.request.form.get("color")
    flask.g.number = flask.request.form.get("number")
    flask.g.fruit = flask.request.form.get("fruit")
    next_form = flask.request.form.get("next_form")
    return flask.render_template(next_form)

###################
#   Error handlers
###################


@app.errorhandler(404)
def error_404(e):
    app.logger.warning("++ 404 error: {}".format(e))
    return flask.render_template('404.html'), 404


@app.errorhandler(500)
def error_500(e):
    app.logger.warning("++ 500 error: {}".format(e))
    assert not True  # I want to invoke the debugger
    return flask.render_template('500.html'), 500


@app.errorhandler(403)
def error_403(e):
    app.logger.warning("++ 403 error: {}".format(e))
    return flask.render_template('403.html'), 403


####

if __name__ == "__main__":
    if CONFIG.DEBUG:
        app.debug = True
        app.logger.setLevel(logging.DEBUG)
    app.logger.info(
            "Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
