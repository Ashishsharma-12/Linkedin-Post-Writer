# sub_agents/hashtag_generator.py
import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class HashtagGenerator:
    """
    Generates relevant and potentially trending hashtags based on the post content.

    Args:
        text: The post content.
        num_hashtags: The desired number of hashtags.

    Returns:
        A list of recommended hashtags.

    """
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it or pass it.")
        genai.configure(api_key=api_key)
        llm = os.getenv("MODEL_NAME")
        # print(llm)
        self.model = genai.GenerativeModel(llm) 

    def generate_hashtags(self, text: str, num_hashtags: int = 5) -> list[str]:
        """
        Generates relevant hashtags for the given text.

        Args:
            text: The post content.
            num_hashtags: The desired number of hashtags.

        Returns:
            A list of recommended hashtags.
        """
        prompt = f"""
        Generate {num_hashtags} relevant hashtags for the following LinkedIn post content.
        Suggest a mix of popular, niche, and potentially trending hashtags related to the topic.
        Do not include hashtags that are too generic (like #post or #linkedin).
        Provide only the hashtags, one per line, starting with '#'.

        Post Content:
        {text}

        Hashtags:
        """
        try:
            response = self.model.generate_content(prompt)
            if response and response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                 hashtags_str = "".join([part.text for part in response.candidates[0].content.parts]).strip()
                 # Split lines, filter for valid hashtags, remove duplicates
                 hashtags = [h.strip() for h in hashtags_str.split('\n') if h.strip().startswith('#') and len(h.strip()) > 1]
                 return list(set(hashtags))[:num_hashtags] # Return unique hashtags up to limit
            else:
                print("Warning: LLM response empty for hashtag generation. Returning empty list.")
                return []
        except Exception as e:
            print(f"Error generating hashtags: {e}. Returning empty list.")
            return []

# Example usage (for testing)
if __name__ == '__main__':
    generator = HashtagGenerator()
    post_content = "Excited to share our new AI-powered analytics platform for small businesses. It simplifies data insights."
    hashtags = generator.generate_hashtags(post_content, num_hashtags=7)
    print(f"Post Content:\n{post_content}\n")
    print(f"Suggested Hashtags:\n{hashtags}\n")