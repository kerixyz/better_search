import asyncio
from twitchAPI.twitch import Twitch
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
app_id = os.getenv('TWITCH_APP_ID')
secret = os.getenv('TWITCH_SECRET')

# Test user ID
test_user_id = "641972806"  # Replace with a real user ID

# Asynchronous function to test get_followed_channels
async def test_get_followed_channels():
    twitch = await Twitch(app_id, secret)
    await twitch.authenticate_app([])  # Ensure authentication

    try:
        # Initialize pagination cursor
        cursor = None
        total_channels = []

        while True:
            # Fetch followed channels for the test user ID
            response = await twitch.get_followed_channels(user_id=test_user_id, first=100, after=cursor)

            # Debugging output
            print("Type of response:", type(response))
            print("Attributes of response:", dir(response))
            print("Response content:", response)

            # Access followed channels
            if response.data:
                for channel in response.data:
                    total_channels.append({
                        "broadcaster_id": channel.broadcaster_id,
                        "broadcaster_name": channel.broadcaster_name,
                        "followed_at": channel.followed_at,
                    })

            # Debug: Print the number of followed channels fetched so far
            print(f"Fetched {len(total_channels)} followed channels so far.")

            # Handle pagination
            cursor = response.current_cursor
            if not cursor:
                break  # No more pages

        # Debug: Print all collected channels
        print(f"Total followed channels collected: {len(total_channels)}")
        for channel in total_channels[:5]:  # Print a sample
            print(f"Broadcaster: {channel['broadcaster_name']} followed at {channel['followed_at']}")

    except Exception as e:
        print(f"Error fetching followed channels for user {test_user_id}: {e}")
    finally:
        await twitch.close()

# Run the test
if __name__ == "__main__":
    asyncio.run(test_get_followed_channels())
