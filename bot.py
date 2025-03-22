import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:\n/show_city <город> - показать город на карте\n/show_my_cities - показать все сохраненные города\n/remember_city <город> - сохранить город")

@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    city_name = message.text.split(maxsplit=1)[-1]
    path = f"{city_name}.png"
    coordinates = manager.get_coordinates(city_name)
    if coordinates:
        manager.create_graph(path, [city_name])
        with open(path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, "Город не найден в базе данных.")

@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split(maxsplit=1)[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    if cities:
        path = "my_cities.png"
        manager.create_graph(path, cities)
        with open(path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, "У вас пока нет сохраненных городов.")

if __name__ == "__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
