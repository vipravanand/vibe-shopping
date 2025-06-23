from typing import List, Literal, Optional
from pydantic import BaseModel, Field


fit_options = Literal['Relaxed', 'Stretch to fit', 'Body hugging', 'Tailored', 'Flowy', 'Bodycon', 'Oversized', 'Slim', 'Sleek and straight']

fabric_options = Literal['Linen', 'Silk', 'Cotton', 'Rayon', 'Satin', 'Modal jersey', 'Crepe', 'Tencel', 'Organic cotton', 'Sequined mesh', 'Viscose',
                          'Chiffon', 'Cotton poplin', 'Linen blend', 'Cotton gauze', 'Ribbed jersey', 'Lace overlay', 'Tencel twill', 'Chambray', 'Velvet', 
                          'Silk chiffon', 'Bamboo jersey', 'Ribbed knit', 'Tweed', 'Organza overlay', 'Sequined velvet', 'Cotton-blend', 'Crushed velvet', 
                          'Tulle', 'Denim', 'Wool-blend', 'Scuba knit', 'Linen-blend', 'Polyester georgette', 'Cotton twill', 'Poly-crepe', 'Viscose voile', 
                          'Vegan leather', 'Lamé', 'Polyester twill', 'Tencel-blend', 'Stretch denim']


sleeve_length_options = Literal['Short Flutter Sleeves', 'Cropped', 'Long sleeves with button cuffs', 'Sleeveless', 'Full sleeves', 'Short sleeves', 
                                'Quarter sleeves', 'Straps', 'Long sleeves', 'Spaghetti straps', 'Short flutter sleeves', 'Tube', 'Balloon sleeves', 
                                'Halter', 'Bishop sleeves', 'One-shoulder', 'Cap sleeves', 'Cropped long sleeves', 'Bell sleeves', 'Short puff sleeves']

color_or_print_options = Literal['Pastel yellow', 'Deep blue', 'Floral print', 'Red', 'Off-white', 'Pastel pink', 'Aqua blue', 'Green floral', 'Charcoal', 'Pastel coral', 'Dusty rose', 'Seafoam green', 'Multicolor mosaic print', 'Pastel floral', 'Storm grey', 'Cobalt blue', 'Blush pink', 'Sunflower yellow', 'Aqua wave print', 'Black iridescent', 'Orchid purple', 'Amber gold', 'Watercolor petals', 'Stone/black stripe', 'Sage green', 'Ruby red', 'Soft teal', 'Charcoal marled', 'Lavender', 'Ombre sunset', 'Coral stripe', 'Jet black', 'Olive green', 'Mustard yellow', 'Silver metallic', 'Teal abstract print', 'Lavender haze', 'Warm taupe', 'Black polka dot', 'Midnight navy sequin', 'Sunshine yellow', 'Charcoal pinstripe', 'Plum purple', 'Mid-wash indigo', 'Emerald green', 'Mustard windowpane check', 'Sand beige', 'Ruby red micro–dot', 'Terracotta', 'Heather quartz', 'Goldenrod yellow', 'Deep-wash indigo', 'Sapphire blue', 'Peony watercolor print', 'Slate grey', 'Emerald green grid check', 'Bronze metallic', 'Midnight navy', 'Classic indigo', 'Stone beige', 'Sand taupe', 'Graphite grey', 'Deep indigo', 'Platinum grey']

occasion_options = Literal['Party', 'Vacation', 'Everyday', 'Evening', 'Work', 'Vocation']

neckline_options = Literal['Sweetheart', 'Square neck', 'V neck', 'Boat neck', 'Tubetop', 'Halter', 'Cowl neck', 'Collar', 'One-shoulder', 'Polo collar', 'Illusion bateau', 'Round neck']


length_options = Literal['Mini', 'Short', 'Midi', 'Maxi']

