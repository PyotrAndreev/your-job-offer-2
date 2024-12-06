from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional

from entities.enums import LanguageLevelEnum


@dataclass_json
@dataclass
class CountryModel:
    """
    Represents a country in the system.

    Attributes:
        id (int): The unique identifier of the country.
        name (Optional[str]): The name of the country.
        area_id (Optional[int]): The identifier of the area to which the country belongs.

    Methods: __str__: Returns a string representation of the CountryModel instance, displaying the country's ID,
    name, and area_id.
    """
    id: int
    name: Optional[str] = None
    area_id: Optional[int] = None

    def __str__(self):
        return f"Country(id={self.id}, name={self.name}, area_id={self.area_id})"


@dataclass_json
@dataclass
class CityModel:
    """
     Represents a city in the system.

     Attributes:
         id (int): The unique identifier of the city.
         name (Optional[str]): The name of the city.
         area_id (Optional[int]): The identifier of the area to which the city belongs.

     Methods: __str__: Returns a string representation of the CityModel instance, displaying the city's ID, name,
     and area_id.
    """
    id: int
    name: Optional[str] = None
    area_id: Optional[int] = None

    def __str__(self):
        return f"City(id={self.id}, name={self.name}, area_id={self.area_id})"


@dataclass_json
@dataclass
class LanguageModel:
    """
    Represents a language in the system.

    Attributes:
        id (int): The unique identifier of the language.
        name (Optional[str]): The name of the language.

    Methods:
        __str__: Returns a string representation of the LanguageModel instance, displaying the language's ID and name.
    """
    id: int
    name: Optional[str] = None
    level: Optional[LanguageLevelEnum] = None

    def __str__(self):
        return f"Language(id={self.id}, name={self.name}, level={self.level})"


@dataclass_json
@dataclass
class SkillModel:
    """
    Represents a skill in the system.

    Attributes:
        id (int): The unique identifier of the skill.
        name (Optional[str]): The name of the skill.
        description (Optional[str]): A description of the skill.

    Methods: __str__: Returns a string representation of the SkillModel instance, displaying the skill's ID, name,
    and description.
    """
    id: int
    name: Optional[str] = None
    description: Optional[str] = None

    def __str__(self):
        return f"Skill(id={self.id}, name={self.name}, description={self.description})"
