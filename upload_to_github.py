import os
import time
from datetime import datetime
from pathlib import Path
from shutil import copy2
import subprocess

# POSTAVKE
SOURCE_DIR = Path(r"C:\MuraDrava_PrognostickiModel\MuraDravaFFS\Reports\images")
TARGET_DIR = Path("reports")
TRIGGER_FILE = Path(r"C:\MuraDrava_PrognostickiModel\MuraDravaFFS\Trigger.txt")


def cleanup_git_locks():
    git_dir = Path.cwd() / ".git"
    if not git_dir.exists():
        return
    for lock_name in ["index.lock", "HEAD.lock", "config.lock",
                      "refs/heads/main.lock", "refs/heads/master.lock"]:
        lock_file = git_dir / lock_name
        if lock_file.exists():
            try: lock_file.unlink()
            except Exception: pass
    time.sleep(1)


def kill_git_processes():
    if os.name == 'nt':
        try:
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq git.exe'],
                                    capture_output=True, text=True)
            if 'git.exe' in result.stdout:
                subprocess.run(['taskkill', '/F', '/IM', 'git.exe'], capture_output=True)
                time.sleep(1)
        except Exception: pass


def check_git_config():
    """Provjeri Git konfiguraciju"""
    try:
        # Provjeri remote URL
        result = subprocess.run(["git", "remote", "-v"], 
                              capture_output=True, text=True, check=True)
        print(f"[ℹ] Git remotes:\n{result.stdout}")
        
        # Provjeri user config
        user = subprocess.run(["git", "config", "user.name"], 
                            capture_output=True, text=True)
        email = subprocess.run(["git", "config", "user.email"], 
                             capture_output=True, text=True)
        
        if user.returncode == 0 and email.returncode == 0:
            print(f"[ℹ] Git user: {user.stdout.strip()} <{email.stdout.strip()}>")
        else:
            print("[⚠] Git user/email nije konfiguriran!")
            
        return True
    except subprocess.CalledProcessError as e:
        print(f"[✗] Git config greška: {e}")
        return False


