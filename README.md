# 🇺🇸 | TelegramRemotePC (EN)
Remote computer management via Telegram is a convenient and secure way to control your computer from anywhere in the world. This script provides a wide range of functions for computer management:

- The ability to run programs, files, as well as a special function for running Python scripts.
- Complete file and folder management: create, delete, edit.
- The ability to enter commands in the Windows command prompt.
- Creation of dialog boxes (MSGBOX).
- Taking screenshots of the screen and camera, as well as recording video from the camera (up to 60 seconds) and recording voice messages (up to 60 seconds).
- Full keyboard access to use keyboard shortcuts and print characters.
- Automatic output of information about the computer when the bot is launched: IP address, startup time, screen resolution, information about memory, user name, active window, installed OS, processor, RAM, battery. This function can be called at any time.
- Opening websites, controlling the brightness of the screen.
- Download files from a PC up to 50 MB and upload files up to 20 MB with the option of choosing a path.
- Trolling with moving the mouse, opening websites and explorer.
- Quick shutdown, PC reboot or logout

For the effective functioning of this script, it is necessary to compile it and implement the necessary parameters of the telegram bot API into it, as well as specify your own Telegram ID. This process will allow you to gain full control over access control to your computer. Thanks to this security measure, you can reliably protect your device from unwanted intrusions.

❗️ Please note that as the author of this script, I am not responsible for any actions that may be performed by you based on my recommendations or instructions. You take full responsibility for your actions and the risks associated with them. I want to emphasize that I do not urge you to perform any actions without proper assessment and understanding of their consequences. Please remember that the use of this script is intended solely for remote control of your computer and should not be used for illegal purposes.

# RUN THE COMMAND IN THE COMMAND PROMPT:
pip install pyautogui subprocess keyboard psutil sqlite3 opencv-python pyaudio pywin32 telebot pygetwindow requests aiohttp asyncio screen_brightness_control

# HOW TO CREATE A BOT IN TELEGRAM AND GIVE YOURSELF RIGHTS:
- Find the Telegram bot @BotFather in the search and start a dialogue with him by clicking the "Start" button.
- Write the /newbot command to create a new bot.
- Follow the instructions of BotFather, enter a name for your bot and get a unique username for it.
- Replace "YOUR_BOT_TOKEN_HERE" in the script called "TelegramRemotePCUS" with the copied token from BotFather.
- Replace "YOUR_ID_TELEGRAM" in the script called "TelegramRemotePCUS" with your Telegram ID.

# TO COMPILE A PYTHON FILE INTO AN EXECUTABLE FILE (EXE) USING PYINSTALLER AND ADD AN ICON, FOLLOW THE INSTRUCTIONS BELLOW

1. Install PyInstaller if you don't have it yet. You can install it using pip by running the following command:

       pip install PyInstaller

2. Open a command Prompt or terminal and navigate to the directory where your Python file is located, which you want to compile into an EXE.

       pyinstaller -w -F --icon "path/to/your/icon.ico" "path/to/your/script.py"

       -w means that the console window will not be displayed at startup.
       -F tells PyInstaller to create a single executable file (exe).
       --icon "path/to/your/icon.ico" allows you to add an icon to your executable file. Specify the path to your icon in the .ico format.
       "path/to/your/script.py " - path to your Python file

3. After executing this command, PyInstaller will compile your Python file into an executable file (EXE) with the specified icon.

# HOW TO PUT AN EXECUTABLE FILE IN STARTUP:
1. First download the exe file that you want to wrap in a shortcut to your computer.
2. Locate the exe file on your computer and right-click on it.
3. In the context menu that opens, select "Send to desktop (shortcut)".
4. Now you will have a shortcut on your desktop that leads to your exe file.
5. To add this shortcut to the startup, press Win + R to open the Run window. Type "shell:startup" and press Enter. This will open the startup folder.
6. Transfer the shortcut of the exe file from the desktop to the open startup folder. Now, every time you start your computer, your exe file will automatically start.
7. Restart your computer to make sure everything is working correctly.

# 🇷🇺 | TelegramRemotePC
Удаленное управление компьютером через Telegram - это удобный и безопасный способ контролировать свой компьютер из любой точки мира. Данный скрипт предоставляет широкий спектр функций для управления компьютером:

