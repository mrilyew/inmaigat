from executables.extractors.Vk.VkTemplate import VkTemplate
from resources.Globals import os, download_manager, VkApi, Path, json5, config, utils, logger
from resources.Exceptions import NotFoundException
#from core.Wheels import metadata_wheel, additional_metadata_wheel

# Downloads photo from vk.com using api.
class VkPhoto(VkTemplate):
    name = 'VkPhoto'
    category = 'Vk'
    params = {
        "item_id": {
            "desc_key": "item_id_desc",
            "type": "string",
            "maxlength": 3
        },
    }
    
    def setArgs(self, args):
        self.passed_params["item_id"] = args.get("item_id")
        self.passed_params["__json_info"] = args.get("__json_info", None)

        assert self.passed_params.get("item_id") != None or self.passed_params.get("__json_info") != None, "item_id not passed"

        super().setArgs(args)
    
    async def __recieveById(self, item_id):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("photos.getById", {"photos": item_id, "extended": 1, "photo_sizes": 1})
    
    async def run(self, args):
        # TODO add check for real links like vk.com/photo1_1
        __PHOTO_RES = None
        __PHOTO_ID  = self.passed_params.get("item_id")
        __PHOTO_OBJECT = None
        if self.passed_params.get("__json_info") == None:
            __PHOTO_RES = await self.__recieveById(__PHOTO_ID)
            try:
                __PHOTO_OBJECT = __PHOTO_RES[0]
                __PHOTO_ID  = f"{__PHOTO_OBJECT.get("owner_id")}_{__PHOTO_OBJECT.get("id")}"
            except:
                __PHOTO_OBJECT = None
        else:
            __PHOTO_RES = self.passed_params.get("__json_info")
            try:
                __PHOTO_OBJECT = __PHOTO_RES
            except Exception:
                __PHOTO_OBJECT = None
        
        if __PHOTO_OBJECT == None:
            raise NotFoundException("photo not found")

        ORIGINAL_NAME = f"photo_{__PHOTO_OBJECT.get("date")}.jpg"
        SAVE_PATH = Path(os.path.join(self.temp_dir, ORIGINAL_NAME))
        logger.log(message=f"Recieved photo {__PHOTO_ID}",section="VK",name="message")
        
        # So, downloading photo
        PHOTO_URL = ""
        if __PHOTO_OBJECT.get("orig_photo") != None:
            PHOTO_URL = __PHOTO_OBJECT.get("orig_photo").get("url")
        else:
            if __PHOTO_OBJECT.get("url") != None:
                PHOTO_URL = __PHOTO_OBJECT.get("url")
            else:
                try:
                    __photo_size = next((d for d in __PHOTO_OBJECT.get("sizes") if d.get("type") == "w"), None)
                    PHOTO_URL = __photo_size.get("url")
                except Exception as ___e:
                    logger.logException(___e, section="Vk")

                    __photo_sizes = sorted(__PHOTO_OBJECT.get("sizes"), key=lambda x: (x['width'] is None, x['width']))
                    PHOTO_URL = __photo_sizes[0].get("url")
        
        try:
            HTTP_REQUEST = await download_manager.addDownload(end=PHOTO_URL,dir=SAVE_PATH)
            FILE_SIZE = SAVE_PATH.stat().st_size

            __PHOTO_OBJECT["site"] = self.passed_params.get("vk_path")
            __indexation = utils.clearJson(__PHOTO_OBJECT)
            FILE = self._fileFromJson({
                "extension": "jpg",
                "upload_name": ORIGINAL_NAME,
                "filesize": FILE_SIZE,
            })
            ENTITY = self._entityFromJson({
                "file": FILE,
                "suggested_name": f"VK Photo {str(__PHOTO_ID)}",
                "source": "vk:photo"+str(__PHOTO_ID),
                "indexation_content": __indexation,
                "internal_content": __PHOTO_OBJECT,
                "unlisted": self.passed_params.get("unlisted") == 1,
            })
            
            return {
                "entities": [
                    ENTITY
                ]
            }
        except FileNotFoundError as _ea:
            logger.log(message="Photo's file cannot be found. Probaly broken file?",section="VK",name="error")
            raise _ea
