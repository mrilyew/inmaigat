from utils.MainUtils import dump_json
from app.App import logger
from executables.Executable import Executable
import asyncio, time

class BaseService(Executable):
    name = 'base'
    config = {}
    interval = 10
    i = 0
    service_object = None

    def __init__(self):
        self.is_stopped = False

    def setConfig(self, conf):
        self.config = conf

    async def run(self):
        logger.log(message=f"Making run №{self.i + 1}",name="message",section="Services")

        try:
            res = await self.execute(args)
            print(utils.dump_json(res,indent=4))
        except Exception as e:
            logger.logException(input_exception=e,section="Services",silent=False)

        self.i = self.i+1

    def stop(self):
        self.is_stopped = True

    def execute(self, args = {}):
        pass

    def terminate(self):
        exit(-1)
