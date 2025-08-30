from colorama import Fore, Style
import pyfiglet 
import os
from pathlib import Path
import sys

def show_info(info):
    """Mostrar información básica del video"""
    print(f"\n{Fore.CYAN}Título:{Style.RESET_ALL} {info.get('title', 'Desconocido')}")
    print(f"{Fore.CYAN}Duración:{Style.RESET_ALL} {info.get('duration_string', 'N/A')}")

def choose_option():
    """Preguntar al usuario qué quiere descargar"""
    print(f"\n{Fore.YELLOW}¿Qué quieres descargar?{Style.RESET_ALL}")
    print("1. Solo Video")
    print("2. Solo Audio (MP3)")
    print("3. Video + Audio (combinado)")
    return input(f"{Fore.GREEN}Selecciona una opción (1-3): {Style.RESET_ALL}")

def show_formats(formats, kind):
    """Mostrar las calidades disponibles"""
    print(f"\n{Fore.MAGENTA}Opciones disponibles:{Style.RESET_ALL}")
    for i, f in enumerate(formats):
        size = round(f.get("filesize", 0) / (1024 * 1024), 2) if f.get("filesize") else "?"
        if kind == "audio":
            print(f"{i+1}. {f.get('abr', '?')} kbps - {f.get('ext')} - {size} MB")
        else:
            print(f"{i+1}. {f.get('format_note', '?')} - {f.get('ext')} - {size} MB")

def clean_url(url: str) -> str:
    if "youtube.com" in url and "watch?v=" in url:
        url = url.split("&")[0]  # elimina parámetros extra
    return url.strip()

def banner():
    ascii_banner = pyfiglet.figlet_format("YTDownloader")
    print(Fore.RED + ascii_banner + Style.RESET_ALL)
    print(Fore.RED + "V1.0 by Meg4Lo\n" + Style.RESET_ALL)

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")
    banner()

def choose_save_path():
    print("\nDónde quieres guardar el archivo?")
    print("1. Carpeta Descargas")
    print("2. Carpeta del programa")
    print("3. Elegir ruta manual")

    choice = input("> ").strip()

    if choice == "1":
        return str(Path.home() / "Downloads")

    elif choice == "2":
        # Si está compilado a exe, usa la ruta del exe
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        else:
            return os.getcwd()

    elif choice == "3":
        path = input("Ingresa la ruta de carpeta: ").strip()
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    else:
        print("Opción inválida, usando carpeta actual.")
        return os.getcwd()
