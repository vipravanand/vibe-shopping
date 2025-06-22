from pydantic import BaseModel, Field




class RetailCategoryVibeKeywors(BaseModel):
    category: str = Field(description="The category of the vibe keywords in the apparel retail sector")
    key_words: list[str] = Field(description="The list of vibe keywords for the category in the apparel retail sector")

    class Config:
        extra = "forbid"
        schema_extra = {
            "examples": [
                {
                    "category": "Chic & Elegant",
                    "key_words": ["chic", "classy", "elegant", "sophisticated", "polished", "refined", "luxe"]
                },
                {"category": "Cute & Playful",
                 "key_words": ["cute", "kawaii", "playful", "flirty", "charming", "delightful", "sweet", "whimsical", "girly", "fun"]
                }
            ]

        }


class RetailVibeKeywords(BaseModel):
    retail_category_vibe_keywords: list[RetailCategoryVibeKeywors] = Field(description="The list of retail category vibe keywords")

    class Config:
        extra = "forbid"
