import os
import subprocess
import json
from pathlib import Path

class ProjectManager:
    def __init__(self, base_dir="C:/Projects"):
        self.base_dir = Path(base_dir)
        self.projects_file = self.base_dir / "projects.json"
        self.load_projects()

    def load_projects(self):
        """Load existing projects from JSON file"""
        if self.projects_file.exists():
            with open(self.projects_file) as f:
                self.projects = json.load(f)
        else:
            self.projects = {}

    def save_projects(self):
        """Save projects to JSON file"""
        with open(self.projects_file, 'w') as f:
            json.dump(self.projects, f, indent=4)

    def create_project(self, name, python_packages=None):
        """Create a new project with virtual environment"""
        project_dir = self.base_dir / name
        
        # Create project directory
        project_dir.mkdir(exist_ok=True)
        
        print(f"Creating project: {name}")
        print("Setting up virtual environment...")
        
        # Create virtual environment
        subprocess.run(["python", "-m", "venv", str(project_dir / "venv")])
        
        # Create VS Code settings
        vscode_dir = project_dir / ".vscode"
        vscode_dir.mkdir(exist_ok=True)
        
        settings = {
            "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
            "python.terminal.activateEnvironment": True
        }
        
        with open(vscode_dir / "settings.json", 'w') as f:
            json.dump(settings, f, indent=4)
        
        # Install packages if specified
        if python_packages:
            print("Installing packages...")
            packages = " ".join(python_packages)
            subprocess.run(f"{project_dir}\\venv\\Scripts\\pip install {packages}", shell=True)
        
        # Save project info
        self.projects[name] = {
            "path": str(project_dir),
            "packages": python_packages or []
        }
        self.save_projects()
        
        print(f"\nProject {name} created successfully!")
        print(f"To open in VS Code: code {project_dir}")

    def list_projects(self):
        """List all projects"""
        print("\nExisting Projects:")
        for name, info in self.projects.items():
            print(f"\n{name}:")
            print(f"  Path: {info['path']}")
            print(f"  Packages: {', '.join(info['packages'])}")

if __name__ == "__main__":
    manager = ProjectManager()
    
    # Example: Create new project
    manager.create_project(
        "pumpjack_project", 
        python_packages=["asyncua", "pandas"]
    )
    
    # List all projects
    manager.list_projects()