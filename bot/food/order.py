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
        'item_id' : item_id,
        'order_type' : order_type,
        }
    response = requests.post(url, headers=headers,data=json.dumps(body))
    if response.status_code > 201:
        logger.error("Error: API request unsuccessful.\nresponse status code: " + str(response.status_code)+ "\nresponse: " + str(response.text))
        raise Exception("Error: API request unsuccessful.\nresponse status code: " + str(response.status_code)+ "\nresponse: " + str(response.text))
    logger.info(f"order {order_type}:{item_id} for user {user.id}:{user.username}|{user.first_name} is successful")
    logger.info("response: " + str(response.text))
    return response.json()