import logging
from MVCmain.ABC import ABCController

from MVCmain.view import MainView
from MVCmain.model import Model

from MVCsub.info import InfoController
from MVCsub.scanformaps import ScanForMapsController
from MVCsub.listofmap import ListOfMapController


class Controller(ABCController):

    def __init__(self, view: MainView, model: Model):
        logging.debug(f"Controller")
        self.view = view
        self.model = model

        self.register_module(InfoController(self))
        self.register_module(ScanForMapsController(self))
        self.register_module(ListOfMapController(self))

    def register_module(self, module):
        logging.debug(f"Controller")
        self.view.add_view_to_menu_bar(module.view)

    def start(self):
        logging.debug(f"Controller")
        self.view.start_main_loop()

    def get_gui_opt(self):
        logging.debug(f"Controller")
        return self.model.get_gui_opt()

    def get_mega_settings(self):
        logging.debug(f"Controller")
        return self.model.get_settings()['MEGA']
