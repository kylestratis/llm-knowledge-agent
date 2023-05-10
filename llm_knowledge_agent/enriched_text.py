SUMMARIZE_LIMIT = 100_000  # text limit for cohere summarize endpoint


class EnrichedText:
    def __init__(self, full_text: str):
        self.full_text: str = full_text  # Remove any newlines
        self.enriched_text: str = self._reduce_text()

    def _reduce_text(self) -> str:
        """
        Reduces text to fit within cohere's summarize limits and any others
        Placeholder for now. TODO: Pick method to reduce length
        """
        if len(self.full_text) <= SUMMARIZE_LIMIT:
            return self.full_text.strip()
        else:
            # TODO: Handle this more gracefully in the agent
            raise ValueError(f"Full text length {len(self.full_text)} greater than {SUMMARIZE_LIMIT} character limit, try a smaller article")


if __name__ == "__main__":
    e = EnrichedText(full_text="This is sentence one. This is sentence two. Hello!")
    print(e.enriched_text)