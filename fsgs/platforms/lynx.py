from fsgs.drivers.mednafen.lynxdriver import MednafenLynxDriver
from fsgs.platform import PlatformHandler
from fsgs.platforms.loader import SimpleLoader


class LynxPlatformHandler(PlatformHandler):
    PLATFORM_NAME = "Lynx"

    def __init__(self):
        PlatformHandler.__init__(self)

    def get_loader(self, fsgs):
        return GameGearLoader(fsgs)

    def get_runner(self, fsgs):
        return MednafenLynxDriver(fsgs)


class GameGearLoader(SimpleLoader):
    pass
