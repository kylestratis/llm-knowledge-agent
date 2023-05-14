# Std. lib imports
import pathlib

# Third party imports
import click
from dotenv import dotenv_values

# Internal imports
from demo_file import demo_item_1, demo_item_2
from llm_knowledge_agent import agent, SourceNote, EvergreenNote

ENV_LOCATION = pathlib.Path(__file__).parent.resolve() / ".env"
CONFIG: dict = dotenv_values(ENV_LOCATION)


@click.command()
def load_knowledgebase():
    agent.load_knowledgebase()


@click.command()
def delete_knowledgebase():
    pass


@click.command()
@click.option(
    "-f", "--file", "article", help="Article filepath. Not required in demo mode"
)
@click.option("-d", "--demo", default=False, is_flag=True)
def make_note(article: str, demo: bool):
    if demo:
        title = demo_item_2["title"]
        authors = demo_item_2["authors"]
        tags = demo_item_2["tags"]
        text = demo_item_2["text"]
        link = demo_item_2["link"]
    else:
        if article[-3:] != ".txt":
            raise ValueError(f"Unrecognized file extension for {article}")
        with open(article, "rb") as f:
            article_text = f.readlines()
            title = article_text[0]
            authors = [author.strip() for author in article_text[1].split(",")]
            tags = [tag.strip() for tag in article_text[2].split(",")]
            link = article_text[3]
            text = "".join(article_text[4:]).rstrip()
    enriched_text = agent.ingest_article(text)
    summary = agent.summarize_article(enriched_text)
    outline = agent.generate_outline(enriched_text)
    main_ideas = agent.get_main_ideas(enriched_text)

    source_note = SourceNote(
        title=title,
        tags=tags,
        text_authors=authors,
        summary=summary,
        outline=outline,
        note_directory=CONFIG["SOURCE_NOTE_DIRECTORY"],
        link=link,
    )
    if demo:
        source_note.generate_note(tool_name="obsidian", save=False)
        click.echo(source_note)
    else:
        source_note.generate_note(tool_name="obsidian")

    for main_idea in main_ideas:
        evergreen_text = agent.generate_evergreen_note_text(
            main_idea=main_idea, outline=outline
        )
        evergreen_note = EvergreenNote(
            title=main_idea,
            text=evergreen_text,
            tags=tags,
            note_directory=CONFIG["EVERGREEN_NOTE_DIRECTORY"],
            sources=[link],
        )
        evergreen_note.related_notes = agent.find_and_connect_related_notes(
            evergreen_note=evergreen_note
        )
        if demo:
            evergreen_note.generate_note(tool_name="obsidian", save="False")
            click.echo(evergreen_note)
        else:
            evergreen_note.generate_note(tool_name="obsidian")


if __name__ == "__main__":
    make_note(article="", demo=True)
