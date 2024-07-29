# ГИТХАБ АВТОРА: github.com/resppl
# СКРИПТ НА ГИТХАБЕ: github.com/resppl/TelegramRemotePC
# САЙТ АВТОРА: resppl.ru

import os, pyautogui, subprocess, keyboard, psutil, sqlite3, cv2, pyaudio, wave, asyncio, time

from shutil import rmtree, disk_usage
from ctypes import windll
from telebot import types, TeleBot
from typing import List
from random import randint
from time import sleep
import urllib.parse
from platform import uname
from pygetwindow import getActiveWindowTitle
from http.client import HTTPConnection
from webbrowser import open as webopen
from datetime import datetime
from screen_brightness_control import set_brightness, get_brightness

conn = sqlite3.connect('visitors.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS visitors (id INTEGER PRIMARY KEY)''')
conn.commit()
conn.close()


conn = sqlite3.connect('fulldostup.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users_with_access (user_id INTEGER PRIMARY KEY)''')
conn.commit()
conn.close()

KEYS = ["enter", "backspace", "space", "tab", "ctrl+a", "ctrl+z", "ctrl+c", "ctrl+v", "ctrl+s", "ctrl+shift+esc"]
CMDS = ['tasklist', 'ping']

title_files_and_folders = "📂 Управление файлами и папками"
title_keys = "⌨️ Управление клавишами"
title_console = "💻 Управление консолью"
title_settings_pc = "⚙️ Настройки ПК"
title_trolling = "😈 Троллинг"
title_specfunc = "🛠️ Специальные функции"
title_info_cmd = "💡 Информация о скрипте"

text_give_access = "✅ Выдать полный доступ"
text_list_access = "📋 Список пользователей с полным доступом"
text_remove_access = "❌ Отобрать полный доступ"


wrong_choice = "❌ *Неверный выбор! Повторите попытку*"

back_text = "◀️ Вернуться"

file_menu_create_files_and_folders = "📋 Создать файл / папку"
file_menu_delete_files_and_folders = "🗑 Удалить файл / папку"
file_menu_edit_files = "✏️ Изменить файл"
file_menu_start_programm = "🚀 Запустить исполняемый файл"
file_menu_download_file_by_pc = "⬇️ Скачать файл с ПК"
file_menu_upload_file_to_pc = "⬆️ Выгрузить файл на ПК"

console_menu_enter_commands = "⌨️ Ввести команду"
console_menu_start_python_script = "🗄 Запустить скрипт Python"
console_menu_screenshot = "🖥 Сделать скриншот экрана"
console_menu_webcam = "📸 Сделать фото веб-камеры"
console_menu_webvideocam = "📹 Записать видео на камеру"
console_menu_check_directories = "📂 Директория компьютера"
console_menu_microphone = "🎙 Записать голос"
console_menu_open_site = "🌐 Открыть сайт"
console_menu_create_msgbox = "❗️ Создать сообщение в диалоговом окне (MSGBOX)"
console_menu_list_process = "📋 Список активных процессов"

keys_menu_write = "⌨️ Напечатать текст"
keys_menu_press_keys = "⌨️ Нажать на клавишу"
keys_menu_media_keys = "▶️⏸⏹ Нажать на медиа-клавишу"

settings_pc_menu_change_brightness = "☀️ Изменить яркость экрана"
settings_pc_menu_info_pc = "🖥 Информация о ПК"
settings_pc_menu_change_volume = "🔊 Изменить громкость"

packs_menu_open_sites = "🌐 Открыть множество сайтов"
packs_menu_open_conductors = "📂 Открыть множество проводников"
packs_menu_moving_mouse = "🖱 Перемещение мышки"
packs_menu_open_cmds = "🗄 Открыть несколько окон командной консоли"

admin_panel_text = "🔒 Административная панель"

specfunc_menu_restart_pc = "🔄 Перезагрузить компьютер"
specfunc_menu_logout_your_account = "👤 Выйти из учетной записи"
specfunc_menu_turn_off_pc = "❌ Выключить компьютер"
specfunc_menu_logout_script = "📂 Выйти из скрипта"
specfunc_menu_delete_script_by_folders = "📂 Удалить папку со скриптом"

specfunc_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
specfunc_keyboard.add(types.KeyboardButton(specfunc_menu_restart_pc), types.KeyboardButton(specfunc_menu_logout_your_account), types.KeyboardButton(specfunc_menu_turn_off_pc))
specfunc_keyboard.add(types.KeyboardButton(specfunc_menu_logout_script), types.KeyboardButton(specfunc_menu_delete_script_by_folders))
specfunc_keyboard.add(types.KeyboardButton(back_text))


mainmenu_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
mainmenu_keyboard.add(types.KeyboardButton(title_files_and_folders), types.KeyboardButton(title_keys))
mainmenu_keyboard.add(types.KeyboardButton(title_console), types.KeyboardButton(title_settings_pc))
mainmenu_keyboard.add(types.KeyboardButton(title_trolling), types.KeyboardButton(title_specfunc))
mainmenu_keyboard.add(types.KeyboardButton(title_info_cmd))

mainmenu_keyboard_admin = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
mainmenu_keyboard_admin.add(types.KeyboardButton(title_files_and_folders), types.KeyboardButton(title_keys))
mainmenu_keyboard_admin.add(types.KeyboardButton(title_console), types.KeyboardButton(title_settings_pc))
mainmenu_keyboard_admin.add(types.KeyboardButton(title_trolling), types.KeyboardButton(title_specfunc))
mainmenu_keyboard_admin.add(types.KeyboardButton(title_info_cmd), types.KeyboardButton(admin_panel_text))


back_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
back_keyboard.add(types.KeyboardButton(back_text))

change_file_menu_text_add_content = "➕ Добавить содержимое"
change_file_menu_text_full_edit_content = "✏️ Полностью изменить содержимое"
change_file_menu_text_clear_file = "🗑 Очистить файл"

delete_menu_text_delete_file = "🗑 Удалить файл"
delete_menu_text_delete_folder = "🗑 Удалить папку"

download_on_pc_menu_text_upload_photo = "⬆️🖼 Выгрузить фотографию"
download_on_pc_menu_text_upload_other = "⬆️📂 Выгрузить другое"

files_menu_check_text_create_file = "➕ Создать файл"
files_menu_check_text_create_folder = "➕ Создать папку"

media_keys_text_start_or_pause = "▶️⏸⏹ Старт / Остановить"

if_confirm = "Да, подтверждаю"
if_deny = "Нет, я передумал"

full_dostup_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
full_dostup_keyboard.add(types.KeyboardButton(text_give_access))
full_dostup_keyboard.add(types.KeyboardButton(text_list_access))
full_dostup_keyboard.add(types.KeyboardButton(text_remove_access))
full_dostup_keyboard.add(types.KeyboardButton(back_text))

pc_settings_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
pc_settings_keyboard.add(types.KeyboardButton(settings_pc_menu_change_brightness), types.KeyboardButton(settings_pc_menu_info_pc), types.KeyboardButton(settings_pc_menu_change_volume))
pc_settings_keyboard.add(types.KeyboardButton(back_text))

packs_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
packs_keyboard.add(types.KeyboardButton(packs_menu_open_sites), types.KeyboardButton(packs_menu_open_conductors))
packs_keyboard.add(types.KeyboardButton(packs_menu_moving_mouse), types.KeyboardButton(packs_menu_open_cmds))
packs_keyboard.add(types.KeyboardButton(back_text))

logout_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
logout_keyboard.add(types.KeyboardButton(if_confirm), types.KeyboardButton(if_deny))

off_computer_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
off_computer_keyboard.add(types.KeyboardButton(if_confirm), types.KeyboardButton(if_deny))

reboot_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
reboot_keyboard.add(types.KeyboardButton(if_confirm), types.KeyboardButton(if_deny))

menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu_keyboard.add(types.KeyboardButton(keys_menu_write), types.KeyboardButton(keys_menu_press_keys), types.KeyboardButton(keys_menu_media_keys))
menu_keyboard.add(types.KeyboardButton(back_text))

media_keys_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
media_keys_keyboard.add(types.KeyboardButton(media_keys_text_start_or_pause))
media_keys_keyboard.add(types.KeyboardButton(back_text))

console_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
console_menu_keyboard.add(types.KeyboardButton(console_menu_enter_commands), types.KeyboardButton(console_menu_start_python_script))
console_menu_keyboard.add(types.KeyboardButton(console_menu_screenshot), types.KeyboardButton(console_menu_open_site))
console_menu_keyboard.add(types.KeyboardButton(console_menu_webcam), types.KeyboardButton(console_menu_webvideocam))
console_menu_keyboard.add(types.KeyboardButton(console_menu_microphone), types.KeyboardButton(console_menu_list_process))
console_menu_keyboard.add(types.KeyboardButton(console_menu_create_msgbox), types.KeyboardButton(console_menu_check_directories))
console_menu_keyboard.add(types.KeyboardButton(back_text))

