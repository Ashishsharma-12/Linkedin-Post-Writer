# main_agent.py

import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv
from typing import Optional, Dict, List, Any, Union

# Import our sub-agents
from sub_agents.tone_style_selector import ToneStyleSelector
from sub_agents.hashtag_generator import HashtagGenerator
from sub_agents.charachter_formater import CharacterFormatter
from sub_agents.engagement_optimizer import EngagementOptimiser
from sub_agents.content_validator import ContentValidator
from sub_agents.tagging_assist import TaggingAssist

load_dotenv(find_dotenv())

class LinkedInPostGenerator:
    """
    Orchestrates various sub-agents to generate and refine a LinkedIn post.
    """
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it or pass it.")
        genai.configure(api_key=api_key)

        # Initialize the main generative model for initial drafting
        llm = os.getenv("MODEL_NAME")
        self.main_model = genai.GenerativeModel(llm)

        # Initialize sub-agents
        self.tone_selector = ToneStyleSelector(api_key=api_key)
        self.hashtag_gen = HashtagGenerator(api_key=api_key)
        self.formatter = CharacterFormatter(api_key=api_key) # LinkedIn default limit
        self.engagement_opt = EngagementOptimiser(api_key=api_key)
        self.validator = ContentValidator(api_key=api_key)
        self.tagging_assist = TaggingAssist(api_key=api_key)

    def generate_initial_draft(self, topic: str, tone: str = "Professional", length_preference: str = "moderate") -> str:
        """Generates an initial draft of the LinkedIn post using the main model."""
        length_instruction = {
            "short": "Keep it concise, under 500 characters.",
            "moderate": "Write a moderate length post, aiming for 1000-1500 characters.",
            "long": "Write a detailed post, potentially up to 2500 characters."
        }.get(length_preference.lower(), "Write a moderate length post.")

        prompt = f"""
        Draft a LinkedIn post about the following topic: "{topic}".
        The desired tone is: {tone}.
        {length_instruction}
        Focus on creating engaging content relevant to a professional audience.
        """

        # Configure generation parameters for better quality
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

        # Safety settings to ensure appropriate content
        safety_settings = [
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

        try:
            response = self.main_model.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            if response and response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                #  print("----------------------------------------")
                #  print("".join([part.text for part in response.candidates[0].content.parts]).strip())
                #  print("----------------------------------------")
                 return "".join([part.text for part in response.candidates[0].content.parts]).strip()
            else:
                 return "[Error generating initial draft.]"
        except Exception as e:
            print(f"Error generating initial draft: {e}")
            return "[Error generating initial draft.]"

    def translate_text(self, text: str, target_language: str) -> str:
        """
        Translates the given text to the target language.

        Args:
            text: The text to translate.
            target_language: The target language (e.g., "French", "Spanish").

        Returns:
            The translated text.
        """
        if not text or not target_language:
            return ""

        prompt = f"""
        Translate the following LinkedIn post to {target_language}.
        Maintain the professional tone and formatting of the original post.

        Original Post:
        {text}

        {target_language} Translation:
        """

        generation_config = {
            "temperature": 0.2,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

        try:
            response = self.main_model.generate_content(
                prompt,
                generation_config=generation_config
            )
            if response and response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                 return "".join([part.text for part in response.candidates[0].content.parts]).strip()
            else:
                 print("Warning: LLM response empty for translation. Returning empty string.")
                 return ""
        except Exception as e:
            print(f"Error translating text: {e}")
            return ""


    def generate_linkedin_post(self,
                               topic: str,
                               tone: str = "Professional",
                               length_preference: str = "moderate",
                               num_hashtags: int = 5,
                               include_cta: bool = True,
                               target_language: str = None,
                               audience_type: str = "general") -> dict:
        """
        Generates a LinkedIn post by orchestrating sub-agents.

        Args:
            topic: The main subject of the post.
            tone: The desired tone (e.g., "Professional", "Conversational").
            length_preference: "short", "moderate", or "long".
            num_hashtags: Number of hashtags to suggest.
            include_cta: Whether to include a call-to-action suggestion.
            target_language: Optional language for translation (e.g., "Spanish").
            audience_type: Type of audience.

        Returns:
            A dictionary containing the generated post and other suggestions.
        """
        print(f"Generating LinkedIn post about '{topic}' with '{tone}' tone...")

        # 1. Generate Initial Draft
        post_draft = self.generate_initial_draft(topic, tone, length_preference)
        print("\n--- Initial Draft ---")
        print(post_draft)

        # --- Refine and Augment Draft using Sub-Agents ---

        # Tone adjustment (optional, the initial draft prompt already included tone)
        post_draft = self.tone_selector.apply_tone_style(post_draft, tone)
        print("\n--- Tone Adjusted Draft ---")
        print(post_draft) # Might not look different if initial draft was good

        # 2. Validate Content
        print("\n--- Running Validation ---")
        validation_issues = self.validator.validate_post(post_draft, tone)
        if validation_issues:
            print("Validation Issues Found:")
            for issue in validation_issues:
                print(f"- {issue}")
            # Decide how to handle issues: either stop, report, or attempt auto-correction
            # For this example, we'll just report. A real agent might try to fix.
        else:
            print("Validation: No major issues found.")

        # 3. Generate Hashtags
        print("\n--- Generating Hashtags ---")
        suggested_hashtags = self.hashtag_gen.generate_hashtags(post_draft, num_hashtags)
        print(f"Suggested Hashtags: {suggested_hashtags}")

        # 4. Suggest Tags
        print("\n--- Suggesting Tags ---")
        suggested_tags = self.tagging_assist.suggest_tags(post_draft)
        print(f"Suggested Tag Placeholders: {suggested_tags}") # Remember these are placeholders

        # 5. Add CTA (Optional)
        suggested_cta = ""
        if include_cta:
            print("\n--- Suggesting Call-to-Action ---")
            suggested_cta = self.engagement_opt.suggest_cta(post_draft)
            print(f"Suggested CTA: {suggested_cta}")
            # Optionally append CTA to the post draft
            if post_draft and suggested_cta:
                 # Add a line break before CTA
                 post_draft += f"\n\n{suggested_cta}"
            elif suggested_cta:
                 post_draft = suggested_cta # If draft generation failed, just use CTA? probably not ideal.

        # 6. Format and Check Character Count (after potentially adding CTA)
        print("\n--- Formatting & Length Check ---")
        formatted_post = self.formatter.format_text(post_draft)
        is_within_limit, char_count = self.formatter.check_length(formatted_post)

        if not is_within_limit:
            print(f"Warning: Post exceeds character limit ({char_count}/{self.formatter.max_chars}). Trimming.")
            final_post = self.formatter.trim_text(formatted_post)
            final_char_count = len(final_post)
            print(f"Trimmed post length: {final_char_count}")
        else:
            print(f"Post length is within limit ({char_count}/{self.formatter.max_chars}).")
            final_post = formatted_post
            final_char_count = char_count


        # --- Compile Final Output ---
        output = {
            "final_post": final_post,
            "character_count": final_char_count,
            "is_within_limit": final_char_count <= self.formatter.max_chars, # Re-check after trimming
            "suggested_hashtags": suggested_hashtags,
            "suggested_tags_placeholders": suggested_tags, # User needs to manually add/replace
            "suggested_cta": suggested_cta,
            "validation_issues": validation_issues,
        }

        print("\n--- Generation Complete ---")
        return output

# --- How to run ---
if __name__ == '__main__':
    # Ensure your GOOGLE_API_KEY environment variable is set
    # export GOOGLE_API_KEY='YOUR_API_KEY'

    generator = LinkedInPostGenerator()

    # Example 1: Standard professional post
    post_details_1 = generator.generate_linkedin_post(
        topic="Launch of our new AI-powered customer support tool",
        tone="Professional",
        length_preference="moderate",
        num_hashtags=7,
        include_cta=True,
        audience_type="tech"
    )

    # print("\n===== GENERATED POST 1 =====")
    # print("\nCharacter Count:", post_details_1['character_count'])
    # print("Within Limit:", post_details_1['is_within_limit'])
    # print("Suggested Hashtags:", post_details_1['suggested_hashtags'])
    # print("Suggested Tag Placeholders:", post_details_1['suggested_tags_placeholders'])
    # print("Validation Issues:", post_details_1['validation_issues'])
    print("\n\n============================")
    print("\nPost Content:\n", post_details_1['final_post'])
