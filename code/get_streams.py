import asyncio
from twitchAPI.twitch import Twitch
import datetime
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
app_id = os.getenv('TWITCH_APP_ID')
secret = os.getenv('TWITCH_SECRET')

langs = ['en']
list_df = []

# Asynchronous query function
async def query(twitch, lang):
    global list_df
    count = 0  # To track the number of streams processed
    try:
        # Use async for to iterate over the streams async_generator
        async for stream in twitch.get_streams(first=100, language=lang):
            captured_at = datetime.datetime.now()
            user_id = stream.user_id
            user_name = stream.user_name
            game_id = stream.game_id
            game_name = stream.game_name
            title = stream.title
            viewer_count = stream.viewer_count
            started_at = stream.started_at
            is_mature = stream.is_mature
            language = stream.language

            # Append data to the list
            df = pd.DataFrame({
                "captured_at": [captured_at],
                "user_id": [user_id],
                "user_name": [user_name],
                "game_id": [game_id],
                "game_name": [game_name],
                "title": [title],
                "viewer_count": [viewer_count],
                "started_at": [started_at],
                "is_mature": [is_mature],
                "lang": [language],
            })
            list_df.append(df)

            count += 1
            print(f"Fetched stream {count}: {user_name} - {game_name} - {viewer_count} viewers")
    except Exception as e:
        print(f"Error fetching streams for language {lang}: {e}")


# Main function
async def main():
    global list_df
    twitch = await Twitch(app_id, secret)
    await twitch.authenticate_app([])

    try:
        for lang in langs:
            list_df.clear()  # Clear the list for each language
            await query(twitch, lang)

            # Combine all DataFrames and export to CSV
            if list_df:
                final_df = pd.concat(list_df, ignore_index=True)
                final_df.to_csv(f"data/twitch-live-export.csv", index=False)
                print(f"Data exported for language: {lang}")
            else:
                print(f"No data collected for language: {lang}")
    finally:
        await twitch.close()


# Run the script
if __name__ == "__main__":
    asyncio.run(main())
