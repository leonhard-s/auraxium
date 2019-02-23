class LocalizedString():
    """A localized string.

    The Census API uses localized strings for player-visible values,
    such as item descriptions and names.
    This object acts as a dummy to allow accessing the name fields
    through attributes.

    """

    def __init__(self, data):
        if data is None:
            data_dict = {}
        else:
            data_dict = data
        self.de = data_dict.get('de')
        self.en = data_dict.get('en')
        self.es = data_dict.get('es')
        self.fr = data_dict.get('fr')
        self.it = data_dict.get('it')
        self.tr = data_dict.get('tr')
