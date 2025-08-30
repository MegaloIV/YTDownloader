from downloader import download
from utils import clean_url, banner


def main():
    banner()
    url = input("Ingresa el link de YouTube: ")
    url = clean_url(url)
    download(url)

if __name__ == "__main__":
    main()
