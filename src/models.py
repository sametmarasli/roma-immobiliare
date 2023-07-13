from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional
import inspect

DEFAULT_STR_NA = 'n/a'
DEFAULT_INT_NA = 0

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
class RealEstatePropertiesMultimediaSchema(BaseModel):
    photos : list[dict]  = field(default_factory=dict)

@dataclass
class RealEstatePropertiesCategorySchema(BaseModel):
    name : str  = DEFAULT_STR_NA
    id : int  = DEFAULT_INT_NA

@dataclass
class RealEstatePropertiesLocationSchema(BaseModel):
    microzone : str = DEFAULT_STR_NA
    province : str = DEFAULT_STR_NA
    macrozone : str = DEFAULT_STR_NA
    region : str = DEFAULT_STR_NA
    city : str = DEFAULT_STR_NA
    longitude : float = DEFAULT_INT_NA
    latitude : float = DEFAULT_INT_NA

@dataclass
class RealEstatePropertiesSchema(BaseModel):
    category : dict = field(default_factory=dict)
    description : str = DEFAULT_STR_NA
    features : list = field(default_factory=list)
    income : str = DEFAULT_STR_NA
    multimedia : dict = field(default_factory=dict)
    # price : dict = field(default_factory=dict)
    rooms : str = DEFAULT_STR_NA
    surface : str = DEFAULT_STR_NA
    surfaceValue : str = DEFAULT_STR_NA
    # typology : dict = field(default_factory=dict)
    # typologyV2 : dict = field(default_factory=dict)
    location : dict = field(default_factory=dict)
    hasElevators : bool = DEFAULT_STR_NA
    bedRoomsNumber : str  = DEFAULT_STR_NA
    typologyGA4Translation : str = DEFAULT_STR_NA
    ga4Bathrooms : str = DEFAULT_STR_NA
    ga4features : list = field(default_factory=list)
    condition : str = DEFAULT_STR_NA
    ga4Condition : str = DEFAULT_STR_NA
    # floor : dict = field(default_factory=dict)
    floors : str = DEFAULT_STR_NA
    caption : str = DEFAULT_STR_NA
    bathrooms : str = DEFAULT_STR_NA

    def __post_init__(self):
        self.multimedia = RealEstatePropertiesMultimediaSchema.from_dict(self.multimedia)
        self.category = RealEstatePropertiesCategorySchema.from_dict(self.category)
        self.location = RealEstatePropertiesLocationSchema.from_dict(self.location)
        

@dataclass
class RealEstatePriceSchema(BaseModel):
    visible: str = DEFAULT_STR_NA
    value: str = DEFAULT_STR_NA
    formattedValue: str = DEFAULT_STR_NA
    priceRange: str = DEFAULT_STR_NA



@dataclass
class RealEstateAdvertiserAgencySchema(BaseModel):
    label : str = DEFAULT_STR_NA
    displayName : str = DEFAULT_STR_NA
    isPaid : str = DEFAULT_STR_NA
    type : str = DEFAULT_STR_NA

@dataclass
class RealEstateAdvertiserSchema(BaseModel):
    hasCallNumbers: bool = DEFAULT_STR_NA
    agency: dict = field(default_factory=dict)
    
    def __post_init__(self):
        self.agency = RealEstateAdvertiserAgencySchema.from_dict(self.agency)

@dataclass
class RealEstateTypologySchema(BaseModel):
    name : str  = DEFAULT_STR_NA
    id : int  = DEFAULT_INT_NA

@dataclass
class RealEstateSchema(BaseModel):
    dataType: str = DEFAULT_STR_NA
    advertiser: dict = field(default_factory=dict)
    contract: str = DEFAULT_STR_NA
    id: str = DEFAULT_STR_NA
    isNew: bool = DEFAULT_STR_NA
    luxury: bool = DEFAULT_STR_NA
    price: dict = field(default_factory=dict)
    properties: List[dict] = field(default_factory=list)
    title: str = DEFAULT_STR_NA
    type: str = DEFAULT_STR_NA
    typology: dict = field(default_factory=dict)
    hasMainProperty: bool = DEFAULT_STR_NA
    isProjectLike: bool = DEFAULT_STR_NA
    visibility: str = DEFAULT_STR_NA
    
    def __post_init__(self):
        self.advertiser = RealEstateAdvertiserSchema.from_dict(self.advertiser)
        self.price = RealEstatePriceSchema.from_dict(self.price)
        self.typology = RealEstateTypologySchema.from_dict(self.typology)
        self.properties = [RealEstatePropertiesSchema.from_dict(i) for i in self.properties]

@dataclass
class AdvertSchema(BaseModel):
    realEstate: dict 
    seo: dict  = field(default_factory=dict)
    
    def __post_init__(self):
        self.realEstate = RealEstateSchema.from_dict(self.realEstate)
        
@dataclass
class ApiResponse(BaseModel):
    count: int = DEFAULT_STR_NA
    totalAds: int = DEFAULT_STR_NA
    isResultsLimitReached: bool = DEFAULT_STR_NA
    results: List[dict] = field(default_factory=list)
    breadcrumbs: List[dict] = field(default_factory=list)
    agencies: List[dict] = field(default_factory=list)
    seoData: List[dict] = field(default_factory=list)
    relatedSearches: dict = field(default_factory=dict)
    suggestedSearchData: dict = field(default_factory=dict)
    currentPage: int = DEFAULT_STR_NA
    maxPages: int = DEFAULT_STR_NA

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
