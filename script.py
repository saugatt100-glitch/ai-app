# Create complete AI SaaS platform project folder structure
import os
import shutil

# Create main project directory
project_name = "ai-saas-platform"
if os.path.exists(project_name):
    shutil.rmtree(project_name)
os.makedirs(project_name)

# Create all subdirectories
directories = [
    "components",
    "pages/api/auth",
    "pages/api/ai", 
    "pages/api/admin",
    "pages/auth",
    "pages/dashboard",
    "pages/admin",
    "lib",
    "types",
    "styles",
    "public",
    "database",
    "docs"
]

for directory in directories:
    os.makedirs(os.path.join(project_name, directory), exist_ok=True)

print(f"✅ Created project folder: {project_name}")
print("📁 Directory structure:")
for directory in directories:
    print(f"   ├── {directory}/")