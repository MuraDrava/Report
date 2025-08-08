import sys
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

# 📌 Mapiranje triggera na fajl
TRIGGER_MAP = {
    "DAILY": "redovni.jpeg",
    "ALERT": "posebni.jpeg"
}


def copy_and_rename_file(trigger):
    """Kopira i preimenuje fajl s datumom i vremenom."""
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = TRIGGER_MAP.get(trigger.upper())

    if not filename:
        print(f"[✗] Nepoznat trigger: {trigger}")
        return None

    src_path = SOURCE_DIR / filename
    if src_path.exists():
        new_name = f"{src_path.stem}_{now_str}{src_path.suffix}"
        dest_path = DEST_DIR / new_name
        shutil.copy2(src_path, dest_path)
        print(f"[✓] Spremljeno: {filename} → {new_name}")
        return dest_path
    else:
        print(f"[!] Fajl nije pronađen: {filename}")
        return None


def run_git_command(cmd):
    subprocess.run(cmd, cwd=GIT_REPO_PATH, check=True)


def git_commit_and_push(file, commit_message):
    try:
        # Stash ako ima promjena
        run_git_command(["git", "stash", "--include-untracked"])
        run_git_command(["git", "pull", "--no-edit", "origin", "main"])
        run_git_command(["git", "stash", "pop"])

        # Commit i push
        run_git_command(["git", "add", str(file.relative_to(GIT_REPO_PATH))])
        run_git_command(["git", "commit", "-m", commit_message])
        run_git_command(["git", "push", "origin", "main"])

        print("[✅] Uspješno uploadano na GitHub!")

        # URL prikaz
        github_url = f"https://github.com/MuraDrava/Report/blob/main/{file.relative_to(GIT_REPO_PATH).as_posix()}"
        print(f"[🌐] Link na GitHub: {github_url}")

    except subprocess.CalledProcessError as e:
        print(f"[✗] Git greška: {e}")


def main():
    if len(sys.argv) < 2:
        print("[✗] Nisi naveo trigger! Koristi: DAILY ili ALERT")
        return

    trigger = sys.argv[1]
    saved_file = copy_and_rename_file(trigger)
    if saved_file:
        git_commit_and_push(saved_file, f"Dodan {trigger} izvještaj s datumom")


if __name__ == "__main__":
    main()

