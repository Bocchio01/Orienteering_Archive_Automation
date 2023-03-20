from MVCmain.ABC import ABCController

from MVCmain.view import MainView
from MVCmain.model_composition import Model

from MVCsub.info import InfoController
from MVCsub.mapsmanagement import MapsManagementController


class Controller(ABCController):

    def __init__(self, view: MainView, model: Model):
        self.view = view
        self.model = model

        self.register_module(InfoController(self))
        self.register_module(MapsManagementController(self))

        self.view.show_target_frame(
            target_frame=MapsManagementController(self).view
        )

    def register_module(self, module):
        self.view.add_view_to_menu_bar(view=module.view)

    def start(self):
        self.view.start_main_loop()
