# sub_agents/content_validator.py

import google.generativeai as genai
import os
import re
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class ContentValidator:
    """
    Checks for grammar, spelling, tone consistency, and potentially sensitive language.
    Leverages LLM for contextual checks (like tone consistency) and basic rules/regex for others.
    """
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it or pass it.")
        genai.configure(api_key=api_key)
        llm = os.getenv("MODEL_NAME")
        self.model = genai.GenerativeModel(llm)

    def validate_post(self, text: str, expected_tone: str) -> list[str]:
        """
        Performs various validation checks on the post content.

        Args:
            text: The post content.
            expected_tone: The tone that was intended for the post.

        Returns:
            A list of issues found (empty list if no issues).
        """
        issues = []

        # --- Basic Checks (using Python/regex) ---
        # Simple placeholder for basic checks - real ones would use libraries like NLTK, SpaCy, or regex patterns
        if re.search(r'\b(lol|lmao|brb)\b', text, re.IGNORECASE):
             issues.append("Avoid informal abbreviations like 'lol', 'lmao', 'brb'.")
        if re.search(r'!!!|\?\?\?|!!!\?\?\?', text):
             issues.append("Excessive use of exclamation/question marks can appear unprofessional.")
        # Add checks for repetitive phrases, all caps sections (unless intentional), etc.

        # --- LLM-based Checks (for grammar, spelling, tone, sensitivity) ---
        prompt = f"""
        Analyze the following LinkedIn post draft for potential issues:
        1.  **Grammar and Spelling:** Identify any clear errors.
        2.  **Tone Consistency:** Does the text maintain a {expected_tone} tone throughout? Point out sections that deviate.
        3.  **Professionalism/Sensitivity:** Are there any phrases, words, or concepts that might be considered unprofessional, overly casual, or sensitive for a public LinkedIn audience?

        List any identified issues clearly and concisely. If no issues are found, respond with "No issues found.".

        Post Content:
        {text}

        Analysis:
        """
        try:
            response = self.model.generate_content(prompt)
            if response and response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                 analysis_text = "".join([part.text for part in response.candidates[0].content.parts]).strip()
                 if "no issues found" in analysis_text.lower():
                     pass # No LLM issues
                 else:
                     # Split the analysis into potential issues
                     llm_issues = [line.strip() for line in analysis_text.split('\n') if line.strip()]
                     issues.extend(llm_issues)
            else:
                print("Warning: LLM response empty for validation.")
                # Cannot perform LLM-based checks without response
                if not issues: # If no rule-based issues found either
                    issues.append("Validation check could not be completed.")

        except Exception as e:
            print(f"Error during LLM validation: {e}.")
            if not issues: # If no rule-based issues found either
                 issues.append("Validation check could not be completed due to an error.")


        return issues

# Example usage (for testing)
if __name__ == '__main__':
    validator = ContentValidator()
    good_post = "We are excited to announce our new partnership. This collaboration will enable us to deliver greater value to our customers."
    bad_post = "OMG! Our team's new widget is like, SO COOL!!! You guys gotta check it out. #awesome #like"
    tone_issue_post = "Our Q3 results are out! We saw significant growth across all segments. This is fantastic news! Anyway, what are you having for lunch today?"


    print(f"Validating Good Post (Professional):\n{good_post}\nIssues: {validator.validate_post(good_post, 'Professional')}\n---")
    print(f"Validating Bad Post (Professional expected):\n{bad_post}\nIssues: {validator.validate_post(bad_post, 'Professional')}\n---")
    print(f"Validating Tone Issue Post (Professional expected):\n{tone_issue_post}\nIssues: {validator.validate_post(tone_issue_post, 'Professional')}\n---")