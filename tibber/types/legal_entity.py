"""A class representing the LegalEntity type from the GraphQL Tibber API."""
from tibber.types.contact_info import ContactInfo
from tibber.types.address import Address


class LegalEntity:
    """A LegalEntity (most commonly an owner of a home for example). This class contains methods to get information such as address, name and contact info."""
    def __init__(self, data: dict, tibber_client: "Client"):
        self.cache: dict = data
        self.tibber_client: "Client" = tibber_client
        
    @property
    def id(self) -> str:
        return self.cache.get("id")
        
    @property
    def first_name(self) -> str:
        return self.cache.get("firstName")
        
    @property
    def is_company(self) -> bool:
        return self.cache.get("isCompany")
        
    @property
    def name(self) -> str:
        return self.cache.get("name")
        
    @property
    def middle_name(self) -> str:
        return self.cache.get("middleName")
        
    @property
    def last_name(self) -> str:
        return self.cache.get("lastName")
        
    @property
    def organization_no(self) -> str:
        return self.cache.get("organizationNo")
        
    @property
    def language(self) -> str:
        return self.cache.get("language")
        
    @property
    def contact_info(self) -> ContactInfo:
        return ContactInfo(self.cache.get("contactInfo"), self.tibber_client)
        
    @property
    def address(self) -> Address:
        return Address(self.cache.get("address"), self.tibber_client)