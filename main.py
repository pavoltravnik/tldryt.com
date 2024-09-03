from youtube_subtitle_downloader import extract_subtitles_from_chapters, get_youtube_title
from claude_api_processor import process_with_claude
import os

def main():
    # Get YouTube video URL
    video_url = input("Enter YouTube video URL: ")
    
    title = get_youtube_title(video_url)

    # Download subtitles
    subtitles = extract_subtitles_from_chapters(video_url)
    # print(subtitles)
    if not subtitles:
        print("Failed to download subtitles. Exiting.")
        return

    for subtitle in subtitles:
        # print(subtitle)
        prompt = f"""Summarize the following video subtitles, focusing on the main ideas and key points. Provide a concise TLDR (Too Long; Didn't Read) version that captures the essential information. Highlight any crucial insights, important facts, or central arguments. Aim to distill the content into a clear, easily digestible format that saves time while conveying the core message. Title is: {subtitle['chapter_title']}
        The subtitles are as follows:
        {subtitle['text']}
        Please provide:
        A TLDR summary (10 - 50 sentences)
        Any particularly noteworthy quotes or statistics, if applicable"""
        # print(prompt)
        if os.path.exists(f"{title}/{subtitle['num']} - {subtitle['chapter_title']}.txt"):
            print(f"Skipping {subtitle['chapter_title']} as it already exists.")
        else:
            result = process_with_claude(prompt)

            if result:
                print("Claude API analysis:", subtitle['chapter_title'])
                with open(f"{title}/{subtitle['num']} - {subtitle['chapter_title']}.txt", 'w') as f:
                    f.write(result[0].text)
            else:
                print("Failed to process subtitles with Claude API.")
            # break

if __name__ == "__main__":
    main()