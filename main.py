from dataclasses import dataclass
from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError

@dataclass
class Location:
    city: str
    country: str
    continent: str
    postal_code: str
    subdivision: str

class GeoClient(Reader):
    @classmethod
    def get_city_by_ip(cls, ip_address: str) -> Location | None:
        with cls("GeoLite2-City.mmdb") as reader: 
            try:
                response = reader.city(ip_address)
                result = Location(
                    city = response.city.name,
                    country = response.country.name,
                    continent = response.continent.name,
                    postal_code = response.postal.code,
                    subdivision = response.subdivisions.most_specific.name,
                )
                return result
            except AddressNotFoundError:
                return None
            
    @classmethod
    def get_organization_by_ip(cls, ip_address: str) -> str | None:
        with cls("GeoLite2-ASN.mmdb") as reader: 
            try:
                response = reader.asn(ip_address)
                return response.autonomous_system_organization
            except AddressNotFoundError:
                return None

for i in range(128, 255):
    print(GeoClient.get_city_by_ip(f"{i}.8.8.8"))
    # print(GeoClient.get_organization_by_ip(f"{i}.8.8.8"))
