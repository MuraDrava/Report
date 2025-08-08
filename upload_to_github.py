import shutil
from pathlib import Path
from datetime import datetime
import subprocess

# 📌 LOKALNI PATH do GitHub repozitorija
GIT_REPO_PATH = Path(r"C:\MuraDrava_PrognostickiModel\StreamlitApp_MuraDravaFFS\Report")

# 📌 Izvorni folder sa slikama
SOURCE_DIR = Path(r"C:\MuraDrava_PrognostickiModel\MuraDravaFFS\Reports\images")

# 📌 Odredište unutar repozitorija
DEST_DIR = GIT_REPO_PATH / "reports"
DEST_DIR.mkdir(parents=True, exist_ok=True)

# 📌 Imena fajlova koje tražimo
TARGET_FILES = ["redovni.jpeg", "posebni.jpeg", "redovni_IGOR.jpeg"]


def copy_and_rename_files():
    """Kopira i preimenuje fajlove s datumom i vremenom."""
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_files = []

    for filename in TARGET_FILES:
        src_path = SOURCE_DIR / filename
        if src_path.exists():
            new_name = f"{src_path.stem}_{now_str}{src_path.suffix}"
            dest_path = DEST_DIR / new_name
            shutil.copy2(src_path, dest_path)
            saved_files.append(dest_path)
            print(f"[✓] Spremljeno: {filename} → {new_name}")
        else:
            print(f"[!] Fajl nije pronađen: {filename}")

    return saved_files


def run_git_command(cmd):
    """Pokreće git naredbu u repozitoriju."""
    subprocess.run(cmd, cwd=GIT_REPO_PATH, check=True)


def git_commit_and_push(files, commit_message):
    """Dodaje, commita i push-a promjene."""
    try:
        # Spremi lokalne izmjene prije povlačenja
        run_git_command(["git", "stash", "--include-untracked"])

        # Povuci zadnje promjene
        run_git_command(["git", "pull", "--no-edit", "origin", "main"])

        # Vrati lokalne izmjene
        run_git_command(["git", "stash", "pop"])

        # Dodaj nove fajlove
        for file in files:
            run_git_command(["git", "add", str(file.relative_to(GIT_REPO_PATH))])

        # Commit
        run_git_command(["git", "commit", "-m", commit_message])

        # Push
        run_git_command(["git", "push", "origin", "main"])

        print("[✅] Uspješno uploadano na GitHub!")

    except subprocess.CalledProcessError as e:
        print(f"[✗] Git greška: {e}")


def main():
    saved_files = copy_and_rename_files()
    if saved_files:
        git_commit_and_push(saved_files, commit_message="Dodani izvještaji s datumom")


if __name__ == "__main__":
    main()
