import flask
from flask import request
import requests
import json

app = flask.Flask(__name__)

# Dictionary that maps a user identifier to their chat_id
# This acts as your 'case' statement for chat IDs
CHAT_ID_DESTINOS = {
    "user1": "-4818664703", # Replace with actual chat ID for user1
    "user2": "0987654321", # Replace with actual chat ID for user2
    "user3": "1122334455"  # Replace with actual chat ID for user3
}

# The single API endpoint URL
TELEGRAM_API_URL = "https://api.telegram.org/bot8183417686:AAFvDfHVSravXTBVOQYub6QNJrxY7VnFevo/sendMessage"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # 1. Get the data from the Telegram message
        update = request.get_json()
        message_text = update['message']['text']
        
        # 2. Extract the user and the message from the "||" separator
        if '||' in message_text:
            parts = message_text.split('||', 1)
            user_id = parts[0].strip()
            message_to_send = parts[1].strip()
            
            # 3. Get the correct chat ID from the dictionary
            target_chat_id = CHAT_ID_DESTINOS.get(user_id)
            
            if target_chat_id:
                # 4. Prepare the payload with the dynamic chat_id
                payload = {
                    "chat_id": target_chat_id,
                    "text": message_to_send
                }
                
                # 5. Send the POST request to the single API URL
                try:
                    response = requests.post(TELEGRAM_API_URL, json=payload)
                    response.raise_for_status() # Raises an exception for HTTP errors
                    print(f"Message sent to {user_id} (chat_id: {target_chat_id})")
                    return "OK", 200
                except requests.exceptions.RequestException as e:
                    print(f"Error sending the request: {e}")
                    return "Error forwarding message", 500
            else:
                print(f"Unknown user: {user_id}")
                return "Invalid user", 400
        else:
            print("Invalid message format")
            return "Invalid format", 400

# To run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)