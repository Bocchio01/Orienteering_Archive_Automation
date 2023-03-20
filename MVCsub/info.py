from datetime import date
import json
import requests
import tkinter as tk
from PIL import ImageTk, Image
from MVCmain.ABC import ABCController
from Utils.GUIWidgets.customwidgets import MultiFrameView
from Utils.TypingHint.locale import InfoView as locale
from Utils.variable import API_URL
from Utils.observable import Observable


class InfoController:
    def __init__(self, main_controller: ABCController):
        self.main_controller = main_controller
        self.main_view = main_controller.view
        self.main_model = main_controller.model

        self.view = InfoView(
            master=self.main_view.root,
        )

        self.model = self.main_model.register_module(InfoModel())
        self.view.login_button.config(
            command=self.model.request_permission_api
        )

        self.model.user_data.addCallback(
            lambda e: self.confirm_login(
                self.model.user_data.get())
        )

    def confirm_login(self, user_data: dict):

        if bool(user_data):
            self.main_view.prompt_message(data={
                'title': locale['login_action']['success']['title'],
                'message': locale['login_action']['success']['message'] + user_data['permission_code']
            })
        else:
            self.main_view.prompt_message(data={
                'title': locale['login_action']['failure']['title'],
                'message': locale['login_action']['failure']['message']
            })


class InfoView(MultiFrameView):
    TAG = 'General Info'

    def __init__(self, master: tk.Tk):

        MultiFrameView.__init__(self, master=master, weights=(1, 10))

        self.user_email = tk.StringVar(value='anonimus@OAA.com')
        self.user_pwd = tk.StringVar(value='')

        image = Image.open(fr'assets/img/ori.png')
        image.thumbnail((300, 300))
        image = ImageTk.PhotoImage(image)

        self.logo = tk.Label(
            self.frames[1],
            image=image,
        )
        self.logo.image = image  # type: ignore

        self.name_of_the_app = tk.Label(
            self.frames[0],
            text=locale['name_of_the_app'],
        )

        self.app_description = tk.Label(
            self.frames[0],
            text=locale['app_description'],
            justify=tk.LEFT,
            anchor='w',
        )

        self.how_to_use = tk.Message(
            self.frames[0],
            text=locale['how_to_use'],
            anchor='w',
        )

        self.form = tk.Frame(self.frames[0])

        self.username_label = tk.Label(self.form, text="Username:")

        self.username_entry = tk.Entry(
            self.form,
            textvariable=self.user_email
        )

        self.password_label = tk.Label(self.form, text="Password:")

        self.password_entry = tk.Entry(
            self.form,
            textvariable=self.user_pwd,
            show="*")
        self.login_button = tk.Button(self.form, text="Login")

        self.username_label.grid(column=0, row=1, sticky=tk.W)
        self.username_entry.grid(column=1, row=1, sticky=tk.E)
        self.password_label.grid(column=0, row=2, sticky=tk.W)
        self.password_entry.grid(column=1, row=2, sticky=tk.E)
        self.login_button.grid(column=1, row=3, sticky=tk.E)

        # self.ocad_path = tk.Label(
        #     self.frames[0],
        #     text=locale['ocad_path'],
        # )

        self.author = tk.Label(
            self.frames[0],
            text=locale['author'] + date.today().year.__str__(),
        )

        self.name_of_the_app.pack(fill=tk.X, pady=15)
        self.app_description.pack(fill=tk.X, padx=30)
        self.how_to_use.pack(fill=tk.BOTH, padx=30, pady=15)

        self.form.pack(fill=tk.X, padx=30, pady=15)

        self.author.pack(fill=tk.X, side=tk.BOTTOM, pady=15)

        self.logo.pack(fill=tk.BOTH, expand=True)


class InfoModel:
    def __init__(self):
        self.user_data = Observable({})

    def request_permission_api(self, api_url: str = API_URL):

        payload = {
            'token': 'sdcjnsdkjn',
            'email': 'tommaso.bocchietti0@gmail.com',
            'password': 'PWD0',
        }

        response = requests.post(
            url=api_url,
            data=json.dumps({
                'action': 'UserLogin',
                'data': payload
            }),
        )

        # print(response.text)
        response = response.json()

        if response['Status'] == 0:
            self.user_data.set(response['Data'])
        else:
            self.user_data.set({})
