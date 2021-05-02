import requests
import time
# global variables
api_key = 'xxxxxxxx-xxxxxxx-xxxxxx-xxxxxx-xxxxxxx'  # your_coinmarketcap_api_key
bot_token = '1xxxxxxxxxx:Axxxxxxxxxxxxxxxxxxxxx'  # your_telegram_bot_token
chat_id = '1234567890'  # your_telegram_account_chat_id_here
btc_threshold_min = dgb_threshold_min = doge_threshold_min = -5
btc_threshold_max = dgb_threshold_max = doge_threshold_max = 5
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
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }
    # make a request to the coinmarketcap api
    response = requests.get(url, headers=headers)
    response_json = response.json()
    # extract the bitcoin price from the json data

    btc_price = response_json['data']['BTC']['quote']['USD']['percent_change_1h']
    dgb_price = response_json['data']['DGB']['quote']['USD']['percent_change_1h']
    dog_price = response_json['data']['DOGE']['quote']['USD']['percent_change_1h']
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
        crpyto_change_output = custom_crypto_price()
        btc_change1h = crpyto_change_output[0]
        dgb_change1h = crpyto_change_output[1]
        doge_change1h = crpyto_change_output[2]
        if btc_change1h > 0:
            status = "UP 💹"

        if dgb_change1h > 0:
            status = "UP 💹"

        if doge_change1h > 0:
            status = "UP 💹"

        price_list.append(btc_change1h)
        price_list.append(dgb_change1h)
        price_list.append(doge_change1h)
        # if the price falls below threshold, send an immediate msg
        if btc_change1h < btc_threshold_min or btc_change1h > btc_threshold_max:
            send_message(chat_id=chat_id,
                         msg=f'BTC: 1hr_chng% {status} {btc_change1h}')

        if dgb_change1h < dgb_threshold_min or dgb_change1h > dgb_threshold_max:
            send_message(chat_id=chat_id,
                         msg=f'DGB: 1hr_chng% {status} {dgb_change1h}')

        if doge_change1h < dgb_threshold_min or doge_change1h > dgb_threshold_max:
            send_message(chat_id=chat_id,
                         msg=f'DOGE: 1hr_chng% {status} {doge_change1h}')
        # send last 6 btc price
        if len(price_list) >= 6:
            send_message(chat_id=chat_id, msg=price_list)
            # empty the price_list
            print(price_list)
            price_list = []
        # fetch the price for every dash minutes
        time.sleep(time_interval)


# fancy way to activate the main() function
if __name__ == '__main__':
    main()
