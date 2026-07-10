"""Mock realtor data for the RCAI real-estate widget test harness.

Each realtor becomes a subdomain: <key>.readychatai.lat.
Listings deliberately carry:
  - the 14 seeded ProductFieldsTable preset fields (so widget answers can be
    checked against visible site content), AND
  - `extra` fields the backend/widget setup does NOT expect (waterfront, flood
    zone, MLS #, furnished, days-on-market, price-per-sqft, ...) plus messy
    formats (acres vs sqft, "Contact for price", "/mo" rents, pending/sold,
    blank fields on land lots) — to challenge onboarding/scraper/widget.

Widget wiring per realtor: `api_url` is the Django env; `api_key` is the
business's WidgetConfiguration.api_key from that env's dashboard
(Dashboard -> Widget -> Embed Code). Leave "" to render the site without the
widget until the key is pasted in.
"""

# The 14 real-estate preset fields (apps/business/services/real_estate_service.py
# REAL_ESTATE_PRESET_FIELDS). Order = display order.
PRESET_FIELDS = [
    "Bedrooms",
    "Bathrooms",
    "Square Footage",
    "Property Type",
    "Address",
    "Listing Type",
    "Year Built",
    "Lot Size",
    "HOA Fee",
    "Parking",
    "Pet Policy",
    "Deposit",
    "Availability Date",
    "Virtual Tour Link",
]


def _listing(id, title, price, fields, extra=None, desc="", status="active"):
    return {
        "id": id,
        "title": title,
        "price": price,          # free-form string on purpose ("$1,250,000", "$3,400/mo", "Contact for price")
        "status": status,        # active | pending | sold
        "fields": fields,        # dict keyed by PRESET_FIELDS names (missing keys render as "—")
        "extra": extra or {},    # fields the setup does not expect
        "desc": desc,
    }


