# Instrukcja uruchomienia

- Pobrać repozytorium, zainstalować python (3.7 lub nowszy) i pip
- (Opcjonalnie) Stworzyć środowisko wirtualne w katalogu głównym `python -m venv venv`
- (Opcjonalnie) Uruchomić środowisko wirtualne: `source venv/bin/activate` (Linux) lub `venv/Scripts/Activate.ps1` (Windows, powershell)
- Pobrać zależności `pip install -r requirements.txt`
- Uruchomić program `python run.py FILENAME.json` podając ścieżkę do planu przestrzeni np. `python run.py intelligent_lights/floor.json`
