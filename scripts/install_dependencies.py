import subprocess
import sys

def install_dependencies():
    """Install all required dependencies."""
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-e", ".[dev]"
        ])
        
        subprocess.check_call([
            sys.executable, "-m", "spacy", "download", "en_core_web_sm"
        ])
        
        print("All dependencies installed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    install_dependencies()