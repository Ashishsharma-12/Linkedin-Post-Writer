import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Load from .env or replace directly here
ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
ORG_URN = os.getenv("LINKEDIN_ORG_URN")  # e.g., "urn:li:organization:107290150"

def post_as_organization(text: str):
    """
    Posts content to LinkedIn as an organization.
    
    Args:
        text: The text content to post
        
    Returns:
        dict: Response information including success status and any error messages
    """
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    payload = {
        "author": ORG_URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 201:
            return {
                "success": True,
                "message": "Post published successfully.",
                "data": response.json() if response.content else None
            }
        else:
            return {
                "success": False,
                "message": f"Failed to post: {response.status_code}",
                "error": response.json() if response.content else None
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error posting to LinkedIn: {str(e)}",
            "error": str(e)
        }

if __name__ == "__main__":
    your_post = "🎉 Big news from our team! We're building smarter agents to automate LinkedIn content generation. Follow us for more AI breakthroughs! #AI #LinkedIn #DLAI"
    result = post_as_organization(your_post)
    if result["success"]:
        print(f"✅ {result['message']}")
    else:
        print(f"❌ {result['message']}")
        if result.get("error"):
            print(result["error"])
