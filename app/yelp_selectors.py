# Yelp Search Page Selectors
SEARCH_DESCRIPTION_INPUT = "//input[@id='search_description']"
SEARCH_LOCATION_INPUT = "//input[@id='search_location']"

# Business Listing Selectors (multiple options for robustness)
BUSINESS_LISTING_SELECTORS = [
    "//ul/li//div[contains(@class,'businessName')]/a",
    "//a[contains(@class,'businessName')]",
    "//div[contains(@class,'businessName')]//a",
    "//a[contains(@href,'/biz/')]"
]

# Pagination Selectors
NEXT_PAGE_SELECTORS = [
    "//a[contains(text(), 'Next')]",
    "//a[contains(@aria-label, 'Next')]",
    "//a[contains(@class, 'next')]",
    "//a[contains(@href, 'start=')]"
]

# Business Detail Page Selectors
BUSINESS_TITLE = "//h1"
BUSINESS_TITLE_ALTERNATIVES = [
    "//h1[contains(@class,'css-1se8maq')]",
    "//h1[contains(@class,'css-')]",
    "//h1",
    "//div[contains(@class,'businessName')]//h1",
    "//div[contains(@class,'title')]//h1",
    "//h1[contains(@class,'title')]"
]
BUSINESS_CATEGORIES = "//span[@data-testid='BizHeaderCategory']/a"
BUSINESS_WEBSITE = "//a[contains(@href,'biz_redir?url=')]"
BUSINESS_PHONE = "//div[p[1][contains(text(), 'Phone number')]]/p[2]"
BUSINESS_RATING = "//div[contains(@aria-label,'star rating')]"
BUSINESS_REVIEWS = "//a[contains(@href,'#reviews')]"
BUSINESS_ADDRESS = "//address"
BUSINESS_HOURS = "//table"

# Alternative selectors for better coverage
ALTERNATIVE_SELECTORS = {
    'phone': [
        "//p[contains(@class,'phone')]",
        "//span[contains(@class,'phone')]",
        "//div[contains(@class,'phone')]"
    ],
    'rating': [
        "//div[contains(@class,'rating')]",
        "//span[contains(@class,'rating')]"
    ],
    'reviews': [
        "//span[contains(@class,'reviewCount')]",
        "//a[contains(@href,'reviews')]"
    ],
    'address': [
        "//address",
        "//div[contains(@class,'address')]",
        "//p[contains(@class,'address')]"
    ]
} 