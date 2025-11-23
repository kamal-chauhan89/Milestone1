"""
URL Loader - Reads mutual fund URLs from file
"""

from typing import List
from pathlib import Path


class URLLoader:
    """Load URLs from text file"""
    
    def __init__(self, file_path: str = "Groww links for mutual funds.txt"):
        self.file_path = file_path
    
    def load_urls(self) -> List[str]:
        """
        Load URLs from file, one URL per line
        Returns list of valid URLs
        """
        urls = []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    url = line.strip()
                    
                    # Only add valid URLs
                    if url and url.startswith('http'):
                        urls.append(url)
            
            print(f"✅ Loaded {len(urls)} URLs from {self.file_path}")
            return urls
            
        except FileNotFoundError:
            print(f"❌ Error: {self.file_path} not found!")
            return []
        except Exception as e:
            print(f"❌ Error loading URLs: {e}")
            return []
    
    def validate_urls(self, urls: List[str]) -> List[str]:
        """Validate URLs are from Groww domain"""
        valid_urls = []
        
        for url in urls:
            if 'groww.in/mutual-funds' in url:
                valid_urls.append(url)
            else:
                print(f"⚠ Skipping invalid URL: {url}")
        
        return valid_urls


if __name__ == "__main__":
    loader = URLLoader()
    urls = loader.load_urls()
    valid_urls = loader.validate_urls(urls)
    
    print(f"\n{'='*60}")
    print(f"Total URLs loaded: {len(urls)}")
    print(f"Valid Groww URLs: {len(valid_urls)}")
    print(f"{'='*60}")
    
    # Show first 5 URLs
    print("\nFirst 5 URLs:")
    for i, url in enumerate(valid_urls[:5], 1):
        print(f"{i}. {url}")
