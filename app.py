import streamlit as st
import os
import json
from dotenv import load_dotenv, find_dotenv
from main_agent import LinkedInPostGenerator
from linkedin_post_api import post_as_organization

# Load environment variables
load_dotenv(find_dotenv())

# Set page configuration
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #0A66C2;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        color: #0A66C2;
    }
    .post-container {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #ddd;
        margin-bottom: 20px;
    }
    .hashtag {
        background-color: #e6f2ff;
        border-radius: 5px;
        padding: 5px 10px;
        margin-right: 5px;
        margin-bottom: 5px;
        display: inline-block;
        color: #0A66C2;
    }
    .tag {
        background-color: #e6fff2;
        border-radius: 5px;
        padding: 5px 10px;
        margin-right: 5px;
        margin-bottom: 5px;
        display: inline-block;
        color: #0A8A5F;
    }
    .validation-issue {
        color: #d9534f;
        margin-bottom: 5px;
    }
    .cta {
        font-weight: bold;
        color: #0A66C2;
    }
    .char-count {
        color: #6c757d;
        font-size: 0.9rem;
    }
    .char-count-warning {
        color: #d9534f;
        font-size: 0.9rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header">LinkedIn Post Generator</div>', unsafe_allow_html=True)
    st.markdown("Generate professional LinkedIn posts with AI assistance")

    # Sidebar for inputs
    with st.sidebar:
        st.markdown('<div class="section-header">Post Parameters</div>', unsafe_allow_html=True)

        # Topic input
        topic = st.text_area("Topic",
                            placeholder="Enter the main subject of your post (e.g., 'Launch of our new AI-powered customer support tool')",
                            height=100)

        # Tone selection
        tone_options = ["Professional", "Conversational", "Enthusiastic", "Informative",
                        "Celebratory", "Thoughtful", "Inspirational", "Educational"]
        tone = st.selectbox("Tone", tone_options, index=0)

        # Length preference
        length_options = ["short", "moderate", "long"]
        length_preference = st.select_slider("Length Preference",
                                            options=length_options,
                                            value="moderate")

        # Number of hashtags
        num_hashtags = st.slider("Number of Hashtags", min_value=0, max_value=10, value=5)

        # Include CTA
        include_cta = st.checkbox("Include Call-to-Action", value=True)

        # Audience type
        audience_options = ["general", "tech", "marketing", "finance", "healthcare", "education", "startup"]
        audience_type = st.selectbox("Target Audience", audience_options, index=0)

        # Translation
        enable_translation = st.checkbox("Enable Translation", value=False)
        target_language = None
        if enable_translation:
            language_options = ["Spanish", "French", "German", "Italian", "Portuguese",
                               "Chinese", "Japanese", "Arabic", "Russian", "Hindi"]
            target_language = st.selectbox("Target Language", language_options)

        # Generate button
        generate_button = st.button("Generate LinkedIn Post", type="primary", use_container_width=True)

    # Main content area
    if 'post_details' not in st.session_state:
        st.session_state.post_details = None

    if generate_button and topic:
        with st.spinner("Generating your LinkedIn post..."):
            try:
                # Initialize the generator
                generator = LinkedInPostGenerator()

                # Generate the post
                post_details = generator.generate_linkedin_post(
                    topic=topic,
                    tone=tone,
                    length_preference=length_preference,
                    num_hashtags=num_hashtags,
                    include_cta=include_cta,
                    target_language=target_language,
                    audience_type=audience_type
                )

                st.session_state.post_details = post_details
            except Exception as e:
                st.error(f"Error generating post: {str(e)}")

    # Display generated post
    if st.session_state.post_details:
        post_details = st.session_state.post_details

        # Post content
        st.markdown('<div class="section-header">Generated LinkedIn Post</div>', unsafe_allow_html=True)

        # Character count display
        char_count = post_details['character_count']
        max_chars = 3000  # LinkedIn's approximate limit

        if post_details['is_within_limit']:
            st.markdown(f'<div class="char-count">Character count: {char_count}/{max_chars}</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="char-count-warning">Character count: {char_count}/{max_chars} (exceeds limit)</div>',
                        unsafe_allow_html=True)

        # Post content in a container
        st.markdown('<div class="post-container">', unsafe_allow_html=True)
        st.markdown(post_details['final_post'].replace('\n', '<br>'), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Action buttons
        col_copy, col_post = st.columns(2)

        # Copy button
        with col_copy:
            if st.button("Copy to Clipboard", use_container_width=True):
                st.code(post_details['final_post'], language=None)
                st.success("Post copied to clipboard! (Use Ctrl+C to copy the text above)")

        # Post to LinkedIn button
        with col_post:
            linkedin_button = st.button("Post to LinkedIn", use_container_width=True,
                                       help="Post directly to LinkedIn using your API credentials")

            if linkedin_button:
                # Check if LinkedIn credentials are set
                access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
                org_urn = os.getenv("LINKEDIN_ORG_URN")

                if not access_token or not org_urn:
                    st.error("LinkedIn API credentials not found. Please set LINKEDIN_ACCESS_TOKEN and LINKEDIN_ORG_URN in your .env file.")
                    with st.expander("How to set up LinkedIn API credentials"):
                        st.markdown("""
                        1. Create a LinkedIn Developer App at [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
                        2. Get your Access Token and Organization URN
                        3. Add these to your `.env` file:
                        ```
                        LINKEDIN_ACCESS_TOKEN=your_access_token_here
                        LINKEDIN_ORG_URN=urn:li:organization:your_org_id_here
                        ```
                        """)
                else:
                    # Post to LinkedIn
                    with st.spinner("Posting to LinkedIn..."):
                        result = post_as_organization(post_details['final_post'])

                        if result["success"]:
                            st.success(f"✅ {result['message']}")
                        else:
                            st.error(f"❌ {result['message']}")
                            if result.get("error"):
                                with st.expander("Error Details"):
                                    st.json(result["error"] if isinstance(result["error"], dict) else {"error": result["error"]})

        # Create columns for additional information
        col1, col2 = st.columns(2)

        # Hashtags
        with col1:
            st.markdown('<div class="section-header">Suggested Hashtags</div>', unsafe_allow_html=True)
            if post_details['suggested_hashtags']:
                hashtags_html = ""
                for hashtag in post_details['suggested_hashtags']:
                    hashtags_html += f'<div class="hashtag">{hashtag}</div>'
                st.markdown(hashtags_html, unsafe_allow_html=True)
            else:
                st.info("No hashtags generated")

        # Tags
        with col2:
            st.markdown('<div class="section-header">Suggested Tags</div>', unsafe_allow_html=True)
            if post_details['suggested_tags_placeholders']:
                tags_html = ""
                for tag in post_details['suggested_tags_placeholders']:
                    tags_html += f'<div class="tag">{tag}</div>'
                st.markdown(tags_html, unsafe_allow_html=True)
            else:
                st.info("No tags suggested")

        # Validation issues
        st.markdown('<div class="section-header">Validation Issues</div>', unsafe_allow_html=True)
        if post_details['validation_issues']:
            issues_html = ""
            for issue in post_details['validation_issues']:
                issues_html += f'<div class="validation-issue">• {issue}</div>'
            st.markdown(issues_html, unsafe_allow_html=True)
        else:
            st.success("No validation issues found")

        # Call to Action
        if post_details['suggested_cta']:
            st.markdown('<div class="section-header">Suggested Call-to-Action</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="cta">{post_details["suggested_cta"]}</div>', unsafe_allow_html=True)

    # Instructions if no post has been generated yet
    elif not generate_button:
        st.info("Enter your post details in the sidebar and click 'Generate LinkedIn Post' to create your content.")

if __name__ == "__main__":
    main()
