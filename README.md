

# python-telegram-bot-heroku
A guide to hosting a telegram bot created using the python-telegram-bot library with heroku.
![Deploy your Ember project to Heroku from Github - Philip Mutua ...](https://miro.medium.com/max/3600/1*fIjRtO5P8zc3pjs0E5hYkw.png)
See the full article explaining the steps [here](https://towardsdatascience.com/how-to-deploy-a-telegram-bot-using-heroku-for-free-9436f89575d2). 

## Getting Started
Before you begin, you will need a Telegram bot API token from [BotFather](https://t.me/botfather). 

1. Download the three files in this repo: bot.py (containing your python code for the Telegram bot), requirements.txt (containing the python libraries to be installed), and Procfile (containing the command to execute the python file).
2. Login / [create](https://signup.heroku.com/dc) a Heroku account.
3. Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). 
4. Install the [Heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up). 
5.  Once installed, you can use the _heroku_ command in your terminal / command prompt. Go to the same directory as the files in this repository, and type:

> heroku login

A new window will be opened in your browser prompting you to login, so just click on the button.

6. Once you are logged in, go back to the command line. Type in
> heroku create

to create your new webapp. Heroku will assign your webapp a name as well as the link to your webapp, which should be of the format [https://{yourherokuappname}.herokuapp.com/.](https://yourherokuappname.herokuapp.com/.) 

7. To the bot.py file, change the TOKEN variable to the API token of your telegram bot, and change the yourherokuappname to the name of your heroku app in the line

> updater.bot.setWebhook('https://yourherokuappname.herokuapp.com/'  + TOKEN)

8. Next, in your command line, type the following commands in the following order:

> git init   
> git add .   
> git commit -m "first commit"

> heroku git:remote -a YourAppName

> git push heroku master

(Make sure to replace YourAppName with the name of your Heroku webapp)

You should then see the following messages:

![](https://cdn-images-1.medium.com/max/1000/1*y3JH7a7mY4oYFaAjDCA1Ow.png)

In particular, it will say that a Python app is detected and it will install the required libraries in the requirements.txt file using pip. Then, it will read the Procfile which specifies that the bot.py file is to be executed.

9. Go to your conversation with your Telegram bot on Telegram and type /start. The bot should be working now!

Since you are using the free plan on heroku, the bot will sleep after 30 minutes of inactivity. So do expect the bot to take a few seconds to respond to your /start if you are using it more than 30 minutes after it was previously used. Other than that, the bot will respond almost instantaneously~ 

## What to do if your Bot stops responding
I’ve noticed the bot stops responding after about 24 hours of inactivity (because we are using the free version of Heroku), so if you want to “jolt” the bot awake, one way is to make a change to one of the files (eg. changing the python3 in the procfile to python and vice versa) and then committing the changes with the lines below:
> git add .   
> git commit -m "changing python3 to python in Procfile"   
> git push heroku master

You should see again see the messages about a Python app being detected and once it finishes executing, your bot should revive now!
