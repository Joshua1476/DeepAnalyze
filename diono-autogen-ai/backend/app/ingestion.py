"""
Document and data ingestion module
"""
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import pandas as pd
from loguru import logger
from .media_processor import media_processor


class DocumentIngestion:
    """Handle document and data file ingestion"""
    
    def __init__(self):
        self.supported_formats = {
            'text': ['.txt', '.md', '.rst', '.log'],
            'code': ['.py', '.js', '.java', '.go', '.rs', '.cpp', '.c', '.h'],
            'data': ['.csv', '.json', '.xlsx', '.xls', '.parquet'],
            'config': ['.yaml', '.yml', '.toml', '.ini', '.conf'],
            'document': ['.pdf', '.docx', '.doc'],
            'image': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', '.svg'],
            'video': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
        }
    
    def get_file_type(self, file_path: Path) -> str:
        """Determine file type"""
        ext = file_path.suffix.lower()
        for file_type, extensions in self.supported_formats.items():
            if ext in extensions:
                return file_type
        return 'unknown'
    
    def read_text_file(self, file_path: Path) -> str:
        """Read text-based file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
    
    def read_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Read JSON file"""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def read_csv_file(self, file_path: Path) -> pd.DataFrame:
        """Read CSV file"""
        return pd.read_csv(file_path)
    
    def read_excel_file(self, file_path: Path) -> Dict[str, pd.DataFrame]:
        """Read Excel file (all sheets)"""
        return pd.read_excel(file_path, sheet_name=None)
    
    def ingest_file(self, file_path: Path) -> Dict[str, Any]:
        """Ingest a file and return structured data"""
        file_type = self.get_file_type(file_path)
        
        result = {
            'file_name': file_path.name,
            'file_path': str(file_path),
            'file_type': file_type,
            'size_bytes': file_path.stat().st_size,
            'content': None,
            'metadata': {}
        }
        
        try:
            if file_type in ['text', 'code', 'config']:
                result['content'] = self.read_text_file(file_path)
            
            elif file_type in ['image', 'video']:
                # Process media files
                media_result = media_processor.process_media(file_path)
                if media_result['success']:
                    result['content'] = media_result['transcript']
                    result['metadata']['media_type'] = media_result['file_type']
                else:
                    result['error'] = media_result['error']
                    result['success'] = False
                    return result
            
            elif file_type == 'data':
                ext = file_path.suffix.lower()
                if ext == '.json':
                    result['content'] = self.read_json_file(file_path)
                elif ext == '.csv':
                    df = self.read_csv_file(file_path)
                    result['content'] = df.to_dict('records')
                    result['metadata']['shape'] = df.shape
                    result['metadata']['columns'] = list(df.columns)
                elif ext in ['.xlsx', '.xls']:
                    sheets = self.read_excel_file(file_path)
                    result['content'] = {
                        name: df.to_dict('records')
                        for name, df in sheets.items()
                    }
                    result['metadata']['sheets'] = list(sheets.keys())
            
            result['success'] = True
        
        except Exception as e:
            logger.error(f"Failed to ingest {file_path}: {e}")
            result['success'] = False
            result['error'] = str(e)
        
        return result
    
    def ingest_directory(self, directory: Path, recursive: bool = True) -> List[Dict[str, Any]]:
        """Ingest all files in a directory"""
        results = []
        
        if recursive:
            files = directory.rglob('*')
        else:
            files = directory.glob('*')
        
        for file_path in files:
            if file_path.is_file():
                result = self.ingest_file(file_path)
                results.append(result)
        
        return results
    
    def summarize_data(self, file_path: Path) -> str:
        """Generate a summary of data file"""
        file_type = self.get_file_type(file_path)
        
        if file_type != 'data':
            return f"File: {file_path.name} (not a data file)"
        
        try:
            ext = file_path.suffix.lower()
            
            if ext == '.csv':
                df = self.read_csv_file(file_path)
                summary = f"""File: {file_path.name}
Type: CSV
Shape: {df.shape[0]} rows × {df.shape[1]} columns
Columns: {', '.join(df.columns)}
Memory: {df.memory_usage(deep=True).sum() / 1024:.2f} KB

Sample data:
{df.head(3).to_string()}

Data types:
{df.dtypes.to_string()}
"""
                return summary
            
            elif ext == '.json':
                data = self.read_json_file(file_path)
                summary = f"""File: {file_path.name}
Type: JSON
Structure: {type(data).__name__}
Size: {file_path.stat().st_size / 1024:.2f} KB
"""
                if isinstance(data, list):
                    summary += f"Items: {len(data)}\n"
                elif isinstance(data, dict):
                    summary += f"Keys: {', '.join(list(data.keys())[:10])}\n"
                
                return summary
        
        except Exception as e:
            return f"Error summarizing {file_path.name}: {str(e)}"
        
        return f"File: {file_path.name}"


# Global ingestion instance
ingestion = DocumentIngestion()
