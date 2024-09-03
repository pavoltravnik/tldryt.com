
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import re
import os


def get_youtube_title(video_url):
    try:
        yt = YouTube(video_url)
        title = yt.title
        os.makedirs(title, exist_ok=True)
        return title
    except Exception as e:
        return f"An error occurred: {e}"

def extract_subtitles_from_chapters(video_url):
    # Get video ID from URL
    video_id = video_url.split("v=")[1]

    # Get video information
    yt = YouTube(video_url)

    # Get chapters
    chapters = extract_chapters(yt)
    print(chapters)

    # If no chapters are found, treat the whole video as one chapter
    if not chapters:
        chapters = [{'title': 'Full Video', 'start_time': 0, 'end_time': yt.length}]

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    parts = []
    num = 1
    # Extract subtitles for each chapter
    for chapter in chapters:
        chapter_title = chapter['title']
        start_time = chapter['start_time']
        end_time = chapter['end_time']

        # print(f"\nChapter: {chapter_title}")
        # print("Subtitles:")

        chapter_subtitles = []
        for entry in transcript:
            if start_time <= entry['start'] < end_time:
                chapter_subtitles.append(entry['text'])

        # print(" ".join(chapter_subtitles))


        parts.append({
            "num": str(num).zfill(2),
            "chapter_title": chapter_title,
            "text": " ".join(chapter_subtitles),
        })
        num += 1
        # print(parts)
        # break
        # print(parts)
    return parts


def extract_chapters(yt):
    try:
        chapter_data = yt.initial_data['playerOverlays']['playerOverlayRenderer']['decoratedPlayerBarRenderer']['decoratedPlayerBarRenderer']['playerBar']['multiMarkersPlayerBarRenderer']['markersMap'][0]['value']['chapters']
        chapters = []
        for chapter in chapter_data:
            title = chapter['chapterRenderer']['title']['simpleText']
            start_time = int(chapter['chapterRenderer']['timeRangeStartMillis']) / 1000
            chapters.append({'title': title, 'start_time': start_time})
        
        # Add end times
        for i in range(len(chapters) - 1):
            chapters[i]['end_time'] = chapters[i+1]['start_time']
        chapters[-1]['end_time'] = yt.length

        return chapters
    except:
        return None