pant_type_options = Literal['Wide-legged', 'Ankle length', 'Flared', 'Wide hem', 'Straight ankle', 'Mid-rise', 'Low-rise']

size_options = Literal['XS', 'S', 'M', 'L', 'XL']

category_options = Literal['top', 'dress', 'skirt', ' pants']

class Price(BaseModel):
    min: Optional[int] = Field(description="The minimum price of the item of clothing in $")
    max: Optional[int] = Field(description="The maximum price of the item of clothing in $")


class Reasoning(BaseModel):
    vibe_reasoning: Optional[str] = Field(description="The reasoning for the vibe attribute mapping", default=None)
    name_reasoning: Optional[str] = Field(description="The reasoning for the name attribute mapping", default=None)
    category_reasoning: Optional[str] = Field(description="The reasoning for the category attribute mapping", default=None)
    size_reasoning: Optional[str] = Field(description="The reasoning for the size attribute mapping", default=None)
    fit_reasoning: Optional[str] = Field(description="The reasoning for the fit attribute mapping", default=None)
    fabric_reasoning: Optional[str] = Field(description="The reasoning for the fabric attribute mapping", default=None)
    sleeve_length_reasoning: Optional[str] = Field(description="The reasoning for the sleeve length attribute mapping", default=None)
    colour_or_print_reasoning: Optional[str] = Field(description="The reasoning for the colour or print attribute mapping", default=None)
    occasion_reasoning: Optional[str] = Field(description="The reasoning for the occasion attribute mapping", default=None)
    neckline_reasoning: Optional[str] = Field(description="The reasoning for the neckline attribute mapping", default=None)
    length_reasoning: Optional[str] = Field(description="The reasoning for the length attribute mapping", default=None)
    pant_type_reasoning: Optional[str] = Field(description="The reasoning for the pant type attribute mapping", default=None)
    price_reasoning: Optional[str] = Field(description="The reasoning for the price attribute mapping", default=None)



class QueryToAttribute(BaseModel):

    vibe: Optional[List[str]] = Field(description="The vibe expressed by the shopper in the query", default=[])

    category: Optional[List[category_options]] = Field(description="The category of the item of clothing", default=[])

    size: Optional[List[size_options]] = Field(description="The size of the item of clothing", default=[])
    fit: Optional[List[fit_options]] = Field(description="The fit of the item of clothing", default=[])
    fabric: Optional[List[fabric_options]] = Field(description="The fabric of the item of clothing", default=[])      
    sleeve_length: Optional[List[sleeve_length_options]] = Field(description="The sleeve length of the item of clothing", default=[])

    colour_or_print: Optional[List[color_or_print_options]] = Field(description="The colour or print of the item of clothing", default=[])

    occasion: Optional[List[occasion_options]] = Field(description="The occasion of the item of clothing", default=[])

    neckline: Optional[List[neckline_options]] = Field(description="The neckline of the item of clothing", default=[])
    length: Optional[List[length_options]] = Field(description="The length of the item of clothing", default=[])
    pant_type: Optional[List[pant_type_options]] = Field(description="The pant type of the item of clothing", default=[])

    price: Optional[Price] = Field(description="The price of the item of clothing", default=Price(min=None, max=None))

    # reasoning: Optional[Reasoning] = Field(description="The reasoning for the attribute mapping", default=None)

class VibeToAttribute(BaseModel):

    fit: Optional[List[fit_options]] = Field(description="The fit of the item of clothing implied from the vibe", default=[])

    fabric: Optional[List[fabric_options]] = Field(description="The fabric of the item of clothing implied from the vibe", default=[])      

    colour_or_print: Optional[List[color_or_print_options]] = Field(description="The colour or print of the item of clothing implied from the vibe", default=[])

    occasion: Optional[List[occasion_options]] = Field(description="The occasion of the item of clothing implied from the vibe", default=[])

    reasoning: Optional[str] = Field(description="The reasoning for the attribute mapping", default="")
