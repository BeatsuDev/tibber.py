"""A class for generating GraphQL queries to send to the Tibber API"""

class QueryBuilder:
    
    @classmethod
    @property
    def update_all_info(cls) -> str:
        """Returns the query to update all info on the Tibber client, homes and price (client name, homes, price info, etc.)"""
        pass
    
    @classmethod
    @property
    def update_client_info(cls) -> str:
        """Returns the query to update the Tibber client information (name, id, etc.)."""
    
    @classmethod
    @property
    def update_homes_info(cls) -> str:
        """Returns the query to update information on all the homes (address, homes, etc.)."""
        pass
    
    @classmethod
    @property
    def update_price_info(cls) -> str:
        """Returns the query to update the price for all homes (current price, yesterdays price, etc.)."""
        pass
    