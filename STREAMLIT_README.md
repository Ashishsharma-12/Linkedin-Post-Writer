# LinkedIn Post Generator - Streamlit UI

This is a Streamlit-based user interface for the LinkedIn Post Generator application. It provides an easy-to-use web interface for generating professional LinkedIn posts with AI assistance and posting directly to LinkedIn.

## Features

- Generate LinkedIn posts with customizable parameters
- Choose from different tones and styles
- Set post length preference
- Generate relevant hashtags
- Get suggestions for people to tag
- Validate content for grammar, tone, and professionalism
- Translate posts to different languages
- Copy generated posts to clipboard
- Post directly to LinkedIn using the LinkedIn API

## Installation

1. Make sure you have installed all the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up your environment variables by creating a `.env` file in the project root with your API keys:
   ```
   GOOGLE_API_KEY = "your_google_api_key_here"
   MODEL_NAME = "gemini-2.5-pro-exp-03-25"  # or your preferred Gemini model

   # LinkedIn API credentials (optional, only needed for posting to LinkedIn)
   LINKEDIN_ACCESS_TOKEN = "your_linkedin_access_token"
   LINKEDIN_ORG_URN = "urn:li:organization:your_organization_id"
   ```

## Running the Streamlit App

To run the Streamlit app, use the following command from the project root directory:

```
streamlit run app.py
```

This will start the Streamlit server and open the application in your default web browser.

## Usage

1. Enter your post topic in the sidebar
2. Select the desired tone, length, and other parameters
3. Click "Generate LinkedIn Post" to create your content
4. Review the generated post, hashtags, and suggestions
5. Use the "Copy to Clipboard" button to copy the post for use on LinkedIn
6. Alternatively, click "Post to LinkedIn" to publish directly to your LinkedIn organization page

## LinkedIn API Integration

To use the LinkedIn posting feature:

1. Create a LinkedIn Developer App at [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
2. Request the necessary permissions for posting content (r_organization_social, w_organization_social)
3. Generate an Access Token with the required permissions
4. Find your Organization URN (format: urn:li:organization:YOUR_ORG_ID)
5. Add these credentials to your `.env` file as shown in the Installation section

Note: LinkedIn Access Tokens typically expire after 60 days. You'll need to refresh your token periodically.

## Notes

- The character count shows how close you are to LinkedIn's approximate limit of 3,000 characters
- If validation issues are found, they will be displayed in the "Validation Issues" section
- You can enable translation to convert your post to different languages
