import asyncio
from twitchAPI.twitch import Twitch
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
app_id = os.getenv('TWITCH_APP_ID')
secret = os.getenv('TWITCH_SECRET')
user_token = os.getenv('TWITCH_ACCESS_TOKEN')

# Test user ID
test_user_id = "641972806"  # Replace with the real user ID

# Asynchronous function to test get_followed_streams
async def test_get_followed_streams():
    twitch = await Twitch(app_id, secret)
    twitch.auto_refresh_auth = False  # Disable auto-refresh for simplicity
    twitch.set_user_authentication(user_token, ["user:read:follows"])

    try:
        # Fetch followed streams
        print(f"Fetching active streams followed by user {test_user_id}...")
        total_streams = []
        cursor = None

        async for stream in twitch.get_followed_streams(user_id=test_user_id, first=100, after=cursor):
            # Add the stream information to the list
            total_streams.append({
                "stream_id": stream.id,
                "user_id": stream.user_id,
                "user_name": stream.user_name,
                "game_id": stream.game_id,
                "game_name": stream.game_name,
                "viewer_count": stream.viewer_count,
                "started_at": stream.started_at,
                "title": stream.title,
                "language": stream.language,
                "is_mature": stream.is_mature,
            })

            # Debug: Print the stream
            print(f"Stream: {stream.user_name} playing {stream.game_name} with {stream.viewer_count} viewers")

        # Summary of fetched streams
        print(f"Total active streams collected: {len(total_streams)}")
        for stream in total_streams[:5]:  # Print a sample
            print(f"Sample Stream: {stream['user_name']} playing {stream['game_name']} with {stream['viewer_count']} viewers")

    except Exception as e:
        print(f"Error fetching followed streams for user {test_user_id}: {e}")
    finally:
        await twitch.close()

# Run the test
if __name__ == "__main__":
    asyncio.run(test_get_followed_streams())
