# Media Processing Guide

DionoAutogen AI includes comprehensive media processing capabilities for images and videos.

## Supported Formats

### Images
- **PNG** (.png)
- **JPEG** (.jpg, .jpeg)
- **GIF** (.gif)
- **BMP** (.bmp)
- **TIFF** (.tiff)
- **WEBP** (.webp)
- **SVG** (.svg) - Limited support

### Videos
- **MP4** (.mp4)
- **AVI** (.avi)
- **MOV** (.mov)
- **MKV** (.mkv)
- **FLV** (.flv)
- **WMV** (.wmv)
- **WEBM** (.webm)

## Features

### Image Processing
- **OCR (Optical Character Recognition)**: Extract text from images using Tesseract
- **Metadata Extraction**: Get image format, size, and color mode
- **Automatic Processing**: Images uploaded via API are automatically processed

### Video Processing
- **Speech-to-Text**: Transcribe audio from videos using Google Speech Recognition
- **Metadata Extraction**: Get video duration, FPS, and resolution
- **Audio Extraction**: Automatically extract audio track for transcription

## Usage

### 1. Via API Endpoint

#### Process Image from URL
```bash
curl -X POST http://localhost:8000/api/process-media \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "file_url": "https://example.com/document.png",
    "project_name": "my-project"
  }'
```

#### Process Local Video
```bash
curl -X POST http://localhost:8000/api/process-media \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "presentation.mp4",
    "project_name": "my-project"
  }'
```

### 2. Via File Upload

When you upload files through the `/api/upload` endpoint, media files are automatically processed:

```bash
curl -X POST http://localhost:8000/api/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "project_name=my-project" \
  -F "files=@image.png" \
  -F "files=@video.mp4"
```

Response includes transcripts:
```json
{
  "success": true,
  "message": "Uploaded 2 files",
  "files": [
    {
      "name": "image.png",
      "size": 12345,
      "path": "image.png",
      "transcript": "Image Metadata:\nFormat: PNG\nSize: 800x600\n\nExtracted Text:\nHello World",
      "media_type": "image"
    },
    {
      "name": "video.mp4",
      "size": 1234567,
      "path": "video.mp4",
      "transcript": "Video Metadata:\nDuration: 30.5 seconds\n\nAudio Transcript:\nWelcome to the presentation...",
      "media_type": "video"
    }
  ]
}
```

### 3. Via Python SDK

```python
from pathlib import Path
from diono_autogen.media_processor import media_processor

# Process local image
result = media_processor.process_media(Path("document.png"))
print(result['transcript'])

# Process image from URL
result = media_processor.process_media(Path("https://example.com/image.jpg"), is_url=True)
print(result['transcript'])

# Process video
result = media_processor.process_media(Path("video.mp4"))
print(result['transcript'])
```

## Requirements

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr ffmpeg
```

**macOS:**
```bash
brew install tesseract ffmpeg
```

**Windows:**
- Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- FFmpeg: https://ffmpeg.org/download.html

### Python Dependencies

All required packages are included in `requirements.txt`:
- `pillow` - Image processing
- `pytesseract` - OCR engine wrapper
- `opencv-python-headless` - Video processing
- `moviepy` - Video editing
- `SpeechRecognition` - Speech-to-text
- `pydub` - Audio processing

## Configuration

No additional configuration needed! The system uses:
- **Tesseract OCR** for image text extraction
- **Google Speech Recognition** for video transcription (free, no API key required)

## Limitations

### Image Processing
- SVG files have limited OCR support
- OCR accuracy depends on image quality and text clarity
- Handwritten text may not be recognized accurately

### Video Processing
- Speech recognition requires clear audio
- Background noise may affect transcription accuracy
- Very long videos may take time to process
- Google Speech Recognition has usage limits (free tier)

## Best Practices

1. **Image Quality**: Use high-resolution images for better OCR results
2. **Video Audio**: Ensure clear audio for accurate transcription
3. **File Size**: Large files may take longer to process
4. **Batch Processing**: Process multiple files in parallel for efficiency
5. **Error Handling**: Always check the `success` field in responses

## Troubleshooting

### OCR Not Working
- Ensure Tesseract is installed: `tesseract --version`
- Check image format is supported
- Verify image contains readable text

### Video Transcription Failing
- Ensure FFmpeg is installed: `ffmpeg -version`
- Check video has audio track
- Verify audio is clear and in supported language (English by default)

### URL Download Issues
- Check URL is accessible
- Verify file format from URL
- Ensure network connectivity

## Examples

### Extract Text from Screenshot
```python
result = media_processor.process_media(Path("screenshot.png"))
print(result['transcript'])
# Output:
# Image Metadata:
# Format: PNG
# Size: 1920x1080
# Mode: RGB
#
# Extracted Text:
# [Text from screenshot]
```

### Transcribe Meeting Recording
```python
result = media_processor.process_media(Path("meeting.mp4"))
print(result['transcript'])
# Output:
# Video Metadata:
# Duration: 1800.0 seconds
# FPS: 30.0
# Size: 1920x1080
#
# Audio Transcript:
# [Transcribed speech from video]
```

### Process Image from Web
```python
result = media_processor.process_media(
    Path("https://example.com/document.jpg"),
    is_url=True
)
print(result['transcript'])
```

## Future Enhancements

Planned features:
- Multiple language support for transcription
- Custom OCR models
- Video frame analysis
- Audio enhancement before transcription
- Batch processing optimization
- Progress tracking for long videos
