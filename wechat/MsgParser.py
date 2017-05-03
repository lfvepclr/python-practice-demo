import untangle as xml


class Message:
    def __init__(self, msgXml):
        self.xmlObj = xml.parse(msgXml)