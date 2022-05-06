"""A class for generating GraphQL queries to send to the Tibber API"""

class QueryBuilder:
    @classmethod
    def create_query_from_dict(cls, query_dict: dict, indentation: int = 0, last: bool=True) -> str:
        """Creates a graphQL query from the keys of a dictionary.
        
        :param query_dict: The dictionary to convert to a query.
        :param indentation: The amount of spaces to indent the returned query.
        :param last: Specifies if the function call is the last in a recursive loop.
        
        Example:
            {
                "name": "",
                "homes": {
                    "id": "",
                    "timeZone": ""
                }
            }
            becomes:
            "{
                name
                homes {
                    id
                    timezone
                }
            }"
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
    def update_client_info(cls) -> str:
        """Returns the query to update the Tibber client information (name, id, etc.)."""
        return cls.create_query_from_dict(cls.query_viewer)
    
    @classmethod
    @property
    def update_homes_info(cls) -> str:
        """Returns the query to update information on all the homes (address, homes, etc.)."""
        query_dict = {}
        # TODO: Create home info query.
        return cls.create_query_from_dict(query_dict)
    
    @classmethod
    @property
    def update_price_info(cls) -> str:
        """Returns the query to update the price for all homes (current price, yesterdays price, etc.)."""
        query_dict = {}
        # TODO: Create price info query.
        return cls.create_query_from_dict(query_dict)
        
    @classmethod
    @property
    def update_all_info(cls) -> str:
        """Returns the query to update all info on the Tibber client, homes and price (client name, homes, price info, etc.)"""
        query_dict = cls.query_viewer
        query_dict = cls.combine_dicts(query_dict, cls.bulk_query_homes)
        return cls.create_query_from_dict(query_dict)

    # Larger bulk query building components
    @classmethod
    @property
    def bulk_query_homes(cls) -> dict:
        """Return a dict with query values as keys with all keys under the viewer > homes query."""
        query_dict = {}
        query_dict = cls.combine_dicts(query_dict, cls.query_homes)
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_address)
        query_dict = cls.combine_dicts(query_dict, cls.bulk_query_homes_owner)
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_meteringPointData)
        query_dict = cls.combine_dicts(query_dict, cls.bulk_query_homes_currentSubscription)
        return query_dict
    
    @classmethod
    @property
    def bulk_query_homes_owner(cls) -> dict:
        """Return a dict with query values as keys with all keys under the viewer > homes > address query."""
        query_dict = {}
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_owner)
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_owner_contactInfo)
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_owner_address)
        return query_dict
    
    @classmethod
    @property
    def bulk_query_homes_currentSubscription(cls) -> dict:
        """Return a dict with query values as keys with all keys under the viewer > homes > currentSubscription query."""
        query_dict = {}
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_currentSubscription)
        query_dict = cls.combine_dicts(query_dict, cls.bulk_query_homes_currentSubscription_subscriber)
        query_dict = cls.combine_dicts(query_dict, cls.bulk_query_homes_currentSubscription_priceInfo)
        query_dict = cls.combine_dicts(query_dict, cls.bulk_query_homes_currentSubscription_priceRating)
        return query_dict
    
    @classmethod
    @property
    def bulk_query_homes_currentSubscription_subscriber(cls) -> dict:
        """Return a dict with query values as keys with all keys under the viewer > homes > currentSubscription > subscriber query."""
        query_dict = {}
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_currentSubscription_subscriber)
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_currentSubscription_subscriber_contactInfo)
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_currentSubscription_subscriber_address)
        return query_dict
    
    @classmethod
    @property
    def bulk_query_homes_currentSubscription_priceInfo(cls) -> dict:
        """Return a dict with query values as keys with all keys under the viewer > homes > currentSubscription > priceInfo query."""
        query_dict = {}
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_currentSubscription_priceInfo_current)
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_currentSubscription_priceInfo_today)
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_currentSubscription_priceInfo_tomorrow)
        return query_dict

    @classmethod
    @property
    def bulk_query_homes_currentSubscription_priceRating(cls) -> dict:
        """Return a dict with query values as keys with all keys under the viewer > homes > currentSubscription > priceRating query."""
        query_dict = {}
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_currentSubscription_priceRating_thresholdPercentages)
        query_dict = cls.combine_dicts(query_dict, cls.bulk_query_homes_currentSubscription_priceRating_hourly)
        query_dict = cls.combine_dicts(query_dict, cls.bulk_query_homes_currentSubscription_priceRating_daily)
        query_dict = cls.combine_dicts(query_dict, cls.bulk_query_homes_currentSubscription_priceRating_monthly)
        return query_dict

    @classmethod
    @property
    def bulk_query_homes_currentSubscription_priceRating_hourly(cls) -> dict:
        """Return a dict with query values as keys with all keys under the viewer > homes > currentSubscription > priceRating > hourly query."""
        query_dict = {}
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_currentSubscription_priceRating_hourly)
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_currentSubscription_priceRating_hourly_entries)
        return query_dict

    @classmethod
    @property
    def bulk_query_homes_currentSubscription_priceRating_daily(cls) -> dict:
        """Return a dict with query values as keys with all keys under the viewer > homes > currentSubscription > priceRating > daily query."""
        query_dict = {}
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_currentSubscription_priceRating_daily)
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_currentSubscription_priceRating_daily_entries)
        return query_dict
    
    @classmethod
    @property
    def bulk_query_homes_currentSubscription_priceRating_monthly(cls) -> dict:
        """Return a dict with query values as keys with all keys under the viewer > homes > currentSubscription > priceRating > monthly query."""
        query_dict = {}
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_currentSubscription_priceRating_monthly)
        query_dict = cls.combine_dicts(query_dict, cls.query_homes_currentSubscription_priceRating_monthly_entries)
        return query_dict
    
    # The smallest queries building components
    @classmethod
    @property
    def query_viewer(cls) -> dict:
        return {
            "viewer": {
                "name": "",
                "login": "",
                "userId": "",
                "accountType": ""
            }
        }
    
    @classmethod
    @property
    def query_homes(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "id": "",
                    "timeZone": "",
                    "appNickname": "",
                    "appAvatar": "",
                    "size": "",
                    "type": "",
                    "numberOfResidents": "",
                    "primaryHeatingSource": "",
                    "hasVentilationSystem": "",
                    "mainFuseSize": ""
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_address(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "address": {
                        "address1": "",
                        "address2": "",
                        "address3": "",
                        "city": "",
                        "postalCode": "",
                        "country": "",
                        "latitude": "",
                        "longitude": ""
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_owner(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "owner": {     
                        "id": "",
                        "firstName": "",
                        "isCompany": "",
                        "name": "",
                        "middleName": "",
                        "lastName": "",
                        "organizationNo": "",
                        "language": ""
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_owner_contactInfo(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "owner": {
                        "contactInfo": {
                            "email": "",
                            "mobile": ""
                        }
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_owner_address(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "owner": {
                        "address": {
                            "address1": "",
                            "address2": "",
                            "address3": "",
                            "city": "",
                            "postalCode": "",
                            "country": "",
                            "latitude": "",
                            "longitude": ""
                        }
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_meteringPointData(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "meteringPointData": {
                        "consumptionEan": "",
                        "gridCompany": "",
                        "gridAreaCode": "",
                        "priceAreaCode": "",
                        "productionEan": "",
                        "energyTaxType": "",
                        "vatType": "",
                        "estimatedAnnualConsumption": ""
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_currentSubscription(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "currentSubscription": {
                        "id": "",
                        "validFrom": "",
                        "validTo": "",
                        "status": ""
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_currentSubscription_subscriber(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "currentSubscription": {
                        "subscriber": {
                            "id": "",
                            "firstName": "",
                            "isCompany": "",
                            "name": "",
                            "middleName": "",
                            "lastName": "",
                            "organizationNo": "",
                            "language": ""
                        }
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_currentSubscription_subscriber_contactInfo(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "currentSubscription": {
                        "subscriber": {
                            "contactInfo": {
                                "email": "",
                                "mobile": ""
                            }
                        }
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_currentSubscription_subscriber_address(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "currentSubscription": {
                        "subscriber": {
                            "address": {
                                "address1": "",
                                "address2": "",
                                "address3": "",
                                "city": "",
                                "postalCode": "",
                                "country": "",
                                "latitude": "",
                                "longitude": ""
                            }
                        }
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_currentSubscription_priceInfo_current(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "currentSubscription": {
                        "priceInfo": {
                            "current": {
                                "total": "",
                                "energy": "",
                                "tax": "",
                                "startsAt": "",
                                "currency": "",
                                "level": ""
                            }
                        }
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_currentSubscription_priceInfo_today(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "currentSubscription": {
                        "priceInfo": {
                            "today": {
                                "total": "",
                                "energy": "",
                                "tax": "",
                                "startsAt": "",
                                "currency": "",
                                "level": ""
                            }
                        }
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_currentSubscription_priceInfo_tomorrow(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "currentSubscription": {
                        "priceInfo": {
                            "tomorrow": {
                                "total": "",
                                "energy": "",
                                "tax": "",
                                "startsAt": "",
                                "currency": "",
                                "level": ""
                            }
                        }
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_currentSubscription_priceRating_thresholdPercentages(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "currentSubscription": {
                        "priceRating": {
                            "thresholdPercentages": {
                                "high": "",
                                "low": ""
                            }
                        }
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_currentSubscription_priceRating_hourly(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "currentSubscription": {
                        "priceRating": {
                            "hourly": {
                                "minEnergy": "",
                                "maxEnergy": "",
                                "minTotal": "",
                                "maxTotal": "",
                                "currency": ""
                            }
                        }
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_currentSubscription_priceRating_hourly_entries(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "currentSubscription": {
                        "priceRating": {
                            "hourly": {
                                "entries": {
                                    "time": "",
                                    "energy": "",
                                    "total": "",
                                    "tax": "",
                                    "difference": "",
                                    "level": ""
                                }
                            }
                        }
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_currentSubscription_priceRating_daily(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "currentSubscription": {
                        "priceRating": {
                            "daily": {
                                "minEnergy": "",
                                "maxEnergy": "",
                                "minTotal": "",
                                "maxTotal": "",
                                "currency": ""
                            }
                        }
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_currentSubscription_priceRating_daily_entries(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "currentSubscription": {
                        "priceRating": {
                            "daily": {
                                "entries": {
                                    "time": "",
                                    "energy": "",
                                    "total": "",
                                    "tax": "",
                                    "difference": "",
                                    "level": ""
                                }
                            }
                        }
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_currentSubscription_priceRating_monthly(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "currentSubscription": {
                        "priceRating": {
                            "monthly": {
                                "minEnergy": "",
                                "maxEnergy": "",
                                "minTotal": "",
                                "maxTotal": "",
                                "currency": ""
                            }
                        }
                    }
                }
            }
        }
    
    @classmethod
    @property
    def query_homes_currentSubscription_priceRating_monthly_entries(cls) -> dict:
        return {
            "viewer": {
                "homes": {
                    "currentSubscription": {
                        "priceRating": {
                            "monthly": {
                                "entries": {
                                    "time": "",
                                    "energy": "",
                                    "total": "",
                                    "tax": "",
                                    "difference": "",
                                    "level": ""
                                }
                            }
                        }
                    }
                }
            }
        }
    
# Template for creating more builder methods:
#    @classmethod
#    @property
#    def query_(cls) -> dict:
#        pass