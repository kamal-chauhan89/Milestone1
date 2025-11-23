"""
Fix .env file encoding issues
"""

import os

def fix_env_file():
    """Fix .env file encoding"""
    env_file = '.env'
    
    if not os.path.exists(env_file):
        print(f"{env_file} does not exist. Creating it...")
        api_key = input("Enter your Google Gemini API key: ").strip()
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(f"GOOGLE_GEMINI_API_KEY={api_key}\n")
        print(f"Created {env_file} with UTF-8 encoding")
        return
    
    # Try to read and rewrite with proper encoding
    try:
        # Try different encodings
        content = None
        for encoding in ['utf-8', 'utf-8-sig', 'latin-1']:
            try:
                with open(env_file, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"Successfully read {env_file} with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        
        if content:
            # Extract API key
            api_key = None
            for line in content.split('\n'):
                if 'GOOGLE_GEMINI_API_KEY' in line:
                    api_key = line.split('=', 1)[1].strip()
                    break
            
            if api_key:
                # Rewrite with UTF-8 encoding
                with open(env_file, 'w', encoding='utf-8') as f:
                    f.write(f"GOOGLE_GEMINI_API_KEY={api_key}\n")
                print(f"Fixed {env_file} encoding to UTF-8")
            else:
                print("Could not find API key in .env file")
        else:
            print(f"Could not read {env_file} with any encoding")
            
    except Exception as e:
        print(f"Error fixing {env_file}: {e}")

if __name__ == "__main__":
    fix_env_file()

