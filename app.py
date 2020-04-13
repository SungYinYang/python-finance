from flask import Flask, request
import yfinance as yf
import datetime
import time


now = time.strftime("%c")

app = Flask(__name__)

def print_stock_price(history):
    symbol=''
    if(history[1] - history[0] >=0):
        symbol = '+'
    priceDiff = history[1] - history[0]
    pricePercent = priceDiff/history[0]
    return ( str(round(history[1], 2)) +" "+ symbol+ str(round(priceDiff, 2))+" ("+symbol+ str(("%.2f" % round(pricePercent, 2))+"%)"))

def get_day_of_week(num):
    switcher = {
        1: "Mon",
        2: "Tue",
        3: "Wed",
        4: "Thu",
        5: "Fri",
        6: "Sat",
        7: "Sun"
    }
    return switcher.get(num)

def get_month(num):
    switcher = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    return switcher.get(num)

def print_time():
    cur = datetime.datetime.now()

    day_of_week = get_day_of_week(cur.isoweekday())
    month = get_month(cur.month)
    date = str(cur.day)
    time = '{date:%H:%M:%S}'.format( date=datetime.datetime.now())
    timeZone= 'PDT'
    year = str(cur.year)
    #print(day_of_week, month, date, time, timeZone, year)
    return (day_of_week+" "+month+" "+date+" "+time+" "+timeZone+" "+year)

def print_name(information):
    return (information['longName']+ "(" + information['symbol']+")")

@app.route('/', methods=['GET', 'POST']) #allow both GET and POST requests
def index():
    if request.method == 'POST':  #this block is only entered when the form is submitted

        try:
            symbol = request.form['symbol']
            msft = yf.Ticker(symbol)
            hist = msft.history(period="2d")

            time = print_time()
            name = print_name(msft.info)
            price = print_stock_price(hist.Close)

        except:
            name="there is an error in the input"
            curr_time=" yFinance do not have this stock's information."
            price = " Please try another valid input such as 'msft', 'aapl' or 'googl'"

        return '''<title>Python Finance Info - Individual Homework</title>
            <form method="POST">
                <h3>Python Finance Info - Individual Homework</h3><br/>
                <i>Input:</i><br/><br/>
                Enter a stock symbol <input type="text" name="symbol">
                <input type="submit" value="Submit"><br/><br/>
            </form>
            <i>Output: </i><br/><br/> {} <br/> {} <br/> {} </h5>'''.format(name, time, price)

    return '''<title>Python Finance Info - Individual Homework</title>
        <form method="POST">
            <h3>Python Finance Info</h3><br/>
            <i> Input: </i><br/><br/>
            Enter a stock symbol: <input type="text" name="symbol"><br/>
            <input type="submit" value="Submit"><br/>
        </form>'''

@app.errorhandler(AttributeError)
def attribute_error_handle(e):
    return '''{}'''.format(e)

@app.errorhandler(ValueError)
def value_error_handle(e):
    return '''{}'''.format(e)

@app.errorhandler(404)
def page_not_found(e):
    return '''{}'''. format(e)

@app.errorhandler(500)
def internal_server_error(e):
    return '''{}'''. format(e)

if __name__ == '__main__':
    app.run(debug=True)
