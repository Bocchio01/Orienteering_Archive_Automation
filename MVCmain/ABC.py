from abc import ABC, abstractmethod

from MVCmain.model import Model
from MVCmain.view import MainView


class ABCController(ABC):
    @abstractmethod
    def __init__(self, view: MainView, model: Model) -> None:
        self.view = view
        self.model = model
