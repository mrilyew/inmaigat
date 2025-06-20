from executables.representations.ExtractStrategy import ExtractStrategy
from executables.representations.Representation import Representation
from db.DbInsert import db_insert

class Scratch(Representation):
    category = "Abstract"
    executable_cfg =  {
        'free_args': True
    }

    class Extractor(ExtractStrategy):
        async def extractByDefault(self, i = {}):
            out = db_insert.contentFromJson({
                'content': i,
            })

            return [out]

        def extractWheel(self, i = {}):
            return 'extractByDefault'