files_menu_check_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
files_menu_check_keyboard.add(types.KeyboardButton(files_menu_check_text_create_file), types.KeyboardButton(files_menu_check_text_create_folder))
files_menu_check_keyboard.add(types.KeyboardButton(back_text))

files_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
files_menu_keyboard.add(types.KeyboardButton(file_menu_create_files_and_folders), types.KeyboardButton(file_menu_delete_files_and_folders))
files_menu_keyboard.add(types.KeyboardButton(file_menu_edit_files), types.KeyboardButton(file_menu_start_programm))
files_menu_keyboard.add(types.KeyboardButton(file_menu_download_file_by_pc), types.KeyboardButton(file_menu_upload_file_to_pc))
files_menu_keyboard.add(types.KeyboardButton(back_text))

script_exit_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
script_exit_keyboard.add(types.KeyboardButton(if_confirm), (types.KeyboardButton(if_deny)))

download_on_pc_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
download_on_pc_menu_keyboard.add(types.KeyboardButton(download_on_pc_menu_text_upload_photo), types.KeyboardButton(download_on_pc_menu_text_upload_other))
download_on_pc_menu_keyboard.add(types.KeyboardButton(back_text))

delete_menu_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
delete_menu_keyboard.add(types.KeyboardButton(delete_menu_text_delete_file), types.KeyboardButton(delete_menu_text_delete_folder))
delete_menu_keyboard.add(types.KeyboardButton(back_text))

change_file_menu_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
change_file_menu_keyboard.add(types.KeyboardButton(change_file_menu_text_add_content), types.KeyboardButton(change_file_menu_text_full_edit_content), types.KeyboardButton(change_file_menu_text_clear_file))
change_file_menu_keyboard.add(types.KeyboardButton(back_text))

admin_panel_text_access_control = "🗝️ Управление полным доступом"

access_control_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
access_control_keyboard.add(text_give_access)
access_control_keyboard.add(text_remove_access)
access_control_keyboard.add(text_list_access)

admin_panel_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_panel_keyboard.add(types.KeyboardButton(admin_panel_text_access_control))
admin_panel_keyboard.add(types.KeyboardButton(back_text))

directories_check_all_directories = "📂 Посмотреть всю директорию компьютера"
directories_search_directories = "📂 Выбрать директорию компьютера"

directories_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
directories_keyboard.add(types.KeyboardButton(directories_check_all_directories))
directories_keyboard.add(types.KeyboardButton(directories_search_directories))
directories_keyboard.add(types.KeyboardButton(back_text))

TOKEN = "YOUR_BOT_TOKEN_HERE" # TOKEN вашего бота
ACCESS = YOUR_ID_TELEGRAM # ID вашего аккаунта телеграм

LOGGING = False # если вы хотите, чтобы логи отображались, то установите значение True, если нет, то оставьте как есть (False)

bot = TeleBot(TOKEN, parse_mode=None) 
pyautogui.FAILSAFE = False

