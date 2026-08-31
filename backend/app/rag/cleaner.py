import re

class TextCleaner:
    """Normalizes and sanitizes extracted text for embedding and chunking."""

    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""

        # Replace non-breaking spaces and special whitespace characters
        text = text.replace("\u00a0", " ").replace("\r\n", "\n").replace("\r", "\n")

        # Normalize multiple spaces and tabs to a single space
        text = re.sub(r"[ \t]+", " ", text)

        # Replace 3 or more consecutive newlines with two newlines (paragraph boundary)
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Strip leading and trailing whitespace from each line
        lines = [line.strip() for line in text.split("\n")]
        text = "\n".join(lines)

        return text.strip()
