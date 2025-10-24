"""
Media processing module for images and videos
Handles OCR for images and speech-to-text for videos
"""
from pathlib import Path
from typing import Optional, Dict, Any
import tempfile
import requests
from PIL import Image
import pytesseract
import cv2
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from loguru import logger
import os


class MediaProcessor:
    """Process images and videos for transcription"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.supported_image_formats = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', '.svg'}
        self.supported_video_formats = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'}
    
    def is_image(self, file_path: Path) -> bool:
        """Check if file is an image"""
        return file_path.suffix.lower() in self.supported_image_formats
    
    def is_video(self, file_path: Path) -> bool:
        """Check if file is a video"""
        return file_path.suffix.lower() in self.supported_video_formats
    
    def download_file(self, url: str, dest: Path) -> bool:
        """Download file from URL"""
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(dest, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True
        except Exception as e:
            logger.error(f"Failed to download file from {url}: {e}")
            return False
    
    def extract_text_from_image(self, image_path: Path) -> str:
        """Extract text from image using OCR"""
        try:
            # Handle SVG separately (convert to PNG first)
            if image_path.suffix.lower() == '.svg':
                logger.warning("SVG OCR not fully supported, attempting basic conversion")
                # For SVG, we'd need cairosvg or similar, skip for now
                return "[SVG image - OCR not supported]"
            
            # Open image
            image = Image.open(image_path)
            
            # Perform OCR
            text = pytesseract.image_to_string(image)
            
            # Also get image metadata
            metadata = {
                'format': image.format,
                'size': image.size,
                'mode': image.mode
            }
            
            result = f"Image Metadata:\n"
            result += f"Format: {metadata['format']}\n"
            result += f"Size: {metadata['size'][0]}x{metadata['size'][1]}\n"
            result += f"Mode: {metadata['mode']}\n\n"
            result += f"Extracted Text:\n{text.strip()}\n"
            
            return result
        
        except Exception as e:
            logger.error(f"Failed to extract text from image {image_path}: {e}")
            return f"[Error extracting text from image: {str(e)}]"
    
    def extract_audio_from_video(self, video_path: Path, audio_path: Path) -> bool:
        """Extract audio from video file"""
        try:
            video = VideoFileClip(str(video_path))
            video.audio.write_audiofile(str(audio_path), logger=None)
            video.close()
            return True
        except Exception as e:
            logger.error(f"Failed to extract audio from video {video_path}: {e}")
            return False
    
    def transcribe_audio(self, audio_path: Path) -> str:
        """Transcribe audio file to text"""
        try:
            with sr.AudioFile(str(audio_path)) as source:
                audio_data = self.recognizer.record(source)
                
                # Try Google Speech Recognition (free, no API key needed)
                try:
                    text = self.recognizer.recognize_google(audio_data)
                    return text
                except sr.UnknownValueError:
                    return "[Speech recognition could not understand audio]"
                except sr.RequestError as e:
                    return f"[Speech recognition service error: {e}]"
        
        except Exception as e:
            logger.error(f"Failed to transcribe audio {audio_path}: {e}")
            return f"[Error transcribing audio: {str(e)}]"
    
    def process_video(self, video_path: Path) -> str:
        """Process video file and extract transcript"""
        try:
            # Get video metadata
            video = VideoFileClip(str(video_path))
            duration = video.duration
            fps = video.fps
            size = video.size
            video.close()
            
            result = f"Video Metadata:\n"
            result += f"Duration: {duration:.2f} seconds\n"
            result += f"FPS: {fps}\n"
            result += f"Size: {size[0]}x{size[1]}\n\n"
            
            # Extract audio and transcribe
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as audio_file:
                audio_path = Path(audio_file.name)
            
            try:
                if self.extract_audio_from_video(video_path, audio_path):
                    result += "Audio Transcript:\n"
                    transcript = self.transcribe_audio(audio_path)
                    result += transcript
                else:
                    result += "[Failed to extract audio from video]"
            finally:
                # Cleanup temp audio file
                if audio_path.exists():
                    audio_path.unlink()
            
            return result
        
        except Exception as e:
            logger.error(f"Failed to process video {video_path}: {e}")
            return f"[Error processing video: {str(e)}]"
    
    def process_media(self, file_path: Path, is_url: bool = False) -> Dict[str, Any]:
        """Process media file (image or video) and return transcript"""
        result = {
            'success': False,
            'file_type': None,
            'transcript': '',
            'error': None
        }
        
        try:
            # If URL, download first
            if is_url:
                url = str(file_path)
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_path = Path(tmp_file.name)
                
                if not self.download_file(url, tmp_path):
                    result['error'] = "Failed to download file from URL"
                    return result
                
                file_path = tmp_path
            
            # Determine file type and process
            if self.is_image(file_path):
                result['file_type'] = 'image'
                result['transcript'] = self.extract_text_from_image(file_path)
                result['success'] = True
            
            elif self.is_video(file_path):
                result['file_type'] = 'video'
                result['transcript'] = self.process_video(file_path)
                result['success'] = True
            
            else:
                result['error'] = f"Unsupported file format: {file_path.suffix}"
            
            # Cleanup temp file if it was a URL
            if is_url and file_path.exists():
                file_path.unlink()
        
        except Exception as e:
            logger.error(f"Failed to process media {file_path}: {e}")
            result['error'] = str(e)
        
        return result


# Global media processor instance
media_processor = MediaProcessor()
