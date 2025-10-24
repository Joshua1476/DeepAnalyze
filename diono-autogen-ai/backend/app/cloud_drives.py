"""
Cloud storage integration for DionoAutogen AI
"""
from typing import List, Optional
from pathlib import Path
import requests
from .models import CloudProvider, CloudFile
from .crypto_utils import crypto
from loguru import logger


class CloudDrive:
    """Base class for cloud storage providers"""
    
    def __init__(self, provider: CloudProvider, credentials: dict):
        self.provider = provider
        self.credentials = credentials
    
    def list_files(self, folder_id: Optional[str] = None) -> List[CloudFile]:
        """List files in cloud storage"""
        raise NotImplementedError
    
    def download(self, file_id: str, dest: Path) -> bool:
        """Download file from cloud storage"""
        raise NotImplementedError
    
    def upload(self, file_path: Path, folder_id: Optional[str] = None) -> CloudFile:
        """Upload file to cloud storage"""
        raise NotImplementedError


class GoogleDriveClient(CloudDrive):
    """Google Drive integration"""
    
    def __init__(self, credentials: dict):
        super().__init__(CloudProvider.GOOGLE_DRIVE, credentials)
        self._init_service()
    
    def _init_service(self):
        """Initialize Google Drive service"""
        try:
            from googleapiclient.discovery import build
            from google.oauth2.credentials import Credentials
            
            creds = Credentials.from_authorized_user_info(self.credentials)
            self.service = build('drive', 'v3', credentials=creds)
        except Exception as e:
            logger.error(f"Failed to initialize Google Drive: {e}")
            self.service = None
    
    def list_files(self, folder_id: Optional[str] = None) -> List[CloudFile]:
        """List files in Google Drive"""
        if not self.service:
            return []
        
        try:
            query = f"'{folder_id}' in parents" if folder_id else None
            results = self.service.files().list(
                q=query,
                pageSize=100,
                fields="files(id, name, size, mimeType, modifiedTime)"
            ).execute()
            
            files = []
            for item in results.get('files', []):
                files.append(CloudFile(
                    id=item['id'],
                    name=item['name'],
                    size=int(item.get('size', 0)),
                    mime_type=item.get('mimeType'),
                    provider=CloudProvider.GOOGLE_DRIVE
                ))
            return files
        except Exception as e:
            logger.error(f"Failed to list Google Drive files: {e}")
            return []
    
    def download(self, file_id: str, dest: Path) -> bool:
        """Download file from Google Drive"""
        if not self.service:
            return False
        
        try:
            from googleapiclient.http import MediaIoBaseDownload
            import io
            
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            with open(dest, 'wb') as f:
                f.write(fh.getvalue())
            
            return True
        except Exception as e:
            logger.error(f"Failed to download from Google Drive: {e}")
            return False


class DropboxClient(CloudDrive):
    """Dropbox integration"""
    
    def __init__(self, credentials: dict):
        super().__init__(CloudProvider.DROPBOX, credentials)
        self._init_client()
    
    def _init_client(self):
        """Initialize Dropbox client"""
        try:
            import dropbox
            access_token = self.credentials.get('access_token')
            self.client = dropbox.Dropbox(access_token)
        except Exception as e:
            logger.error(f"Failed to initialize Dropbox: {e}")
            self.client = None
    
    def list_files(self, folder_id: Optional[str] = None) -> List[CloudFile]:
        """List files in Dropbox"""
        if not self.client:
            return []
        
        try:
            path = folder_id or ''
            result = self.client.files_list_folder(path)
            
            files = []
            for entry in result.entries:
                if hasattr(entry, 'size'):  # It's a file
                    files.append(CloudFile(
                        id=entry.id,
                        name=entry.name,
                        size=entry.size,
                        provider=CloudProvider.DROPBOX
                    ))
            return files
        except Exception as e:
            logger.error(f"Failed to list Dropbox files: {e}")
            return []
    
    def download(self, file_id: str, dest: Path) -> bool:
        """Download file from Dropbox"""
        if not self.client:
            return False
        
        try:
            metadata, response = self.client.files_download(file_id)
            with open(dest, 'wb') as f:
                f.write(response.content)
            return True
        except Exception as e:
            logger.error(f"Failed to download from Dropbox: {e}")
            return False


def get_cloud_client(provider: CloudProvider, credentials: dict) -> CloudDrive:
    """Factory function to get cloud storage client"""
    if provider == CloudProvider.GOOGLE_DRIVE:
        return GoogleDriveClient(credentials)
    elif provider == CloudProvider.DROPBOX:
        return DropboxClient(credentials)
    else:
        raise ValueError(f"Unsupported provider: {provider}")
