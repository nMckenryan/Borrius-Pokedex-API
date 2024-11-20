import datetime
import pytest
from borrius_pokedex_api.pokemon_scraper import BorriusPokedexHelpers, scrape_pokemon_indexes


@pytest.fixture
def bph():
    return BorriusPokedexHelpers()


@pytest.mark.asyncio
async def test_scrape_pokemon_indexes(bph):
    indexes = await scrape_pokemon_indexes()
    assert len(indexes) == 495
    assert 1 in indexes
    assert 495 in indexes
    assert 246 in indexes
    assert 374 in indexes
    assert 443 in indexes


def test_bph_init(bph):
    assert bph.national_numbers == [246, 247, 248, 374, 375, 376, 443, 444, 445]
    assert list(bph.borrius_numbers) == list(range(1, 495))
    assert bph.national_page == "https://www.pokemonunboundpokedex.com/national/"
    assert bph.borrius_page == "https://www.pokemonunboundpokedex.com/borrius/"
    assert bph.json_header == [
        {
            "info": {
                "description": "Data pulled from BorriusPokedexScraper. https://github.com/nMckenryan/BorriusPokedexScraper",
                "dataPulledOn": str(datetime.datetime.now()),
            },
            "pokemon": [],
        }
    ]

