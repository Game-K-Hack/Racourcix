import re
import os
import io
import sys
import time
import base64
import pylnk3
import colorama
import subprocess
from PIL import Image
from googlesearch import search as ggsearch, SearchResult

os.system("title Racourcix && cls")
os.system("mode con cols=190 lines=51")

DIR_ICON = fr"C:\Users\{os.environ['username']}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Liens Internet"

def is_in_terminal():
    try:
        return sys.stdout.isatty()
    except:
        False

def find_info(url:str) -> SearchResult | None:
    for i in ggsearch(url, num_results=1, lang="fr", advanced=True):
        return i
    return None

def download_image(data:SearchResult) -> str:
    imgpath = "/".join([DIR_ICON, ".icon", data.name + ".ico"])
    img = Image.open(io.BytesIO(base64.b64decode(data.icon.split(',')[1])))
    img.save(imgpath)
    return imgpath

def display_colored_ascii(ascii_art) -> str:
    # Initialise colorama
    colorama.init(autoreset=True)
    
    # Divise l'image ASCII en lignes
    lines = ascii_art.split('\n')

    image_ascii = []
    
    for line in lines:
        # Traite chaque ligne pour extraire et afficher les couleurs
        colored_line = ''
        i = 0
        while i < len(line):
            # Vérifie si c'est un début de balise de couleur
            if line[i:i+8] == '[color=#':
                # Extrait le code couleur hexadécimal
                end_color_index = line.find(']', i)
                color_code = line[i+8:end_color_index]
                
                # Trouve le texte coloré
                start_text = end_color_index + 1
                end_text_index = line.find('[/color]', start_text)
                colored_text = line[start_text:end_text_index]
                
                # Convertit le code couleur hexadécimal en code ANSI
                try:
                    # Convertit le code hex en valeurs RGB
                    r = int(color_code[0:2], 16)
                    g = int(color_code[2:4], 16)
                    b = int(color_code[4:6], 16)
                    
                    # Utilise le code ANSI 256 couleurs
                    color_code = f'\033[38;2;{r};{g};{b}m'
                    
                    # Ajoute le texte coloré
                    colored_line += color_code + colored_text + colorama.Style.RESET_ALL
                except:
                    # Fallback si la conversion échoue
                    colored_line += colored_text
                
                # Avance l'index
                i = end_text_index + 8
            else:
                # Ajoute les caractères normaux
                # colored_line += line[i]
                i += 1
        
        # Affiche la ligne complète
        image_ascii.append(colored_line)
    
    # Réinitialise les couleurs
    image_ascii.append(colorama.Style.RESET_ALL)

    return "\n".join(image_ascii)

def displaybanner(strlist):
    global strbanner
    b = strbanner.split("\n")
    for i, v in enumerate("".join(strlist).split("\n")):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        result = ansi_escape.sub('', b[startwriteheight+i])
        if (startwritewidth-len(result)) > 0:
            b[startwriteheight+i] += " "*(startwritewidth-len(result))
        b[startwriteheight+i] += v
    print("\n".join(b))

l = 100

strbanner = display_colored_ascii(open("./ascii_light.art", "r", encoding="utf8").read())

strinputlist = [
    "┌", "─"*(l+6), "┐\n", 
    "│ URL: ", " "*l, "│\n", 
    "└", "─"*(l+6), "┘"
]

straddedlist = [
    "\033[32m┌", "─"*(l+6), "┐\033[0m\n", 
    "\033[32m│ L'URL a bien été ajouté !", " "*(l-20), "│\033[0m\n", 
    "\033[32m└", "─"*(l+6), "┘\033[0m", 
]

if not is_in_terminal():
    subprocess.run(["cmd", "/k", "python", sys.argv[0]])
    sys.exit(0)

startwriteheight = 5
startwritewidth = 70

while True:

    displaybanner(strinputlist)

    r, c = len(strbanner.split("\n"))-1-startwriteheight, startwritewidth+7
    url = input(f"\033[{r}A\033[{c}C")

    info = find_info(url)
    path_icon = download_image(info)
    path_icon = os.path.realpath(path_icon)
    open("/".join([DIR_ICON, ".script", info.name + ".bat"]), "w", encoding="utf8").write("start " + url)
    pylnk3.for_file("/".join([DIR_ICON, ".script", info.name + ".bat"]), 
                    "/".join([DIR_ICON, info.name + ".lnk"]), 
                    icon_file=path_icon)

    os.system("cls")
    displaybanner(straddedlist)
    time.sleep(1.5)
    os.system("cls")
