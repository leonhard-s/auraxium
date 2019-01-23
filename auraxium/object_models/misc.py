class LocalizedString():
    """A localized string.

    The Census API uses localized strings for player-visible values,
    such as item descriptions and names.
    This object acts as a dummy to allow accessing the name fields
    through attributes.

    """

    def __init__(self, data):
        if data is None:
            d = {}
        else:
            d = data
        self.de = d.get('de')
        self.en = d.get('en')
        self.es = d.get('es')
        self.fr = d.get('fr')
        self.it = d.get('it')
        self.tr = d.get('tr')
