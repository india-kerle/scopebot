import os
import datetime
import time
import string
import argparse

from slack import WebClient
from slack.errors import SlackApiError

#to run script: python scopebot.py -c "#test-bot" -p "YOUR SLACK BOT TOKEN"

#add the slack bot to the channels you want to count the word 'scope' in the slack app.
 
def get_slack_history(client):
    '''get the last week of slack messages across all channels the bot is part of.'''
    
    channel_ids = [channel['id'] for channel in client.conversations_list()['channels'] if channel['is_member'] == True]

    time_stamp = datetime.datetime.now(tz=None)
    last_week = time_stamp - datetime.timedelta(days=7)

    channel_messages = []
    for channel_id in channel_ids:
        try:
            rs = client.conversations_history(
                    channel=channel_id,
                    latest=time.mktime(time_stamp.timetuple()),
                    oldest=time.mktime(last_week.timetuple()),
                    inclusive=True)
            if rs['messages']:
                for channel_message in rs['messages']:
                    if 'bot_id' not in channel_message.keys():
                        channel_messages.append(channel_message['text'])
            else:
                print('no messages!')
    
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")
    
    return channel_messages

def scope_counter(channel_text):
    '''counts the number of times words begin with 'scop' across channel messages.'''
    
    scope_counts = []
    if channel_text is not None:
        for text in channel_text:
            text = text.translate(str.maketrans('', '', string.punctuation))
            text = text.lower()
            for t in text.split(' '):
                if t.startswith('scop'):
                    scope_counts.append(t)

        return f'We said some version of the word "scope" {len(scope_counts)} times this week! So the scoping talk rages on...'
    
    else:
        print('no messages!')

def scopebot(client, channel_name='#test-bot'):
    '''scopebot.'''
    try:       
        slack_messages = get_slack_history(client)  
        response = client.chat_postMessage(
            channel=channel_name,
            text=scope_counter(slack_messages),
        )
        
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]  
        print(f"Got an error: {e.response['error']}")

        
# Start your app
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--password', help='slack bot token')
	parser.add_argument('-c', '--channel', help='channel name scopebot will message to')
	
	args = parser.parse_args()
	SLACK_TOKEN = args.password
	channel_name = args.channel

	client = WebClient(token=SLACK_TOKEN)
	scopebot(client, channel_name)