class AssetHolder:
    """class to allow instantiating our lists so we don't have to reload"""

    def __init__(self):
        self.given = self._load_as_set("assets/lists/given-names")
        self.surnames = self._load_as_set("assets/lists/surnames")
        self.states = self._load_as_set("assets/lists/states")
        self.canada = self._load_as_set("assets/lists/canada")
        self.cities = self._load_as_set("assets/lists/cities")
        self.counties = self._load_as_set("assets/lists/counties")
        self.zipcodes = self._load_as_set("assets/lists/zipcodes")
        self.fips = self._load_as_set("assets/lists/fips")

    @staticmethod
    def _load_as_set(filepath) -> set:
        """load a newline separated file as a set"""
        with open(filepath) as f:
            content = f.read().splitlines()
        return set(content)
