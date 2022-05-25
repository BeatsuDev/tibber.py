"""A class for generating GraphQL queries to send to the Tibber API"""

class QueryBuilder:
    @classmethod
    def create_query_from_dict(cls, query_dict: dict, indentation: int = 0, last: bool = True) -> str:
        """Creates a graphQL query from the keys of a dictionary.

        :param query_dict: The dictionary to convert to a query.
        :param indentation: The amount of spaces to indent the returned query.
        :param last: Specifies if the function call is the last in a recursive loop.
        """
        string_query = "{\n"

        for key, value in query_dict.items():                
            if isinstance(value, dict):
                string_query += " "*(indentation + 2) + key + " "
                string_query += cls.create_query_from_dict(value, indentation + 2, False)
                string_query += " "*(indentation + 2) + "}\n"
            else:
                string_query += " "*(indentation + 2) + key + "\n"

        if last:
            string_query += "}"
            
        return string_query
    
    @classmethod
    def create_query(cls, *args):
        """Creates a query given keys. The last argument must be a valid property of QueryBuilder that fits
        according to the GraphQL structure of the Tibber API.
        
        Exmaple:
            create_query("viewer", "homes", "currentSubscription", QueryBuilder.price_info)
        
            This returns a string query that queries specifically for the
            price_info of the current subscription in all homes.
        """
        if len(args) == 0:
            raise TypeError("The QueryBuilder.create_query method requires at least one argument!")
        
        def nest_dict(*keys):
            if len(keys) == 1:
                return keys[0]
            return {keys[0]: nest_dict(*keys[1:])}
        
        return QueryBuilder.create_query_from_dict(nest_dict(*args))
        
    @classmethod
    def combine_dicts(cls, dict1: dict, dict2: dict) -> dict:
        """Combines two nested dictionaries. The values from second dictionary overwrites the first one
        if the keys are exactly the same. The only exception to this is if the first dictionary's value
        is a dict, while the second dictionary value is a string. Then the dictionary with a dictionary
        typed value is prioritized.

        This method is meant to be used to combine query building components in dictionary form.

        :param dict1: The first dict to combine with the second dict
        :param dict2: The second dict to combine with the first dict
        :throws TypeError: If none of the parameters are dicts
        """
        if not (isinstance(dict1, dict) and isinstance(dict2, dict)):
            raise TypeError(f"Cannot combine types {type(dict1)} and {type(dict2)}.")

        result_dict = dict1

        for key, value in dict2.items():
            # The key in the second dict does not exist in the first so it's safe to add it
            # without overwriting the value from dict1 (because there is none)
            if not key in dict1.keys():
                result_dict[key] = value

            # If the value in dict1 is a string, and we know the key exists in both dict1
            # and dict2, the value from dict2 overwrite the value in dict1.
            elif isinstance(dict1[key], str):
                result_dict[key] = value

            # We know the key already exists in both dicts now. If the values in dict1 and dict 2
            # are also dicts, we need to call the function again on these dicts to resolve "merge conflicts"
            elif isinstance(value, dict):
                result_dict[key] = cls.combine_dicts(dict1[key], dict2[key])

            # We know the key exists in both dicts. If the value in dict1 is a dictionary, but
            # the value in dict2 is a string, the dict1 value is prioritized.
            elif isinstance(dict1[key], dict):
                # We can continue because the values of dict1 is already in the resulting dict
                continue

            # If the value in both dicts are strings.
            else:
                result_dict[key] = value

        return result_dict

    @classmethod
    @property
    def query_all_data(cls) -> str:
        return cls.create_query_from_dict(QueryBuilder.query)
    
    # -------------------------------------------------------------------
    # Query dicts for the Tibber API types. Remember that values ignored.
    # -------------------------------------------------------------------
    
    @classmethod
    @property
    def query(cls) -> dict:
        """Return a dict with query values as keys for all information on the `Query` type. This type is the base type
        which all queries are nested in. Therefore, this query returns all information available from the api.
        """
        return {"viewer": QueryBuilder.viewer}
    
    @classmethod
    @property
    def viewer(cls) -> dict:
        """Return a dict with query values as keys for all information on the `Viewer` type."""
        return {
            "login": "",
            "userId": "",
            "name": "",
            "accountType": [],
            "homes": QueryBuilder.home
        }

    @classmethod
    @property
    def home(cls) -> dict:
        """Return a dict with query values as keys for all information on the `Home` type."""
        return {
            "id": "",
            "timeZone": "",
            "appNickname": "",
            "appAvatar": "",
            "size": 0,
            "type": "",
            "numberOfResidents": 0,
            "primaryHeatingSource": "",
            "hasVentilationSystem": False,
            "mainFuseSize": 0,
            "address": QueryBuilder.address,
            "owner": QueryBuilder.legal_entity,
            "meteringPointData": QueryBuilder.metering_point_data,
            "currentSubscription": QueryBuilder.subscription,
            "subscriptions": QueryBuilder.subscription,
            "features": QueryBuilder.features
        }

    @classmethod
    @property
    def address(cls) -> dict:
        """Return a dict with query values as keys for all information on the `Address` type."""
        return {
            "address1": "",
            "address2": "",
            "address3": "",
            "city": "",
            "postalCode": "",
            "country": "",
            "latitude": "",
            "longitude": ""
        }

    @classmethod
    @property
    def legal_entity(cls) -> dict:
        """Return a dict with query values as keys for all information on the `LegalEntity` type."""
        return {
            "id": "",
            "firstName": "",
            "isCompany": False,
            "name": "",
            "middleName": "",
            "lastName": "",
            "organizationNo": "",
            "language": "",
            "contactInfo": QueryBuilder.contact_info,
            "address": QueryBuilder.address
        }

    @classmethod
    @property
    def metering_point_data(cls) -> dict:
        """Return a dict with query values as keys for all information on the `MeteringPointData` type."""
        return {
            "consumptionEan": "",
            "gridCompany": "",
            "gridAreaCode": "",
            "priceAreaCode": "",
            "productionEan": "",
            "energyTaxType": "",
            "vatType": "",
            "estimatedAnnualConsumption": 0
        }

    @classmethod
    @property
    def subscription(cls) -> dict:
        """Return a dict with query values as keys for all information on the `Subscription` type."""
        return {
            "id": "",
            "subscriber": QueryBuilder.legal_entity,
            "validFrom": "",
            "validTo": "",
            "status": "",
            "priceInfo": QueryBuilder.price_info,
            "priceRating": QueryBuilder.price_rating
        }

    @classmethod
    @property
    def features(cls) -> dict:
        """Return a dict with query values as keys for all information on the `HomeFeatures` type."""
        return {
            "realTimeConsumptionEnabled": False
        }

    @classmethod
    @property
    def contact_info(cls) -> dict:
        """Return a dict with query values as keys for all information on the `ContactInfo` type."""
        return {
            "email": "",
            "mobile": ""
        }

    @classmethod
    @property
    def price_info(cls) -> dict:
        """Return a dict with query values as keys for all information on the `PriceInfo` type."""
        return {
            "current": QueryBuilder.price,
            "today": QueryBuilder.price,
            "tomorrow": QueryBuilder.price
        }

    @classmethod
    @property
    def price_rating(cls) -> dict:
        """Return a dict with query values as keys for all information on the `PriceRating` type."""
        return {
            "thresholdPercentages": QueryBuilder.price_rating_threshold_percentages,
            "hourly": QueryBuilder.price_rating_type,
            "daily": QueryBuilder.price_rating_type,
            "monthly": QueryBuilder.price_rating_type,
        }

    @classmethod
    @property
    def price(cls) -> dict:
        """Return a dict with query values as keys for all information on the `Price` type."""
        return {
            "total": 0.0,
            "energy": 0.0,
            "tax": 0.0,
            "startsAt": "",
            "currency": "",
            "level": ""
        }

    @classmethod
    @property
    def price_rating_threshold_percentages(cls) -> dict:
        """Return a dict with query values as keys for all information on the `PriceRatingThresholdPercentages` type."""
        return {
            "high": 0.0,
            "low": 0.0
        }

    @classmethod
    @property
    def price_rating_type(cls) -> dict:
        """Return a dict with query values as keys for all information on the `PriceRatingType` type."""
        return {
            "minEnergy": 0.0,
            "maxEnergy": 0.0,
            "minTotal": 0.0,
            "maxTotal": 0.0,
            "currency": "",
            "entries": QueryBuilder.price_rating_entry
        }

    @classmethod
    @property
    def price_rating_entry(cls) -> dict:
        """Return a dict with query values as keys for all information on the `PriceRatingEntry` type."""
        return {
            "time": "",
            "energy": 0.0,
            "total": 0.0,
            "tax": 0.0,
            "difference": 0.0,
            "level": ""
        }

    # Queries with arguments. Note that these are different than queries in the way that
    # these components need to return the key for the query as well as all it's properties
    # not just the queries. This means that these should be unpacked when combined with
    # other queries, not added as a value of a key.

    @classmethod
    def single_home(home_id: str) -> dict:
        return {
            f"home({home_id})": QueryBuilder.home
        }
        
    @classmethod
    def consumption_query(cls, resolution: str, 
                          first: int = None, 
                          last: int = None, 
                          before: str = None, 
                          after: str = None, 
                          filter_empty_nodes: bool = False):
        # TODO: I feel like this can be improved...
        first_arg = f"first: {first}" if first else ""
        last_arg = f"last: {last}" if last else ""
        before_arg = f"before: \"{before}\"" if before else ""
        after_arg = f"after: \"{after}\"" if after else ""

        args = ", ".join([arg for arg in [first_arg, last_arg, before_arg, after_arg] if arg])
        return {
            f"consumption(resolution: {resolution}, {args}, filterEmptyNodes: {str(filter_empty_nodes).lower()})": {
                "pageInfo": QueryBuilder.home_consumption_page_info,
                "nodes": QueryBuilder.consumption,
                "edges": QueryBuilder.home_consumption_edge
            }
        }

    @classmethod
    def production_query(cls, resolution: str,
                         first: int = None,
                         last: int = None,
                         before: str = None,
                         after: str = None,
                         filter_empty_nodes: bool = False):
        first_arg = f"first: {first}" if first else ""
        last_arg = f"last: {last}" if last else ""
        before_arg = f"before: \"{before}\"" if before else ""
        after_arg = f"after: \"{after}\"" if after else ""

        args = ", ".join([arg for arg in [first_arg, last_arg, before_arg, after_arg] if arg])
        return {
            f"production(resolution: {resolution}, {args}, filterEmptyNodes: {str(filter_empty_nodes).lower()})": {
                "pageInfo": QueryBuilder.home_production_page_info,
                "nodes": QueryBuilder.production,
                "edges": QueryBuilder.home_production_edge
            }
        }

    @classmethod
    @property
    def home_consumption_page_info(cls):
        return {
            "endCursor": "",
            "hasNextPage": False,
            "hasPreviousPage": False,
            "startCursor": "",
            "count": 0,
            "currency": "",
            "totalCost": 0.0,
            "totalConsumption": 0.0,
            "filtered": 0
        }

    @classmethod
    @property
    def consumption(cls):
        return {
            "from": "",
            "to": "",
            "unitPrice": 0.0,
            "unitPriceVAT": 0.0,
            "consumption": 0.0,
            "consumptionUnit": "",
            "cost": 0.0,
            "currency": ""
        }

    @classmethod
    @property
    def home_consumption_edge(cls):
        return {
            "cursor": "",
            "node": QueryBuilder.consumption
        }

    @classmethod
    @property
    def home_production_page_info(cls):
        return {
            "endCursor": "",
            "hasNextPage": False,
            "hasPreviousPage": False,
            "startCursor": "",
            "count": 0,
            "currency": "",
            "totalProfit": 0.0,
            "totalProduction": 0.0,
            "filtered": 0
        }

    @classmethod
    @property
    def production(cls):
        return {
            "from": "",
            "to": "",
            "unitPrice": 0.0,
            "unitPriceVAT": 0.0,
            "production": 0.0,
            "productionUnit": "",
            "profit": 0.0,
            "currency": ""
        }

    @classmethod
    @property
    def home_production_edge(cls):
        return {
            "cursor": "",
            "node": QueryBuilder.production
        }
        
    # Live data - This WILL be rewritten together with this whole class.
    @classmethod
    def live_measurement(cls, home_id):
        return f"""subscription {{
            liveMeasurement(homeId: "{home_id}") {{
                timestamp
                power
                lastMeterConsumption
                accumulatedConsumption
                accumulatedProduction
                accumulatedConsumptionLastHour
                accumulatedProductionLastHour
                accumulatedCost
                accumulatedReward
                currency
                minPower
                averagePower
                maxPower
                powerProduction
                powerProductionReactive
                minPowerProduction
                maxPowerProduction
                lastMeterProduction
                powerFactor
                voltagePhase1
                voltagePhase2
                voltagePhase3
                currentL1
                currentL2
                currentL3
                signalStrength
            }}
        }}"""
