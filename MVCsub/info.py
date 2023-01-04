from datetime import date
import requests
import tkinter as tk
from PIL import ImageTk, Image
from MVCmain.ABC import ABCController
from Utils.TypingHint.settings import GUIType
from Utils.multiframetemplate import TwoFrameView
from Utils.TypingHint.locale import InfoView as locale
from Utils.variable import API_URL, PERMISSION_ASKED
from Utils.observable import Observable


class InfoController:
    def __init__(self, main_controller: ABCController):
        self.main_controller = main_controller
        self.main_view = main_controller.view
        self.main_model = main_controller.model

        self.view = InfoView(
            master=self.main_view.root,
            opt=self.main_model.get_gui_opt()
        )
        self.model = InfoModel(controller=self)

        self.view.login_button.config(
            command=self.model.request_permission_api
        )

        self.model.user_data.addCallback(
            lambda e: self.confirm_login(self.model.user_data.get())
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


class InfoView(TwoFrameView):
    TAG = 'General Info'

    def __init__(self, master: tk.Tk, opt: GUIType):

        TwoFrameView.__init__(self, master=master, opt=opt)

        image = Image.open(fr'assets/img/ori.png')
        image.thumbnail((300, 300))
        image = ImageTk.PhotoImage(image)

        self.logo = tk.Label(
            self.right_frame,
            image=image,
            bg=opt['bg_general']
        )
        self.logo.image = image  # type: ignore

        self.name_of_the_app = tk.Label(
            self.left_frame,
            text=locale['name_of_the_app'],
            **opt['title_config'],
        )

        self.app_description = tk.Label(
            self.left_frame,
            text=locale['app_description'],
            justify=tk.LEFT,
            anchor='w',
            **opt['text_config']
        )

        self.how_to_use = tk.Message(
            self.left_frame,
            text=locale['how_to_use'],
            anchor='w',
            **opt['subtitle_config']
        )

        self.login_button = tk.Button(
            self.left_frame,
            text=locale['login_button'],
            padx=10,
            pady=10,
            **opt['button_config']
        )

        self.author = tk.Label(
            self.left_frame,
            text=locale['author'] + date.today().year.__str__(),
            **opt['text_config']
        )

        self.name_of_the_app.pack(fill=tk.X, pady=15)
        self.app_description.pack(fill=tk.X, padx=30)
        self.how_to_use.pack(fill=tk.BOTH, padx=30, pady=15)
        self.login_button.pack(fill=tk.Y)
        self.author.pack(fill=tk.X, side=tk.BOTTOM, pady=15)

        self.logo.pack(fill=tk.BOTH, expand=True)


class InfoModel:
    def __init__(self, controller):
        self.controller = controller
        self.user_data = Observable({})

    def request_permission_api(self, api_url: str = API_URL):

        # payload = {
        #     "action": 'UserLogin',
        #     "data": {
        #         'token': None,
        #         'nickname': 'Tommaso' + str(PERMISSION_ASKED),
        #         'password': str(PERMISSION_ASKED),

        #     }
        # }

        response = requests.get(api_url+'?action=UserLogin')
        print(response.text)
        response = response.json()

        if response['Status'] == 0:
            self.user_data.set(response['Data'])
        else:
            self.user_data.set({})
