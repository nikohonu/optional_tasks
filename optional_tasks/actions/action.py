from abc import ABC, abstractmethod


class Action(ABC):
    def __init__(self, subparsers, names: list, help: str):
        self.names = names
        self.parser = subparsers.add_parser(self.names[0],
                                            aliases=self.names[1:], help=help)

    @abstractmethod
    def do(self, args):
        pass
