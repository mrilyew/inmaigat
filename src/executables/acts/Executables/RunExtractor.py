from db.ContentUnit import ContentUnit
from executables.acts.Base.Base import BaseAct
from app.App import logger
from repositories.ExtractorsRepository import ExtractorsRepository

class RunExtractor(BaseAct):
    name = 'RunExtractor'
    category = 'Executables'
    docs = {
        "description": {
            "name": {
                "ru": "...",
                "en": "..."
            },
            "definition": {
                "ru": "...",
                "en": "..."
            }
        },
        "returns": {
            "end": True,
            "type": "list",
        }
    }
    declaration_cfg = {
        'free_args': True
    }

    def declare():
        params = {}
        params["extractor"] = {
            "type": "string",
            "assertion": {
                "not_null": True
            }
        }
        params["return_raw"] = {
            'type': 'bool',
            'default': False,
            'assertion': {
                'not_null': True
            }
        }
        params["append_ids"] = {
            'type': 'csv',
            'default': [],
            'assertion': {
                'not_null': True
            }
        }

        return params

    async def execute(self, i = {}):
        extractor_name = i.get('extractor') # Extractor that will be using for export

        assert extractor_name != None, 'extractor not passed'

        append_ids = i.get('append_ids', None)

        colls_list = ContentUnit.ids(append_ids)

        extractor_class = (ExtractorsRepository()).getByName(extractor_name)

        assert extractor_class != None, 'Extractor not found'
        assert extractor_class.canBeExecuted(), 'Extractor is abstract'

        extractor = extractor_class()
        for _col in colls_list:
            if _col.is_collection == True:
                pass

            extractor.add_after.append(_col)

        results = []
        out = []

        extractor.link(results)

        try:
            await extractor.safeExecute(i)

            assert results != None, "Nothing returned"
        except KeyboardInterrupt:
            pass
        except Exception as __ee:
            logger.logException(__ee, section='Extractors')

            raise __ee

        assert len(results) > 0, "nothing exported"

        for __res in results:
            __res.save()

            for ext in extractor.add_after:
                if ext != None:
                    ext.addLink(__res)

            if i.get("return_raw") == True:
                out.append(__res)
            else:
                out.append(__res.api_structure())

        return out
