"""This is a Flask App that allows for web based user database interaction"""

from flask import Flask
from ProductionCode import data_procesor

app = Flask(__name__)

@app.route('/')
def homepage():
    """Creates a home page that has user instructions"""
    return "Hello, this is the homepage. " \
    "To find the frequency of meeting attended please do /meeting/frequency. " \
    "To find the average number of meeting attended please do /meeting/count. " \
    "To find the number of people with drug arrst counts within " \
    "a range low-high please do /arrests/low/high eg. /arrests/1/3"

@app.errorhandler(404)
def page_not_found(e):
    """Makes a page for the user when an incorrect url is given"""
    return str(e)+" Sorry, wrong format, do this instead /meeting/frequency or /meeting/count" \
    " or arrests/low/high"

@app.errorhandler(500)
def python_bug(e):
    """Makes a page when there is a bug in the underlying python code"""
    return "Eek, a bug: "+str(e)

@app.route('/meeting/frequency', strict_slashes=False)
def get_meeting_freq():
    """Makes a page that runs when a user request is given for meeting data"""
    freq = data_procesor.meeting_frequency()
    return "The average percentage of meetings attended is "+str(freq)+"%"

@app.route('/meeting/count', strict_slashes=False)
def get_meeting_count():
    """Makes a page that runs when a user request is given for meeting data"""
    count = data_procesor.meeting_count()
    return "The average number of meetings attended is "+str(count)

@app.route('/arrests/<lower>/<upper>', strict_slashes=False)
def drug_sale(lower, upper):
    """Determines the route to the drug sale arrests page"""
    return str(data_procesor.drug_sale_arrests(int(lower), int(upper))) + " people"

if __name__ == '__main__':
    app.run()
