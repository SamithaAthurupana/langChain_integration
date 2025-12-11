from typing import Optional, List
from pydantic import BaseModel, Field


class Car(BaseModel):
    id:str = Field(description="Unique Id for the vehicle listing")
    title:str = Field(description="Title of the listing")
    make:str = Field(description="Brand or manufacturer of the car")
    model:str = Field(description="Model of the car")
    year:str = Field(description="model of the year")
    mileage: Optional[int] = Field(default="None", description="mileage of the car")
    price: float = Field(description="Price of the car")

class CarAnalysis(BaseModel):
    key_insights: str = Field(description="Key insights of the car deals")
    buyer_types: str = Field(description="suggested buyer types")
    summary: str = Field(description="Best average price to buy")
    best_average_price: str = Field(description="Best average price to buy")

class CarDealsResponse(BaseModel):
    cars: List[Car] = Field(description="List of car details available")
    analysis: CarAnalysis = Field(description="AI generated analysis of the listing")

class CarAnalysisRequest(BaseModel):
    car_type: str
    car_brand: str