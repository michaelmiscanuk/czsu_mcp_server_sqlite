import os
import shutil
import zipfile
from pathlib import Path

# Get the base directory
try:
    BASE_DIR = Path(__file__).resolve().parents[0]
except NameError:
    BASE_DIR = Path(os.getcwd())

# Configuration of path to unzip
ZIP_PATH = BASE_DIR / "data" / "czsu_data.zip"


def safe_remove_directory(target_path: Path):
    """Safely remove directory, handling Windows permissions."""
    if not target_path.exists():
        return

    print(f"Removing existing: {target_path}")
    try:
        if target_path.is_dir():
            shutil.rmtree(target_path)
        else:
            target_path.unlink()
    except PermissionError:
        # Force remove on Windows
        if os.name == "nt":
            os.system(f'rmdir /s /q "{target_path}"')
        else:
            raise


def unzip_czsu_data():
    """Unzip the CZSU data file."""
    zip_path = ZIP_PATH

    if not zip_path.exists():
        print(f"Warning: Zip file does not exist: {zip_path}")
        return

    if not zip_path.suffix == ".zip":
        print(f"Warning: Not a zip file: {zip_path}")
        return

    target_path = zip_path.with_suffix("")
    print(f"Unzipping: {zip_path}")
    print(f"Output: {target_path}")

    # Remove existing target
    safe_remove_directory(target_path)

    try:
        # Extract zip file
        with zipfile.ZipFile(zip_path, "r") as zipf:
            zipf.extractall(target_path.parent)
        print(f"Successfully unzipped: {zip_path}")
    except (zipfile.BadZipFile, zipfile.LargeZipFile, OSError) as e:
        print(f"Error extracting {zip_path}: {e}")


def main():
    print(f"Base directory: {BASE_DIR}")
    print("\nStarting unzip process...")
    print("=" * 60)
    unzip_czsu_data()
    print("=" * 60)
    print("Unzip process completed!")


if __name__ == "__main__":
    main()
