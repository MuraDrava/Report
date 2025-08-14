import os
from datetime import datetime
from pathlib import Path
from shutil import copy2
import subprocess
import glob

# Postavke
SOURCE_DIR = Path(r"C:\MuraDrava_PrognostickiModel\MuraDravaFFS\Reports\images")
TARGET_DIR = Path("reports")  # Relativna putanja unutar tvog git repozitorija
TRIGGER_FILE = Path(r"C:\MuraDrava_PrognostickiModel\MuraDravaFFS\Trigger.txt")  # Putanja do trigger datoteke

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
        print(f"[⚠️] Trigger datoteka ne postoji: {TRIGGER_FILE}")
        print(f"[ℹ️] Koristim default: {config}")
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
                print(f"[⚠️] Nepoznat trigger: '{content}'. Očekuje se 'Daily' ili 'Alert'")
                print(f"[ℹ️] Koristim default: redovni.jpeg")
        
        return config
        
    except Exception as e:
        print(f"[✗] Greška pri čitanju trigger datoteke: {e}")
        print(f"[ℹ️] Koristim default: {config}")
        return config

def save_specific_file(source_dir: Path, target_folder: Path, config: dict) -> Path:
    """
    Kopira specifičnu datoteku (redovni.jpeg ili posebni.jpeg) s novim nazivom
    Format: {tip}_{datum}_{timestamp}.jpeg
    """
    os.makedirs(target_folder, exist_ok=True)
    
    # Pronađi specifičnu datoteku
    source_file = source_dir / config['source_file']
    
    if not source_file.exists():
        raise FileNotFoundError(f"Datoteka ne postoji: {source_file}")
    
    # Generiraj novi naziv
    timestamp = datetime.now().strftime("%H%M%S")  
    report_type = config['type']
    report_date = config['date'].replace('-', '')  # Ukloni crtice iz datuma
    
    new_name = f"{report_date}_{timestamp}_{report_type}.jpeg"
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
            print(f"[ℹ️] Sadržaj: 'Daily' (promijeni na 'Alert' za posebni izvještaj)")
            
        except Exception as e:
            print(f"[✗] Ne mogu stvoriti Trigger.txt: {e}")

def git_commit_and_push(files: list[Path], config: dict):
    """
    Git commit i push s opisnim commit message-om
    Prvo očisti git stanje, zatim kopiraj datoteke
    """
    try:
        commit_message = f"Dodani {config['type']} izvještaji za {config['date']}"
        
        # 1. Resetiraj na čisto stanje PRIJE kopiranja
        print("[🔧] Resetiram git na čisto stanje...")
        subprocess.run(["git", "reset", "--hard", "HEAD"], cwd=Path.cwd(), check=True)
        subprocess.run(["git", "clean", "-fd"], cwd=Path.cwd(), check=True)
        print("[✓] Git reset završen")
        
        # 2. Pull najnovije promjene
        print("[ℹ️] Dohvaćam najnovije promjene s GitHub-a...")
        subprocess.run(["git", "pull", "origin", "main"], cwd=Path.cwd(), check=True)
        print("[✓] Git pull uspješan")
        
        # 3. Provjeri postoje li datoteke (nakon reset-a možda su obrisane)
        for file in files:
            if not file.exists():
                print(f"[⚠️] Datoteka je obrisana resetom: {file}")
                return False
        
        # 4. Dodaj datoteke
        for file in files:
            subprocess.run(["git", "add", str(file)], cwd=Path.cwd(), check=True)
        
        # 5. Commit
        subprocess.run(["git", "commit", "-m", commit_message], cwd=Path.cwd(), check=True)
        
        # 6. Push
        subprocess.run(["git", "push", "origin", "main"], cwd=Path.cwd(), check=True)
        print(f"[✓] Git push uspješan: {commit_message}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[✗] Git greška: {e}")
        return False

def main():
    print("=" * 50)
    print("🌊 MuraDrava-FFS Automatski Upload")
    print("=" * 50)
    
    # 1. Stvori trigger datoteku ako ne postoji
    create_trigger_example()
    
    # 2. Učitaj trigger konfiguraciju
    config = read_trigger_config()
    
    # 3. Provjeri postoji li source direktorij
    if not SOURCE_DIR.exists():
        print(f"[✗] Izvorna mapa ne postoji: {SOURCE_DIR}")
        return
    
    # 4. PRVO očisti git stanje
    try:
        print("[🔧] Pripremam git za upload...")
        subprocess.run(["git", "reset", "--hard", "HEAD"], cwd=Path.cwd(), check=True)
        subprocess.run(["git", "clean", "-fd"], cwd=Path.cwd(), check=True)
        subprocess.run(["git", "pull", "origin", "main"], cwd=Path.cwd(), check=True)
        print("[✓] Git priprema završena")
    except subprocess.CalledProcessError as e:
        print(f"[⚠️] Git priprema neuspješna: {e}")
    
    # 5. ZATIM kopiraj datoteku
    try:
        print(f"[ℹ️] Tražim {config['source_file']} u {SOURCE_DIR}")
        
        saved_file = save_specific_file(SOURCE_DIR, TARGET_DIR, config)
        
        # 6. Git add, commit i push
        try:
            commit_message = f"Dodani {config['type']} izvještaji za {config['date']}"
            
            subprocess.run(["git", "add", str(saved_file)], cwd=Path.cwd(), check=True)
            subprocess.run(["git", "commit", "-m", commit_message], cwd=Path.cwd(), check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=Path.cwd(), check=True)
            
            print(f"[✓] Git push uspješan: {commit_message}")
            
        except subprocess.CalledProcessError as e:
            print(f"[✗] Git greška: {e}")
        
        print(f"\n[✅] Uspješno uploadana datoteka!")
        print(f"[📊] Tip: {config['type']}")
        print(f"[📅] Datum: {config['date']}")
        print(f"[📁] Izvorni file: {config['source_file']}")
        print(f"[📁] Novi file: {saved_file.name}")
        
    except FileNotFoundError as e:
        print(f"[✗] {e}")
        print(f"[ℹ️] Provjeri postoji li {config['source_file']} u {SOURCE_DIR}")
    
    except Exception as e:
        print(f"[✗] Greška pri kopiranju: {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    main()


