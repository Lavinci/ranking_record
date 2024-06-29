import json

def parseJson(txt:str):
    try:
        obj = json.loads(txt, strict=False)
    except Exception as e:
        print(f'parse error:', e.args[0])
        return {}
    return obj