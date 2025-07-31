class DataSourceBase:
    def fetch(self, location, disaster_type):
        """
        Fetch data for the given location and disaster type.
        Returns a dict of standardized features.
        """
        raise NotImplementedError 