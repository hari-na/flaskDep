from flask import Flask, request
import requests, os, datetime

app = Flask(__name__)

# Finnhub API endpoint
finnhub_api_url = 'https://finnhub.io/api/v1/stock/candle'

@app.route('/candle-data', methods=['GET'])
def get_candle_data():
    # Get query parameters from request URL
    stock_symbol = request.args.get('symbol')
    sta_date = request.args.get('start')
    end_date = request.args.get('end')

    # Intermediatary Objects
    sta_obj = datetime.datetime.strptime(sta_date, '%d-%m-%Y')
    end_obj = datetime.datetime.strptime(end_date, '%d-%m-%Y')
    # Convert dates to Unix timestamps
    start_unix_time = int(sta_obj.timestamp())
    end_unix_time = int(end_obj.timestamp())

    # Construct API query parameters
    api_query_params = {
        'symbol': stock_symbol,
        'resolution': 'D',
        'from': start_unix_time,
        'to': end_unix_time,
        'token': 'cf31a9iad3i7csbbt00gcf31a9iad3i7csbbt010'
    }

    # Call Finnhub API to get candle data
    response = requests.get(finnhub_api_url, params=api_query_params)

    # Upload candle data to MongoDB collection
    data = response.json()
    os.system(f'mongosh "mongodb+srv://diyaasanthosh.fljw0uj.mongodb.net/candle_data" --apiVersion 1 --username 20z327 --password CrazyLakshu --eval "db.candle_data.insertOne({data})"')
    print("data uploaded")
    # Download stored candle data from MongoDB collection
    stored_data = os.popen(f'mongosh "mongodb+srv://diyaasanthosh.fljw0uj.mongodb.net/candle_data" --apiVersion 1 --username 20z327 --password CrazyLakshu --eval "JSON.stringify(db.candle_data.find().limit(1).sort({{$natural:-1}}).next())"').read()

    # Return stored candle data
    return jsonify(stored_data)
