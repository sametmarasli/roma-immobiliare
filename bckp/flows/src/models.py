from dataclasses import dataclass
from typing import Dict, List, Literal, Optional
import inspect

NOTAPPLICAPLE = 'n/a'

@dataclass
class BaseModel:
    '''
    from_dict method helps to manage schema changes if there are unforseen attributes by ignoring them
    '''
    @classmethod
    def from_dict(cls, env):      
        return cls(**{
            k: v for k, v in env.items() 
            if k in inspect.signature(cls).parameters
        })

@dataclass
class RealEstatePropertiesSchema(BaseModel):
    category : dict = NOTAPPLICAPLE
    description : str = NOTAPPLICAPLE
    features : list = NOTAPPLICAPLE
    income : str = NOTAPPLICAPLE
    multimedia : dict = NOTAPPLICAPLE
    price : dict = NOTAPPLICAPLE
    rooms : str = NOTAPPLICAPLE
    surface : str = NOTAPPLICAPLE
    surfaceValue : str = NOTAPPLICAPLE
    typology : dict = NOTAPPLICAPLE
    typologyV2 : dict = NOTAPPLICAPLE
    location : dict = NOTAPPLICAPLE
    hasElevators : bool = NOTAPPLICAPLE
    bedRoomsNumber : str  = NOTAPPLICAPLE
    typologyGA4Translation : str = NOTAPPLICAPLE
    ga4Bathrooms : str = NOTAPPLICAPLE
    ga4features : list = NOTAPPLICAPLE
    condition : str = NOTAPPLICAPLE
    ga4Condition : str = NOTAPPLICAPLE
    floor : dict = NOTAPPLICAPLE
    floors : str = NOTAPPLICAPLE
    caption : str = NOTAPPLICAPLE
    bathrooms : str = NOTAPPLICAPLE

@dataclass
class RealEstatePriceSchema(BaseModel):
    visible: str
    value: str
    formattedValue: str
    priceRange: str

@dataclass
class RealEstateAdvertiserSchema(BaseModel):
    hasCallNumbers: bool = NOTAPPLICAPLE
    agency: dict = NOTAPPLICAPLE

@dataclass
class RealEstateSchema(BaseModel):
    dataType: str
    advertiser: dict
    contract: str
    id: str
    isNew: bool
    luxury: bool
    price: dict
    properties: List[dict]
    title: str
    type: str
    typology: dict
    hasMainProperty: bool
    isProjectLike: bool
    visibility: str = NOTAPPLICAPLE
    
    def __post_init__(self):
        self.advertiser = RealEstateAdvertiserSchema.from_dict(self.advertiser)
        self.price = RealEstatePriceSchema.from_dict(self.price)
        self.properties = [RealEstatePropertiesSchema.from_dict(i) for i in self.properties]

@dataclass
class AdvertSchema(BaseModel):
    realEstate: dict
    seo: dict
    
    def __post_init__(self):
        self.realEstate = RealEstateSchema.from_dict(self.realEstate)
        
@dataclass
class ApiResponse(BaseModel):
    count: int
    totalAds: int
    isResultsLimitReached: bool
    results: List[dict]
    breadcrumbs: List[dict]
    agencies: List[dict]
    seoData: List[dict]
    relatedSearches: dict
    suggestedSearchData: dict
    currentPage: int
    maxPages: int

    def __post_init__(self):
        self.results = [AdvertSchema.from_dict(i) for i in self.results]



@dataclass
class ApiParameters:
    prezzoMinimo: Optional[int]
    prezzoMassimo: Optional[int]
    pag: Optional[int] = 1
    idCategoria: int = 1
    idContratto: int = 1
    idProvincia: str = 'RM'
