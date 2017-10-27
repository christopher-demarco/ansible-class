import codecs

def rot13(text):
    return codecs.encode(text, 'rot_13')

class FilterModule(object):
    def filters(self):
        return { 'rot13': rot13 }
    
