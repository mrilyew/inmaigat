from executables.extractors.Vk.VkTemplate import VkTemplate
from executables.extractors.Vk.VkPhoto import VkPhoto
from resources.Globals import VkApi, logger, math, asyncio

class VkAllPhotos(VkTemplate):
    name = 'VkAllPhotos'
    category = 'Vk'

    def declare():
        params = {}
        params["item_id"] = {
            "desc_key": "-",
            "type": "string",
            "assertion": {
                "assert_not_null": True,
            }
        }
        params["download_timeout"] = {
            "desc_key": "-",
            "type": "int",
            "default": 1,
        }
        params["api_timeout"] = {
            "desc_key": "-",
            "type": "int",
            "default": 1,
        }
        params["limit"] = {
            "desc_key": "-",
            "type": "int",
            "default": 0,
        }
        params["per_page"] = {
            "desc_key": "-",
            "type": "int",
            "default": 100
        }

        return params

    async def run(self, args):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        first_call = await __vkapi.call("photos.getAll", {"owner_id": self.passed_params.get("item_id"), "count": 1})
        total_count = first_call.get("count")
        final_entites_list = []

        logger.log(message=f"Total {total_count} photos",section="VkCollection",name="message")

        __per_page = self.passed_params.get("per_page")
        __downloaded_count = 0
        times = math.ceil(total_count / __per_page)
        vphoto_ext = VkPhoto(need_preview=self.need_preview)
        for time in range(0, times):
            OFFSET = __per_page * time
            if self.passed_params.get("limit") > 0 and (__downloaded_count > self.passed_params.get("limit")):
                break

            logger.log(message=f"{time + 1}/{times} time of photos recieving; {OFFSET} offset",section="VkCollection",name="message")
            photo_call = await __vkapi.call("photos.getAll", {"owner_id": self.passed_params.get("item_id"), "extended": 1, "count": 100, "photo_sizes": 1, "offset": OFFSET})
            for photo_item in photo_call.get("items"):
                if self.passed_params.get("limit") > 0 and (__downloaded_count > self.passed_params.get("limit")):
                    break
                
                __PHOTO_ID = str(photo_item.get("owner_id")) + "_" + str(photo_item.get("id"))
                vphoto_ext.setArgs({
                    "unlisted": 1,
                    "item_id": __PHOTO_ID,
                    "__json_info": photo_item,
                    "access_token": self.passed_params.get("access_token"),
                    "api_url": self.passed_params.get("api_url"),
                    "vk_path": self.passed_params.get("vk_path"),
                    "download_file": 1,
                })

                try:
                    executed = await vphoto_ext.execute({})
                    for __photo in executed.get("entities"):
                        final_entites_list.append(__photo)
                except Exception:
                    pass

                if self.passed_params.get("download_timeout") != 0:
                    await asyncio.sleep(self.passed_params.get("download_timeout"))

                __downloaded_count += 1
            
            await vphoto_ext.postRun(return_entities=final_entites_list)
            
            if self.passed_params.get("api_timeout") != 0:
                await asyncio.sleep(self.passed_params.get("api_timeout"))

        del vphoto_ext
        
        return {
            "entities": final_entites_list,
            "collection": {
                "suggested_name": f"Vk Photos {self.passed_params.get("item_id")}",
            },
        }
