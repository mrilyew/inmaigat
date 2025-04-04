from resources.Globals import VkApi, utils, logger
from executables.extractors.Vk.VkTemplate import VkTemplate
from resources.Exceptions import NotFoundException

# Downloads document from vk.com using api.
class VkPoll(VkTemplate):
    name = 'VkPoll'
    category = 'Vk'
    params = {
        "item_id": {
            "desc_key": "vk_poll_desc",
            "type": "string",
            "maxlength": 3
        },
    }

    def setArgs(self, args):
        self.passed_params["item_id"] = args.get("item_id")
        self.passed_params["__json_info"] = args.get("__json_info", None)
        self.passed_params["indexation_text_cut"] = int(args.get("indexation_text_cut", "699"))

        assert self.passed_params.get("item_id") != None or self.passed_params.get("preset_json") != None, "item_id not passed"

        super().setArgs(args)
    
    async def __recieveById(self, item_id):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        spl = item_id.split("_")
        return await __vkapi.call("polls.getById", {"owner_id": spl[0], "poll_id": spl[1], "extended": 1})
    
    async def run(self, args):
        __ITEM_RES = None
        __SOURCE   = None
        POLL = None
        __ITEM_ID  = self.passed_params.get("item_id")
        if self.passed_params.get("__json_info") == None:
            try:
                __ITEM_RES = await self.__recieveById(__ITEM_ID)
                if __ITEM_RES != None:
                    POLL = __ITEM_RES
            except:
                POLL = None
        else:
            try:
                __ITEM_RES = self.passed_params.get("__json_info")
                POLL = __ITEM_RES
            except:
                POLL = None

        if POLL == None:
            raise NotFoundException("poll not found")
        
        # TODO: background downloader
        logger.log(message=f"Recieved poll {__ITEM_ID}",section="VkPoll",name="message")
        if __ITEM_ID == None:
            __ITEM_ID  = f"{POLL.get("owner_id")}_{POLL.get("id")}"
            __SOURCE   = f"vk:poll{__ITEM_ID}"
        else:
            __SOURCE = f"vk:poll{__ITEM_ID}"
        
        POLL["site"] = self.passed_params.get("vk_path")
        __indexation = utils.clearJson(POLL)
        ENTITY = self._entityFromJson({
            "source": __SOURCE,
            "indexation_content": __indexation,
            "internal_content": POLL,
            "unlisted": self.passed_params.get("unlisted") == 1,
        })

        return {
            "entities": [
                ENTITY
            ]
        }
