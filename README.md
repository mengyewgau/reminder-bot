# reminder-bot
Telegram Reminder Bot

# reminder-bot
Telegram Reminder Bot

Simple webhook server that takes in all POST requests, and sends the data automatically via Telegram to the user. 
Best suited for emails and simple notifications.


Telegram Bot Commands 
```
/start [REQUEST_ID]
```
Sets notification status to ACTIVE/ON for users. It can be used to specify 
ID to be associated for the Telegram user as well.

```
/setId REQUEST_ID
```
Specifies the request ID to be associated for the Telegram user.

```
/stop
```
Turns off notifications for the Telegram user.

/status
Check if notifs are active.