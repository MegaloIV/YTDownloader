import yt_dlp
from colorama import Fore, Style
from utils import show_info, choose_option, show_formats, clear_console, choose_save_path
import os


def download(url: str):
    try:
        # Obtener info del video sin descargar
        ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        show_info(info)
        
        # Selección de ruta de guardado
        save_path = choose_save_path()

        # Bucle hasta que elija opción válida
        while True:
            option = choose_option()
            formats = []
            kind = None

            if option == "1":
                formats = [f for f in info["formats"] if f.get("vcodec") != "none" and f.get("acodec") == "none"]
                kind = "video"
            elif option == "2":
                formats = [f for f in info["formats"] if f.get("acodec") != "none" and f.get("vcodec") == "none"]
                kind = "audio"
            elif option == "3":
                formats = [f for f in info["formats"] if f.get("vcodec") != "none" and f.get("acodec") != "none"]
                kind = "video+audio"
            else:
                clear_console()
                print(f"{Fore.RED}Opción inválida. Intenta de nuevo.{Style.RESET_ALL}")
                continue  # vuelve a preguntar

            if not formats:
                clear_console()
                print(f"{Fore.RED}No se encontraron streams disponibles.{Style.RESET_ALL}")
                continue

            break  # salió del bucle, tiene opción correcta

        show_formats(formats, kind)

        # Bucle hasta que elija calidad válida
        while True:
            try:
                selection = int(input(f"\n{Fore.GREEN}Elige la calidad (número): {Style.RESET_ALL}")) - 1
                if selection < 0 or selection >= len(formats):
                    clear_console()
                    print(f"{Fore.RED}Opción inválida. Intenta de nuevo.{Style.RESET_ALL}")
                    show_formats(formats, kind)
                    continue
                break
            except ValueError:
                clear_console()
                print(f"{Fore.RED}Entrada inválida, escribe un número.{Style.RESET_ALL}")
                show_formats(formats, kind)

        format_id = formats[selection]["format_id"]

        # Configuración final de descarga
        ydl_opts = {
            "format": format_id,
            "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
            "quiet": False,
            "no_warnings": True
        }

        if kind == "audio":
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]

        print(f"\n{Fore.YELLOW}Descargando...{Style.RESET_ALL}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"{Fore.GREEN}Descarga completa{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
