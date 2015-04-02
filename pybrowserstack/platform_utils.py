
_caps = []

def setcap(caps):
    global _caps
    if not isinstance(caps,list):
        caps = [caps]
    _caps = _caps + caps

def getcaps():
    global _caps
    return list(set(_caps))

def reset_caps():
    _caps = []
