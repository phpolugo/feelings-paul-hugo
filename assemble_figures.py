#!/usr/bin/env python3
"""
Range les images fournies par Paul-Hugo en fig-01 … fig-09 exploitables par le PDF.
Les groupes (plusieurs captures pour une seule figure) sont montés en planche.

Usage : python3 assemble_figures.py
"""
import pathlib
from PIL import Image

BASE = pathlib.Path("/Users/polugo/Library/Mobile Documents/iCloud~md~obsidian/Documents/"
                    "Le Vrai Cerveau de Paul-Hugo ✨/01_PROJET/2. EFAP/"
                    "2. Mémoire IA x Humain 🧬/2. Mémoire/images")
SRC = BASE / "Images"
LARGE = 1800          # largeur cible des figures


def charge(p):
    im = Image.open(p)
    if im.mode in ("RGBA", "LA", "P"):
        fond = Image.new("RGB", im.size, "white")
        im = im.convert("RGBA")
        fond.paste(im, mask=im.split()[-1])
        im = fond
    return im.convert("RGB")


def simple(src, dst, largeur=LARGE):
    im = charge(SRC / src)
    r = largeur / im.width
    im = im.resize((largeur, int(im.height * r)), Image.LANCZOS)
    im.save(BASE / dst, quality=88)
    return f"{dst}  ←  {src}"


def planche(srcs, dst, cols=2, largeur=LARGE, gap=18):
    ims = [charge(SRC / s) for s in srcs if (SRC / s).exists()]
    if not ims:
        return f"{dst} : AUCUNE SOURCE"
    lignes = (len(ims) + cols - 1) // cols
    cw = (largeur - gap * (cols - 1)) // cols
    # hauteur de cellule = la plus grande hauteur ramenée à cw
    ch = max(int(im.height * cw / im.width) for im in ims)
    out = Image.new("RGB", (largeur, ch * lignes + gap * (lignes - 1)), "white")
    for i, im in enumerate(ims):
        h = int(im.height * cw / im.width)
        im = im.resize((cw, h), Image.LANCZOS)
        x = (i % cols) * (cw + gap)
        y = (i // cols) * (ch + gap) + (ch - h) // 2      # centré verticalement
        out.paste(im, (x, y))
    out.save(BASE / dst, quality=88)
    return f"{dst}  ←  planche de {len(ims)}"


def groupe(dossier, dst, n=4, cols=2):
    d = SRC / dossier
    fs = sorted([f.name for f in d.iterdir()
                 if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")])[:n]
    return planche([f"{dossier}/{f}" for f in fs], dst, cols=cols)


if __name__ == "__main__":
    taches = [
        # fig-01 : Tommy dans son atelier
        lambda: simple("IMG_4809.JPG", "fig-01.jpg"),
        # fig-02 : le selfie avec le distillateur + les alambics
        lambda: planche(["IMG_4716.JPG", "IMG_4685.JPG"], "fig-02.jpg", cols=2),
        # fig-03 : la charte graphique de Gaëtan
        lambda: groupe("Gaetan Pers Brand screenshot", "fig-03.jpg", n=4, cols=2),
        # fig-04 : le graphe Obsidian
        lambda: groupe("Obsidian", "fig-04.jpg", n=1, cols=1),
        # fig-05 : les projets shippés
        lambda: planche(["La Sève/Screenshot 2026-09-08 at 12.09.06.png",
                         "La Sève/Screenshot 2026-09-08 at 12.09.54.png",
                         "Buddy App.png"], "fig-05.jpg", cols=3),
        # fig-06 : la publicité Cetelem
        lambda: simple("Pub Cetelem.png", "fig-06.jpg"),
        # fig-07 : les notes du cours de sémiologie
        lambda: planche(["Pages Punctum/IMG_8556.jpg",
                         "Pages Punctum/IMG_8558.jpg"], "fig-07.jpg", cols=2),
        # fig-08 : les fiches papier à côté du rendu
        lambda: simple("Process Fiches Papier Hyperframe.jpg", "fig-08.jpg"),
        # fig-09 : la carte des niveaux de conscience
        lambda: simple("carte conscience Hawkins.webp", "fig-09.jpg"),
    ]
    for t in taches:
        try:
            print(" ", t())
        except Exception as e:
            print("  ÉCHEC :", e)
    print("\nfig-10 (schéma DPB) est généré séparément par schema_dpb.html")
