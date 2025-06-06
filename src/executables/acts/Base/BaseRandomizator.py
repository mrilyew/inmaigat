from executables.acts.Base.Base import BaseAct

class BaseRandomizator(BaseAct):
    name = 'baseRandomizer'
    category = 'base'

    def declare():
        params = {}
        params["limit"] = {
            "type": "int",
            "default": 10,
            "docs": {
                "definition": {
                    "ru": "Лимит полученных данных",
                    "en": "Limit of recieved items",
                }
            },
            "assertion": {
                "not_null": True,
            },
        }

        return params

    async def execute(self, args={}):
        return {"entities": await self._returnItems()}

    async def _returnItems(self):
        items = await self._recieveItems()
        fnl = []
        for item in items:
            fnl.append(item)

        return fnl

    async def _recieveItems(self)->list:
        return []
