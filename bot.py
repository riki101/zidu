# -*- coding: utf-8 -*-
import telebomb, Settings

# Some declarations
bot = telebomb.Bot(Settings.BOT_TOKEN)

@bot.handle()
def do(message):
	if message.new_chat_members:
		bot.req(
			"sendMessage",
			data={
				"chat_id": message.chat.id,
				"text": Settings.WELCOME_MESSAGE % ", ".join(user['first_name'] for user in message.new_chat_members)
			}
		)
	elif message.new_chat_member:
		bot.req(
			"sendMessage",
			data={
				"chat_id": message.chat.id,
				"text": Settings.WELCOME_MESSAGE % message.new_chat_member.first_name
			}
		)

bot.polling()