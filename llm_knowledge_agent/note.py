"""
A representation of a note with utilities for converting to knowledgebase formats
"""
# Standard library imports

# Third party imports
import pathvalidate

# Internal imports
from .obsidian_templates import (
    obsidian_source_note_template,
    obsidian_evergreen_note_template,
)


class Note:
    def __init__(
        self,
        title: str,
        tags: list[str],
        note_directory: str,
        publish: bool = False,
    ):
        self.title = title
        self.tags = []
        self.publish = publish
        self.tool_dispatch = {"obsidian": self._generate_obsidian_note()}
        self.note_directory = note_directory
        self.filename: str = None

    def generate_note(self, tool_name: str, save: bool = True):
        supported_tools = ["obsidian"]

        if tool_name not in supported_tools:
            raise ValueError(f"{tool_name} not currently supported") from None
        self.tool_dispatch[tool_name]
        if save:
            self._save_note()

    def _generate_obsidian_note(self):
        raise NotImplementedError

    def _save_note(self):
        with open(f"{self.note_directory}/{self.filename}", "w") as f:
            f.write(self.generate_note)

    def __str__(self):
        return self.generated_note


class SourceNote(Note):
    def __init__(
        self,
        title: str,  # Article title
        tags: list[str],
        text_authors: list[str],
        summary: str,
        outline: str,
        note_directory: str,
        link: str = "",
        publish: bool = False,
    ):
        self.text_authors = text_authors
        self.status = "To Review"
        self.summary = summary
        self.outline = outline
        self.link = link
        super().__init__(
            title=title,
            tags=tags,
            note_directory=note_directory,
            publish=publish,
        )

    def _generate_obsidian_note(self) -> None:
        # Format tags
        tags = " ".join(self.tags)
        # Format authors
        linked_authors = " ".join([f"[[{author}]]" for author in self.text_authors])
        # Set file name
        self.filename = f"{pathvalidate.sanitize_filename(self.title)}.md"
        # Run template
        self.generated_note = obsidian_source_note_template.substitute(
            publish=self.publish,
            tags=tags,
            author=linked_authors,
            title=self.title,
            status=self.status,
            link=self.link,
            summary=self.summary,
            outline=self.outline,
        )


class EvergreenNote(Note):
    def __init__(
        self,
        title: str,  # Note title
        text: str,
        tags: list[str],
        note_directory: str,
        sources: list[str],
        publish: bool = False,
        status: str = "boat",
    ):
        self.status = status
        self.sources = sources
        self.text = text
        super().__init__(
            title=title,
            tags=tags,
            note_directory=note_directory,
            publish=publish,
        )
        self.tags.append("#note/evergreen")

    def _generate_obsidian_note(self):
        # Format tags
        tags = " ".join(self.tags)
        # Format sources
        metadata_sources = " ".join(self.sources)
        body_sources = "\n".join([f"- {source}" for source in self.sources])
        # Set file name
        self.filename = f"{pathvalidate.sanitize_filename(self.title)}.md"
        self.generated_note = obsidian_evergreen_note_template.substitute(
            publish=self.publish,
            status=self.status,
            metadata_sources=metadata_sources,
            tags=tags,
            text=self.text,
            body_sources=body_sources,
        )


# Simple test
if __name__ == "__main__":
    s = SourceNote(
        title="Test title",
        text="This is an article",
        tags=["a"],
        text_authors=["Kyle Stratis"],
        summary="Summary",
        outline="Outline",
        note_directory="/dir",
    )
    s.generate_note("obsidian", save=False)
    print(s.generated_note)
    e = EvergreenNote(
        title="Evergreen Title",
        text="Lorem ipsum dolor est",
        tags=["#test"],
        note_directory="/dir",
        sources=["source 1", "source π"],
    )
    e.generate_note("obsidian", save=False)
    print(e.generated_note)
