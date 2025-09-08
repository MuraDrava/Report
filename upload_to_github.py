import os
import time
from datetime import datetime
from pathlib import Path
from shutil import copy2
import subprocess
import glob

# Postavke
SOURCE_DIR = Path(r"C:\MuraDrava_PrognostickiModel\MuraDravaFFS\Reports\images")
TARGET_DIR = Path("reports")  # Relativna putanja unutar tvog git repozitorija
TRIGGER_FILE = Path(r"C:\MuraDrava_PrognostickiModel\MuraDravaFFS\Trigger.txt")  # Putanja do trigger datoteke

def cleanup_git_locks():
    """Agresivno uklanjanje Git lock datoteka"""
    git_dir = Path.cwd() / ".git"
    
    if not git_dir.exists():
        print(f"[⚠] Git direktorij ne postoji: {git_dir}")
        return
    
    lock_files = [
        "index.lock",
        "HEAD.lock", 
        "config.lock",
        "refs/heads/main.lock",
        "refs/heads/master.lock"
    ]
    
    print("[🔧] Čišćenje Git lock datoteka...")
    cleaned = False
    
    for lock_name in lock_files:
        lock_file = git_dir / lock_name
        if lock_file.exists():
            try:
                lock_file.unlink()
                print(f"[✓] Uklonjen: {lock_name}")
                cleaned = True
            except Exception as e:
                print(f"[⚠] Ne mogu ukloniti {lock_name}: {e}")
                # Pokušaj s sistemskom komandom
                try:
                    if os.name == 'nt':  # Windows
                        os.system(f'del /f /q "{lock_file}" 2>nul')
                    else:  # Linux/Mac
                        os.system(f'rm -f "{lock_file}" 2>/dev/null')
                    if not lock_file.exists():
                        print(f"[✓] Uklonjen sistemskom komandom: {lock_name}")
                        cleaned = True
                except:
                    pass
    
    if cleaned:
        print("[ℹ] Čekam 3 sekunde nakon čišćenja...")
        time.sleep(3)
    else:
        print("[ℹ] Nema lock datoteka za brisanje")

def kill_git_processes():
    """Završi sve Git procese (Windows)"""
    if os.name == 'nt':  # Samo na Windows-u
        try:
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq git.exe'], 
                                  capture_output=True, text=True)
            if 'git.exe' in result.stdout:
                print("[🔧] Završavam Git procese...")
                subprocess.run(['taskkill', '/F', '/IM', 'git.exe'], 
                             capture_output=True)
                time.sleep(2)
                print("[✓] Git procesi završeni")
        except Exception as e:
            print(f"[⚠] Ne mogu završiti Git procese: {e}")

