# import logging

from MVCmain.view import MainView
from MVCmain.controller import Controller
from MVCmain.model import Model

# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(levelname)s:%(funcName)s():%(lineno)i: %(message)s"
# )


if __name__ == "__main__":
    c = Controller(MainView(), Model())
    c.start()
