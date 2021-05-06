import requests
import time
# global variables
api_key = 'xxxxxxxx'  # your_coinmarketcap_api_key
bot_token = 'xxxxxxxxx'  # your_telegram_bot_token
chat_id = 'xxxxxxxxxx'  # your_telegram_account_chat_id_here
btc_threshold_min = 4000000
btc_threshold_max = 4300000
dgb_threshold_min = 10
dgb_threshold_max = 12
doge_threshold_min = 40
doge_threshold_max = 52
time_interval = 15 * 60  # in seconds


def get_btc_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

    # make a request to the coinmarketcap api
    response = requests.get(url, headers=headers)
    response_json = response.json()
    # extract the bitcoin price from the json data
    btc_price = response_json['data'][0]
    return btc_price['quote']['USD']['price']


def custom_crypto_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC,DOGE,DGB'
    parameters = {
        'convert': 'INR'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }
    # make a request to the coinmarketcap api
    response = requests.get(url, headers=headers, params=parameters)
    response_json = response.json()
    # extract the bitcoin price from the json data

    btc_price = response_json['data']['BTC']['quote']['INR']['price']
    dgb_price = response_json['data']['DGB']['quote']['INR']['price']
    dog_price = response_json['data']['DOGE']['quote']['INR']['price']
    return (btc_price, dgb_price, dog_price)

# function to send_message through telegram


def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"
    # send the msg
    requests.get(url)


# main fn
def main():
    price_list = []
    status = "Drop 🔻"
# infinite loop
    while True:
        # price = get_btc_price()
        crpyto_price = custom_crypto_price()
        btc_price = crpyto_price[0]
        dgb_price = crpyto_price[1]
        doge_price = crpyto_price[2]
        if btc_price > btc_threshold_max:
            status = "UP 💹"

        if dgb_price > dgb_threshold_max:
            status = "UP 💹"

        if doge_price > doge_threshold_max:
            status = "UP 💹"

        price_list.append(btc_price)
        price_list.append(dgb_price)
        price_list.append(doge_price)
        # if the price falls below threshold, send an immediate msg
        if btc_price < btc_threshold_min or btc_price > btc_threshold_max:
            send_message(chat_id=chat_id,
                         msg=f'BTC: price {status} {btc_price}')

        if dgb_price < dgb_threshold_min or dgb_price > dgb_threshold_max:
            send_message(chat_id=chat_id,
                         msg=f'DGB: price {status} {dgb_price}')

        if doge_price < doge_threshold_min or doge_price > doge_threshold_max:
            send_message(chat_id=chat_id,
                         msg=f'DOGE: price {status} {doge_price}')
        # send last 6 btc price
        if len(price_list) >= 6:
            min_max_msg = f"BTC: min:{btc_threshold_min} max:{btc_threshold_max}\nDGB: min:{dgb_threshold_min} max:{dgb_threshold_max}\nDOGE: min:{doge_threshold_min} max:{doge_threshold_max}"
            send_message(chat_id=chat_id, msg=price_list)
            send_message(chat_id=chat_id, msg=min_max_msg)
            # empty the price_list
            print(price_list)
            price_list = []
        # fetch the price for every dash minutes
        time.sleep(time_interval)


# fancy way to activate the main() function
if __name__ == '__main__':
    main()
