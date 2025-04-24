import csv
from flask import Flask
from ProductionCode import data_procesor

app = Flask(__name__)

@app.route('/')
def homepage():
    """Creates a home page that has user instructions"""
    return "Hello, this is the homepage. " \
    "To find the frequency of meeting attended please do (url)/meeting/frequency"

@app.errorhandler(404)
def page_not_found(e):
    """Makes a page for the user when an incorrect url is given"""
    return "sorry, wrong format, do this instead (url)/meeting/frequency"

@app.errorhandler(500)
def python_bug(e):
    """Makes a page when there is a bug in the underlying python code"""
    return "Eek, a bug!"

@app.route('/meeting/frequency', strict_slashes=False)
def get_meeting_freq():
    """Makes a page that runs when a user request is given for meeting data"""
    freq = data_procesor.meeting_frequency()
    return "The average percentage of meetings attended is "+str(freq)+"%"

if __name__ == '__main__':
    app.run()
