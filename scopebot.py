import os
import datetime
import time
import string
import argparse

from dotenv import load_dotenv
from slack import WebClient
from slack.errors import SlackApiError

#to run script: python scopeboy/scopebot.py -p "YOUR SLACK BOT TOKEN" -channel "#test-bot"

#add the slack bot to the channels you want to count the word 'scope' in the slack app.
 
def get_slack_history(client):
    '''get the last week of slack messages across all channels the bot is part of.'''
    
    channel_ids = [channel['id'] for channel in client.conversations_list()['channels'] if channel['is_private'] == False]
    
    messages = []
    time_stamp = datetime.datetime.now(tz=None)
    last_week = time_stamp - datetime.timedelta(days=7)
    
    for channel_id in channel_ids:
        try:
            response = client.conversations_history(
                channel=channel_id,
                latest=time.mktime(time_stamp.timetuple()),
                oldest=time.mktime(last_week.timetuple()),
                inclusive=True
            )
            if response['messages']:
                messages.extend(text['text'] for text in response['messages'])

            else:
                print('no messages!')

            return messages

        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")

def scope_counter(channel_text):
    '''counts the number of times words begin with 'scop' across channel messages.'''
   
    scope_counter = 0    
    if channel_text is not None:
        for text in channel_text:
            text = text.translate(str.maketrans('', '', string.punctuation))
            text = text.lower()
            if text.startswith('scop'):
                scope_counter += 1
                
        return f'We said some version of the word "scope" {scope_counter} times this week! So the scoping talk rages on...'
    
    else:
        print('no messages!')

def scopebot(client, channel_name='#test-bot'):
    '''scopebot.'''
    try:       
        slack_messages = get_slack_history(client)  
        response = client.chat_postMessage(
            channel=channel_name,
            text=scope_counter(slack_messages),
            icon_emoji= ':chart_with_upwards_trend:'

        )
        
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]  
        print(f"Got an error: {e.response['error']}")

        
# Start your app
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--password', help='slack bot token')
	parse.add_argument('-channel', '--channel', help='channel name scopebot will message to')
	
	args=parser.parse_args()
	SLACK_TOKEN = args.password
	channel_name = args.channel

	client = WebClient(token=SLACK_TOKEN)
	scopebot(client, channel_name)