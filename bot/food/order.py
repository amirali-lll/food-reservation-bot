import requests,logging,json
from bot.conf import HOST,BASE_URL

logger = logging.getLogger(__name__)




def order(user,order_type,item_id):
    url = f'{BASE_URL}orders/order/'
    headers = {
        'Content-Type': 'application/json',
        'company':'BASA',
        }
    body = {
        'telegram_id' : user.id,
        'username' : user.username,
        'user_first_name' : user.first_name,
        'user_last_name' : user.last_name,
        'item_id' : item_id,
        'order_type' : order_type,
        }
    response = requests.post(url, headers=headers,data=json.dumps(body))
    if response.status_code > 201:
        raise Exception(response.text)
        
    logger.info(f"order {order_type}:{item_id} for user {user.id}:{user.username}|{user.first_name} is successful")
    logger.info("response: " + str(response.text))
    return response.json()


def order_rice(user,have_rice):
    order_type = 'rice'
    url = f'{BASE_URL}orders/order/'
    headers = {
        'Content-Type': 'application/json',
        'company':'BASA',
        }
    body = {
        'telegram_id' : user.id,
        'username' : user.username,
        'user_first_name' : user.first_name,
        'user_last_name' : user.last_name,
        'order_type' : order_type,
        'rice' : have_rice,
        }
    response = requests.post(url, headers=headers,data=json.dumps(body))
    if response.status_code > 201:
        raise Exception(response.text)
        
    logger.info(f"order {order_type}={have_rice} for user {user.id}:{user.username}|{user.first_name} is successful")
    logger.info("response: " + str(response.text))
    return response.json()



def get_today_orders():
    url = f'{BASE_URL}orders/today'
    headers = {
        'Content-Type': 'application/json',
        'company':'BASA',
        }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Error: API request unsuccessful.\nresponse status code: " + str(response.status_code)+ "\nresponse: " + str(response.text))
    return response.json()


def delete_order(user):
    url = f'{BASE_URL}orders/order/'
    headers = {
        'Content-Type': 'application/json',
        'company':'BASA',
        }
    body = {
        'telegram_id' : user.id,
        'username' : user.username,
        'user_first_name' : user.first_name,
        }
    response = requests.delete(url, headers=headers,data=json.dumps(body))
    if response.status_code == 404:
        return "اصلا سفارشی برات ثبت نشده بود 🤷‍♂️"
    elif response.status_code != 204:
        return "مشکلی تو پاک کردن سفارش پیش اومده 😕"
    return "سفارشت پاک شد  🥲"


def fetch_today_export():
    url = f'{BASE_URL}orders/today_export'
    headers = {
        'Content-Type': 'application/json',
        'company':'BASA',
        }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Error: API request unsuccessful.\nresponse status code: " + str(response.status_code)+ "\nresponse: " + str(response.text))
    return response.json()

def today_export():
    orders_summery = fetch_today_export()
    text = "سفارشات امروز:\n\n"
    foods = orders_summery['foods']
    desserts = orders_summery['desserts']
    beverages = orders_summery['beverages']
    rice_count = orders_summery['rice_count']
    for food in foods:
        text += f"{food['name']} : {food['count']} عدد\n"
    text += f"\n\nبرنج : {rice_count} عدد\n\n"
    for dessert in desserts:
        text += f"{dessert['name']} : {dessert['count']} عدد\n"
    text += "\n\n"
    for beverage in beverages:
        text += f"{beverage['name']} : {beverage['count']} عدد\n"
    return text