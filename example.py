# example.py
from main_agent import LinkedInPostGenerator

def main():
    """
    Example script demonstrating how to use the LinkedIn Post Generator.
    """
    print("LinkedIn Post Generator Example")
    print("===============================")
    
    # Initialize the generator
    generator = LinkedInPostGenerator()
    
    # Example 1: Generate a professional post about AI
    print("\n\nExample 1: Professional Post about AI")
    print("-------------------------------------")
    
    post_details = generator.generate_linkedin_post(
        topic="How AI is transforming customer service in 2024",
        tone="Professional",
        length_preference="moderate",
        num_hashtags=5,
        include_cta=True,
        audience_type_for_timing="tech"
    )
    
    print("\n=== Generated Post ===")
    print(post_details['final_post'])
    print("\n=== Post Details ===")
    print(f"Character Count: {post_details['character_count']}")
    print(f"Within Limit: {post_details['is_within_limit']}")
    print(f"Suggested Hashtags: {post_details['suggested_hashtags']}")
    print(f"Suggested Tags: {post_details['suggested_tags_placeholders']}")
    print(f"Suggested CTA: {post_details['suggested_cta']}")
    print(f"Timing Advice: {post_details['timing_advice']}")
    
    # Example 2: Generate a celebratory post with translation
    print("\n\nExample 2: Celebratory Post with French Translation")
    print("--------------------------------------------------")
    
    post_details = generator.generate_linkedin_post(
        topic="Our team just reached 1 million users on our platform",
        tone="Celebratory",
        length_preference="short",
        num_hashtags=3,
        include_cta=True,
        target_language="French"
    )
    
    print("\n=== Generated Post (English) ===")
    print(post_details['final_post'])
    print("\n=== French Translation ===")
    print(post_details['translated_post'])
    print("\n=== Post Details ===")
    print(f"Character Count: {post_details['character_count']}")
    print(f"Suggested Hashtags: {post_details['suggested_hashtags']}")
    
    # Example 3: Generate a conversational post
    print("\n\nExample 3: Conversational Post")
    print("-----------------------------")
    
    post_details = generator.generate_linkedin_post(
        topic="My journey transitioning from marketing to data science",
        tone="Conversational",
        length_preference="long",
        num_hashtags=4,
        include_cta=True
    )
    
    print("\n=== Generated Post ===")
    print(post_details['final_post'])
    print("\n=== Post Details ===")
    print(f"Character Count: {post_details['character_count']}")
    print(f"Suggested Hashtags: {post_details['suggested_hashtags']}")
    print(f"Validation Issues: {post_details['validation_issues']}")

if __name__ == "__main__":
    main()
