bok već neko vrime  radimo na ovom automatskom uploadu to github...pošaljem ti kod i error pa mi pliz pomozi

Bok! Naravno, rado ću pomoći s automatskim upload-om na GitHub. Pošalji mi kod i error poruku pa ću pogledati što se događa i pokušat riješiti problem.

Samo naprijed s kodom i detaljima o grešci! 👍


import os import time from datetime import datetime from pathlib import Path from shutil import copy2 import subprocess # POSTAVKE SOURCE_DIR = Path(r"C:\MuraDrava_PrognostickiModel\MuraDravaFFS\Reports\images") TARGET_DIR = Path("reports") TRIGGER_FILE = Path(r"C:\MuraDrava_PrognostickiM

pasted

Vidim kod za automatski upload na GitHub! Izgleda prilično dobro strukturiran. Da bih ti mogao pomoći, trebam vidjeti error poruku koju dobivaš.

Možeš li mi poslati:

Exact error message koji se pojavljuje
U kojem koraku se greška događa (kopiranje datoteke, git operacije, push, itd.)
Sadržaj Trigger.txt datoteke (ako postoji)
Također, par brzih pitanja:

Je li GitHub repo već postavljen i imaš li git credentials konfigurirane?
Postoji li .git folder u direktoriju gdje pokrećeš skriptu?
Kada pokrećeš skriptu, što točno ispisuje prije greške?
Pošalji mi te detalje pa ću ti brzo pomoći riješiti problem! 🔧

🌊 MuraDrava-FFS Automatski Upload
==================================================
[ℹ] Tražim redovni.jpeg u C:\MuraDrava_PrognostickiModel\MuraDravaFFS\Reports\images
[✓] Spremljeno: redovni.jpeg → 2025-09-1013redovni.jpeg
[🔧] Git operacije... (branch: main)
[✗] Git greška: Command '['git', 'pull', 'origin', 'main']' returned non-zero exit status 2.
[📋] REZULTAT:
[📊] Tip: redovni
[📅] Datum: 2025-09-10
[📁] Izvorni file: redovni.jpeg
[📁] Novi file: 2025-09-1013redovni.jpeg
==================================================
Press any key to continue . . .

Vidim problem! Git pull komanda vraća error kod 2. Ovo je najčešće zbog problema s autentifikacijom ili konfigracijom remote repository-ja.

Evo poboljšane verzije koda s boljim error handling-om:

Poboljšana skripta s detaljnijim error handling
Code 
Također, možeš pokušati i ove brze provjere:

1. Provjeri Git credentials:

bash
git config --list
git remote -v
2. Ručno testiraj git pull:

bash
cd C:\put\do\tvog\repo
git pull origin main
3. Možda treba Personal Access Token: Ako koristiš GitHub, možda trebaš postaviti Personal Access Token umjesto password-a.

4. Alternativno rješenje - preskoči pull: Ako pull stalno pada, možeš modificirati kod da preskoče pull i ide direktno na push. To funkcionira ako nema konflikata.

Pokreni novu verziju i reci mi što ispisuje! Trebao bi dati puno detaljnije informacije o tome što se događa s git operacijama.


==================================================
🌊 MuraDrava-FFS Automatski Upload
==================================================
[ℹ] Git remotes:
origin  https://github.com/MuraDrava/Report (fetch)
origin  https://github.com/MuraDrava/Report (push)
[⚠] Git user/email nije konfiguriran!
[ℹ] Tražim redovni.jpeg u C:\MuraDrava_PrognostickiModel\MuraDravaFFS\Reports\images
[✓] Spremljeno: redovni.jpeg → 2025-09-1013redovni.jpeg
[🔧] Pokušavam git pull...
[⚠] Git komanda neuspješna (pokušaj 1/3)
[⚠] Komanda: git pull origin main
[⚠] Error: From https://github.com/MuraDrava/Report
 * branch            main       -> FETCH_HEAD
   eeb3e39..d39e25f  main       -> origin/main
error: Your local changes to the following files would be overwritten by merge:
        upload_to_github.py
Please commit your changes or stash them before you merge.
Aborting
Merge with strategy ort failed.
[⚠] Git pull neuspješan: Command '['git', 'pull', 'origin', 'main']' returned non-zero exit status 2.
[🔧] Pokušavam bez pull-a...
[ℹ] Ima lokalne promjene, nastavljam bez pull-a
[🔧] Dodajem datoteku: reports/2025-09-1013redovni.jpeg
[🔧] Commit: Dodani redovni izvještaji za 2025-09-10
[✓] Git commit uspješan
[🔧] Push na origin/main...
[⚠] Git komanda neuspješna (pokušaj 1/3)
[⚠] Komanda: git push origin main
[⚠] Error: To https://github.com/MuraDrava/Report
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/MuraDrava/Report'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
[✗] Git operacija neuspješna: Command '['git', 'push', 'origin', 'main']' returned non-zero exit status 1.
[✗] Finalna Git greška: Command '['git', 'push', 'origin', 'main']' returned non-zero exit status 1.
[📋] REZULTAT:
[📊] Tip: redovni
[📅] Datum: 2025-09-10
[📁] Izvorni file: redovni.jpeg
[📁] Novi file: 2025-09-1013redovni.jpeg
==================================================

Odlično! Sad vidim što se događa. Imaš dva glavna problema:

