from MVCmain.ABC import ABCController

from MVCmain.view import MainView
from MVCmain.model import Model

from MVCsub.info import InfoController
from MVCsub.foldersanalysis import FoldersAnalysisController
from MVCsub.mapdetail import MapDetailController


class Controller(ABCController):

    def __init__(self, view: MainView, model: Model):
        self.view = view
        self.model = model

        self.register_module(InfoController(self))
        self.register_module(FoldersAnalysisController(self))
        self.register_module(MapDetailController(self))

    def register_module(self, module):
        self.view.add_view_to_menu_bar(module.view)

    def start(self):
        self.view.start_main_loop()