PALM = {
    "key": "palmrealty",
    "name": "Palm Realty",
    "tagline": "Coastal Florida homes, condos & investment properties",
    "city": "Sarasota, FL",
    "phone": "(941) 555-0142",
    "email": "hello@palmrealty.example",
    "accent": "#0f9b8e",       # teal
    "accent_dark": "#0a6f66",
    "api_url": "https://dev2.readychatai.com",
    "api_key": "",             # <-- Palm Realty (#621, DEV) WidgetConfiguration.api_key
    "listings": [
        _listing(
            "pr-1001", "Gulf-Front Modern Villa", "$2,450,000",
            {
                "Bedrooms": 4, "Bathrooms": 4.5, "Square Footage": "3,820",
                "Property Type": "Villa", "Address": "18 Beachwalk Dr, Siesta Key, FL 34242",
                "Listing Type": "For Sale", "Year Built": 2019, "Lot Size": "0.42 acres",
                "HOA Fee": 0, "Parking": "3-car garage + circular drive",
                "Pet Policy": "N/A (owner-occupied)", "Deposit": None,
                "Availability Date": "Immediate", "Virtual Tour Link": "https://tours.example/pr-1001",
            },
            extra={
                "Waterfront": "Gulf-front, private dock", "Flood Zone": "AE",
                "MLS #": "A4599121", "Price per sqft": "$641", "Days on Market": 12,
                "Furnished": "Turnkey furnished", "Impact Windows": "Yes (hurricane-rated)",
            },
            desc="Contemporary Gulf-front villa with floor-to-ceiling glass, rooftop terrace, "
                 "infinity pool and 60ft of private beach frontage.",
        ),
        _listing(
            "pr-1002", "Downtown Sarasota High-Rise Condo", "$785,000",
            {
                "Bedrooms": 2, "Bathrooms": 2, "Square Footage": "1,410",
                "Property Type": "Condo", "Address": "1350 Main St #1704, Sarasota, FL 34236",
                "Listing Type": "For Sale", "Year Built": 2008, "Lot Size": "N/A",
                "HOA Fee": 985, "Parking": "1 assigned covered space",
                "Pet Policy": "2 pets, 25 lb limit", "Deposit": None,
                "Availability Date": "2026-08-01", "Virtual Tour Link": "",
            },
            extra={"Floor": "17th", "View": "Bay & city skyline", "MLS #": "A4600233",
                   "Price per sqft": "$557", "HOA Includes": "water, cable, concierge"},
            desc="17th-floor corner unit with wraparound balcony and bay views. Walk to Marina Jack.",
        ),
        _listing(
            "pr-1003", "Lido Key Beach Cottage — Weekly Rental", "$3,400/mo",
            {
                "Bedrooms": 3, "Bathrooms": 2, "Square Footage": "1,650",
                "Property Type": "House", "Address": "412 Tyler Dr, Lido Key, FL 34236",
                "Listing Type": "For Rent", "Year Built": 1962, "Lot Size": "6,500 sqft",
                "HOA Fee": None, "Parking": "Driveway (2 cars)",
                "Pet Policy": "Cats only, $300 pet deposit", "Deposit": 3400,
                "Availability Date": "2026-07-20", "Virtual Tour Link": "https://tours.example/pr-1003",
            },
            extra={"Min Lease": "3 months", "Furnished": "Fully furnished", "Utilities": "Tenant pays electric"},
            desc="Restored mid-century cottage two blocks from Lido Beach. Seasonal & annual leases.",
        ),
        _listing(
            "pr-1004", "Vacant Bayfront Lot", "Contact for price",
            {
                "Bedrooms": None, "Bathrooms": None, "Square Footage": None,
                "Property Type": "Land/Lot", "Address": "0 Manatee Cove Rd, Osprey, FL 34229",
                "Listing Type": "For Sale", "Year Built": None, "Lot Size": "1.1 acres",
                "HOA Fee": 0, "Parking": None, "Pet Policy": None, "Deposit": None,
                "Availability Date": "Immediate", "Virtual Tour Link": "",
            },
            extra={"Zoning": "RSF-1", "Utilities": "Water & sewer at street", "Buildable": "Yes",
                   "Seawall": "Existing, 2021"},
            desc="Rare buildable bayfront parcel with existing seawall. Bring your own builder.",
        ),
        _listing(
            "pr-1005", "Palmer Ranch Family Home", "$639,900",
            {
                "Bedrooms": 4, "Bathrooms": 3, "Square Footage": "2,540",
                "Property Type": "House", "Address": "7821 Silver Oak Ct, Sarasota, FL 34238",
                "Listing Type": "For Sale", "Year Built": 2015, "Lot Size": "0.24 acres",
                "HOA Fee": 145, "Parking": "2-car garage",
                "Pet Policy": "No breed restrictions", "Deposit": None,
                "Availability Date": "2026-09-15", "Virtual Tour Link": "https://tours.example/pr-1005",
            },
            extra={"MLS #": "A4601987", "Pool": "Heated saltwater", "Schools": "A-rated",
                   "Solar Panels": "Owned (2022)", "Price per sqft": "$252"},
            desc="Turnkey 4/3 in gated Palmer Ranch with heated pool and owned solar.",
            status="pending",
        ),
        _listing(
            "pr-1006", "St. Armands Circle Retail/Office Unit", "$1,190,000",
            {
                "Bedrooms": 0, "Bathrooms": 1, "Square Footage": "2,100",
                "Property Type": "Commercial", "Address": "9 N Blvd of Presidents, Sarasota, FL 34236",
                "Listing Type": "For Sale", "Year Built": 1974, "Lot Size": "N/A",
                "HOA Fee": 640, "Parking": "Public + 2 reserved",
                "Pet Policy": "N/A", "Deposit": None,
                "Availability Date": "Immediate", "Virtual Tour Link": "",
            },
            extra={"Cap Rate": "5.8%", "Current Tenant": "Boutique (lease thru 2027)",
                   "Zoning": "CT", "NOI": "$69,000/yr"},
            desc="Ground-floor commercial condo on St. Armands Circle. Currently leased.",
        ),
        _listing(
            "pr-1007", "Downtown Studio Loft — Rental", "$1,850/mo",
            {
                "Bedrooms": 0, "Bathrooms": 1, "Square Footage": "560",
                "Property Type": "Studio", "Address": "500 N Tamiami Trl #210, Sarasota, FL 34236",
                "Listing Type": "For Rent", "Year Built": 2021, "Lot Size": "N/A",
                "HOA Fee": None, "Parking": "1 garage spot",
                "Pet Policy": "No pets", "Deposit": 1850,
                "Availability Date": "2026-07-15", "Virtual Tour Link": "",
            },
            extra={"Min Lease": "12 months", "Furnished": "Unfurnished", "Laundry": "In-unit"},
            desc="Efficient downtown studio loft, 12-ft ceilings, walkable to bayfront.",
        ),
        _listing(
            "pr-1008", "Casey Key Estate", "$6,900,000",
            {
                "Bedrooms": 6, "Bathrooms": 7, "Square Footage": "8,240",
                "Property Type": "Villa", "Address": "3400 Casey Key Rd, Nokomis, FL 34275",
                "Listing Type": "For Sale", "Year Built": 2011, "Lot Size": "1.8 acres",
                "HOA Fee": 0, "Parking": "5-car garage",
                "Pet Policy": "N/A", "Deposit": None,
                "Availability Date": "Immediate", "Virtual Tour Link": "https://tours.example/pr-1008",
            },
            extra={"Waterfront": "Gulf-to-Bay, 2 docks", "Flood Zone": "VE", "Elevator": "Yes",
                   "Guest House": "1,200 sqft", "MLS #": "A4602440"},
            desc="Gulf-to-bay estate on gated Casey Key with private beach, guest house, elevator.",
        ),
        _listing(
            "pr-1009", "Fixer-Upper Bungalow", "$319,000",
            {
                "Bedrooms": 2, "Bathrooms": 1, "Square Footage": "980",
                "Property Type": "House", "Address": "2214 Goodrich Ave, Sarasota, FL 34234",
                "Listing Type": "For Sale", "Year Built": 1951, "Lot Size": "5,000 sqft",
                "HOA Fee": 0, "Parking": "Street",
                "Pet Policy": "N/A", "Deposit": None,
                "Availability Date": "Immediate", "Virtual Tour Link": "",
            },
            extra={"Condition": "As-is / cash preferred", "Roof": "2009", "Days on Market": 3},
            desc="Investor special near Rosemary District. Sold as-is, cash or 203k.",
        ),
        _listing(
            "pr-1010", "Waterside Place Townhome", "$549,000",
            {
                "Bedrooms": 3, "Bathrooms": 2.5, "Square Footage": "1,890",
                "Property Type": "Townhouse", "Address": "1470 Blue Heron Way, Lakewood Ranch, FL 34240",
                "Listing Type": "For Sale", "Year Built": 2022, "Lot Size": "2,100 sqft",
                "HOA Fee": 310, "Parking": "2-car garage",
                "Pet Policy": "3 pets max", "Deposit": None,
                "Availability Date": "2026-08-30", "Virtual Tour Link": "https://tours.example/pr-1010",
            },
            extra={"MLS #": "A4603001", "Community": "Waterside Place", "Price per sqft": "$291"},
            desc="Like-new 3-story townhome walkable to Waterside restaurants and Sunday market.",
            status="sold",
        ),
    ],
}


