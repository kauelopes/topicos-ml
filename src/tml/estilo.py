"""Estilo único dos gráficos: mesma paleta e fonte dos slides (metropolis)."""

from __future__ import annotations

import shutil
import subprocess

import matplotlib as mpl
from matplotlib import font_manager

CORES = {
    "primaria": "#23373B",
    "destaque": "#EB811B",
    "verde": "#14B03D",
    "azul": "#2A6F97",
    "vermelho": "#B22234",
    "cinza": "#8C8C8C",
}
CICLO = [CORES[k] for k in ("azul", "destaque", "verde", "vermelho", "primaria", "cinza")]


def _registrar_fira() -> str | None:
    """Tenta registrar Fira Sans da instalação do TeX (se houver)."""
    if not shutil.which("kpsewhich"):
        return None
    for arquivo in ("FiraSans-Regular.otf", "FiraSans-SemiBold.otf"):
        caminho = subprocess.run(["kpsewhich", arquivo], capture_output=True, text=True).stdout.strip()
        if caminho:
            font_manager.fontManager.addfont(caminho)
    return "Fira Sans" if "Fira Sans" in {f.name for f in font_manager.fontManager.ttflist} else None


def aplicar(contexto: str = "slides") -> None:
    """Aplica o estilo. contexto='slides' (letras maiores) ou 'notas'."""
    fonte = _registrar_fira() or "DejaVu Sans"
    escala = 1.0 if contexto == "slides" else 0.9
    mpl.rcParams.update({
        "font.family": fonte,
        "font.size": 11 * escala,
        "axes.prop_cycle": mpl.cycler(color=CICLO),
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": CORES["primaria"],
        "axes.labelcolor": CORES["primaria"],
        "axes.titleweight": "semibold",
        "axes.grid": True,
        "grid.alpha": 0.25,
        "xtick.color": CORES["primaria"],
        "ytick.color": CORES["primaria"],
        "legend.frameon": False,
        "lines.linewidth": 2.0,
        "figure.figsize": (6.0, 3.4),
        "savefig.bbox": "tight",
        "pdf.fonttype": 42,
    })
