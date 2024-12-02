from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional


@dataclass_json
@dataclass
class CountryModel:
    id: int
    name: Optional[str] = None
    area_id: Optional[int] = None

    def __str__(self):
        return f"Country(id={self.id}, name={self.name}, area_id={self.area_id})"


@dataclass_json
@dataclass
class CityModel:
    id: int
    name: Optional[str] = None
    area_id: Optional[int] = None

    def __str__(self):
        return f"City(id={self.id}, name={self.name}, area_id={self.area_id})"


@dataclass_json
@dataclass
class LanguageModel:
    id: int
    name: Optional[str] = None

    def __str__(self):
        return f"Language(id={self.id}, name={self.name})"


@dataclass_json
@dataclass
class SkillModel:
    id: int
    name: Optional[str] = None
    description: Optional[str] = None

    def __str__(self):
        return f"Skill(id={self.id}, name={self.name}, description={self.description})"