def read_trigger_config():
    config = {
        'type': 'redovni',
        'source_file': 'redovni.jpeg',
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    if not TRIGGER_FILE.exists(): return config
    try:
        with open(TRIGGER_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip().strip('"\'')
            if content.upper() == 'DAILY':
                config['type'] = 'redovni'
                config['source_file'] = 'redovni.jpeg'
            elif content.upper() == 'ALERT':
                config['type'] = 'posebni'
                config['source_file'] = 'posebni.jpeg'
    except Exception: pass
    return config


def save_specific_file(source_dir: Path, target_folder: Path, config: dict) -> Path:
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
    for attempt in range(max_retries):
        try:
            result = subprocess.run(cmd, cwd=Path.cwd(), check=True,
                                  capture_output=True, text=True, timeout=30)
            return result
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr or str(e)
            print(f"[⚠] Git komanda neuspješna (pokušaj {attempt + 1}/{max_retries})")
            print(f"[⚠] Komanda: {' '.join(cmd)}")
            print(f"[⚠] Error: {err_msg}")
            
            if ("index.lock" in err_msg or "Another git process" in err_msg) and attempt < max_retries - 1:
                print("[🔧] Čistim git lockove...")
                kill_git_processes()
                cleanup_git_locks()
                time.sleep(2)
            else:
                raise
        except subprocess.TimeoutExpired:
            print(f"[⚠] Git komanda timeout (pokušaj {attempt + 1}/{max_retries})")
            if attempt == max_retries - 1:
                raise


def detect_git_branch():
    """Automatski otkriva default granu (main/master)"""
    try:
        result = subprocess.run(["git", "branch", "-r"],
                                capture_output=True, text=True, check=True)
        branches = result.stdout.lower()
        if "origin/main" in branches: return "main"
        elif "origin/master" in branches: return "master"
        return "main"
    except Exception: return "main"


def ensure_upstream(branch):
    """Postavlja lokalnu granu da prati remote ako nije već postavljeno"""
    try:
        local = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                               capture_output=True, text=True, check=True).stdout.strip()
        upstream = subprocess.run(["git", "rev-parse", "--abbrev-ref", f"{local}@{{upstream}}"],
                                  capture_output=True, text=True)
        if upstream.returncode != 0:
            # Postavi upstream
            subprocess.run(["git", "branch", "--set-upstream-to", f"origin/{branch}", local],
                           check=True)
            print(f"[✓] Lokalna grana '{local}' povezana s 'origin/{branch}'")
    except Exception as e:
        print(f"[⚠] Ne mogu postaviti upstream: {e}")


def git_operations_with_fallback(config, saved_file, branch):
    """Git operacije s fallback opcijama"""
    git_path = f"{TARGET_DIR}/{saved_file.name}"
    
    try:
        # Pokušaj normalni pull
        print(f"[🔧] Pokušavam git pull...")
        safe_git_command(["git", "pull", "origin", branch])
        print("[✓] Git pull uspješan")
        
    except Exception as e:
        print(f"[⚠] Git pull neuspješan: {e}")
        print("[🔧] Pokušavam bez pull-a...")
        
        # Provjeri status repo-a
        try:
            status = subprocess.run(["git", "status", "--porcelain"], 
                                  capture_output=True, text=True, check=True)
            if status.stdout.strip():
                print("[ℹ] Ima lokalne promjene, nastavljam bez pull-a")
            else:
                print("[ℹ] Nema lokalne promjene")
        except Exception:
            print("[⚠] Ne mogu provjeriti git status")
    
    # Nastavi s add, commit, push
    try:
        print(f"[🔧] Dodajem datoteku: {git_path}")
        safe_git_command(["git", "add", git_path])
        
        commit_message = f"Dodani {config['type']} izvještaji za {config['date']}"
        
        # Provjeri ima li što za commit
        status = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True, check=True)
        
        if status.stdout.strip():
            print(f"[🔧] Commit: {commit_message}")
            safe_git_command(["git", "commit", "-m", commit_message])
            print("[✓] Git commit uspješan")
            
            print(f"[🔧] Push na origin/{branch}...")
            safe_git_command(["git", "push", "origin", branch])
            print("[✅] Git push uspješan!")
        else:
            print("[ℹ] Nema novih promjena za commit")
            
    except Exception as e:
        print(f"[✗] Git operacija neuspješna: {e}")
        raise


def main():
    print("="*50)
    print("🌊 MuraDrava-FFS Automatski Upload")
    print("="*50)

    kill_git_processes()
    cleanup_git_locks()

    # Postavi Git konfiguraciju
    if not setup_git_config():
        print("[✗] Git nije pravilno konfiguriran!")
        return

    config = read_trigger_config()

    if not SOURCE_DIR.exists():
        print(f"[✗] Izvorna mapa ne postoji: {SOURCE_DIR}")
        return

    try:
        print(f"[ℹ] Tražim {config['source_file']} u {SOURCE_DIR}")
        saved_file = save_specific_file(SOURCE_DIR, TARGET_DIR, config)
    except Exception as e:
        print(f"[✗] Greška pri spremanju datoteke: {e}")
        return

    branch = detect_git_branch()
    ensure_upstream(branch)

    try:
        git_operations_with_fallback(config, saved_file, branch)
    except Exception as e:
        print(f"[✗] Finalna Git greška: {e}")

    print("\n[📋] REZULTAT:")
    print(f"[📊] Tip: {config['type']}")
    print(f"[📅] Datum: {config['date']}")
    print(f"[📁] Izvorni file: {config['source_file']}")
    print(f"[📁] Novi file: {saved_file.name}")
    print("="*50)



if __name__ == "__main__":
    main()

