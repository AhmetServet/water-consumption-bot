from db.db import DB
import telebot
import dotenv, os
from datetime import datetime, timedelta
import pytz
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot_logging import logger

dotenv.load_dotenv()

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(bot_token)
logger.info("Bot started!")

db = DB("water-consumptions.db")
logger.info(f"Database connected! Conn: {db.conn}")

tz = pytz.timezone('Asia/Istanbul')
logger.info(f"Timezone set to {tz}.")



@bot.message_handler(commands=['start'])
def start(message):
    try:
        db.add_user(message.from_user.id, message.from_user.username, message.date)
        logger.info(f"User {message.from_user.username} started the bot. User ID: {message.from_user.id}, added to the database.")
        bot.reply_to(message, 'Welcome to Water Consumption Bot! You can add your water consumption by clicking /add command. You can also view your water consumption by clicking /view command.')

    except Exception as e:
        print(e)
        logger.error(f"Error adding user {message.from_user.username} to the database. Already exists.")
        bot.reply_to(message, 'You have already started the bot. Click /add to add water consumption or /view to view your water consumption.')

@bot.message_handler(commands=['add'])
def add(message):
    logger.info(f"User {message.from_user.username} clicked /add command.")

    bot.reply_to(message, 'Please enter the amount of water you consumed in milliliters.')
    bot.register_next_step_handler(message, add_water_consumption)

def add_water_consumption(message):
    try:
        amountML = int(message.text)
        db.add_water_consumption(message.from_user.id, message.date, amountML)

        logger.info(f"User {message.from_user.username} added {amountML} mL of water.")
        
        bot.reply_to(message, f'You added {amountML} mL of water.')
    except ValueError:
        logger.error(f"User {message.from_user.username} entered an invalid number.")
        bot.reply_to(message, 'Please enter a valid number.')


# Function to handle /view command and show date selection
@bot.message_handler(commands=['view'])
def view(message):
    logger.info(f"User {message.from_user.username} clicked /view command.")

    user_id = message.from_user.id
    user_signup_date = db.get_user(user_id)[2]  # Assuming this is the signup date in timestamp format

    if user_signup_date:
        # Convert signup date from timestamp to datetime
        
        dt = datetime.fromtimestamp(int(user_signup_date), tz)
        date_diff = (datetime.now(tz) - dt).days + 1

        logger.info(f"User {message.from_user.username} signed up on {dt}. Date difference: {date_diff} days.")

        # Create inline buttons for date selection
        markup = InlineKeyboardMarkup()

        for i in range(date_diff + 1):
            selected_date = (dt + timedelta(days=i)).strftime('%Y-%m-%d')
            markup.add(InlineKeyboardButton(selected_date, callback_data=f'date_select:{selected_date}'))
        # Send date selection message
        bot.send_message(message.chat.id, 'Please select a date:', reply_markup=markup)
    else:
        logger.error(f"Signup date not found for user {message.from_user.username}.")
        bot.reply_to(message, 'Signup date not found.')

# Function to handle the selected date and show consumption for that date
@bot.callback_query_handler(func=lambda call: call.data.startswith('date_select'))
def handle_date_selection(call):
    selected_date = call.data.split(":")[1]  # Extract the selected date

    logger.info(f"User {call.from_user.username} selected date: {selected_date}.")

    user_id = call.from_user.id

    # Convert selected date to timestamp for querying the database
    selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
    start_of_day = int(selected_date_obj.timestamp())
    end_of_day = int((selected_date_obj + timedelta(days=1)).timestamp())

    # Fetch water consumption for the selected date
    water_consumption = db.get_water_consumption_for_date(user_id, start_of_day, end_of_day)
    logger.info(f"User {call.from_user.username} water consumption on {selected_date} is fetched from the database.")

    if water_consumption:
        for wc in water_consumption:
            # Create inline buttons for update and delete
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Delete", callback_data=f'delete:{wc[0]}'),
                       InlineKeyboardButton("Update", callback_data=f'update:{wc[0]}'))
            
            # Display the consumption entry with buttons
            bot.send_message(call.message.chat.id, f'You consumed {wc[3]} mL of water on {tz.localize(datetime.fromtimestamp(int(wc[2])))}.', reply_markup=markup)
        
        # Display the total water consumption for the selected date
        total_consumption = sum([wc[3] for wc in water_consumption])
        bot.send_message(call.message.chat.id, f'Total water consumption for {selected_date}: {total_consumption} mL.\n Equivalent to { (total_consumption / 600):.2f} in 600mL.')
    
        logger.info(f"Total water consumption for {selected_date} is displayed to user {call.from_user.username}.")
    else:
        # If no water consumption is recorded for the selected
        bot.send_message(call.message.chat.id, 'No water consumption recorded for this date.')

    # Answer the callback to remove the "loading" icon in Telegram
    bot.answer_callback_query(call.id)


# Handle delete and update actions
@bot.callback_query_handler(func=lambda call: call.data.startswith('delete'))
def delete_water_consumption(call):
    logger.info(f"User {call.from_user.username} clicked delete button.")

    consumption_id = call.data.split(":")[1]
    db.delete_water_consumption(consumption_id) 
    
    logger.info(f"Water consumption entry {consumption_id} deleted.")

    bot.answer_callback_query(call.id, 'Water consumption entry deleted.')
    bot.delete_message(call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('update'))
def update_water_consumption(call):
    logger.info(f"User {call.from_user.username} clicked update button.")

    consumption_id = call.data.split(":")[1]
    bot.answer_callback_query(call.id, 'Please enter the updated amount of water in milliliters.')
    bot.register_next_step_handler(call.message, process_update, consumption_id)

def process_update(message, consumption_id):
    try:
        amountML = int(message.text)

        logger.info(f"User {message.from_user.username} updated water consumption entry {consumption_id} to {amountML} mL.")

        db.update_water_consumption(consumption_id, amountML)
        bot.reply_to(message, f'Updated water consumption to {amountML} mL.')
    except ValueError:
        bot.reply_to(message, 'Please enter a valid number.')

bot.polling(none_stop=True)