Git user/email nije konfiguriran
Lokalne promjene u upload_to_github.py sprečavaju merge
Repository je "behind" remote-a
Evo rješenja:

Poboljšana skripta s detaljnijim error handling
Code 
Poboljšana skripta s detaljnijim error handling
Code 
Poboljšana skripta s detaljnijim error handling
Code ∙ Version 2 
ALTERNATIVNO BRŽE RJEŠENJE:

Možeš i ručno riješiti ovaj problem s ovim komandama:

bash
# Idi u direktorij s repom
cd C:\path\to\your\repo

# Postavi git user/email
git config user.name "MuraDrava-AutoUpload"
git config user.email "mura.drava.auto@example.com"

# Stash trenutne promjene
git stash

# Pull najnovije promjene
git pull origin main

# Pokreni skriptu ponovo
Nova verzija koda će:

Automatski postaviti Git user/email
Riješiti konflikte pomoću stash-a
Pokušati pull s rebase prije push-a
Imati retry logiku za push operacije
Probaj novu verziju i reci mi kako ide! 🚀


==================================================
🌊 MuraDrava-FFS Automatski Upload
==================================================
Traceback (most recent call last):
  File "C:\MuraDrava_PrognostickiModel\StreamlitApp_MuraDravaFFS\Report\upload_to_github.py", line 245, in <module>
    main()
  File "C:\MuraDrava_PrognostickiModel\StreamlitApp_MuraDravaFFS\Report\upload_to_github.py", line 210, in main
    if not setup_git_config():
           ^^^^^^^^^^^^^^^^
NameError: name 'setup_git_config' is not defined. Did you mean: 'check_git_config'?
Press any key to continue . . .

Ups! Vidim da update nije prošao kako treba. Evo kompletne ispravne verzije koda:

Poboljšana skripta s detaljnijim error handling
Code ∙ Version 3 
Sada je kod potpun i trebao bi raditi! Nova verzija će:

✅ Automatski postaviti Git user/email
✅ Riješiti konflikte pomoću git stash
✅ Pokušati različite strategije za pull/push
✅ Imati retry logiku
Probaj ponovo i reci mi kako ide! 🚀

Ako još uvijek imaš problema, možeš i ručno riješiti prije pokretanja:

bash
git config user.name "MuraDrava-AutoUpload"
git config user.email "mura.drava.auto@example.com"
git stash



5-hour limit reached ∙ resets 6:00 PM
Upgrade


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


def setup_git_config():
    """Postavi Git konfiguraciju ako nije postavljena"""
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
            print("[🔧] Postavljam Git user/email...")
            subprocess.run(["git", "config", "user.name", "MuraDrava-AutoUpload"], check=True)
            subprocess.run(["git", "config", "user.email", "mura.drava.auto@example.com"], check=True)
            print("[✓] Git user/email postavljen")
            
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


def resolve_git_conflicts():
    """Riješi Git konflikte stash-om"""
    try:
        print("[🔧] Riješavam Git konflikte...")
        # Stash lokalne promjene
        safe_git_command(["git", "stash", "push", "-m", "Auto-stash before sync"])
        print("[✓] Lokalne promjene stash-ane")
        return True
    except Exception as e:
        print(f"[⚠] Ne mogu stash-ati promjene: {e}")
        return False


def git_operations_with_fallback(config, saved_file, branch):
    """Git operacije s rješavanjem konflikata"""
    git_path = f"{TARGET_DIR}/{saved_file.name}"
    
    # Prvo pokušaj riješiti postojeće konflikte
    try:
        print(f"[🔧] Sinkronizacija s remote repository...")
        safe_git_command(["git", "pull", "origin", branch])
        print("[✓] Git pull uspješan")
        
    except Exception as e:
        print(f"[⚠] Git pull neuspješan, riješavam konflikte...")
        
        # Pokušaj stash i pull
        if resolve_git_conflicts():
            try:
                safe_git_command(["git", "pull", "origin", branch])
                print("[✓] Git pull uspješan nakon stash")
            except Exception:
                print("[⚠] Pull i dalje neuspješan, nastavljam bez sinkronizacije")
        else:
            # Ako stash ne radi, resetiraj samo ovu datoteku
            try:
                print("[🔧] Pokušavam reset problematične datoteke...")
                safe_git_command(["git", "checkout", "HEAD", "--", "upload_to_github.py"])
                safe_git_command(["git", "pull", "origin", branch])
                print("[✓] Git pull uspješan nakon reset")
            except Exception:
                print("[⚠] Nastavljam bez pull-a")
    
    # Dodaj novu datoteku
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
            
            # Push s retry logikom
            max_push_retries = 3
            for attempt in range(max_push_retries):
                try:
                    print(f"[🔧] Push na origin/{branch} (pokušaj {attempt + 1}/{max_push_retries})...")
                    safe_git_command(["git", "push", "origin", branch])
                    print("[✅] Git push uspješan!")
                    return
                except Exception as push_error:
                    if attempt < max_push_retries - 1:
                        print(f"[⚠] Push neuspješan, pokušavam pull i retry...")
                        try:
                            # Pokušaj pull prije sljedećeg push-a
                            safe_git_command(["git", "pull", "origin", branch, "--rebase"])
                            continue
                        except Exception:
                            print("[⚠] Rebase pull neuspješan")
                            time.sleep(2)
                    else:
                        raise push_error
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


