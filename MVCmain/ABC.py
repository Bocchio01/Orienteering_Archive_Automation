from abc import ABC, abstractmethod

from matplotlib.backend_bases import ShowBase

# from MVCmain.model import Model
from MVCmain.model_composition import Model
from MVCmain.view import MainView


class ABCController(ABC):
    @abstractmethod
    def __init__(self, view: MainView, model: Model) -> None:
        self.view = view
        self.model = model


class ABCModel(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def register_module(self, module) -> None:
        pass
