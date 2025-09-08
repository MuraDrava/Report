import os
import time
from datetime import datetime
from pathlib import Path
from shutil import copy2
import subprocess

# Postavke
SOURCE_DIR = Path(r"C:\MuraDrava_PrognostickiModel\MuraDravaFFS\Reports\images")
TARGET_DIR = Path("reports")  # Relativna putanja unutar git repozitorija
TRIGGER_FILE = Path(r"C:\MuraDrava_PrognostickiModel\MuraDravaFFS\Trigger.txt")  # Putanja do trigger datoteke
BRANCH = "main"  # promijeni u "master" ako repo koristi master granu


def cleanup_git_locks():
    """Uklanjanje Git lock datoteka"""
    git_dir = Path.cwd() / ".git"
    if not git_dir.exists():
        return

    lock_files = [
        "index.lock", "HEAD.lock", "config.lock",
        "refs/heads/main.lock", "refs/heads/master.lock"
    ]

    for lock_name in lock_files:
        lock_file = git_dir / lock_name
        if lock_file.exists():
            try:
                lock_file.unlink()
                print(f"[✓] Uklonjen lock: {lock_name}")
            except Exception:
                pass
    time.sleep(1)


def kill_git_processes():
    """Završi sve Git procese (Windows only)"""
    if os.name == 'nt':
        try:
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq git.exe'],
                                    capture_output=True, text=True)
            if 'git.exe' in result.stdout:
                subprocess.run(['taskkill', '/F', '/IM', 'git.exe'], capture_output=True)
                print("[✓] Git procesi završeni")
                time.sleep(1)
        except Exception:
            pass


def read_trigger_config():
    """Čita Trigger.txt datoteku"""
    config = {
        'type': 'redovni',
        'source_file': 'redovni.jpeg',
        'date': datetime.now().strftime('%Y-%m-%d')
    }

    if not TRIGGER_FILE.exists():
        return config

    try:
        with open(TRIGGER_FILE, 'r', encoding='utf-8') as file:
            content = file.read().strip().strip('"\'')
            if content.upper() == 'DAILY':
                config['type'] = 'redovni'
                config['source_file'] = 'redovni.jpeg'
            elif content.upper() == 'ALERT':
                config['type'] = 'posebni'
                config['source_file'] = 'posebni.jpeg'
    except Exception:
        pass

    return config


def save_specific_file(source_dir: Path, target_folder: Path, config: dict) -> Path:
    """Kopira odabranu datoteku s novim nazivom"""
    os.makedirs(target_folder, exist_ok=True)
    source_file = source_dir / config['source_file']

    if not source_file.exists():
        raise FileNotFoundError(f"Datoteka ne postoji: {source_file}")

    timestamp = datetime.now().strftime("%H")
    new_name = f"{config['date']}{timestamp}{config['type']}.jpeg"
    target_path = target_folder / new_name

    copy2(source_file, target_path)
    print(f"[✓] Spremljeno: {source_file.name} → {target_path.name}")
    return target_path


def safe_git_command(cmd, max_retries=3):
    """Izvršava Git komandu s retry logikom"""
    for attempt in range(max_retries):
        try:
            result = subprocess.run(cmd, cwd=Path.cwd(), check=True,
                                    capture_output=True, text=True, timeout=30)
            return result
        except subprocess.CalledProcessError as e:
            err = e.stderr or str(e)
            if ("index.lock" in err or "Another git process" in err) and attempt < max_retries - 1:
                kill_git_processes()
                cleanup_git_locks()
                time.sleep(2)
            else:
                raise
        except subprocess.TimeoutExpired:
            if attempt == max_retries - 1:
                raise


def main():
    print("=" * 50)
    print("🌊 MuraDrava-FFS Automatski Upload")
    print("=" * 50)

    # Očisti stanje
    kill_git_processes()
    cleanup_git_locks()

    # Učitaj trigger
    config = read_trigger_config()

    # Provjeri izvorni folder
    if not SOURCE_DIR.exists():
        print(f"[✗] Izvorna mapa ne postoji: {SOURCE_DIR}")
        return

    # Kopiraj datoteku
    try:
        print(f"[ℹ] Tražim {config['source_file']} u {SOURCE_DIR}")
        saved_file = save_specific_file(SOURCE_DIR, TARGET_DIR, config)
    except Exception as e:
        print(f"[✗] Greška: {e}")
        return

    # Git dio
    try:
        print("[🔧] Git operacije...")
        safe_git_command(["git", "pull", "origin", BRANCH])
        git_path = f"{TARGET_DIR}/{saved_file.name}"
        safe_git_command(["git", "add", git_path])
        commit_message = f"Dodani {config['type']} izvještaji za {config['date']}"
        # commit samo ako ima promjena
        status = subprocess.run(["git", "status", "--porcelain"],
                                capture_output=True, text=True)
        if status.stdout.strip():
            safe_git_command(["git", "commit", "-m", commit_message])
        else:
            print("[ℹ] Nema novih promjena za commit")
        safe_git_command(["git", "push", "origin", BRANCH])
        print(f"[✅] Git push uspješan")
    except Exception as e:
        print(f"[✗] Git greška: {e}")

    # Rezultat
    print("\n[📋] REZULTAT:")
    print(f"[📊] Tip: {config['type']}")
    print(f"[📅] Datum: {config['date']}")
    print(f"[📁] Izvorni file: {config['source_file']}")
    print(f"[📁] Novi file: {saved_file.name}")
    print("=" * 50)

if __name__ == "__main__":
    main()
