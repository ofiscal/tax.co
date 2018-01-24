def printInRed(message):
    """from https://stackoverflow.com/a/287934/916142"""
    CSI="\x1B["
    print( CSI+"31;40m" + message + CSI + "0m")
