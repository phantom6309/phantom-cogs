import json

def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {'trakt_credentials': {}, 'tracked_users': {}, 'last_activity': {}, 'channel_id': None}
    if 'last_activity' not in data:
        data['last_activity'] = {}
    return data

def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
      
