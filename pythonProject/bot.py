from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from MAIN import Trip

TOKEN: Final = '7148147033:AAF9NFgnEs5FnB1DWY7MfWWjnfNjYbJhYls'
BOT_USERNAME: Final = '@Dispatch_one_bot'
# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text('Hello Nigga')

# Responses
def handle_response(text: str):
	processed: str = '\n' + text
	if 'hello' in processed.lower():
		return f'hello muchacho'
	if 'нахуй' in processed.lower() or 'naxuy' in processed.lower():
		return 'Озин пошёл нахуй.🤬j'
	if 'Spot' in processed:
		processed = processed.split(sep='\n')
		trip = Trip(processed)
		trip.build_message()
		return trip.message + '\nPlease confirm?'

	return f'🤬🤬🤬 Copy the text correctly dude'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
	message_type: str = update.message.chat.type
	text: str = update.message.text

	print(f'User ({update.message.chat.id}) in {message_type} :"{text})"')
	if message_type == 'group':
		if BOT_USERNAME in text:
			new_text: str = text.replace(BOT_USERNAME, '').strip()
			response: str = handle_response(new_text)
		else:
			return
	else:
		response: str = handle_response(text)
	print('BOT:', response)
	await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
	print(f'Update "{update}" caused error "{context.error}"')


if __name__ == '__main__':
	app = Application.builder().token(TOKEN).build()
	# Commands
	app.add_handler(CommandHandler('start', start_command))
	# Messages
	app.add_handler(MessageHandler(filters.TEXT, handle_message))
	# Errors
	app.add_error_handler(error)

	# Polls
	print("Polling....")
	app.run_polling(poll_interval=3)