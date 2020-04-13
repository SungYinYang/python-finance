from flask import Flask, request
from iexfinance import Stock
import iexfinance.utils.exceptions as excep
import time

now = time.strftime("%c")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST']) #allow both GET and POST requests
def index():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        stock = request.form['symbol']
        symbol = Stock(stock)

        name = symbol.get_company_name() + " (" + str(stock) +  ")\n\n"
        curr_time = now
        price = str(symbol.get_price()) + " " + str(symbol.get_quote().get('change')) + " (" + str(symbol.get_quote().get('changePercent')) + ")"

        return '''<title>Python Finance Info</title>
            <form method="POST">
                <h3>Python Finance Info</h3><br/>
                <i>Input:</i><br/><br/> 
                Enter a symbol <input type="text" name="symbol">
                <input type="submit" value="Submit"><br/><br/>
            </form>
            <i>Output: </i><br/><br/> {} <br/> {} <br/> {} </h5>'''.format(name, curr_time, price)

    return '''<title>Python Finance Info</title>
        <form method="POST">
            <h3>Python Finance Info</h3><br/>
            <i> Input: </i><br/><br/>
            Enter a symbol: <input type="text" name="symbol"><br/>
            <input type="submit" value="Submit"><br/>
        </form>'''

@app.errorhandler(excep.IEXSymbolError)
def symbol_error_handle(e):
    return '''{} Please enter a valid ticker symbol!'''.format(e)

@app.errorhandler(excep.IEXEndpointError)
def endpoint_error_handle(e):
    return '''{}'''.format(e)

@app.errorhandler(excep.IEXFieldError)
def field_error_handle(e):
    return '''{}'''.format(e)

@app.errorhandler(excep.IEXQueryError)
def query_error_handle(e):
    return '''{}'''.format(e)

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