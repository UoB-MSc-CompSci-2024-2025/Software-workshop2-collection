import random

from flask import Flask, render_template
from jinja2 import StrictUndefined
from datetime import datetime

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined


# @app.route("/")
# def hello():
#     return "Hello, Alan!"

@app.route('/')
def home():
    return render_template('home.html', name='Logesh')

@app.route('/time')
def logged_in_time():
    now = datetime.now()
    current_date_time = now.strftime('%d-%m-%Y %H:%M:%S')
    return render_template('time.html', current_date_time=current_date_time,)

@app.route('/quotes')
def show_quotes():
    # quotes_list = ["All our dreams can come true if we have the courage to pursue them. ~Walt Disney",
    #                "Good things come to people who wait, but better things come to those who go out and get them. ~Anonymous",
    #                "If you do what you always did, you will get what you always got. ~Anonymous", ]
    quotes_list = get_random_quotes()
    return render_template('quotes.html', quotes_list=quotes_list)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html',
                           name=name,
                           title='Rendering Example')

@app.route('/primeChecker/<number>')
def check_prime_number(number):
    result  = is_prime(number)
    result_text = f'No, the number {number} is not prime number'
    if result:
        result_text = f'Yes, the number {number} is a prime number'
    return render_template('prime_number_checker.html', result_text= result_text)


def get_random_quotes():
    the_quotes_file = open('static/quotes.text', 'r')
    quotes = the_quotes_file.readlines()
    the_quotes_file.close()
    return random.choices(quotes, k=3)

def is_prime(number):
    number = int(number)
    if number <= 1:
        return False

    for i in range(2, number):
        if number % i == 0:
            return False

    return True
