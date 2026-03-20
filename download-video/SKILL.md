---
name: download-video
description: Download a video from YouTube, X/Twitter, or other supported sites using yt-dlp. Use when the user wants to download, save, or grab a video from a URL.
---

Download a video to the user's Desktop using `yt-dlp`.

## Steps

1. **Get the URL** — The user must provide a video URL. If they haven't, ask for one.

2. **Download** — Run:

   ```bash
   yt-dlp -o "~/Desktop/%(title)s.%(ext)s" "<URL>"
   ```

3. **Report** — Tell the user the filename and where it was saved.

## Notes

- If the user asks for audio only, add `-x --audio-format mp3`.
- If the user wants a specific format or quality, use `-f` (e.g. `-f "bestvideo[height<=1080]+bestaudio"`).
- yt-dlp supports YouTube, X/Twitter, Vimeo, Reddit, and hundreds of other sites.
- If the download fails, check that yt-dlp is installed (`brew install yt-dlp`) and that the URL is valid.
