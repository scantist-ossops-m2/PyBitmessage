"""The Inventory singleton"""

# TODO make this dynamic, and watch out for frozen, like with messagetypes
import storage.filesystem
import storage.sqlite
from bmconfigparser import config
from singleton import Singleton


def create_inventory_instance(backend="sqlite"):
    """
    Create an instance of the inventory class
    defined in `storage.<backend>`.
    """
    return getattr(
        getattr(storage, backend),
        "{}Inventory".format(backend.title()))()


@Singleton
class Inventory():
    """
    Inventory singleton class which uses storage backends
    to manage the inventory.
    """
    def __init__(self):
        self._moduleName = config.safeGet("inventory", "storage")
        self._realInventory = create_inventory_instance(self._moduleName)
        self.numberOfInventoryLookupsPerformed = 0

    # cheap inheritance copied from asyncore
    def __getattr__(self, attr):
        if attr == "__contains__":
            self.numberOfInventoryLookupsPerformed += 1
        try:
            realRet = getattr(self._realInventory, attr)
        except AttributeError:
            raise AttributeError(
                "%s instance has no attribute '%s'" %
                (self.__class__.__name__, attr)
            )
        else:
            return realRet

    # hint for pylint: this is dictionary like object
    def __getitem__(self, key):
        return self._realInventory[key]

    def __setitem__(self, key, value):
        self._realInventory[key] = value
