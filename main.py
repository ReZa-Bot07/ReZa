from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
import requests
import threading

# آدرس سرور (فعلاً تستی است، بعداً عوض می‌شود)
BASE_URL = "https://my-bot-server.onrender.com"

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=40, spacing=20, md_bg_color=(0.05, 0.05, 0.1, 1))
        
        layout.add_widget(MDLabel(text="ورود به پنل مدیریت", halign="center", theme_text_color="Custom", text_color=(1,1,1,1), font_style="H5"))
        
        self.user_input = MDTextField(hint_text="نام کاربری", text="Javad", mode="rectangle", icon_right="account")
        self.pass_input = MDTextField(hint_text="رمز عبور", password=True, mode="rectangle", icon_right="lock")
        self.pass_input.text = "123456"
        
        layout.add_widget(self.user_input)
        layout.add_widget(self.pass_input)
        
        self.login_btn = MDRaisedButton(text="ورود به پنل", md_bg_color=(0, 1, 0.5, 1), size_hint=(1, None), height=50)
        self.login_btn.bind(on_release=self.do_login)
        layout.add_widget(self.login_btn)
        
        self.status_label = MDLabel(text="", halign="center", theme_text_color="Error")
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)

    def do_login(self, instance):
        self.status_label.text = "در حال اتصال..."
        username = self.user_input.text
        password = self.pass_input.text
        threading.Thread(target=self.send_login_request, args=(username, password)).start()

    def send_login_request(self, username, password):
        try:
            response = requests.post(f"{BASE_URL}/api/app/login", json={"username": username, "password": password}, timeout=5)
            if response.status_code == 200:
                self.status_label.text = "اتصال موفق!"
                self.status_label.theme_text_color = "Custom"
                self.status_label.text_color = (0, 1, 0, 1)
            else:
                self.status_label.text = "نام کاربری یا رمز اشتباه است"
        except Exception as e:
            self.status_label.text = f"خطای اتصال: سرور روشن نیست یا IP اشتباه است"

class SoroushApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        return LoginScreen()

if __name__ == '__main__':
    SoroushApp().run()
