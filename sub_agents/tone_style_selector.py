# sub_agents/tone_style_selector.py
import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class ToneStyleSelector:
    """
    Adjusts the tone and style of a given text based on the selected option.
    This agent primarily provides instructions or modifies a draft.

    Args:
        text: The input text draft.
        tone: The desired tone (e.g., "Professional", "Conversational", "Celebratory").

    Returns:
        The text adjusted to the specified tone and style.

    """
    def __init__(self, api_key=None):
        # Initialize the Generative AI model
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it or pass it.")
        genai.configure(api_key=api_key)
        llm = os.getenv("MODEL_NAME")
        self.model = genai.GenerativeModel(llm)

    def apply_tone_style(self, text: str, tone: str) -> str:
        """
        Applies the specified tone and style to the input text.

        Args:
            text: The input text draft.
            tone: The desired tone (e.g., "Professional", "Conversational", "Celebratory").

        Returns:
            The text adjusted to the specified tone and style.
        """
        prompt = f"""
        Rewrite the following text in a {tone} tone suitable for a LinkedIn post.
        Focus on adjusting vocabulary, sentence structure, and formality without losing the core message.
        make sure you only the converted text content in the output and no additional text.

        Original Text:
        {text}

        Rewritten Text ({tone} Tone):
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
            print(f"Error applying tone '{tone}': {e}. Returning original text.")
            return text

# Example usage (for testing)
if __name__ == '__main__':
    selector = ToneStyleSelector()
    original_text = "Hey team, check out the new product! It's really cool and helps a lot."
    professional_text = selector.apply_tone_style(original_text, "Professional")
    print(f"Original:\n{original_text}\n")
    print(f"Professional:\n{professional_text}\n")

    conversational_text = selector.apply_tone_style(original_text, "Conversational")
    print(f"Conversational:\n{conversational_text}\n")