import os
from datetime import datetime
from pathlib import Path
from shutil import copy2
import subprocess
import glob

# Postavke
SOURCE_DIR = Path(r"C:\MuraDrava_PrognostickiModel\MuraDravaFFS\Reports\images")
TARGET_DIR = Path("reports")  # Relativna putanja unutar tvog git repozitorija

def save_with_timestamp(file_path: Path, target_folder: Path) -> Path:
    os.makedirs(target_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
    target_path = target_folder / new_name

    copy2(file_path, target_path)
    print(f"[✓] Spremljeno: {target_path}")
    return target_path

def git_commit_and_push(files: list[Path], commit_message="Automatski commit izvještaja"):
    try:
        for file in files:
            subprocess.run(["git", "add", str(file)], cwd=Path.cwd(), check=True)

        subprocess.run(["git", "commit", "-m", commit_message], cwd=Path.cwd(), check=True)
        subprocess.run(["git", "push"], cwd=Path.cwd(), check=True)
        print("[✓] Git push uspješan.")
    except subprocess.CalledProcessError as e:
        print(f"[✗] Git greška: {e}")

def main():
    if not SOURCE_DIR.exists():
        print(f"[✗] Izvorna mapa ne postoji: {SOURCE_DIR}")
        return

    extensions = ("*.jpg", "*.jpeg", "*.png")
    image_files = []
    for ext in extensions:
        image_files.extend(SOURCE_DIR.glob(ext))

    if not image_files:
        print("[ℹ️] Nema slika za obradu.")
        return

    saved_files = []
    for image in image_files:
        saved = save_with_timestamp(image, TARGET_DIR)
        saved_files.append(saved)

    if saved_files:
        git_commit_and_push(saved_files, commit_message="Dodani izvještaji s datumom")



if __name__ == "__main__":
    main()

