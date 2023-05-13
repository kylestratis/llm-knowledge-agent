# Std. lib imports
import pathlib

# Internal imports
from .enriched_text import EnrichedText
from .note import EvergreenNote

# Third party imports
import cohere
from dotenv import dotenv_values
import pinecone

ENV_LOCATION = pathlib.Path(__file__).parent.parent.resolve() / ".env"
CONFIG = dotenv_values(ENV_LOCATION)
cohere_client = cohere.Client(CONFIG["COHERE_KEY"])


def ingest_article(text: str) -> EnrichedText:
    enriched_text = EnrichedText(full_text=text)
    return enriched_text


def summarize_article(text: EnrichedText) -> str:
    # TODO: use human language interface in runner to determine type of summary (bullets vs paragraph)?
    summarize_response = cohere_client.summarize(
        text=text.enriched_text, length="long", temperature=0.2
    )
    return summarize_response.summary


def get_main_ideas(text:EnrichedText) -> str:
    summarize_response = cohere_client.summarize(
        text=text.enriched_text,
        length='long',
        format='bullets',
        model='summarize-xlarge',
        additional_command='focus on getting main ideas and arguments',
        temperature=0.7,
    )
    return summarize_response.summary


def generate_outline(text: EnrichedText) -> str:
    prompt = f"read the following text bounded by %%: %%{text.enriched_text}%% For the previous text, please generate a numbered outline that follows precisely the inherent structure of the text and would allow a reader to quickly understand what the text is about. If there are obvious headers, use those in the outline."
    response = cohere_client.generate(
        model="command-xlarge-nightly",
        prompt=prompt,
        max_tokens=300,
        temperature=0.4,
        k=0,
        stop_sequences=[],
        return_likelihoods="NONE",
    )
    return response.generations[0].text

def parse_evergreen_note(note: EvergreenNote):
    raise NotImplementedError