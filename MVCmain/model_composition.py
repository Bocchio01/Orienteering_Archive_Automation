from Utils.composition import Composite


class Model(Composite):
    def __init__(self):
        super().__init__()

    def register_module(self, module):
        self.add(module)

        return module