def read_trigger_config():
    """
    Čita Trigger.txt datoteku koja sadrži "Daily" ili "Alert"
    
    Daily -> redovni.jpeg
    Alert -> posebni.jpeg
    """
    config = {
        'type': 'redovni',  # default
        'source_file': 'redovni.jpeg',  # default
        'date': datetime.now().strftime('%Y-%m-%d')  # default današnji datum
    }
    
    if not TRIGGER_FILE.exists():
        print(f"[⚠] Trigger datoteka ne postoji: {TRIGGER_FILE}")
        print(f"[ℹ] Koristim default: {config}")
        return config
    
    try:
        with open(TRIGGER_FILE, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            
            # Ukloni navodnike ako postoje
            content = content.strip('"\'')
            
            if content.upper() == 'DAILY':
                config['type'] = 'redovni'
                config['source_file'] = 'redovni.jpeg'
                print(f"[✓] Trigger: DAILY → kopiram redovni.jpeg")
                
            elif content.upper() == 'ALERT':
                config['type'] = 'posebni'
                config['source_file'] = 'posebni.jpeg'
                print(f"[✓] Trigger: ALERT → kopiram posebni.jpeg")
                
            else:
                print(f"[⚠] Nepoznat trigger: '{content}'. Očekuje se 'Daily' ili 'Alert'")
                print(f"[ℹ] Koristim default: redovni.jpeg")
        
        return config
        
    except Exception as e:
        print(f"[✗] Greška pri čitanju trigger datoteke: {e}")
        print(f"[ℹ] Koristim default: {config}")
        return config

def save_specific_file(source_dir: Path, target_folder: Path, config: dict) -> Path:
    """
    Kopira specifičnu datoteku (redovni.jpeg ili posebni.jpeg) s novim nazivom
    Format: {datum}{sat}{tip}.jpeg
    """
    os.makedirs(target_folder, exist_ok=True)
    
    # Pronađi specifičnu datoteku
    source_file = source_dir / config['source_file']
    
    if not source_file.exists():
        raise FileNotFoundError(f"Datoteka ne postoji: {source_file}")
    
    # Generiraj novi naziv
    timestamp = datetime.now().strftime("%H")  
    report_type = config['type']
    report_date = config['date']
    
    new_name = f"{report_date}{timestamp}{report_type}.jpeg"
    target_path = target_folder / new_name
    
    # Kopiraj datoteku
    copy2(source_file, target_path)
    print(f"[✓] Spremljeno: {source_file.name} → {target_path.name}")
    return target_path

def create_trigger_example():
    """
    Stvori primjer Trigger.txt datoteke ako ne postoji
    """
    if not TRIGGER_FILE.exists():
        try:
            TRIGGER_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            example_content = "Daily"
            
            with open(TRIGGER_FILE, 'w', encoding='utf-8') as file:
                file.write(example_content)
                
            print(f"[✓] Stvoren primjer Trigger.txt: {TRIGGER_FILE}")
            print(f"[ℹ] Sadržaj: 'Daily' (promijeni na 'Alert' za posebni izvještaj)")
            
        except Exception as e:
            print(f"[✗] Ne mogu stvoriti Trigger.txt: {e}")

def safe_git_command(cmd, max_retries=3):
    """Izvršava Git komandu s retry logikom"""
    for attempt in range(max_retries):
        try:
            result = subprocess.run(cmd, cwd=Path.cwd(), check=True, 
                                  capture_output=True, text=True, timeout=30)
            return result
        except subprocess.CalledProcessError as e:
            error_msg = str(e.stderr) if e.stderr else str(e)
            
            if ("index.lock" in error_msg or "Another git process" in error_msg) and attempt < max_retries - 1:
                print(f"[⚠] Git lock detected, pokušaj {attempt + 1}/{max_retries}")
                kill_git_processes()
                cleanup_git_locks()
                time.sleep(3)
            else:
                raise
        except subprocess.TimeoutExpired:
            print(f"[⚠] Git timeout, pokušaj {attempt + 1}/{max_retries}")
            kill_git_processes()
            if attempt == max_retries - 1:
                raise

def main():
    print("=" * 50)
    print("🌊 MuraDrava-FFS Automatski Upload")
    print("=" * 50)
    
    # 0. PRVO - Agresivno čišćenje Git stanja
    kill_git_processes()
    cleanup_git_locks()
    
    # 1. Stvori trigger datoteku ako ne postoji
    create_trigger_example()
    
    # 2. Učitaj trigger konfiguraciju
    config = read_trigger_config()
    
    # 3. Provjeri postoji li source direktorij
    if not SOURCE_DIR.exists():
        print(f"[✗] Izvorna mapa ne postoji: {SOURCE_DIR}")
        return
    
    # 4. Kopiraj datoteku PRIJE Git operacija
    try:
        print(f"[ℹ] Tražim {config['source_file']} u {SOURCE_DIR}")
        saved_file = save_specific_file(SOURCE_DIR, TARGET_DIR, config)
    except FileNotFoundError as e:
        print(f"[✗] {e}")
        print(f"[ℹ] Provjeri postoji li {config['source_file']} u {SOURCE_DIR}")
        return
    except Exception as e:
        print(f"[✗] Greška pri kopiranju: {e}")
        return
    
    # 5. Git operacije s retry logikom
    try:
        print("[🔧] Pripremam git za upload...")
        
        # Jednostavniji pristup - bez reset/clean
        safe_git_command(["git", "pull", "origin", "main"])
        print("[✓] Git pull uspješan")
        
        # Git add s relativnom putanjom
        git_path = f"reports/{saved_file.name}"
        safe_git_command(["git", "add", git_path])
        print(f"[✓] Datoteka dodana u git: {git_path}")
        
        # Commit i push
        commit_message = f"Dodani {config['type']} izvještaji za {config['date']}"
        safe_git_command(["git", "commit", "-m", commit_message])
        safe_git_command(["git", "push", "origin", "main"])
        
        print(f"[✅] Git push uspješan: {commit_message}")
        
    except subprocess.CalledProcessError as e:
        print(f"[✗] Git greška: {e}")
        print(f"[ℹ] Datoteka je spremljena lokalno: {saved_file}")
    except Exception as e:
        print(f"[✗] Neočekivana greška: {e}")
    
    # 6. Rezultat
    print(f"\n[📋] REZULTAT:")
    print(f"[📊] Tip: {config['type']}")
    print(f"[📅] Datum: {config['date']}")
    print(f"[📁] Izvorni file: {config['source_file']}")
    print(f"[📁] Novi file: {saved_file.name}")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
