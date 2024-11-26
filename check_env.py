import sys
import os

def check_environment():
    """Check if running in correct virtual environment"""
    # Get the virtual environment path
    venv_path = os.environ.get('VIRTUAL_ENV')
    
    print("\n=== Environment Check ===")
    
    # Check if running in a virtual environment
    if venv_path:
        print(f"✅ Virtual environment active: {venv_path}")
    else:
        print("❌ Not running in a virtual environment!")
        print("Run: .\\venv\\Scripts\\activate")
        return False
    
    # Check Python location
    print(f"\nPython executable: {sys.executable}")
    
    # Check installed packages
    import pkg_resources
    print("\nInstalled packages:")
    for pkg in pkg_resources.working_set:
        print(f"  - {pkg.key} (Version: {pkg.version})")
    
    return True

if __name__ == "__main__":
    check_environment()