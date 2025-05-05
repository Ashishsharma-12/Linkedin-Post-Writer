# sub_agents/character_formatter.py
import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class CharacterFormatter:
    """
    Ensures the post is within LinkedIn character limits and optimizes formatting.
    LinkedIn limits: Post body ~3000 chars, Comments ~1250 chars, Headlines ~220 chars.
    We focus on the main post body limit (~3000).
    """
    def __init__(self, api_key=None, max_chars: int = 3000):
        self.max_chars = max_chars
        # Initialize the Generative AI model
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it or pass it.")
        genai.configure(api_key=api_key)
        llm = os.getenv("MODEL_NAME")
        self.model = genai.GenerativeModel(llm)
        

    def check_length(self, text: str) -> (bool, int):
        """
        Checks if the text is within the character limit.

        Args:
            text: The post content.

        Returns:
            A tuple: (is_within_limit, character_count).
        """
        count = len(text)
        return count <= self.max_chars, count

    def trim_text(self, text: str) -> str:
        """
        Trims the text to the maximum character limit if necessary.
        Attempts to trim gracefully by ending near the last word.

        Args:
            text: The post content.

        Returns:
            The potentially trimmed text.
        """
        if len(text) > self.max_chars:
            prompt = f"""
            Summarize and rewrite the following text in a {self.max_chars} charachters.
            make sure you do not miss out any important information while summarizing.
            make sure you only the converted text content in the output and no additional text.

            Original Text:
            {text}
            """
            try:
                response = self.model.generate_content(prompt)
                # Accessing text from Content object response
                if response and response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                    return "".join([part.text for part in response.candidates[0].content.parts])
                else:
                    print(f"Warning: LLM response empty for tone adjustment. Returning original text.")
                    return text
            except Exception as e:
                print(f"Error : {e}. Returning original text.")
                return text

    def format_text(self, text: str) -> str:
        """
        Optimizes basic formatting like excessive line breaks (LinkedIn treats
        multiple line breaks as one blank line) and leading/trailing whitespace.
        Does NOT handle complex Markdown or HTML.

        Args:
            text: The post content.

        Returns:
            The formatted text.
        """
        
        formatted_text = '\n\n'.join(block.strip() for block in text.split('\n\n\n') if block.strip())
        formatted_text = '\n'.join(line.rstrip() for line in formatted_text.split('\n'))
        return formatted_text.strip()

# Example usage (for testing)
if __name__ == '__main__':
    formatter = CharacterFormatter(max_chars=200)
    short_text = "This is a short post."
    long_text = "This is a very very long post that will definitely exceed the character limit for testing purposes. Let's see how the trimming logic handles this situation gracefully by trying to find a space near the end of the allowed limit. Hopefully, it cuts off nicely."
    formatted_text = "Line 1\n\n\n\nLine 2\n\nLine 3   "

    is_short, count_short = formatter.check_length(short_text)
    print(f"Short text length: {count_short}, within limit: {is_short}")
    print(f"Trimmed short text:\n{formatter.trim_text(short_text)}\n")

    is_long, count_long = formatter.check_length(long_text)
    print(f"Long text length: {count_long}, within limit: {is_long}")
    print(f"Trimmed long text:\n{formatter.trim_text(long_text)}\n")

    print(f"Original formatted text:\n---\n{formatted_text}\n---")
    print(f"Formatted text:\n---\n{formatter.format_text(formatted_text)}\n---")