# Std. lib imports
import pathlib

# Internal imports
from .enriched_text import EnrichedText

# Third party imports
import cohere
from dotenv import dotenv_values
import pinecone

ENV_LOCATION = pathlib.Path(__file__).parent.parent.resolve() / ".env"
CONFIG = dotenv_values(ENV_LOCATION)
SUMMARIZE_TEMP = 0.2
cohere_client = cohere.Client(CONFIG["COHERE_KEY"])


def ingest_article(text: str) -> EnrichedText:
    enriched_text = EnrichedText(full_text=text)
    return enriched_text


def summarize_article(text: EnrichedText) -> str:
    # TODO: use human language interface in runner to determine type of summary (bullets vs paragraph)?
    summarize_response = cohere_client.summarize(
        text=text.enriched_text, length="long", temperature=SUMMARIZE_TEMP
    )
    return summarize_response.summary
