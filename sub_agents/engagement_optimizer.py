# sub_agents/engagement_optimiser.py

import google.generativeai as genai
import os
import random
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class EngagementOptimiser:
    """
    Suggests calls-to-action and offers generic timing advice.
    Note: Timing advice is highly generalized here; real advice needs data.
    """
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it or pass it.")
        genai.configure(api_key=api_key)
        llm = os.getenv("MODEL_NAME")
        self.model = genai.GenerativeModel(llm)

        self.common_ctas = [
            "What are your thoughts on this?",
            "Let's connect and discuss!",
            "Excited to hear your feedback!",
            "Have you experienced something similar?",
            "Looking forward to your insights in the comments!",
            "Feel free to reach out if you'd like to learn more.",
            "Open to collaboration - let me know if you're interested!",
            "Read more in the comments below 👇",
            "What's your take?",
            "Share your experiences below!"
        ]

    def suggest_cta(self, text: str) -> str:
        """
        Suggests a relevant call-to-action based on the text content.

        Args:
            text: The post content.

        Returns:
            A suggested CTA string.
        """
        # Using LLM to suggest a contextually relevant CTA
        prompt = f"""
        Based on the following LinkedIn post content, suggest a concise call-to-action to encourage engagement (comments, likes, shares, connections).
        Choose a CTA that fits the tone and topic of the post.
        Provide only the suggested call-to-action text.

        Post Content:
        {text}

        Suggested Call-to-Action:
        """
        try:
            response = self.model.generate_content(prompt)
            if response and response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                 cta = "".join([part.text for part in response.candidates[0].content.parts]).strip()
                 # Simple validation: check if it's too long or nonsensical
                 if 10 < len(cta) < 150 and '\n' not in cta:
                     return cta
                 else:
                     print("Warning: LLM generated potentially unsuitable CTA. Selecting a common one.")
                     return random.choice(self.common_ctas)
            else:
                print("Warning: LLM response empty for CTA suggestion. Selecting a common one.")
                return random.choice(self.common_ctas)
        except Exception as e:
            print(f"Error suggesting CTA: {e}. Selecting a common one.")
            return random.choice(self.common_ctas)

    def get_timing_advice(self, audience_type: str = "general") -> str:
        """
        Provides generic timing advice for posting on LinkedIn.
        (Highly generalized - needs actual data for accuracy).

        Args:
            audience_type: Type of audience (e.g., "general", "tech", "finance").

        Returns:
            A string providing timing advice.
        """
        # Disclaimer needed as this is highly variable
        disclaimer = "Note: This is general advice. Optimal timing varies greatly by your specific audience and location."

        advice = "General best times are typically Tuesday-Thursday during business hours (9 AM - 3 PM local time)."
        if "tech" in audience_type.lower():
             advice = "Tech professionals might be active slightly later in the day or even early morning. Tuesday-Thursday, 9 AM - 4 PM."
        elif "finance" in audience_type.lower():
             advice = "Finance professionals often check LinkedIn early. Monday-Friday, 7 AM - 10 AM and 1 PM - 3 PM."
        # Add more audience types as needed

        return f"{advice} {disclaimer}"

# Example usage (for testing)
if __name__ == '__main__':
    optimiser = EngagementOptimiser()
    post_content = "Our team just hit a major milestone on Project Phoenix! Couldn't have done it without everyone's hard work."

    suggested_cta = optimiser.suggest_cta(post_content)
    print(f"Post Content:\n{post_content}\n")
    print(f"Suggested CTA: {suggested_cta}\n")

    timing_advice = optimiser.get_timing_advice("general")
    print(f"Timing Advice: {timing_advice}\n")
    timing_advice_tech = optimiser.get_timing_advice("tech")
    print(f"Timing Advice (Tech Audience): {timing_advice_tech}\n")