HARBOR = {
    "key": "harborestates",
    "name": "Harbor Estates",
    "tagline": "New England coastal & historic homes",
    "city": "Newport, RI",
    "phone": "(401) 555-0177",
    "email": "info@harborestates.example",
    "accent": "#1f4e79",       # navy
    "accent_dark": "#14375a",
    "api_url": "https://qa2.readychatai.com",
    "api_key": "",             # <-- Harbor Estates (#501, QA) WidgetConfiguration.api_key
    "listings": [
        _listing(
            "he-2001", "Historic Bellevue Ave Mansion", "$8,250,000",
            {
                "Bedrooms": 8, "Bathrooms": 9, "Square Footage": "11,400",
                "Property Type": "House", "Address": "612 Bellevue Ave, Newport, RI 02840",
                "Listing Type": "For Sale", "Year Built": 1889, "Lot Size": "1.4 acres",
                "HOA Fee": 0, "Parking": "Carriage house (4)",
                "Pet Policy": "N/A", "Deposit": None,
                "Availability Date": "Immediate", "Virtual Tour Link": "https://tours.example/he-2001",
            },
            extra={"Historic Register": "Yes (1972)", "Ocean View": "Partial", "Fireplaces": 11,
                   "MLS #": "1350012", "Zoning": "R-60"},
            desc="Gilded-Age Bellevue mansion with original woodwork, ballroom, and carriage house.",
        ),
        _listing(
            "he-2002", "Harborfront Condo at The Wharf", "$1,150,000",
            {
                "Bedrooms": 2, "Bathrooms": 2, "Square Footage": "1,320",
                "Property Type": "Condo", "Address": "22 Bowens Wharf #4, Newport, RI 02840",
                "Listing Type": "For Sale", "Year Built": 1985, "Lot Size": "N/A",
                "HOA Fee": 1250, "Parking": "1 deeded space",
                "Pet Policy": "1 dog under 40 lb", "Deposit": None,
                "Availability Date": "2026-08-10", "Virtual Tour Link": "",
            },
            extra={"View": "Harbor", "HOA Includes": "dock rights, water", "Slip": "Available to rent",
                   "MLS #": "1350120", "Price per sqft": "$871"},
            desc="Harborfront condo on Bowens Wharf with optional boat slip and walk-to-everything location.",
        ),
        _listing(
            "he-2003", "Colonial in Historic Hill — Rental", "$4,200/mo",
            {
                "Bedrooms": 4, "Bathrooms": 2.5, "Square Footage": "2,600",
                "Property Type": "House", "Address": "35 Mary St, Newport, RI 02840",
                "Listing Type": "For Rent", "Year Built": 1798, "Lot Size": "4,000 sqft",
                "HOA Fee": None, "Parking": "2 tandem off-street",
                "Pet Policy": "Case by case, $500 deposit", "Deposit": 4200,
                "Availability Date": "2026-09-01", "Virtual Tour Link": "https://tours.example/he-2003",
            },
            extra={"Min Lease": "12 months", "Furnished": "Unfurnished", "Heat": "Oil / radiator",
                   "Historic": "Yes — exterior changes restricted"},
            desc="Restored 1798 colonial on the Historic Hill, walk to Thames St and the harbor.",
        ),
        _listing(
            "he-2004", "Middletown Ranch with Water View", "$729,000",
            {
                "Bedrooms": 3, "Bathrooms": 2, "Square Footage": "1,760",
                "Property Type": "House", "Address": "88 Green End Ave, Middletown, RI 02842",
                "Listing Type": "For Sale", "Year Built": 1968, "Lot Size": "0.35 acres",
                "HOA Fee": 0, "Parking": "1-car garage + driveway",
                "Pet Policy": "N/A", "Deposit": None,
                "Availability Date": "2026-07-25", "Virtual Tour Link": "",
            },
            extra={"View": "Sakonnet River (seasonal)", "Flood Zone": "X", "MLS #": "1350210",
                   "Solar Panels": "Leased", "Days on Market": 21},
            desc="Single-level ranch minutes from Second Beach with a seasonal water view.",
            status="pending",
        ),
        _listing(
            "he-2005", "Waterfront Building Lot — Jamestown", "$975,000",
            {
                "Bedrooms": None, "Bathrooms": None, "Square Footage": None,
                "Property Type": "Land/Lot", "Address": "0 Seaside Dr, Jamestown, RI 02835",
                "Listing Type": "For Sale", "Year Built": None, "Lot Size": "2.0 acres",
                "HOA Fee": 0, "Parking": None, "Pet Policy": None, "Deposit": None,
                "Availability Date": "Immediate", "Virtual Tour Link": "",
            },
            extra={"Zoning": "R-40", "Waterfront": "West Passage", "Perc Test": "Passed 2025",
                   "Utilities": "Well & septic required"},
            desc="Two-acre waterfront parcel on Jamestown's west passage. Approved perc, no HOA.",
        ),
        _listing(
            "he-2006", "Thames Street Mixed-Use Building", "$2,300,000",
            {
                "Bedrooms": 2, "Bathrooms": 3, "Square Footage": "4,800",
                "Property Type": "Commercial", "Address": "204 Thames St, Newport, RI 02840",
                "Listing Type": "For Sale", "Year Built": 1901, "Lot Size": "2,800 sqft",
                "HOA Fee": 0, "Parking": "Municipal lot adjacent",
                "Pet Policy": "N/A", "Deposit": None,
                "Availability Date": "Immediate", "Virtual Tour Link": "",
            },
            extra={"Use": "Retail down / 2 apts up", "Cap Rate": "6.1%", "Gross Income": "$142k/yr",
                   "Zoning": "WB (Waterfront Business)"},
            desc="Mixed-use Thames St building: ground-floor retail plus two rental apartments.",
        ),
        _listing(
            "he-2007", "Studio Carriage Apartment — Rental", "$1,975/mo",
            {
                "Bedrooms": 0, "Bathrooms": 1, "Square Footage": "600",
                "Property Type": "Studio", "Address": "9 Kay St (rear), Newport, RI 02840",
                "Listing Type": "For Rent", "Year Built": 1905, "Lot Size": "N/A",
                "HOA Fee": None, "Parking": "1 off-street",
                "Pet Policy": "No pets", "Deposit": 1975,
                "Availability Date": "2026-07-18", "Virtual Tour Link": "",
            },
            extra={"Min Lease": "9 months", "Furnished": "Furnished", "Utilities": "Included except electric"},
            desc="Charming carriage-house studio off Kay St, includes heat and water.",
        ),
        _listing(
            "he-2008", "Ocean Drive Contemporary", "$4,600,000",
            {
                "Bedrooms": 5, "Bathrooms": 5.5, "Square Footage": "5,900",
                "Property Type": "House", "Address": "150 Ocean Ave, Newport, RI 02840",
                "Listing Type": "For Sale", "Year Built": 2016, "Lot Size": "0.9 acres",
                "HOA Fee": 0, "Parking": "3-car garage",
                "Pet Policy": "N/A", "Deposit": None,
                "Availability Date": "Immediate", "Virtual Tour Link": "https://tours.example/he-2008",
            },
            extra={"Ocean View": "Full", "Flood Zone": "VE", "MLS #": "1350330",
                   "Geothermal": "Yes", "Price per sqft": "$780"},
            desc="Glass-and-stone contemporary on Ocean Drive with unobstructed Atlantic views.",
        ),
        _listing(
            "he-2009", "Portsmouth Townhome", "$465,000",
            {
                "Bedrooms": 3, "Bathrooms": 2.5, "Square Footage": "1,700",
                "Property Type": "Townhouse", "Address": "14 Anchor Ln, Portsmouth, RI 02871",
                "Listing Type": "For Sale", "Year Built": 2007, "Lot Size": "1,800 sqft",
                "HOA Fee": 265, "Parking": "1-car garage",
                "Pet Policy": "2 pets max", "Deposit": None,
                "Availability Date": "2026-08-20", "Virtual Tour Link": "",
            },
            extra={"MLS #": "1350401", "Community": "Anchorage", "HOA Includes": "landscaping, pool"},
            desc="Move-in ready townhome in Portsmouth's Anchorage community with pool access.",
            status="sold",
        ),
        _listing(
            "he-2010", "Antique Farmhouse on 5 Acres", "$1,395,000",
            {
                "Bedrooms": 4, "Bathrooms": 3, "Square Footage": "3,100",
                "Property Type": "House", "Address": "770 East Main Rd, Little Compton, RI 02837",
                "Listing Type": "For Sale", "Year Built": 1840, "Lot Size": "5.2 acres",
                "HOA Fee": 0, "Parking": "Barn + driveway",
                "Pet Policy": "N/A", "Deposit": None,
                "Availability Date": "Immediate", "Virtual Tour Link": "https://tours.example/he-2010",
            },
            extra={"Outbuildings": "Barn + workshop", "Fireplaces": 4, "Well": "Private",
                   "Historic": "Yes", "Acreage Use": "Agricultural allowed"},
            desc="1840 antique farmhouse on 5+ rolling acres with barn, near Sakonnet vineyards.",
        ),
    ],
}


REALTORS = {r["key"]: r for r in (PALM, HARBOR)}
