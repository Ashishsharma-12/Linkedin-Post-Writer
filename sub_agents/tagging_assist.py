# sub_agents/tagging_assist.py
import google.generativeai as genai
import os
import re
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class TaggingAssist:
    """
    Suggests relevant people to tag in the LinkedIn post.
    This is a placeholder class that generates tag suggestions.
    In a real implementation, this would connect to LinkedIn's API
    or use a database of connections.
    """
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it or pass it.")
        genai.configure(api_key=api_key)
        llm = os.getenv("MODEL_NAME")
        self.model = genai.GenerativeModel(llm)
        
        # Safety settings to ensure appropriate content
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]

    def suggest_tags(self, text: str, max_tags: int = 3) -> list[str]:
        """
        Suggests relevant people to tag based on the post content.
        
        Args:
            text: The post content.
            max_tags: Maximum number of tags to suggest.
            
        Returns:
            A list of tag placeholders (e.g., "@AI_Expert", "@Marketing_Leader").
        """
        prompt = f"""
        Based on the following LinkedIn post content, suggest {max_tags} relevant professional roles or expertise areas 
        that would be good to tag. These should be generic placeholders, not actual people's names.
        
        For example: @AI_Expert, @Marketing_Leader, @Startup_Founder
        
        Provide only the tag placeholders, one per line, starting with '@'.
        
        Post Content:
        {text}
        
        Tag Suggestions:
        """
        
        try:
            generation_config = {
                "temperature": 0.2,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 256,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=self.safety_settings
            )
            
            if response and response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                tags_str = "".join([part.text for part in response.candidates[0].content.parts]).strip()
                # Split lines, filter for valid tags, remove duplicates
                tags = [t.strip() for t in tags_str.split('\n') if t.strip().startswith('@') and len(t.strip()) > 1]
                return list(set(tags))[:max_tags]  # Return unique tags up to limit
            else:
                print("Warning: LLM response empty for tag suggestion. Returning empty list.")
                return []
        except Exception as e:
            print(f"Error suggesting tags: {e}. Returning empty list.")
            return []

# Example usage (for testing)
if __name__ == '__main__':
    tagger = TaggingAssist()
    post_content = "Excited to share our new AI-powered analytics platform for small businesses. It simplifies data insights."
    tags = tagger.suggest_tags(post_content, max_tags=3)
    print(f"Post Content:\n{post_content}\n")
    print(f"Suggested Tags:\n{tags}\n")
