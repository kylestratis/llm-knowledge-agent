"""
A representation of a note with utilities for converting to knowledgebase formats
"""
# Standard library imports
from abc import abstractmethod

# Third party imports
import pathvalidate

# Internal imports
from obsidian_lit_note import obsidian_source_note_template


class Note:
    def __init__(self, title: str, text: str, tags: list[str], note_directory: str, publish: bool = False):
        self.title = title
        self.text = text
        self.tags = []
        self.publish = publish
        self.tool_dispatch = {"obsidian": self._generate_obsidian_note()}
        self.note_directory = note_directory
        self.filename: str = None

    def generate_note(self, tool_name: str):
        supported_tools = ["obsidian"]

        if tool_name not in supported_tools:
            raise ValueError(f"{tool_name} not currently supported") from None

    def _generate_obsidian_note(self):
        raise NotImplementedError


class SourceNote(Note):
    def __init__(
        self,
        title: str,
        text: str,
        tags: list[str],
        text_authors: list[str],
        summary: str,
        outline: str,
        note_directory: str,
        link: str = "",
        publish: bool = False,
    ):
        self.text_authors = text_authors
        self.status = "Machine-read"
        self.summary = summary
        self.outline = outline
        self.link = link
        super().__init__(title=title, text=text, tags=tags, note_directory=note_directory, publish=publish)

    def generate_note(self, tool_name: str) -> None:
        super().generate_note(tool_name)
        self.tool_dispatch[tool_name]

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

    def _save_note(self):
        with open(f"{self.note_directory}/{self.filename}", "w") as f:
            f.write(self.generate_note)


# Simple test
if __name__ == "__main__":
    s = SourceNote(
        title="Test title",
        text="This is an article",
        tags=["a"],
        text_authors=["Kyle Stratis"],
        summary="Summary",
        outline="Outline",
    )
    s.generate_note("obsidian")
    s.generate_note("tana")
