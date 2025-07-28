from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your API key from exchangerate-api
API_KEY = "02d9460dcada7df4b06c9a4c"

@app.route('/', methods=['POST'])
def index():
    try:
        data = request.get_json()

        # Extract data from Dialogflow request
        source_currency = data['queryResult']['parameters']['unit-currency']['currency']
        amount = data['queryResult']['parameters']['unit-currency']['amount']
        target_currency = data['queryResult']['parameters']['currency-name']

        # Get conversion factor
        conversion_factor = fetch_conversion_factor(source_currency, target_currency)

        # Calculate converted amount
        converted_amount = round(amount * conversion_factor, 4)

        # Prepare response for Dialogflow
        response = {
            "fulfillmentText": f"{amount} {source_currency} is {converted_amount} {target_currency}."
        }

        return jsonify(response)

    except Exception as e:
        print("Error:", str(e))
        return jsonify({
            "fulfillmentText": f"Sorry, I couldn't convert the currency due to an error: {str(e)}"
        })


def fetch_conversion_factor(source_currency, target_currency):
    # Make request to exchangerate-api
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{source_currency}"
    res = requests.get(url)
    data = res.json()

    # Ensure response is valid
    if data['result'] != 'success':
        raise Exception("Failed to fetch exchange rates.")

    # Get conversion rate for target currency
    return data['conversion_rates'][target_currency]


if __name__ == "__main__":
    app.run(debug=True, port=5000)
