import requests,logging,json
from bot.conf import HOST,BASE_URL

logger = logging.getLogger(__name__)




def order(user,meal,meal_id):
    url = f'{BASE_URL}order/{meal}'
    headers = {
        'Content-Type': 'application/json',
        'company':'BASA',
        }
    body = {
        'user_id' : user.id,
        'username' : user.username,
        'user_first_name' : user.first_name,
        'id' : meal_id,
        }
    response = requests.post(url, headers=headers,data=json.dumps(body))
    if response.status_code > 201:
        logger.error("Error: API request unsuccessful.\nresponse status code: " + str(response.status_code)+ "\nresponse: " + str(response.text))
        raise Exception("Error: API request unsuccessful.\nresponse status code: " + str(response.status_code)+ "\nresponse: " + str(response.text))
    logger.info(f"order {meal}:{meal_id} for user {user.id}:{user.username}|{user.first_name} is successful")
    logger.info("response: " + str(response.text))
    return response.json()