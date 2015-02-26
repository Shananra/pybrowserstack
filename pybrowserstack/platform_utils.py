
_caps = []

def setcap(caps):
    global _caps
    if not isinstance(caps,list):
        caps = [caps]
    _caps = _caps + caps

def getcaps():
    global _caps
    return _caps
