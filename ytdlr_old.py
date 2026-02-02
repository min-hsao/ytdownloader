import argparse
import yt_dlp
import subprocess
import os

def check_codec_compatibility(filename):
    """Verify video codec and fix HEVC tag if needed"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
             '-show_entries', 'stream=codec_name,codec_tag_string',
             '-of', 'csv=p=0', filename],
            capture_output=True, text=True
        )
        codec, tag = result.stdout.strip().split(',')

        if codec == 'hevc' and tag != 'hvc1':
            print("⚠️  Fixing HEVC tag for QuickTime compatibility...")
            base, ext = os.path.splitext(filename)
            new_filename = f"{base}_quicktime{ext}"
            subprocess.run([
                'ffmpeg', '-i', filename,
                '-c', 'copy', '-tag:v', 'hvc1',
                new_filename
            ], check=True)
            os.replace(new_filename, filename)
            print("✅  HEVC tag fixed")

    except Exception as e:
        print(f"⚠️  Codec check failed: {e}")

def download_youtube_video(url, output_name=None, resolution=None, audio_only=False):
    try:
        ydl_opts = {
            'quiet': True,
            'outtmpl': f"{output_name}.%(ext)s" if output_name else "%(title)s.%(ext)s",
            'format': 'bestvideo[ext=mp4][vcodec^=avc]+bestaudio[ext=m4a]/best[ext=mp4]',
            'merge_output_format': 'mp4',
            'postprocessor_args': ['-movflags', '+faststart'],
        }

        if audio_only:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            })
        elif resolution:
            res = ''.join(filter(str.isdigit, resolution))
            if res:
                ydl_opts['format'] = f'bestvideo[ext=mp4][vcodec^=avc][height<={res}]+bestaudio[ext=m4a]/best[ext=mp4]'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
            ext = 'mp3' if audio_only else 'mp4'

            print(f"⏬ Downloading: {title}...")
            ydl.download([url])

            filename = f"{output_name or title}.{ext}"
            if not audio_only:
                check_codec_compatibility(filename)

            print(f"✅  Download complete: {filename}")
            print(f"📏 File size: {os.path.getsize(filename)//1024}KB")

    except Exception as e:
        print(f"❌ Error: {str(e).split(';')[0]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Downloader (QuickTime-ready MP4/MP3)")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-o", "--output", help="Output filename (without extension)")
    parser.add_argument("-r", "--resolution", help="Max resolution (e.g., 720p, 1080p)")
    parser.add_argument("-a", "--audio", action="store_true", help="Download audio only (MP3)")

    args = parser.parse_args()
    download_youtube_video(args.url, args.output, args.resolution, args.audio)
