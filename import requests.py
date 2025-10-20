import datetime  # Pro práci s datem a časem
import requests  # Pro odesílání HTTP požadavků (např. API volání)
from dateutil import parser  # Pro parsování ISO formátů času
import pytz  # Pro práci s časovými pásmy
import tkinter as tk  # Pro vytvoření GUI aplikace
from tkinter import messagebox  # Pro zobrazování chybových hlášení v GUI

# Funkce pro získání jmenin
def get_name_day():
    """
    Vrací jméno osoby, která má svátek pro aktuální datum.
    Využívá API 'https://svatky.adresa.info/json'.
    """
    today = datetime.datetime.now()  # Získání aktuálního data a času
    formatted_date = today.strftime("%d%m")  # Převedení data do formátu DDMM
    url = f"https://svatky.adresa.info/json?date={formatted_date}"  # Sestavení URL
    response = requests.get(url)  # Odeslání GET požadavku
    if response.status_code == 200:  # Pokud je odpověď úspěšná
        data = response.json()  # Načtení odpovědi jako JSON
        if data:  # Pokud je odpověď neprázdná
            return data[0]['name']  # Vrácení jména osoby
    return "Nepodařilo se získat data o jmeninách."  # Pokud API selže

# Funkce pro získání východu a západu slunce
def get_sun_times(latitude, longitude):
    """
    Vrací časy východu a západu slunce pro dané souřadnice (latitude, longitude).
    Využívá API 'https://api.sunrise-sunset.org/json'.
    """
    url = f"https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&formatted=0"  # Sestavení URL
    response = requests.get(url)  # Odeslání GET požadavku
    if response.status_code == 200:  # Pokud je odpověď úspěšná
        data = response.json()  # Načtení odpovědi jako JSON
        sunrise_utc = data['results']['sunrise']  # Východ slunce (UTC)
        sunset_utc = data['results']['sunset']  # Západ slunce (UTC)

        # Převod času z UTC do časového pásma Evropy/Prahy
        timezone = pytz.timezone("Europe/Prague")
        sunrise = parser.isoparse(sunrise_utc).astimezone(timezone)
        sunset = parser.isoparse(sunset_utc).astimezone(timezone)
        return sunrise.strftime('%H:%M:%S'), sunset.strftime('%H:%M:%S')  # Vrácení časů jako řetězců
    return None, None  # Pokud API selže

# Funkce pro aktualizaci informací v GUI
def update_info():
    """
    Načítá aktuální informace o svátcích a časech východu/západu slunce.
    Aktualizuje zobrazené texty v GUI.
    """
    try:
        today = datetime.datetime.now()  # Získání aktuálního data a času
        
        # Načtení jména osoby, která má dnes svátek
        name_day = get_name_day()
        # Načtení časů východu a západu slunce pro Olomouc
        latitude = 49.5938  # Zeměpisná šířka Olomouce
        longitude = 17.2509  # Zeměpisná délka Olomouce
        sunrise, sunset = get_sun_times(latitude, longitude)
        
        # Aktualizace zobrazených textů
        if sunrise and sunset:
            date_label.config(text="Datum:", fg="black")  # Nastavení černého textu pro "Datum:"
            date_value_label.config(text=f"{today.strftime('%d.%m.%Y')}", fg="blue")  # Datum modře
            name_day_label.config(text="Dnes má svátek:", fg="black")  # Text "Dnes má svátek" černě
            name_label.config(text=f"🌸 {name_day} 🌸", fg="blue")  # Jméno modře
            sun_info_label.config(text="V Olomouci:", fg="black")  # Text "V Olomouci" černě
            sunrise_label.config(text=f"Východ slunce v: {sunrise}", fg="blue")  # Východ slunce modře
            sunset_label.config(text=f"Západ slunce v: {sunset}", fg="blue")  # Západ slunce modře
        else:
            # Zobrazení chybové zprávy, pokud API selže
            messagebox.showerror("Chyba", "Nepodařilo se získat informace o východu a západu slunce.")
    except Exception as e:
        # Zobrazení chybové zprávy při jiné chybě
        messagebox.showerror("Chyba", f"Došlo k chybě: {e}")

# GUI - Grafické uživatelské rozhraní
root = tk.Tk()  # Inicializace hlavního okna aplikace
root.title("Informace o Jmeninách a Slunci")  # Nastavení názvu okna

# Datum: Popisek a hodnota
date_label = tk.Label(root, text="Datum:", font=("Arial", 14))  # Popisek "Datum"
date_label.pack(pady=5)
date_value_label = tk.Label(root, text="---", font=("Arial", 14))  # Hodnota data
date_value_label.pack(pady=5)

# Dnes má svátek: Popisek a jméno
name_day_label = tk.Label(root, text="Dnes má svátek:", font=("Arial", 14))  # Popisek "Dnes má svátek"
name_day_label.pack(pady=5)
name_label = tk.Label(root, text="🌸 --- 🌸", font=("Arial", 18))  # Jméno osoby, která má svátek
name_label.pack(pady=5)

# Informace o Olomouci
sun_info_label = tk.Label(root, text="V Olomouci:", font=("Arial", 14))  # Popisek "V Olomouci"
sun_info_label.pack(pady=5)

# Východ slunce
sunrise_label = tk.Label(root, text="Východ slunce v: ---", font=("Arial", 12))  # Čas východu slunce
sunrise_label.pack(pady=5)

# Západ slunce
sunset_label = tk.Label(root, text="Západ slunce v: ---", font=("Arial", 12))  # Čas západu slunce
sunset_label.pack(pady=5)

# Tlačítko pro aktualizaci
update_button = tk.Button(root, text="Aktualizovat", command=update_info, font=("Arial", 12))  # Tlačítko
update_button.pack(pady=10)

# Inicializace dat při spuštění
update_info()

# Spuštění aplikace
root.mainloop()  # Spuštění hlavní smyčky aplikace
