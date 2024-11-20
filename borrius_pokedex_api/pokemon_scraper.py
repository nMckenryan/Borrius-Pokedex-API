import datetime
from pathlib import Path
from urllib import response

import scrapy
from scrapy.crawler import CrawlerProcess

class BorriusPokedexHelpers:
    def __init__(self):
        self.national_numbers = [246, 247, 248, 374, 375, 376, 443, 444, 445]
        self.borrius_numbers = range(1, 495)
        self.national_page = "https://www.pokemonunboundpokedex.com/national/"
        self.borrius_page = "https://www.pokemonunboundpokedex.com/borrius/"
        self.json_header = [
            {
                "info": {
                    "description": "Data pulled from BorriusPokedexScraper. https://github.com/nMckenryan/BorriusPokedexScraper",
                    "dataPulledOn": str(datetime.datetime.now()),
                },
                "pokemon": [],
            }
        ]
bph = BorriusPokedexHelpers()


# Corrects name of pokemon so it can be successfully found in pokeapi
def correct_pokemon_name(p):
    pokemon = p.lower().replace(". ", "-").replace("'", "")
    corrections = {
        "dome fossil": "kabuto",
        "helix fossil": "omanyte",
        "claw fossil": "anorith",
        "root fossil": "lileep",
        "skull fossil": "cranidos",
        "armor fossil": "shieldon",
        "cover fossil": "tirtouga",
        "plume fossil": "archen",
        "jaw fossil": "tyrunt",
        "sail fossil": "amaura",
        "old amber": "aerodactyl",
        "galarian slowpoke": "slowpoke-galar",
        "galarian darmanitan": "darmanitan-galar-standard",
        "galarian ": lambda x: x.replace("galarian ", "") + "-galar",
        "hisuian ": lambda x: x.replace("hisuian ", "") + "-hisui",
        "alolan ": lambda x: x.replace("alolan ", "") + "-alola",
        "indeedee\u2642": "indeedee-male",
        "indeedee\u2640": "indeedee-female",
        "flabe\u0301be\u0301": "flabebe",
        "flab\u00e9b\u00e9": "flabebe",
        "nidoran\u2642": "nidoran-m",
        "nidoran\u2640": "nidoran-f",
        "basculin": "basculin-red-striped",
        "enamorus": "enamorus-incarnate",
        "morpeko": "morpeko-full-belly",
        "eiscue": "eiscue-ice",
        "minior": "minior-red-meteor",
        "oricorio": "oricorio-baile",
        "pumpkaboo": "pumpkaboo-average",
        "gourgeist": "gourgeist-average",
        "wormadam": "wormadam-plant",
        "meowstic": "meowstic-male",
        "wishiwashi": "wishiwashi-solo",
        "lycanroc": "lycanroc-midday",
        "darmanitan": "darmanitan-standard",
        "deoxys": "deoxys-normal",
        "shaymin": "shaymin-land",
        "keldeo": "keldeo-ordinary",
    }
    for key, value in corrections.items():
        if key in pokemon:
            if callable(value):
                return value(pokemon)
            else:
                return value
    return pokemon


class PokemonNameScraper(scrapy.Spider):
    name = "pokemon_name_scraper"

    def start_requests(self):
        with open('items.json', 'w') as f:
            f.truncate(0)
        borrius_numbers = range(1, 3)
                
        for number in borrius_numbers:
            url = f"https://www.pokemonunboundpokedex.com/borrius/{number}"
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        name_tag = response.xpath('//h3[@class="card-title text-4xl"]/text()').get()
        pokemon_name_sanitised = correct_pokemon_name(name_tag).replace("Name: ", "")
        yield {"pokemon": pokemon_name_sanitised}


process = CrawlerProcess(
    settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    }
)

process.crawl(PokemonNameScraper)
process.start()