# Roger
## Discord Event Reminder Bot
### Purpose
Roger is a Discord bot who reminds users of certain events. To ask Roger to set a reminder, use the '$rogerRemind' command in a reply followed by a correctly formatted date and time. At the specified date and time, Roger will DM the user the original message as a reminder. 
### Bot Commands
* **$rogerHelp** This command will send a list of commands.  
* **$rogerRemind** This command DMs you reminders for messages you REPLIED to. This command only works when you reply to a message.   
    * **FORMAT**: *$rogerRemind DD/MM/YYYY HH:MM AM/PM* 
* **$rogerFormat** This command helps you format reminders that you'll use with the '$rogerRemind' command.  
* **$rogerFormatEvent** This command provides a template to detail information for an event.  

### Notes
* Roger is not able to handle edited messages. If you ask Roger to remind you of a message, but in the meantime the message has been edited, Roger will remind you of the original message NOT the edited message.  
* Roger currently only works for a specified timezone. Hence, this bot is most useful if all members of a server are from the same timezone. 

### Credits
Thanks to Carberra Tutorials I was able to get the general setup of my bot. Here's his GitHub https://github.com/Carberra/updated-discord.py-tutorial and his YouTube channel https://www.youtube.com/channel/UC13cYu7lec-oOcqQf5L-brg. 
