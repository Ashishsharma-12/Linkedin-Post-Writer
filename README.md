# LinkedIn Post Writer

A Python application that uses Google's Generative AI (Gemini) to create engaging LinkedIn posts with various features.

**Read the [Streamlit UI README](STREAMLIT_README.md) for instructions on how to use the web interface.**

## Features

- Generate professional LinkedIn posts on any topic
- Customize tone and style (Professional, Conversational, Celebratory, etc.)
- Validate content for grammar, tone consistency, and professionalism
- Generate relevant hashtags
- Suggest people to tag
- Add engaging calls-to-action
- Format posts to fit LinkedIn character limits
- Translate posts to other languages
- Get timing advice for optimal posting

## Requirements

- Python 3.8+
- Google API key for Gemini models

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with your Google API key:
   ```
   GOOGLE_API_KEY = "your_google_api_key_here"
   MODEL_NAME = "gemini-2.5-pro-exp-03-25"  # or your preferred Gemini model
   ```

## Usage

```python
from main_agent import LinkedInPostGenerator

# Initialize the generator
generator = LinkedInPostGenerator()

# Generate a standard professional post
post_details = generator.generate_linkedin_post(
    topic="Launch of our new AI-powered customer support tool",
    tone="Professional",
    length_preference="moderate",  # "short", "moderate", or "long"
    num_hashtags=5,
    include_cta=True,
    audience_type_for_timing="tech"  # Optional: "general", "tech", etc.
)

# Print the generated post
print(post_details['final_post'])

# Access other generated content
print("Hashtags:", post_details['suggested_hashtags'])
print("Tag suggestions:", post_details['suggested_tags_placeholders'])
print("CTA:", post_details['suggested_cta'])
print("Timing advice:", post_details['timing_advice'])

# Generate a post with translation
post_details_translated = generator.generate_linkedin_post(
    topic="Team milestone celebration",
    tone="Celebratory",
    length_preference="short",
    target_language="French"  # Translate to French
)

# Print the translated post
print(post_details_translated['translated_post'])
```

## Architecture

The application uses a modular architecture with specialized sub-agents:

- **Main Agent**: Orchestrates the entire process
- **Sub-Agents**:
  - **ToneStyleSelector**: Adjusts the tone and style of the post
  - **ContentValidator**: Checks for grammar, spelling, and tone consistency
  - **HashtagGenerator**: Generates relevant hashtags
  - **TaggingAssist**: Suggests people to tag
  - **EngagementOptimiser**: Suggests CTAs and timing advice
  - **CharacterFormatter**: Ensures the post fits LinkedIn's character limits

## Google API Integration

This project uses Google's Generative AI (Gemini) models through the `google-generativeai` Python package. The integration includes:

1. **API Key Configuration**: Set up in the `.env` file or passed directly to the constructor
2. **Model Selection**: Configurable through the `MODEL_NAME` environment variable
3. **Generation Parameters**: Customized for each task with appropriate temperature, top_p, and safety settings
4. **Safety Settings**: Implemented to ensure appropriate content generation
5. **Error Handling**: Robust error handling for API failures

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
