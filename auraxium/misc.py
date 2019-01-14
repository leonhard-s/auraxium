class LocalizedString(object):
    """A localized string.

    The Census API uses localized strings for player-visible values,
    such as item descriptions and names.
    This object acts as a dummy to allow accessing the name fields
    through attributes.

    """

    def __init__(self, data):
        self.de = data.get('de')
        self.en = data.get('en')
        self.es = data.get('es')
        self.fr = data.get('fr')
        self.it = data.get('it')
        self.tr = data.get('tr')
