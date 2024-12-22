import asyncio
from twitchAPI.twitch import Twitch
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
app_id = os.getenv('TWITCH_APP_ID')
secret = os.getenv('TWITCH_SECRET')

# Async function to test data pull
async def test_pull():
    twitch = await Twitch(app_id, secret)  # Asynchronous initialization
    await twitch.authenticate_app([])
    try:
        count = 0  # Counter to limit streams
        limit = 5  # Total number of streams to fetch
        async for stream in twitch.get_streams(first=100):  # Fetch up to 100 per page
            if count >= limit:  # Stop once limit is reached
                break
            print(f"Streamer: {stream.user_name}, Game: {stream.game_name}, Viewers: {stream.viewer_count}")
            count += 1
        print(f"Pull successful! Fetched {count} streams.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await twitch.close()

# Run the async function
asyncio.run(test_pull())
