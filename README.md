# ytdownloader

A simple Python CLI tool to download YouTube videos as QuickTime-compatible MP4 or MP3 audio files.

## Features

- Download videos in MP4 format (H.264 codec for maximum compatibility)
- Extract audio only as MP3
- Specify maximum resolution (720p, 1080p, etc.)
- Automatic HEVC to QuickTime-compatible tag conversion
- Custom output filenames

## Requirements

- Python 3.8+
- ffmpeg (must be installed and in PATH)
- ffprobe (usually comes with ffmpeg)

## Installation

```bash
pip install -r requirements.txt
```

Make sure ffmpeg is installed:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

## Usage

### Download video (default: best quality MP4)

```bash
python ytdlr.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download with custom filename

```bash
python ytdlr.py "https://www.youtube.com/watch?v=VIDEO_ID" -o my_video
```

### Download at specific resolution

```bash
python ytdlr.py "https://www.youtube.com/watch?v=VIDEO_ID" -r 720p
```

### Download audio only (MP3)

```bash
python ytdlr.py "https://www.youtube.com/watch?v=VIDEO_ID" -a
```

## Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `url` | | YouTube video URL (required) |
| `--output` | `-o` | Output filename (without extension) |
| `--resolution` | `-r` | Max resolution (e.g., 720p, 1080p) |
| `--audio` | `-a` | Download audio only as MP3 |

## Output

- Videos are downloaded in MP4 format with H.264 video codec for maximum compatibility
- Audio files are extracted as 192kbps MP3
- HEVC videos are automatically retagged for QuickTime compatibility

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

Min-Hsao Chen