try:
    def make_temp_folder():    
        os.mkdir(r'C:\temp')
        kernel32 = windll.kernel32
        attr = kernel32.GetFileAttributesW(r'C:\temp')
        kernel32.SetFileAttributesW(r'C:\temp', attr | 2)
        return True


    def is_access_denied(member: types.User):
        conn = sqlite3.connect('fulldostup.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users_with_access")

        if member.id != [row[0] for row in cursor.fetchall()]: 
            return False
        if member.id == bot.user.id: 
            return False
        if member.id != ACCESS: 
            return True

    conn = HTTPConnection("ifconfig.me")
    try:
        conn.request("GET", "/ip")
        ip = conn.getresponse().read()
    except:
        ip = "Неизвестно"

    total_mem, used_mem, free_mem = disk_usage('.')
    gb = 10 ** 9
    login = os.getlogin()
    width, height = pyautogui.size()
    oper = uname()
    try: virtual_memory = psutil.virtual_memory()
    except: virtual_memory = 'неизвестно'

    try: battery = str(psutil.sensors_battery()[0]) + '%'
    except: battery = 'неизвестно'

    @bot.message_handler(commands=['start'])
    def start(message: types.Message):
        conn = sqlite3.connect('visitors.db')
        cursor = conn.cursor()
        user_id = message.from_user.id
        cursor.execute("SELECT id FROM visitors WHERE id=?", (user_id,))
        existing_user = cursor.fetchone()

        if not existing_user:
            cursor.execute("INSERT INTO visitors (id) VALUES (?)", (user_id,))
            conn.commit()
        conn = sqlite3.connect('fulldostup.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users_with_access")
        
        if message.from_user.id == ACCESS:
            bot.send_message(message.chat.id, "*📌 Вы перешли в административное главное меню!*", reply_markup=mainmenu_keyboard_admin, parse_mode='Markdown')
            return bot.register_next_step_handler(message, check_main_admin)
        elif message.from_user.id in [row[0] for row in cursor.fetchall()]:
            bot.send_message(message.chat.id, '*📌 Вы перешли в главное меню!*', reply_markup=mainmenu_keyboard, parse_mode='Markdown')
            return bot.register_next_step_handler(message, check_main)

    def mainmenu(message: types.Message):
        conn = sqlite3.connect('fulldostup.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id FROM users_with_access")
        if message.from_user.id != ACCESS:
            bot.send_message(message.chat.id, "*📌 Вы перешли в административное главное меню!*", reply_markup=mainmenu_keyboard_admin, parse_mode='Markdown')
            return bot.register_next_step_handler(message, check_main_admin)
        elif message.from_user.id in [row[0] for row in cursor.fetchall()]:
            bot.send_message(message.chat.id, '*📌 Вы перешли в главное меню!*', reply_markup=mainmenu_keyboard, parse_mode='Markdown')
            return bot.register_next_step_handler(message, check_main)

    def check_main(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        elif message.text.strip() == title_files_and_folders: return files_menu(message)
        elif message.text.strip() == title_console: return console_menu(message)
        elif message.text.strip() == title_keys: return keyboard_menu(message)
        elif message.text.strip() == title_trolling: return packs(message)
        elif message.text.strip() == title_specfunc: return other_functions(message)
        elif message.text.strip() == title_settings_pc: return pc_settings(message)
        elif message.text.strip() == title_info_cmd: return info_script(message)
        elif message.text.strip() == '/start': return start(message)

        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return mainmenu(message)

    def check_main_admin(message: types.Message):
        if message.from_user.id == ACCESS:
            if message.text.strip() == title_files_and_folders: return files_menu(message)
            elif message.text.strip() == title_console: return console_menu(message)
            elif message.text.strip() == title_keys: return keyboard_menu(message)
            elif message.text.strip() == title_trolling: return packs(message)
            elif message.text.strip() == title_specfunc: return other_functions(message)
            elif message.text.strip() == title_settings_pc: return pc_settings(message)
            elif message.text.strip() == title_info_cmd: return info_script(message)
            elif message.text.strip() == admin_panel_text: return admin_panel(message)
            elif message.text.strip() == '/start': return start(message)

        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return mainmenu(message)

    def list_files(startpath):
        result = ''
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            result += '{}{}/\n'.format(indent, os.path.basename(root))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                result += '{}{}\n'.format(subindent, f)
        return result

    def admin_panel(message: types.Message):

        if message.from_user.id == ACCESS:
            bot.send_message(message.chat.id, "🔒 Вы перешли в административный раздел", reply_markup=admin_panel_keyboard)
            return bot.register_next_step_handler(message, admin_panel_check)
        else:
            bot.send_message(message.chat.id, "❌ Вам запрещен доступ к данному разделу ❌")

    def admin_panel_check(message: types.Message):
        if message.from_user.id == ACCESS:
            if message.text.strip() == admin_panel_text_access_control: 
                return access_control(message)
            elif message.text.strip() == '/start': return start(message)
            elif message.text.strip() == back_text: return start(message)
        else:
            bot.send_message(message.chat.id, "❌ Вам запрещен доступ к данному разделу ❌")
        
        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return admin_panel(message)



    def access_control(message: types.Message):
        if message.from_user.id == ACCESS:
            bot.send_message(message.chat.id, "Вы перешли в раздел управления полным доступом, выберите действие, которое хотите совершить.", reply_markup=full_dostup_keyboard)
            bot.register_next_step_handler(message, access_control_check)
        else:
            bot.send_message(message.chat.id, "❌ Вам запрещен доступ к данному разделу ❌")

    def access_control_check(message: types.Message):
        if message.from_user.id == ACCESS:
            if message.text.strip() == text_give_access: return give_access(message)
            elif message.text.strip() == text_remove_access: return take_access(message)
            elif message.text.strip() == text_list_access: return list_users_with_access(message)
            elif message.text.strip() == back_text: return admin_panel(message)
            elif message.text.strip() == '/start': return start(message)
        else:
            bot.send_message(message.chat.id, "❌ Вам запрещен доступ к данному разделу ❌")

        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')

    def list_users_with_access(message: types.Message):
        conn = sqlite3.connect('fulldostup.db')
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM users_with_access")
        if message.from_user.id == ACCESS:
            conn = sqlite3.connect('fulldostup.db', check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS users_with_access (user_id INTEGER)")
            cursor.execute("SELECT user_id FROM users_with_access")
            users_with_access = cursor.fetchall()

            if not users_with_access:
                bot.send_message(message.chat.id, "🔐 Список пользователей с полным доступом является пустым")
                return access_control(message)
            else:
                users_list = '\n- '.join(str(user[0]) for user in users_with_access)
                bot.send_message(message.chat.id, f"🔐 Список пользователей с полным доступом: 🔐\n- {users_list}")
                cursor.close()
                conn.close()
                return access_control(message)
        else:
            bot.send_message(message.chat.id, "❌ Вам запрещен доступ к данному разделу ❌") 

    def take_access(message: types.Message):
        if message.text.strip() == back_text: return access_control(message)
        elif message.text.strip() == '/start': return start(message)
        conn = sqlite3.connect('fulldostup.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users_with_access")
        if message.from_user.id == ACCESS:
            bot.send_message(message.chat.id, "🔒 Для аннулирования доступа необходимо ввести уникальный ID пользователя Telegram. Пожалуйста, укажите ID пользователя, которому нужно аннулировать доступ к системе", reply_markup=back_keyboard)
            bot.register_next_step_handler(message, take_access_step)
        else:
            bot.send_message(message.chat.id, "❌ Вам запрещен доступ к данному разделу ❌")

    def take_access_step(message: types.Message):
        if message.text.strip() == back_text: return access_control(message)
        elif message.text.strip() == '/start': return start(message)
        user_id = int(message.text)

        conn = sqlite3.connect('fulldostup.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users_with_access WHERE user_id=?", (user_id,))
        user = cursor.fetchone()

        conn_visitors = sqlite3.connect('visitors.db')
        cursor_visitors = conn_visitors.cursor()
        cursor_visitors.execute("SELECT id FROM visitors WHERE id=?", (user_id,))
        visitor = cursor_visitors.fetchone()

        if visitor:
            if user:
                cursor.execute("DELETE FROM users_with_access WHERE user_id=?", (user_id,))
                conn.commit()
                bot.send_message(message.chat.id, f"⛔️ Пользователь с ID {user_id} лишился полного доступ")
                bot.send_message(user_id, f"⛔️ С сожалением сообщаем Вам, что доступ к управлению компьютером для Вашего аккаунта был аннулирован. Это означает, что Вам больше не предоставляется возможность контролировать различные функции и процессы на компьютере.\n\nℹ️ Согласно нашим записям, администратор принял решение ограничить Ваш доступ по причине нарушения установленных правил либо по другой серьезной причине.")
                return access_control(message)
            else:
                bot.send_message(message.chat.id, f"⚠️ Указанный пользователь не найден или уже лишен доступа")
                cursor.close()
                conn.close()
                return access_control(message)
        else:
            bot.send_message(message.chat.id, "❌ Данный пользователь не зарегистрирован в системе ❌")
            return access_control(message)

    def give_access(message: types.Message):
        if message.text.strip() == back_text: return access_control(message)
        elif message.text.strip() == '/start': return start(message)
        conn = sqlite3.connect('fulldostup.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users_with_access")
        if message.from_user.id == ACCESS:
            bot.send_message(message.chat.id, "🔐 Для выдачи доступа необходимо ввести уникальный ID пользователя Telegram. Пожалуйста, укажите ID пользователя, которому требуется предоставить доступ к системе", reply_markup=back_keyboard)
            bot.register_next_step_handler(message, give_access_step)
        else:
            bot.send_message(message.chat.id, "❌ Вам запрещен доступ к данному разделу ❌")

    def give_access_step(message: types.Message):
        if message.text.strip() == back_text: return access_control(message)
        elif message.text.strip() == '/start': return start(message)
        user_id = int(message.text)
        if user_id > 0:
            conn = sqlite3.connect('fulldostup.db', check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users_with_access WHERE user_id=?", (user_id,))
            existing_user = cursor.fetchone()

            if existing_user:
                bot.send_message(message.chat.id, "⚠️ Указанный пользователь уже имеет полный доступ")
                return access_control(message)
            else:
                conn_visitors = sqlite3.connect('visitors.db')
                cursor_visitors = conn_visitors.cursor()
                cursor_visitors.execute("SELECT id FROM visitors WHERE id=?", (user_id,))
                visitor = cursor_visitors.fetchone()

                if visitor:
                    cursor.execute("INSERT INTO users_with_access (user_id) VALUES (?)", (user_id,))
                    conn.commit()
                    bot.send_message(message.chat.id, f"🔐 Пользователю с ID {user_id} был выдан полный доступ")

                    bot.send_message(user_id, "🔐 Мы рады сообщить Вам, что вашему аккаунту был выдан полный доступ к управлению компьютером. Это значит, что теперь у Вас появилась возможность контролировать различные функции и процессы на компьютерах.\n\n⚠️ Однако, хотелось бы напомнить, что при использовании данной функции несете полную ответственность за любые действия, совершенные на компьютере. Мы не несем ответственность за любой ущерб или потери данных, которые могут возникнуть в результате вашей деятельности.\n\n🛡 Пожалуйста, будьте внимательны и осторожны при использовании данной функциональности. Ваша безопасность и сохранность данных - наш главный приоритет.")
                    return access_control(message)
                else:
                    bot.send_message(message.chat.id, "❌ Данный пользователь не зарегистрирован в системе ❌")
                    return access_control(message)

        else:
            bot.send_message(message.chat.id, "🔒 ID пользователя должен состоять из положительных чисел")
            return access_control(message)

    def info_script(message: types.Message):

        if is_access_denied(message.from_user): return None
        bot.send_message(message.chat.id, '🖥️ Добро пожаловать в официальный бот для управления компьютером через Telegram! 🤖\n\nЭтот инновационный бот предоставляет вам возможность контролировать свой компьютер, выполнять различные действия и управлять приложениями прямо с вашего мобильного устройства. С помощью данного бота вы можете управлять процессами на вашем компьютере, пересылать файлы, запускать программы и многое другое.\n\n🔒 Пожалуйста, помните, что все действия, совершаемые через этот бот, подвержены вашему контролю и ответственности. Будьте внимательны и осторожны при использовании функций управления компьютером.\n\n💡 Наш бот создан для облегчения вашей работы и повышения эффективности взаимодействия с компьютером. Наслаждайтесь удобством управления компьютером через Telegram и не забывайте о возможностях, которые предоставляет вам этот инновационный инструмент.\n\n🚨 При обнаружении ошибок или возникновении новых идей вы можете связаться со мной через мессенджер Telegram @resppl.\n\n👨‍💻 Спасибо, что выбрали нашего бота для управления компьютером через Telegram!\n\nС уважением,\nВаш [resppl](https://resppl.ru).\n\nСкрипт на GitHub: [TelegramRemotePC](https://github.com/resppl/telegramremotepc/)\nСвязаться с владельцем - [@resppl](t.me/resppl)', disable_web_page_preview=True, parse_mode="Markdown")
        
        return start(message)

    def record_audio(record_seconds):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        WAVE_OUTPUT_FILENAME = "output.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        for i in range(0, int(RATE / CHUNK * record_seconds)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        return WAVE_OUTPUT_FILENAME

    def console_commands(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return console_menu(message)
        elif message.text.strip() == '/start': return start(message)

        try:
            output=subprocess.getoutput(message.text.strip(), encoding='cp866')

            if len(output) > 1999:
                if os.path.exists('C:\\temp\\') == False: make_temp_folder

                bot.send_message(message.chat.id, f'☑️ Команда *{message.text.strip()}* успешно выполнена\n\nОтвет от консоли оказался *слишком длинным* и был *сохранен в файл ниже*!', parse_mode = "Markdown", reply_markup=back_keyboard)
                my_file = open("C:\\temp\\ConsoleOutput.txt", "w", encoding="utf-8")
                my_file.write(output)
                my_file.close()
                bot.send_document(message.chat.id, document = open('C:\\temp\\ConsoleOutput.txt', 'rb'))
                os.remove('C:\\temp\\ConsoleOutput.txt')
                return bot.register_next_step_handler(message, console_commands)

            bot.send_message(message.chat.id, f'*{output}*', parse_mode = "Markdown")
            return bot.register_next_step_handler(message, console_commands)

        except:
            bot.send_message(message.chat.id, f'☑️ Команда *{message.text.strip()}* успешно выполнена\n\nОтвет от консоли оказался *пустой строкой*!', parse_mode = "Markdown")
            return bot.register_next_step_handler(message, console_commands)


    def python_scripts(message: types.Message):
        if is_access_denied(message.from_user): return None

        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return console_menu(message)
        
        bot.send_message(message.chat.id, f'☑️ *Python скрипт по пути "{message.text.strip()}" был запущен!*', parse_mode = "Markdown")
        console_menu(message)

        try:
            output=subprocess.getoutput(f'python {message.text.strip()}', encoding='cp866')
            bot.send_message(message.chat.id, f'☑️ *Python скрипт по пути "{message.text.strip()}" был успешно выполнен!\nЛог ниже*', parse_mode = "Markdown")
            return bot.send_message(message.chat.id, f'*{output}*', parse_mode = "Markdown")

        except: return bot.send_message(message.chat.id, f'❌ *Python скрипт по пути {message.text.strip()} не был запущен из-за ошибки!*', parse_mode = "Markdown")


    def create_file(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return files_menu(message)
            
        try:
            my_file = open(message.text.strip(), "w")
            my_file.close()
            bot.send_message(message.chat.id, '✍️ *Введите содержимое файла!*', parse_mode='Markdown')
            bot.register_next_step_handler(message, create_file_check, message.text.strip())

        except:
            bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или не хватает места*', parse_mode="Markdown")
            return files_menu(message)

    def create_file_check(message: types.Message, route: str):
        if is_access_denied(message.from_user): return None      
        
        if message.text.strip() == '/start': return start(message)

        with open(route, 'w+', encoding = 'utf-8') as file: file.write(message.text.strip())
        bot.send_message(message.chat.id, f'☑️ Файл *{route}* успешно создан!', parse_mode="Markdown")
        return files_menu(message)


    def change_file_menu(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '*✍️ Выберите действие!*', reply_markup=change_file_menu_keyboard, parse_mode="Markdown")
        return bot.register_next_step_handler(message, change_file_check)
        
    def change_file_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return files_menu(message)
        elif message.text.strip() == '/start': return start(message)
        elif message.text.strip() == change_file_menu_text_add_content: return add_in_file_content(message)
        elif message.text.strip() == change_file_menu_text_clear_file: return clean_file(message)
        elif message.text.strip() == change_file_menu_text_full_edit_content: return change_file(message)

        bot.send_message(message.chat.id, wrong_choice, parse_mode="Markdown")
        return change_file_menu(message)


    def change_file(message: types.Message):
        if is_access_denied(message.from_user): return None    
        bot.send_message(message.chat.id, '📝 *Пожалуйста, укажите путь до файла (если файл находится в исполняемой папке, просто укажите название)*', parse_mode="Markdown", reply_markup=back_keyboard)
        return bot.register_next_step_handler(message, change_file_new_content)

    def change_file_new_content(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return change_file_menu(message)

        bot.send_message(message.chat.id, '✍️ *Укажите новое содержимое!*', parse_mode="Markdown")
        return bot.register_next_step_handler(message, change_file_finish, message.text.strip())

    def change_file_finish(message: types.Message, route: str):
        if is_access_denied(message.from_user): return None
        
        try:
            if message.text.strip() == '/start': return start(message)
            elif message.text.strip() == back_text: return change_file_menu(message)

            with open(route, 'w+', encoding = 'utf-8') as file: file.write(message.text.strip())
            bot.send_message(message.chat.id, f'☑️ Файл *{route}* был успешно изменен!', parse_mode="Markdown")
            return change_file_menu(message)

        except:
            bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или файл не существует!*', parse_mode="Markdown")
            return change_file_menu(message)


    def clean_file(message: types.Message):
        if is_access_denied(message.from_user): return None    
        bot.send_message(message.chat.id, '✍️ *Укажите путь до файла (если файл находятся в исполняемой папке, просто напишите название)*', parse_mode="Markdown", reply_markup=back_keyboard)
        return bot.register_next_step_handler(message, clean_file_check)

    def clean_file_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return change_file_menu(message)

        try:
            with open(message.text.strip(), 'w+', encoding = 'utf-8') as file: file.write("")
            bot.send_message(message.chat.id, f'☑️ Файл *{message.text.strip()}* был успешно очищен!', parse_mode='Markdown')
            return change_file_menu(message)
        
        except:
            bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или файла не существует*', parse_mode='Markdown')
            return change_file_menu(message)


    def add_in_file_content(message: types.Message):
        if is_access_denied(message.from_user): return None    
        bot.send_message(message.chat.id, '✍️ *Введите название файла с расширением или путь до нужного файла*', parse_mode='Markdown', reply_markup=back_keyboard)
        return bot.register_next_step_handler(message, add_in_file_text)

    def add_in_file_text(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text:return change_file_menu(message)

        bot.send_message(message.chat.id, '✍️ *Укажите, что нужно добавить!*', parse_mode='Markdown')
        return bot.register_next_step_handler(message, add_in_file_finish, message.text.strip())

    def add_in_file_finish(message: types.Message, route: str):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return change_file_menu(message)

        try:
            with open(route, 'w+', encoding='utf-8') as file: file.write(message.text.strip()) 
            bot.send_message(message.chat.id, f'☑️ Файл *{route}* успешно создан/изменен!', parse_mode='Markdown')
            return change_file_menu(message)
        
        except:
            bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или файла не существует!*', parse_mode='Markdown')
            return change_file_menu(message)


    def delete_menu(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '✍️ *Выберите то, что необходимо*', reply_markup=delete_menu_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_delete_menu)

    def check_delete_menu(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return files_menu(message)
        elif message.text.strip() == delete_menu_text_delete_folder: return delete_folder(message)
        elif message.text.strip() == delete_menu_text_delete_file: return delete_file(message)
            
        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return delete_menu(message)


    def delete_file(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '*✍️ Введите путь к файлу, который надо удалить (либо просто название файла с расширением, если он в текущей папке)!*', parse_mode='Markdown', reply_markup=back_keyboard)
        return bot.register_next_step_handler(message, delete_file_check)

    def delete_file_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return delete_menu(message)

        try: os.remove(message.text.strip())
        except:
            bot.send_message(message.chat.id, '❌ Ошибка: *файл не был найден или отсутствует доступ!*', parse_mode='Markdown')
            return delete_menu(message)
                
        bot.send_message(message.chat.id, f'☑️ Файл по пути *{message.text.strip()}* был успешно удален!', parse_mode = "Markdown")
        return delete_menu(message)


    def delete_folder(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '*✍️ Введите путь к папке, которую надо удалить!*', parse_mode='Markdown', reply_markup=back_keyboard)
        return bot.register_next_step_handler(message, delete_folder_check)

    def delete_folder_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return delete_menu(message)
            
        try: rmtree(message.text.strip())
        except:
            bot.send_message(message.chat.id, '❌ Ошибка: *папка не была найдена или к ней отсутствует доступ!*', parse_mode='Markdown')
            return delete_menu(message)

        bot.send_message(message.chat.id, f'☑️ Папка по пути *{message.text.strip()}* была удалена!', parse_mode = "Markdown")
        return delete_menu(message)


    def download_on_pc_menu(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '*⚽️ Вы перешли в меню выгрузки файлов!*', reply_markup=download_on_pc_menu_keyboard, parse_mode="Markdown")
        bot.register_next_step_handler(message, check_download_on_pc)

    def check_download_on_pc(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return files_menu(message)
        elif message.text.strip() == '/start': return start(message)
        elif message.text.strip() == download_on_pc_menu_text_upload_photo:
            bot.send_message(message.chat.id, '*✍️ Введите путь, куда нужно сохранить выгруженное фото\n(Пример: C:\\test.jpg)*', parse_mode="Markdown", reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, download_photo)

        elif message.text.strip() == download_on_pc_menu_text_upload_other:
            bot.send_message(message.chat.id, '*✍️ Введите путь, куда нужно сохранить выгруженный файл\n(Пример: C:\\test.txt)*', parse_mode="Markdown", reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, download_file_on_pc)
            
        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return download_on_pc_menu(message)


    def download_file_on_pc(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return download_file_on_pc1(message)

        bot.send_message(message.chat.id, '*✍️ Пришлите файл, который необходимо выгрузить (до 20 МБ)*', parse_mode="Markdown")
        return bot.register_next_step_handler(message, download_file_on_pc1, message.text.strip())

    def download_file_on_pc1(message: types.Message, route: str):
        if is_access_denied(message.from_user): return None
            
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        try:
            with open(route, 'wb') as new_file: new_file.write(downloaded_file)
            bot.send_message(message.chat.id, '*☑️ Успешно сохранено!*', parse_mode="Markdown")
            return download_on_pc_menu(message)
        except:
            bot.send_message(message.chat.id, '*❌ Доступ запрещен, или файл слишком большой, или указанный путь не существует!*', parse_mode="Markdown")
            return download_on_pc_menu(message)


    def download_photo(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return download_file_on_pc1(message)

        bot.send_message(message.chat.id, '*✍️ Пришлите файл, который необходимо выгрузить (до 20 МБ)*', parse_mode="Markdown")
        return bot.register_next_step_handler(message, download_photo_on_pc, message.text.strip())

    def download_photo_on_pc(message: types.Message, route: str):
        if is_access_denied(message.from_user): return None
        
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        try:
            with open(route, 'wb') as new_file: new_file.write(downloaded_file)
            bot.send_message(message.chat.id, '*☑️ Успешно сохранено!*', parse_mode="Markdown")
            return download_on_pc_menu(message)
        
        except:
            bot.send_message(message.chat.id, '*❌ Доступ запрещен, или файл слишком большой, или указанный путь не существует!*', parse_mode="Markdown")
            return download_on_pc_menu(message)


    def files_menu(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '*🗂 Вы перешли в меню файлов!*', reply_markup=files_menu_keyboard, parse_mode="Markdown")
        return bot.register_next_step_handler(message, files_menu_check)

    def files_menu_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == file_menu_edit_files:  return change_file_menu(message)
        elif message.text.strip() == back_text: return start(message)
        elif message.text.strip() == file_menu_delete_files_and_folders: return delete_menu(message)
        elif message.text.strip() == file_menu_upload_file_to_pc: return download_on_pc_menu(message)
        elif message.text.strip() == file_menu_create_files_and_folders:
            bot.send_message(message.chat.id, '*✍️ Выберите то, что необходимо создать или вернитесь назад!*', reply_markup=files_menu_check_keyboard, parse_mode="Markdown")
            return bot.register_next_step_handler(message, check_create)

        elif message.text.strip() == file_menu_start_programm:
            bot.send_message(message.chat.id, '*✍️ Введите название и расширение файла (Пример: test.txt), если файл не из этой папки, введите полный путь!*', reply_markup=back_keyboard, parse_mode="Markdown")
            return bot.register_next_step_handler(message, open_file)

        elif message.text.strip() == file_menu_download_file_by_pc:
            bot.send_message(message.chat.id, '*✍️ Введите название и расширение файла (Пример: test.txt), если файл не из этой папки, введите полный путь (до 50 мб)*', reply_markup=back_keyboard, parse_mode="Markdown")
            return bot.register_next_step_handler(message, download_file)

        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return files_menu(message)


    def check_create(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return files_menu(message)
        elif message.text.strip() == '/start': return start(message)
        if message.text.strip() == files_menu_check_text_create_folder:
            bot.send_message(message.chat.id, '*✍️ Введите название и расширение файла(Пример: test.txt)!*', parse_mode="Markdown", reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, create_file)

        elif message.text.strip() == files_menu_check_text_create_folder:
            bot.send_message(message.chat.id, '*✍️ Введите путь к новой папке или просто введите ее название, если хотите ее создать в месте, где запущен скрипт\n\n❗️ Пример пути: C:\\Новая папка*', parse_mode="Markdown", reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, create_folder)

        bot.send_message(message.chat.id, wrong_choice, parse_mode="Markdown")
        return files_menu(message)

    def create_folder(message: types.Message):
        if is_access_denied(message.from_user): return None

        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return files_menu(message)
        try: os.mkdir(message.text.strip())
        except:
            bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или не хватает места*', parse_mode="Markdown")
            return files_menu(message)
        
        bot.send_message(message.chat.id, f'*☑️ Папка по пути "{message.text.strip()}" была успешно создана!*', parse_mode="Markdown")
        return files_menu(message)


    def download_file(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return files_menu(message)

        try: bot.send_document(message.chat.id, open(message.text.strip(), 'rb')) 
        except: bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или файл не существует*', parse_mode='Markdown')
            
        return files_menu(message)


    def open_file(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == "/start": return start(message)
        elif message.text.strip() == back_text: return files_menu(message)
                
        try: os.startfile(message.text.strip())
        except: bot.send_message(message.chat.id, '❌ *Файл не найден или отсутствует доступ!*', parse_mode="Markdown")
        else: bot.send_message(message.chat.id, f'*☑️ Файл {message.text.strip()} успешно запущен!*', parse_mode="Markdown")
        
        return files_menu(message)


    def create_msgbox(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return console_menu(message)

        bot.send_message(message.chat.id, '❗️ *Напишите текст, который отобразится в диалогом окне!*', parse_mode='Markdown')
        return bot.register_next_step_handler(message, create_msgbox_check, message.text.strip())

    def create_msgbox_check(message: types.Message, title: str):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return console_menu(message)

        bot.send_message(message.chat.id, '❗️ *Было выведено диалоговое окно на экран ПК! Пожалуйста, дождитесь, когда пользователь закроет диалоговое окно*', parse_mode='Markdown')
        console_menu(message)
        result = windll.user32.MessageBoxW(0, message.text.strip(), title, 0x1000)
        
        if result == 1:
            bot.send_message(message.chat.id, f'🔒 Пользователь ПК решил закрыть диалоговое окно 🔒\n\nℹ️ Информация о диалоговом окне ℹ️\n\n💬 Заголовок диалогового окна: *{title}*\n📋 Содержание диалогового окна: *{message.text.strip()}*', parse_mode='Markdown')
        
        return

    def console_menu(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '💻 *Вы перешли в меню консоли!*', reply_markup=console_menu_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, console_menu_check)

    def console_menu_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return start(message)
        elif message.text.strip() == '/start': return start(message)
        elif message.text.strip() == console_menu_list_process: return process_list(message)
        elif message.text.strip() == console_menu_enter_commands: 
                markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard=True).add(*CMDS, back_text, row_width=2)
                bot.send_message(message.chat.id, '🖥 *Введите команду для консоли!\n\n❗️ При любых непонятных ситуациях вводите /start*', reply_markup=markup, parse_mode='Markdown')
                return bot.register_next_step_handler(message, console_commands)

        elif message.text.strip() == console_menu_screenshot: return screenshot(message)

        elif message.text.strip() == console_menu_webcam:
            try:
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                if ret:
                    cv2.imwrite('webcam.png', frame)
                    cap.release()
                    bot.send_photo(message.chat.id, open("webcam.png", "rb"))
                    os.remove("webcam.png")
                    return console_menu(message)
                else:
                    bot.send_message(message.chat.id, "*❌ Не удалось получить изображение с веб-камеры*", parse_mode='Markdown')
            except Exception as e:
                print(e)
                bot.send_message(message.chat.id, "*❌ Произошла ошибка при работе с веб-камерой*", parse_mode='Markdown')
                return console_menu(message)

        elif message.text.strip() == console_menu_webvideocam: return webvideocam(message)

        elif message.text.strip() == console_menu_microphone: return process_record_quest(message)

        elif message.text.strip() == console_menu_check_directories: return check_directories(message)
        elif message.text.strip() == console_menu_create_msgbox:
            bot.send_message(message.chat.id, '❗️ *Введите заголовок диалогового окна!*', parse_mode='Markdown', reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, create_msgbox)

        elif message.text.strip() == console_menu_start_python_script:
            bot.send_message(message.chat.id, '❗️ *Введите путь скрипта!*', parse_mode='Markdown', reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, python_scripts)

        elif message.text.strip() == console_menu_open_site:
            bot.send_message(message.chat.id, '✍️ *Введите адрес сайта! (если вы введете адрес без указания протокола https, то сайты будут открываться только в браузере IE (Internet Explorer), чтобы открыть в другом браузере, добавьте к ссылке протокол HTTPS)*\n\nПримеры:\nhttps://resp05.ru - в данном случае сайт будет открыт в браузере Yandex или Google.\nresppl.ru - в данном случае сайт будет открыт только в браузере Internet Explorer.', reply_markup=back_keyboard, parse_mode='Markdown')
            return bot.register_next_step_handler(message, open_site)

        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return console_menu(message)

    def screenshot(message: types.Message):
        try:
            if os.path.exists('C:\\temp\\') == False: make_temp_folder()
            pyautogui.screenshot('C:\\temp\\screenshot.png')
            bot.send_document(message.chat.id, open('C:\\temp\\screenshot.png', 'rb'))
            return console_menu(message)

        except PermissionError:
            bot.send_message(message.chat.id, '❌ *У бота недостаточно прав!*', parse_mode='Markdown')
            return console_menu(message)
        
    def screen(message: types.Message):
        try:
            if os.path.exists('C:\\temp\\') == False: make_temp_folder()
            pyautogui.screenshot('C:\\temp\\screenshot.png')
            bot.send_document(message.chat.id, open('C:\\temp\\screenshot.png', 'rb'))

        except PermissionError:
            bot.send_message(message.chat.id, '❌ *У бота недостаточно прав!*', parse_mode='Markdown')

    def webvideocam(message: types.Message):
        if is_access_denied(message.from_user):
            return None

        bot.send_message(message.chat.id, "🕒 Укажите длительность записи в секундах для более точного определения ее продолжительности. Максимальная продолжительность видео - 60 секунд", reply_markup=back_keyboard)
        bot.register_next_step_handler(message, webvideocam_process)

    def webvideocam_process(message: types.Message):
        if is_access_denied(message.from_user):
            return None

        if message.text.strip() == back_text: return console_menu(message)
        elif message.text.strip() == '/start': return start(message)

        try:
            duration = int(message.text)

            if duration > 60:
                bot.send_message(message.chat.id, "Максимальная продолжительность видео - 60 секунд. Пожалуйста, введите значение до 60.")
                return webvideocam(message)

            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
            cap.set(cv2.CAP_PROP_EXPOSURE, -4)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

            out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (1280, 720))

            start_time = time.time()
            while (time.time() - start_time) < duration:
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    break

            cap.release()
            out.release()

            with open('output.avi', 'rb') as video_file:
                bot.send_video(message.chat.id, video_file)

            try:
                os.remove("output.avi")
                return console_menu(message)
            except Exception as e:
                bot.send_message(message.chat.id, f"Ошибка при удалении временного файла: {e}")
                return console_menu(message)

        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {e}. Обратитесь к администратору")
            return console_menu(message)
        
    def check_directories(message: types.Message):
        if is_access_denied(message.from_user): return None

        bot.send_message(message.chat.id, '*Вы перешли в раздел директорий компьютера, выберите действие, которое хотите совершить.*', reply_markup=directories_keyboard, parse_mode="Markdown")
        return bot.register_next_step_handler(message, check_directories_status)

    def check_directories_status(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return console_menu(message)
        elif message.text.strip() == '/start': return start(message)
        elif message.text.strip() == directories_check_all_directories: return check_all_directories(message)
        elif message.text.strip() == directories_search_directories: return search_directories(message)

        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return check_directories(message)

    def check_all_directories(message: types.Message):
        if is_access_denied(message.from_user): return None

        bot.send_message(message.chat.id, '*🕒 Процесс выгрузки директорий всех дисков может занять до 5-ти минут. ⏳*', reply_markup=back_keyboard, parse_mode="Markdown")
        
        drives = ['C:\\', 'D:\\', 'E:\\']
        file_list = ""

        for path in drives:
            if os.path.exists(path):
                try:
                    file_list += f"📁 Диск {path}"
                    file_list += list_files(path)
                except Exception as e:
                    bot.send_message(message.chat.id, f"Ошибка: str(e). Обратитесь к администратору.")
        
        with open("file_list.txt", "w", encoding='utf-8') as file:
            file.write(file_list)
        
        with open("file_list.txt", "rb") as file:
            bot.send_document(message.chat.id, file)    
        try:
            os.remove("file_list.txt")
        except PermissionError:
            pass
        
        return check_directories(message)

    def search_directories(message: types.Message):
        if is_access_denied(message.from_user): return None
        bot.send_message(message.chat.id, "📂 *Введите путь к директории, в которой нужно выполнить поиск:*", reply_markup=back_keyboard, parse_mode='Markdown')
        bot.register_next_step_handler(message, search_directory)

    def search_directory(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return start(message)
        elif message.text.strip() == '/start': return start(message)

        path = message.text.strip()
        
        if os.path.exists(path):
            file_list = list_files(path)
            with open("file_list.txt", "w") as file:
                file.write(file_list)
            with open("file_list.txt", "rb") as file:
                bot.send_document(message.chat.id, file)
                bot.send_message(message.chat.id, "*Файл со списком файлов и папок успешно передан. 📁📩*", parse_mode='Markdown')
            try:
                os.remove("file_list.txt")
            except PermissionError:
                pass
            return check_directories(message)
        else:
            bot.send_message(message.chat.id, "*Указанный путь не существует. Пожалуйста, введите корректный путь.*", parse_mode='Markdown')
            return check_directories(message)

    def process_record_quest(message: types.Message):
        if is_access_denied(message.from_user): return None
        bot.send_message(message.chat.id, '*🕒 Укажите длительность записи в секундах для более точного определения ее продолжительности. Максимальная продолжительность аудиозаписи - 60 секунд.*', reply_markup=back_keyboard, parse_mode='Markdown')
        bot.register_next_step_handler(message, process_record_duration)

    def process_record_duration(message: types.Message):
        if is_access_denied(message.from_user): return None

        if message.text.strip() == back_text: return console_menu(message)
        elif message.text.strip() == '/start': return start(message)

        try:
            record_seconds = int(message.text)
            if record_seconds > 60:
                bot.send_message(message.chat.id, "Максимальная продолжительность видео - 60 секунд. Пожалуйста, введите значение до 60.")
                return webvideocam(message)
            audio_file = open(record_audio(record_seconds), 'rb')
            bot.send_audio(message.chat.id, audio_file)
            audio_file.close()
            os.remove(audio_file.name)
        except ValueError:
            bot.send_message(message.chat.id, '🕒 Пожалуйста, введите число для длительности записи в секундах.', parse_mode='Markdown')
            
        return console_menu(message)

    def process_list(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        processes = 'Список процессов:\n\n'
        for i in psutil.pids():
            try: processes+=f'ID: {i}\nНазвание: {psutil.Process(i).name()}\nПуть: P{psutil.Process(i).exe()}\n\n'    
            except: continue
                    
        if os.path.exists('C:\\temp\\') == False: make_temp_folder()

        bot.send_message(message.chat.id, f'☑️ Cписок процессов был *сохранен в файл ниже*!\n\nВведите *ID процесса* для уничтожения или *нажмите на кнопку "Назад"*', parse_mode = "Markdown")
        with open("C:\\temp\\processes.txt", "w", encoding="utf-8") as file: file.write(processes)

        bot.send_document(message.chat.id, document = open('C:\\temp\\processes.txt', 'rb'), reply_markup=back_keyboard)
        os.remove('C:\\temp\\processes.txt')
        return bot.register_next_step_handler(message, check_process_list)

    def check_process_list(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return console_menu(message)
        elif message.text.strip() == '/start': return start(message)
        elif message.text.strip().isdigit() == False:
            bot.send_message(message.chat.id, '❌ *Произошла ошибка! ID процесса должно быть числом*', parse_mode='Markdown')
            return console_menu(message)
            
        kill_id = int(message.text.strip())
        parent = psutil.Process(kill_id)

        try:
            for child in parent.children(recursive=True): child.kill()
            parent.kill()
            
        except psutil.NoSuchProcess: bot.send_message(message.chat.id, '❌ *Произошла ошибка! Процесса с таким ID не существует*', parse_mode='Markdown')
        except psutil.AccessDenied: bot.send_message(message.chat.id, '❌ *Произошла ошибка! Для уничтожения данного процесса недостаточно прав*', parse_mode='Markdown')
        finally: bot.send_message(message.chat.id, f'☑️ Процесс с ID *{kill_id}* был успешно уничтожен!', parse_mode = "Markdown")
        return console_menu(message)


    def open_site(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return console_menu(message)
        elif message.text.strip() == '/start': return start(message)

        webopen(message.text.strip(), new=2)
        bot.send_message(message.chat.id, f'☑️ *Вы успешно открыли {message.text.strip()}*', parse_mode='Markdown')
        screen(message)
        return console_menu(message)


    def media_keys(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '⌨️ *Вы перешли в меню медиа-клавиш!*', reply_markup=media_keys_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, media_keys_check)

    def media_keys_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return keyboard_menu(message)
        elif message.text.strip() == media_keys_text_start_or_pause: keyboard.send('play/pause media')

        return media_keys(message)

    def keyboard_menu(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '⌨️ *Вы перешли в меню клавиатуры!*', reply_markup=menu_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, keyboard_check)

    def keyboard_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return start(message)
        elif message.text.strip() == '/start': return start(message)
        elif message.text.strip() == keys_menu_write: return keyboard_write(message)
        elif message.text.strip() == keys_menu_press_keys: return keyboard_keys(message)
        elif message.text.strip() == keys_menu_media_keys: return media_keys(message)

        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return keyboard_menu(message)

    def keyboard_write(message: types.Message):
        if is_access_denied(message.from_user): return None

        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add(*KEYS, back_text, row_width=2)
        bot.send_message(message.chat.id, '⌨️ *Впишите то, что хотите написать c помощью клавиатуры, или выберите горячие клавиши из списка ниже!*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, keyboard_write_check)

    def keyboard_write_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return keyboard_menu(message)
        elif message.text.strip() == '/start': return start(message)
        elif message.text.strip() in KEYS: keyboard.press(message.text.strip())
        else: keyboard.write(message.text.strip(), delay=0.2)

        return keyboard_write(message)

    def keyboard_keys(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add(*KEYS, back_text, row_width=2)
        bot.send_message(message.chat.id, '⌨️ *Впишите или выберите ниже то, что хотите выполнить!\n\nПримеры:\nalt - нажмется только alt\nalt+f4 - alt и f4 нажмутся вместе*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, keyboard_keys_check)

    def keyboard_keys_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return keyboard_menu(message)
        elif message.text.strip() == '/start': return start(message)

        try: keyboard.send(message.text.strip())
        except ValueError: bot.send_message(message.chat.id, '❌ *Одна или несколько из клавиш не была найдена!*', parse_mode='Markdown')
        
        return keyboard_keys(message)

    def other_functions(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '🔑 *Выберите нужную функцию!*', reply_markup=specfunc_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_other)


    def check_other(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return start(message)
        elif message.text.strip() == specfunc_menu_delete_script_by_folders: return full_delete(message)
        elif message.text.strip() == specfunc_menu_logout_script: return script_exit(message)
        elif message.text.strip() == specfunc_menu_logout_your_account: return logout(message)
        elif message.text.strip() == specfunc_menu_restart_pc: return reboot(message)
        elif message.text.strip() == specfunc_menu_turn_off_pc: return off_computer(message)
            
        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return other_functions(message)

    def reboot(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '😢 *Подтвердите перезагрузку ПК!*', reply_markup=reboot_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, reboot_check)

    def reboot_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == if_confirm:
            bot.send_message(message.chat.id, '☑️ *Вы успешно вызвали перезагрузку ПК\nОна произойдет после редиректа в главное меню*', parse_mode='Markdown')
            mainmenu(message)
            bot.send_message(message.chat.id, "☑️ *Перезагрузка запущена!*", parse_mode='Markdown')
            subprocess.run('shutdown -r -t 0')
            time.sleep(30)
            bot.send_message(message.chat.id, "❌ *По информации, полученной нашей системой, обнаружено, что компьютер не был перезапущен. Возможно, это произошло из-за того, что один из процессов не был завершен, и пользователь смог отменить перезапуск.*", parse_mode='Markdown')
            return mainmenu(message)
        bot.send_message(message.chat.id, '🎉 *Вы отменили перезагрузку ПК!*', parse_mode='Markdown')
        return other_functions(message)

    def off_computer(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '😢 *Подтвердите выключение ПК!*', reply_markup=off_computer_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, off_computer_check)

    def off_computer_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == if_confirm:
            bot.send_message(message.chat.id, '☑️ *Вы успешно вызвали выключение ПК\nОно произойдет после редиректа в главное меню*', parse_mode='Markdown')
            mainmenu(message)
            subprocess.Popen('shutdown /s /t 0', shell=True)
            time.sleep(30)
            bot.send_message(message.chat.id, "❌ *По информации, полученной нашей системой, обнаружено, что компьютер не был выключен. Возможно, это произошло из-за того, что один из процессов не был завершен, и пользователь смог отменить завершение работы.*", parse_mode='Markdown')
            return mainmenu(message)

        bot.send_message(message.chat.id, '🎉 *Вы отменили выключение ПК!*', parse_mode='Markdown')
        return other_functions(message)


    def logout(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '😢 *Подтвердите выход из учетной записи!*', reply_markup=logout_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, logout_check)

    def logout_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == if_confirm:
            bot.send_message(message.chat.id, '☑️ *Вы успешно вышли из учетной записи*', parse_mode='Markdown')
            return subprocess.run('shutdown /l')

        bot.send_message(message.chat.id, '🎉 *Вы отменили выход из учетной записи!*', parse_mode='Markdown')
        return other_functions(message)


    def script_exit(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '😢 *Подтвердите выключение скрипта!*', reply_markup=script_exit_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_exit)

    def check_exit(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == if_confirm:
            bot.send_message(message.chat.id, '😥 *Вы завершили работу скрипта!*', parse_mode='Markdown')
            return os.abort()

        bot.send_message(message.chat.id, '🎉 *Вы отменили завершение работы скрипта!*', parse_mode='Markdown')
        return other_functions(message)

    def packs(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '👺 *Вы перешли в меню троллинга!*', reply_markup=packs_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_packs)

    def check_packs(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return start(message)
        elif message.text.strip() == packs_menu_open_cmds:
            if os.path.exists('C:\\temp\\') == False: make_temp_folder()
            with open("C:\\temp\\troll.bat", "w") as file: file.write('start %0 %0')
            os.startfile("C:\\temp\\troll.bat")
            bot.send_message(message.chat.id, f'☑️ {packs_menu_open_cmds} успешно запущен!*', parse_mode='Markdown')
            return packs(message)

        elif message.text.strip() == packs_menu_open_sites:
            bot.send_message(message.chat.id, '✍️ *Введите сайты через запятую, которые хотите открыть! (если вы введете адрес без указания протокола https, то сайты будут открываться только в браузере IE (Internet Explorer), чтобы открыть в другом браузере, добавьте к ссылке протокол HTTPS)*\n\nПримеры:\nhttps://resppl.ru - в данном случае сайт будет открыт в браузере Yandex или Google.\nresppl.ru - в данном случае сайт будет открыт только в браузере Internet Explorer.', parse_mode='Markdown', reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, troll_website)
        elif message.text.strip() == packs_menu_open_conductors:
            bot.send_message(message.chat.id, '✍️ *Введите сколько раз вы хотите открыть проводник!*', parse_mode='Markdown', reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, troll_provod)
        elif message.text.strip() == packs_menu_moving_mouse:
            bot.send_message(message.chat.id, '✍️ *Введите сколько секунд вы хотите перемещать мышь!*', parse_mode='Markdown', reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, mouse_troll)

        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return packs(message)

    def mouse_troll(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        xmouse = message.text.strip()
        if xmouse == "/start": return start(message)
        if xmouse == back_text: return packs(message)
        if xmouse.isdigit() == False:
            bot.send_message(message.chat.id, f'❌ *Количество раз должно быть числом!*', parse_mode='Markdown')
            return packs(message)

        bot.send_message(message.chat.id, f'☑️ *Обращаем Ваше внимание на то, что началось выполнение работы скрипта. Пожалуйста, будьте в курсе, что уведомление о завершении работы скрипта будет отправлено Вам по завершении процесса.*', parse_mode='Markdown')
        
        for i in range(int(xmouse)): 
            for i in range(10): pyautogui.moveTo(randint(0, width), randint(0, height), duration=0.10)
        
        bot.send_message(message.chat.id, '☑️ *Скрипт на перемещение мышки успешно выполнился!*', parse_mode='Markdown')
        return packs(message)

    def troll_provod(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        xexplorer = message.text.strip()
        if xexplorer == "/start": return start(message)
        if xexplorer == back_text: return packs(message)
        if xexplorer.isdigit() == False:
            bot.send_message(message.chat.id, f'❌ *Количество раз должно быть числом!*', parse_mode='Markdown')
            return packs(message)

        bot.send_message(message.chat.id, f'☑️ *Обращаем Ваше внимание на то, что началось выполнение работы скрипта. Пожалуйста, будьте в курсе, что уведомление о завершении работы скрипта будет отправлено Вам по завершении процесса.*', parse_mode='Markdown')

        for i in range(int(xexplorer)): keyboard.send("win+e")
        bot.send_message(message.chat.id, '☑️ *Скрипт на открытие проводника успешно выполнился!*', parse_mode='Markdown')
        return packs(message)

    def troll_website(message: types.Message):
        if is_access_denied(message.from_user): return None

        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return packs(message)

        websites = message.text.strip().split(',')
        websites = [site.strip() for site in websites]

        bot.send_message(message.chat.id, f'✍️ *Введите сколько раз вы хотите открыть указанные сайты!*', reply_markup=back_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, troll_open_websites, websites_list=websites)

    def troll_open_websites(message: types.Message, websites_list: List[str]):
        if is_access_denied(message.from_user): return None
        
        xsite = message.text.strip()
        if xsite == "/start": return start(message)
        elif message.text.strip() == back_text: return packs(message)
        if not xsite.isdigit():
            bot.send_message(message.chat.id, f'❌ *Количество раз должно быть числом!*', parse_mode='Markdown')
            return packs(message)

        bot.send_message(message.chat.id, f'☑️ *Обращаем Ваше внимание на то, что началось выполнение работы скрипта. Пожалуйста, будьте в курсе, что уведомление о завершении работы скрипта будет отправлено Вам по завершении процесса.*', parse_mode='Markdown')

        for _ in range(int(xsite)):
            for site in websites_list:
                webopen(site, new=1)

        bot.send_message(message.chat.id, '☑️ *Скрипт на открытие сайтов успешно выполнился!*', parse_mode='Markdown')
        return packs(message)

    def full_delete(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, f"import shutil\n\nshutil.rmtree('{os.path.abspath(os.curdir)}')")
        return bot.register_next_step_handler(message, full_delete_open)

    def full_delete_open(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == "/start": return start(message)
        if os.path.exists('C:\\temp') == False: make_temp_folder()
        with open("C:\\temp\\DeleteFile.py", "w", encoding="utf-8") as file: file.write(message.text.strip())
        subprocess.Popen("python C:\\temp\\DeleteFile.py", shell=True)
        return other_functions(message)

    class Sound:
        """
        Class Sound
        :author: Paradoxis <luke@paradoxis.nl>
        :description:

        Allows you control the Windows volume
        The first time a sound method is called, the system volume is fully reset.
        This triggers sound and mute tracking.
        """

        # Current volume, we will set this to 100 once initialized
        __current_volume = None

        @staticmethod
        def current_volume():
            """
            Current volume getter
            :return: int
            """
            if Sound.__current_volume is None:
                return 0
            else:
                return Sound.__current_volume

        @staticmethod
        def __set_current_volume(volume):
            """
            Current volumne setter
            prevents numbers higher than 100 and numbers lower than 0
            :return: void
            """
            if volume > 100:
                Sound.__current_volume = 100
            elif volume < 0:
                Sound.__current_volume = 0
            else:
                Sound.__current_volume = volume


        # The sound is not muted by default, better tracking should be made
        __is_muted = False

        @staticmethod
        def is_muted():
            """
            Is muted getter
            :return: boolean
            """
            return Sound.__is_muted


        @staticmethod
        def __track():
            """
            Start tracking the sound and mute settings
            :return: void
            """
            if Sound.__current_volume == None:
                Sound.__current_volume = 0
                for i in range(0, 50):
                    Sound.volume_up()

        @staticmethod
        def volume_up():
            """
            Increase system volume
            Done by triggering a fake VK_VOLUME_UP key event
            :return: void
            """
            Sound.__track()
            Sound.__set_current_volume(Sound.current_volume() + 2)
            keyboard.send('volume up')

        @staticmethod
        def volume_down():
            """
            Decrease system volume
            Done by triggering a fake VK_VOLUME_DOWN key event
            :return: void
            """
            Sound.__track()
            Sound.__set_current_volume(Sound.current_volume() - 2)
            keyboard.send('volume down')

        @staticmethod
        def volume_set(amount):
            """
            Set the volume to a specific volume, limited to even numbers.
            This is due to the fact that a VK_VOLUME_UP/VK_VOLUME_DOWN event increases
            or decreases the volume by two every single time.
            :return: void
            """
            Sound.__track()

            if Sound.current_volume() > amount:
                for i in range(0, int((Sound.current_volume() - amount) / 2)):
                    Sound.volume_down()
            else:
                for i in range(0, int((amount - Sound.current_volume()) / 2)):
                    Sound.volume_up()


    def pc_settings(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '🔧 *Вы перешли в меню настроек ПК!*', reply_markup=pc_settings_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, pc_settings_check)

    def pc_settings_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return start(message)
        elif message.text.strip() == '/start': return start(message)
        elif message.text.strip() == settings_pc_menu_change_brightness: return brightness_set(message)
        elif message.text.strip() == settings_pc_menu_change_volume: return volume_set(message)
        elif message.text.strip() == settings_pc_menu_info_pc:
            conn = HTTPConnection("ifconfig.me")
            try:
                conn.request("GET", "/ip")
                ip = conn.getresponse().read()
            except:
                ip = "Неизвестно"

            total_mem, used_mem, free_mem = disk_usage('.')
            gb = 10 ** 9
            login = os.getlogin()
            width, height = pyautogui.size()
            oper = uname()
                
            try: virtual_memory = psutil.virtual_memory()
            except: virtual_memory = 'неизвестно'
            try: battery = str(psutil.sensors_battery()[0]) + '%'
            except: battery = 'неизвестно'
            active_window = getActiveWindowTitle()

            if active_window == None or active_window == '': active_window = 'Рабочий стол'
            bot.send_message(ACCESS, f'🧐 Компьютер подключен!\n\n⏰ Точное время запуска: *{startup_time}*\n💾 Имя пользователя - *{login}*\n🪑 Операционная система - *{oper[0]} {oper[2]} {oper[3]}*\n🧮 Процессор - *{oper[5]}*\n😻 Оперативная память: *Доступно {int(virtual_memory[0] / 1e+9)} ГБ | Загружено {virtual_memory[2]}%*\n🔋 Батарея заряжена на *{battery}*\n🖥 Разрешение экрана - *{width}x{height}*\n📀 Память: ' + '*{:6.2f}* ГБ'.format(total_mem/gb) + " всего, осталось *{:6.2f}* ГБ".format(free_mem/gb) + f'\n🔑 IP адрес запустившего - *{str(ip)[2:-1]}*\n*🖼 Активное окно - {active_window}*', parse_mode="Markdown")
            return pc_settings(message)

        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return pc_settings(message)


    def volume_set(message: types.Message):
        if is_access_denied(message.from_user): return None
        bot.send_message(message.chat.id, f'🔧 *Введите уровень громкости (0-100)!\n\nТекущий уровень - {Sound.current_volume()}*', reply_markup=back_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_volume_set)

    def check_volume_set(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        level = message.text.strip()
        if level  == back_text: return pc_settings(message)
        elif level == '/start': return start(message)
        elif not message.text.strip().isdigit():
            bot.send_message(message.chat.id, f'❌ *Уровень громкости должен быть числом!*', parse_mode='Markdown')
            return pc_settings(message)

        if int(level) < 0 or int(level) > 100: return bot.send_message(message.chat.id, f'❌ *Уровень громкости должен быть больше 0 и меньше 100!*', parse_mode='Markdown')
            
        Sound.volume_set(int(level))
        bot.send_message(message.chat.id, f'✅ Вы успешно установили уровень громкости *{level}*!', parse_mode='Markdown')
        return pc_settings(message)


    def brightness_set(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, f'🔧 *Введите уровень яркости (0-100)!\n\nТекущий уровень - {get_brightness()}*', reply_markup=back_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_brightness_set)

    def check_brightness_set(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        level = message.text.strip()
        if level  == back_text: return pc_settings(message)
        elif level == '/start': return start(message)
        elif not message.text.strip().isdigit():
            bot.send_message(message.chat.id, f'❌ *Уровень яркости должен быть числом!*', parse_mode='Markdown')
            return pc_settings(message)

        if int(level) < 0 or int(level) > 100: return bot.send_message(message.chat.id, f'❌ *Уровень яркости должен быть больше 0 и меньше 100!*', parse_mode='Markdown')
            
        set_brightness(int(level))
        bot.send_message(message.chat.id, f'✅ Вы успешно установили уровень яркости *{level}*!', parse_mode='Markdown')
        return pc_settings(message)

    if __name__ == '__main__':
        startup_time = datetime.now()
        message = bot.send_message(ACCESS, f'🧐 Компьютер подключен!\n\n⏰ Точное время запуска: *{startup_time}*\n💾 Имя пользователя - *{login}*\n🪑 Операционная система - *{oper[0]} {oper[2]} {oper[3]}*\n🧮 Процессор - *{oper[5]}*\n😻 Оперативная память: *Доступно {int(virtual_memory[0] / 1e+9)} ГБ | Загружено {virtual_memory[2]}%*\n🔋 Батарея заряжена на *{battery}*\n🖥 Разрешение экрана - *{width}x{height}*\n📀 Память: ' + '*{:6.2f}* ГБ'.format(total_mem/gb) + " всего, осталось *{:6.2f}* ГБ".format(free_mem/gb) + f'\n🔑 IP адрес запустившего - *{str(ip)[2:-1]}*', parse_mode="Markdown")
        mainmenu(message)
        bot.infinity_polling(none_stop = True, skip_pending=True)
except:
    pass