- Возможность запуска программ, файлов, а также специальной функции для запуска Python скриптов.
- Полное управление файлами и папками: создание, удаление, редактирование.
- Возможность ввода команд в командной строке Windows.
- Создание диалоговых окон (MSGBOX).
- Создание скриншотов экрана и камеры, а также запись видео с камеры (до 60 секунд) и запись голосовых сообщений (до 60 секунд).
- Полный доступ к клавиатуре для использования сочетаний клавиш и печати символов.
- Автоматический вывод информации о компьютере при запуске бота: IP-адрес, время запуска, разрешение экрана, информация о памяти, имени пользователя, активном окне, установленной ОС, процессоре, ОЗУ, батарее. Эту функцию можно вызвать в любое время.
- Открытие сайтов, управление яркостью экрана.
- Скачивание файлов с ПК до 50 МБ и выгрузка файлов до 20 МБ с возможностью выбора пути.
- Троллинг с перемещением мыши, открытием сайтов и проводника.
- Быстрое выключение, перезагрузка ПК или выход из учетной записи.
- Управление процессами: отображение списка и выключение процессов.
- Максимальная защита от посторонних лиц с неограниченным количеством администраторов, выдача доступа по ID Telegram пользователя.
- Просмотр количества директорий на компьютере и открытие желаемой директории.

Для эффективного функционирования данного скрипта необходимо провести его компиляцию и внедрить в него необходимые параметры API телеграм бота, а также указать собственный Telegram ID. Этот процесс позволит вам получить полный контроль над управлением доступом к вашему компьютеру. Благодаря данной мере безопасности вы сможете надежно защитить ваше устройство от нежелательных вторжений.

❗️ Обратите внимание, что я, как автор данного скрипта, не несу ответственности за любые действия, которые могут быть выполнены Вами на основе моих рекомендаций или инструкций. Вы принимаете на себя полную ответственность за свои действия и риски, связанные с ними. Я хочу подчеркнуть, что не призываю Вас выполнять какие-либо действия без должной оценки и понимания их последствий. Пожалуйста, помните, что использование данного скрипта предназначено исключительно для удаленного управления вашим компьютерм и не должно быть использовано в нелегальных целях.

# Выполните команду в командной строке:
pip install pyautogui subprocess keyboard psutil sqlite3 opencv-python pyaudio pywin32 telebot pygetwindow requests aiohttp asyncio screen_brightness_control

# Как создать бота в Telegram и выдать себе права:
- Найдите в поиске Telegram бота @BotFather и начните с ним диалог, нажав кнопку "Start".
- Напишите команду /newbot, чтобы создать нового бота.
- Следуйте инструкциям BotFather, введите имя для вашего бота и получите уникальное имя пользователя для него.
- Замените "YOUR_BOT_TOKEN_HERE" в скрипте под названием "TelegramRemotePCRU" на скопированный токен от BotFather.
- Замените "YOUR_ID_TELEGRAM" в скрипте под названием "TelegramRemotePCRU" на ваш ID Telegram.

# Для того чтобы скомпилировать файл Python в исполняемый файл (exe) с помощью PyInstaller и добавить иконку, следуйте инструкциям ниже:

1. Установите PyInstaller, если у вас его еще нет. Вы можете установить его с помощью pip, выполнив следующую команду:

       pip install pyinstaller
       
2. Откройте командную строку (Command Prompt) или терминал и перейдите в директорию, где находится ваш файл Python, который вы хотите скомпилировать в exe.

       pyinstaller -w -F --icon "path/to/your/icon.ico" "path/to/your/script.py"

        -w означает, что консольное окно не будет отображаться при запуске.
        -F указывает pyInstaller создать один исполняемый файл (exe).
        --icon "path/to/your/icon.ico" позволяет добавить иконку к вашему исполняемому файлу. Укажите путь к вашей иконке в формате .ico.
        "path/to/your/script.py" - путь к Вашему файлу Python

3. После выполнения этой команды PyInstaller скомпилирует ваш файл Python в исполняемый файл (exe) с указанной иконкой.

# Как поставить исполняемый файл в автозагрузки:
1. Сначала загрузите файл exe, который вы хотите обернуть в ярлык, на ваш компьютер.
2. Найдите файл exe на вашем компьютере и нажмите правой кнопкой мыши на нем.
3. В открывшемся контекстном меню выберите "Отправить на рабочий стол (ярлык)".
4. Теперь у вас будет ярлык на рабочем столе, который ведет к вашему файлу exe.
5. Чтобы добавить этот ярлык в автозагрузку, нажмите Win + R, чтобы открыть окно "Выполнить". Введите "shell:startup" и нажмите Enter. Это откроет папку автозагрузки.
6. Перенесите ярлык файла exe из рабочего стола в открытую папку автозагрузки. Теперь при каждом запуске компьютера ваш файл exe будет автоматически запускаться.
7. Перезагрузите компьютер, чтобы убедиться, что все работает корректно.
