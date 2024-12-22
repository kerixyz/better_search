import asyncio
from twitchAPI.twitch import Twitch
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
app_id = os.getenv('TWITCH_APP_ID')
secret = os.getenv('TWITCH_SECRET')

# Single broadcaster ID for testing
test_broadcaster_id = "641972806" 

# Asynchronous function to fetch and debug followers
async def test_fetch_followers():
    twitch = await Twitch(app_id, secret)
    await twitch.authenticate_app([])

    try:
        # Initialize pagination cursor
        cursor = None

        # Fetch followers for the test broadcaster ID
        response = await twitch.get_channel_followers(broadcaster_id=test_broadcaster_id, first=100, after=cursor)

        # Debugging output
        print("Type of response:", type(response))
        print("Attributes of response:", dir(response))
        print("Response content:", response)

        # Try to extract data
        if response.data:
            print("Sample follower data:")
            for follower in response.data:
                print(f"Follower ID: {follower.user_id}, Name: {follower.user_name}, Followed At: {follower.followed_at}")

        # Handle pagination
        print("Pagination info (if any):")
        if hasattr(response, 'pagination'):
            print("Pagination attribute found:", response.pagination)
        elif hasattr(response, 'cursor'):
            print("Cursor attribute found:", response.cursor)
        else:
            print("No pagination or cursor attribute found.")
    except Exception as e:
        print(f"Error fetching followers for broadcaster {test_broadcaster_id}: {e}")
    finally:
        await twitch.close()


# Run the test
if __name__ == "__main__":
    asyncio.run(test_fetch_followers())
