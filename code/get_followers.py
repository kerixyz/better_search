import asyncio
from twitchAPI.twitch import Twitch
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
app_id = os.getenv('TWITCH_APP_ID')
secret = os.getenv('TWITCH_SECRET')

# Input and output file paths
input_csv = "data/twitch-live-export_en.csv"
output_csv = "data/twitch-followers.csv"

# Asynchronous function to fetch followers
async def fetch_followers(twitch, broadcaster_id, max_followers=100):
    followers_data = []
    cursor = None
    try:
        while True:
            # Fetch a page of followers
            response = await twitch.get_channel_followers(broadcaster_id=broadcaster_id, first=100, after=cursor)

            # Access data directly
            if response.data:
                for follower in response.data:
                    followers_data.append({
                        "broadcaster_id": broadcaster_id,
                        "follower_user_id": follower.user_id,
                        "follower_user_name": follower.user_name,
                        "followed_at": follower.followed_at,
                    })

                    # Stop if max_followers limit is reached
                    if len(followers_data) >= max_followers:
                        return followers_data

            # Handle pagination
            cursor = response.cursor  # Replace this with the correct attribute after debugging
            if not cursor:
                break  # No more pages
    except Exception as e:
        print(f"Error fetching followers for broadcaster {broadcaster_id}: {e}")
    return followers_data

# Main function
async def main():
    # Initialize Twitch client
    twitch = await Twitch(app_id, secret)
    await twitch.authenticate_app([])

    try:
        # Load the input CSV file
        df = pd.read_csv(input_csv)
        all_followers = []

        # Iterate through each broadcaster
        for _, row in df.iterrows():
            broadcaster_id = row["user_id"]
            print(f"Fetching followers for broadcaster: {broadcaster_id} ({row['user_name']})")
            followers = await fetch_followers(twitch, broadcaster_id)
            all_followers.extend(followers)

        # Create a DataFrame from the followers data
        if all_followers:
            followers_df = pd.DataFrame(all_followers)
            followers_df.to_csv(output_csv, index=False)
            print(f"Followers data exported to {output_csv}")
        else:
            print("No followers data collected.")
    finally:
        await twitch.close()

# Run the script
if __name__ == "__main__":
    asyncio.run(main())
