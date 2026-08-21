"""Map of Ontario CSDs already covered by the 53 prod datasets.

Names must match NAR CSD_ENG_NAME values; matching in assess.py is
case-insensitive on the normalized name. Upper-tier providers are expanded
to their lower-tier CSDs here.
"""

# fmt: off
COVERED_CSDS = {
    # single/lower-tier cities and towns with their own dataset
    "Toronto", "Ottawa", "Hamilton", "London", "Windsor", "Kingston",
    "Barrie", "Guelph", "Brantford", "Thunder Bay", "Greater Sudbury",
    "Kitchener", "Cambridge", "Waterloo", "Stratford", "Sarnia", "Cornwall",
    "Niagara Falls", "Quinte West", "Amherstburg", "Cobourg", "Kawartha Lakes",
    "Chatham-Kent", "Norfolk County", "Haldimand County", "Prince Edward County",
    "Brampton",
    # Halton (all four lower tiers have their own dataset)
    "Burlington", "Oakville", "Milton", "Halton Hills",
    # Peel Region
    "Mississauga", "Caledon",
    # York Region
    "Vaughan", "Markham", "Richmond Hill", "Newmarket", "Aurora", "King",
    "Whitchurch-Stouffville", "East Gwillimbury", "Georgina",
    # Durham Region
    "Oshawa", "Whitby", "Ajax", "Pickering", "Clarington", "Scugog",
    "Uxbridge", "Brock",
    # Simcoe County
    "Adjala-Tosorontio", "Bradford West Gwillimbury", "Clearview",
    "Collingwood", "Essa", "Innisfil", "Midland", "New Tecumseth",
    "Oro-Medonte", "Penetanguishene", "Ramara", "Severn", "Springwater",
    "Tay", "Tiny", "Wasaga Beach",
    # Muskoka
    "Bracebridge", "Gravenhurst", "Huntsville", "Lake of Bays",
    "Muskoka Lakes", "Georgian Bay",
    # Wellington County
    "Centre Wellington", "Erin", "Guelph/Eramosa", "Mapleton", "Minto",
    "Puslinch", "Wellington North",
    # Middlesex County
    "Adelaide Metcalfe", "Lucan Biddulph", "Middlesex Centre", "Newbury",
    "North Middlesex", "Southwest Middlesex", "Strathroy-Caradoc",
    "Thames Centre",
    # Lambton County
    "Point Edward", "Petrolia", "Plympton-Wyoming", "St. Clair",
    "Enniskillen", "Brooke-Alvinston", "Dawn-Euphemia", "Lambton Shores",
    "Oil Springs", "Warwick",
    # Huron County
    "Ashfield-Colborne-Wawanosh", "Bluewater", "Central Huron", "Goderich",
    "Howick", "Huron East", "Morris-Turnberry", "North Huron", "South Huron",
    # Bruce County
    "Arran-Elderslie", "Brockton", "Huron-Kinloss", "Kincardine",
    "Northern Bruce Peninsula", "Saugeen Shores", "South Bruce",
    "South Bruce Peninsula",
    # Perth County
    "North Perth", "Perth East", "Perth South", "West Perth", "St. Marys",
    # Elgin County
    "Aylmer", "Bayham", "Central Elgin", "Dutton/Dunwich", "Malahide",
    "Southwold", "West Elgin",
    # Brant County
    "Brant",
    # Frontenac County
    "Central Frontenac", "Frontenac Islands", "North Frontenac",
    "South Frontenac",
    # Hastings County
    "Bancroft", "Carlow/Mayo", "Centre Hastings", "Deseronto", "Faraday",
    "Hastings Highlands", "Limerick", "Madoc", "Marmora and Lake",
    "Stirling-Rawdon", "Tudor and Cashel", "Tweed", "Tyendinaga",
    "Wollaston",
    # Lennox and Addington
    "Addington Highlands", "Greater Napanee", "Loyalist",
    "Stone Mills",
    # Renfrew County
    "Admaston/Bromley", "Arnprior", "Bonnechere Valley", "Brudenell, Lyndoch and Raglan",
    "Deep River", "Greater Madawaska", "Head, Clara and Maria",
    "Horton", "Killaloe, Hagarty and Richards", "Laurentian Hills",
    "Laurentian Valley", "Madawaska Valley", "McNab/Braeside",
    "North Algona Wilberforce", "Petawawa", "Renfrew", "Whitewater Region",
    # Leeds and Grenville
    "Athens", "Augusta", "Edwardsburgh/Cardinal", "Elizabethtown-Kitley",
    "Front of Yonge", "Leeds and the Thousand Islands", "Merrickville-Wolford",
    "North Grenville", "Rideau Lakes", "Westport",
    # Stormont, Dundas and Glengarry
    "North Dundas", "North Glengarry", "North Stormont", "South Dundas",
    "South Glengarry", "South Stormont",
    # Peterborough County (the City of Peterborough is NOT covered)
    "Asphodel-Norwood", "Cavan Monaghan", "Douro-Dummer",
    "Havelock-Belmont-Methuen", "North Kawartha", "Otonabee-South Monaghan",
    "Selwyn", "Trent Lakes",
    # Dufferin County
    "Amaranth", "East Garafraxa", "Grand Valley", "Melancthon", "Mono",
    "Mulmur", "Orangeville", "Shelburne",
    # West Parry Sound
    "Parry Sound", "Archipelago", "Carling", "McDougall", "McKellar",
    "Seguin", "Whitestone",
}
# fmt: on


def norm(name: str) -> str:
    # NAR CSD names can be bilingual ("Greater Sudbury / Grand Sudbury")
    name = name.split(" / ")[0]
    return " ".join(name.lower().replace("’", "'").split())


COVERED_NORM = {norm(n) for n in COVERED_CSDS}
