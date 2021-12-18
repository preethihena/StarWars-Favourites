import requests

from favourites.config import SwapiConfig

class SwapiService:
    """
    SwapiService is a helper class which calls the Star Wars API for getting 
    different resources provided by the API. It has methods to get a specific 
    resource object or all resource objects. It also provide functionality to 
    do search on the searchable parameter.
    """

    def __init__(self, resource) -> None:
        if resource not in SwapiConfig.resources:
            raise ValueError(
                str(resource) + ' is not a supported resource.' + 
                ' Supported resources are: ' + str(SwapiConfig.resources)
            )
        self.resource = resource
        self.resource_url = SwapiConfig.base_url + resource + '/'
    
    def get_all_resources(self, page_number = 1):
        response = requests.get(self.resource_url, params={"page": page_number})
        return response.json(), response.status_code

    def get_resource_by_id(self, id):
        if isinstance(id, int) is not True:
            raise TypeError(
                'id must be a int. Got: ' +
                str(type(id))
            )
        url = self.resource_url + str(id) + '/'
        response = requests.get(url)
        return response.json(), response.status_code
    
    def search(self, search_value, page_number = 1):
        if isinstance(search_value, str) is not True:
            raise TypeError(
                'search_value must be a string. Got: ' +
                str(type(search_value))
            )
        response = requests.get(self.resource_url, params={"search": search_value, "page": page_number})
        return response.json(), response.status_code
