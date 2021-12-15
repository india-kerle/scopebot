### Scopebot

Are people constantly using the word 'scope' or scoping' to describe the next project you're working on in your work slack? Use this script to count the number of times people use some variation of the word 'scope' across slack channels the scopebot. Your scopebot will post the total number to a channel of your choice. 

You'll need to create a slack app and have generated a slack bot token to use. Read more about how [to do so here](https://api.slack.com/apps).

To run the script:

```
git clone git@github.com:india-kerle/scopebot.git
conda create --name scopebot python=3.9
pip install -r requirements.py
python scopebot.py -p "YOUR SLACK BOT TOKEN" -channel "#test-bot"
```
