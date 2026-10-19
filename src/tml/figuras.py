"""Gera as figuras usadas nos slides e nas notas.

Uso (da raiz do repositório):  make figs
    ou:  PYTHONPATH=src python -m tml.figuras [01 02 ...]

Convenção: cada aula tem uma função `aulaNN()` que salva em
aulas/NN-*/figs/aNN_<nome>.pdf. O prefixo evita colisões na apostila.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from tml import estilo

RAIZ = Path(__file__).resolve().parents[2]


def _pasta(aula: str) -> Path:
    (destino,) = RAIZ.glob(f"aulas/{aula}-*/figs")
    return destino


# ---------------------------------------------------------------------
# Aula 01 — Python, NumPy e JAX
# ---------------------------------------------------------------------
def aula01() -> None:
    import jax
    import jax.numpy as jnp

    destino = _pasta("01")

    # (1) Utilidade CRRA e utilidade marginal obtida por jax.grad
    gamma = 2.0

    def u(c):
        return c ** (1 - gamma) / (1 - gamma)

    du = jax.vmap(jax.grad(u))
    c = jnp.linspace(0.3, 3.0, 200)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.0))
    ax1.plot(c, u(c), color=estilo.CORES["azul"])
    ax1.set(title=r"$u(c)$", xlabel="consumo $c$")
    ax2.plot(c, du(c), color=estilo.CORES["destaque"], label="jax.grad(u)")
    ax2.plot(c[::12], c[::12] ** (-gamma), "o", ms=4, color=estilo.CORES["primaria"],
             label=r"analítica $c^{-\gamma}$")
    ax2.set(title=r"$u'(c)$", xlabel="consumo $c$")
    ax2.legend()
    fig.tight_layout()
    fig.savefig(destino / "a01_crra_grad.pdf")
    plt.close(fig)

    # (2) Laço Python x operação vetorizada (NumPy): tempo por tamanho
    def acumulada_laco(taxas):
        fator = 1.0
        for t in taxas:
            fator *= 1 + t
        return fator - 1

    def acumulada_vetor(taxas):
        return np.prod(1 + taxas) - 1

    def cronometrar(f, x, rep=5):
        melhores = []
        for _ in range(rep):
            t0 = time.perf_counter()
            f(x)
            melhores.append(time.perf_counter() - t0)
        return min(melhores)

    rng = np.random.default_rng(0)
    tamanhos = np.array([10**k for k in range(2, 8)])
    t_laco, t_vetor = [], []
    for n in tamanhos:
        x = rng.normal(0.0, 0.002, size=n)  # média 0 evita overflow em n grande
        t_laco.append(cronometrar(acumulada_laco, x))
        t_vetor.append(cronometrar(acumulada_vetor, x))

    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ax.loglog(tamanhos, t_laco, "o-", label="laço for (Python puro)")
    ax.loglog(tamanhos, t_vetor, "s-", label="np.prod (vetorizado)")
    ax.set(xlabel="número de observações", ylabel="tempo (s)")
    ax.legend()
    razao = np.array(t_laco)[-1] / np.array(t_vetor)[-1]
    ax.set_title(f"Vetorizado ≈ {razao:,.0f}× mais rápido com n = 10⁷".replace(",", "."),
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(destino / "a01_laco_vs_vetor.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------
# Aula 02 — O que é aprendizado de máquina?
# ---------------------------------------------------------------------
def aula02() -> None:
    from sklearn.cluster import KMeans
    from sklearn.linear_model import LogisticRegression

    destino = _pasta("02")
    C = estilo.CORES
    rng = np.random.default_rng(7)

    # (1) Três tarefas: regressão, classificação, agrupamento
    fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.3))

    area = rng.uniform(30, 160, 120)
    preco = 80 + 6.5 * area + rng.normal(0, 90, area.size)
    b1, b0 = np.polyfit(area, preco, 1)
    grade = np.linspace(30, 160, 2)
    axs[0].scatter(area, preco, s=12, color=C["azul"], alpha=0.7)
    axs[0].plot(grade, b0 + b1 * grade, color=C["destaque"])
    axs[0].set(title="Regressão: y contínuo", xlabel="área (m²)", ylabel="preço (R$ mil)")

    n = 300
    renda = rng.lognormal(np.log(4), 0.5, n)                  # R$ mil/mês
    comprom = np.clip(rng.beta(2, 5, n) * 0.9, 0, 0.9)       # dívida / renda
    logit = -0.5 - 0.9 * renda + 12.0 * comprom
    inad = rng.uniform(size=n) < 1 / (1 + np.exp(-logit))
    Xc = np.column_stack([renda, comprom])
    clf = LogisticRegression().fit(Xc, inad)
    axs[1].scatter(renda[~inad], comprom[~inad], s=12, color=C["verde"], alpha=0.7, label="adimplente")
    axs[1].scatter(renda[inad], comprom[inad], s=14, color=C["vermelho"], marker="x", label="inadimplente")
    rr = np.linspace(renda.min(), np.percentile(renda, 98), 50)
    w0, (w1, w2) = clf.intercept_[0], clf.coef_[0]
    axs[1].plot(rr, -(w0 + w1 * rr) / w2, color=C["primaria"], ls="--", lw=1.5, label="fronteira")
    axs[1].set(title="Classificação: y categórico", xlabel="renda (R$ mil/mês)",
               ylabel="dívida / renda", ylim=(0, 0.9), xlim=(rr.min(), rr.max()))
    axs[1].legend(fontsize=8, loc="upper right", frameon=True, framealpha=0.9, edgecolor="none")

    centros = np.array([[0.32, 0.06], [0.18, 0.15], [0.12, 0.28]])
    pts = np.vstack([c + rng.normal(0, 0.03, (70, 2)) for c in centros])
    km = KMeans(3, n_init=10, random_state=0).fit(pts)
    for k, cor in zip(range(3), [C["azul"], C["destaque"], C["verde"]]):
        m = km.labels_ == k
        axs[2].scatter(pts[m, 0], pts[m, 1], s=12, color=cor, alpha=0.7)
    axs[2].scatter(*km.cluster_centers_.T, marker="X", s=120, color=C["primaria"], edgecolor="white")
    axs[2].set(title="Agrupamento: sem y", xlabel="parcela gasta com alimentação",
               ylabel="parcela gasta com lazer")
    fig.tight_layout()
    fig.savefig(destino / "a02_tarefas.pdf")
    plt.close(fig)

    # (2) Prever x inferir: coeficientes instáveis, previsões estáveis
    B, n, rho = 1000, 100, 0.98
    cov = np.array([[1, rho], [rho, 1]])
    x0 = np.array([1.0, 1.0, 1.0])                  # (intercepto, x1, x2)
    betas, prevs = [], []
    for _ in range(B):
        X = rng.multivariate_normal([0, 0], cov, n)
        y = X[:, 0] + X[:, 1] + rng.normal(0, 1, n)
        Xd = np.column_stack([np.ones(n), X])
        b = np.linalg.lstsq(Xd, y, rcond=None)[0]
        betas.append(b[1])
        prevs.append(x0 @ b)
    betas, prevs = np.array(betas), np.array(prevs)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 3.0), sharey=True)
    a1.hist(betas, bins=40, color=C["azul"], alpha=0.85)
    a1.axvline(1.0, color=C["primaria"], ls="--", lw=1.2)
    a1.set(title=rf"$\hat\beta_1$ (verdadeiro = 1): dp = {betas.std():.2f}",
           xlabel=r"$\hat\beta_1$", ylabel="nº de amostras")
    a2.hist(prevs, bins=40, color=C["destaque"], alpha=0.85)
    a2.axvline(2.0, color=C["primaria"], ls="--", lw=1.2)
    a2.set(title=rf"$\hat y(x_0)$ (verdadeiro = 2): dp = {prevs.std():.2f}", xlabel=r"$\hat y(x_0)$")
    lim = 4 * betas.std()
    a1.set_xlim(1 - lim, 1 + lim)
    a2.set_xlim(2 - lim, 2 + lim)
    fig.tight_layout()
    fig.savefig(destino / "a02_prever_inferir.pdf")
    plt.close(fig)

    _a02_pixels(destino)


# Imagens 24x24 em tons de cinza (0 = preto, 255 = branco), desenhadas com
# geometria simples: o "processo gerador" das figuras de gato e cachorro.
_N_PIX = 24
_FUNDO = 235.0


def _grade() -> tuple[np.ndarray, np.ndarray]:
    yy, xx = np.mgrid[0:_N_PIX, 0:_N_PIX] + 0.5
    return xx, yy


def _elipse(cx: float, cy: float, rx: float, ry: float) -> np.ndarray:
    xx, yy = _grade()
    return ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1


def _triangulo(p1, p2, p3) -> np.ndarray:
    xx, yy = _grade()

    def lado(a, b):
        return (xx - b[0]) * (a[1] - b[1]) - (a[0] - b[0]) * (yy - b[1])

    d = np.stack([lado(p1, p2), lado(p2, p3), lado(p3, p1)])
    return ~((d < 0).any(0) & (d > 0).any(0))


def gato() -> np.ndarray:
    im = np.full((_N_PIX, _N_PIX), _FUNDO)
    im[_triangulo((4, 2), (4, 12), (11, 8))] = 110        # orelhas pontudas
    im[_triangulo((20, 2), (20, 12), (13, 8))] = 110
    im[_elipse(12, 14, 8, 6.8)] = 110                      # cara
    im[_elipse(8.5, 12.5, 1.5, 1.5)] = 20                  # olhos
    im[_elipse(15.5, 12.5, 1.5, 1.5)] = 20
    im[_triangulo((11, 16), (13, 16), (12, 17.6))] = 40    # nariz
    for linha in (16, 18):                                 # bigodes
        im[linha, 2:7] = 60
        im[linha, 17:22] = 60
    return im


def cachorro() -> np.ndarray:
    im = np.full((_N_PIX, _N_PIX), _FUNDO)
    im[_elipse(12, 12, 8, 7.6)] = 150                      # cara
    im[_elipse(4.5, 13, 2.6, 5.7)] = 70                    # orelhas caídas
    im[_elipse(19.5, 13, 2.6, 5.7)] = 70
    im[_elipse(12, 17, 4.8, 3.0)] = 205                    # focinho
    im[_elipse(9, 10.5, 1.2, 1.2)] = 20                    # olhos
    im[_elipse(15, 10.5, 1.2, 1.2)] = 20
    im[_elipse(12, 15.3, 1.8, 1.3)] = 25                   # nariz
    im[19, 10:15] = 60                                     # boca
    return im


def _mostrar(ax, im: np.ndarray, titulo: str = "") -> None:
    ax.imshow(im, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    _mostrar_eixos(ax)
    if titulo:
        ax.set_title(titulo)


def _a02_pixels(destino: Path) -> None:
    from matplotlib.patches import Rectangle

    C = estilo.CORES
    g, c = gato(), cachorro()

    # (3) A pergunta: duas imagens e seus rótulos
    fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.8))
    _mostrar(axs[0], g, r"$y$ = gato")
    _mostrar(axs[1], c, r"$y$ = cachorro")
    fig.tight_layout()
    fig.savefig(destino / "a02_gato_cachorro.pdf")
    plt.close(fig)

    # (4) O que o computador vê: um recorte 6x6 em volta do olho esquerdo
    l0, c0, k = 9, 5, 6
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.4),
                                 gridspec_kw={"width_ratios": [1, 1.15]})
    _mostrar(a1, g, "o que vemos")
    a1.add_patch(Rectangle((c0 - 0.5, l0 - 0.5), k, k, fill=False,
                           ec=C["destaque"], lw=2.2))
    recorte = g[l0:l0 + k, c0:c0 + k]
    _mostrar(a2, recorte, "o que o computador vê")
    for (i, j), v in np.ndenumerate(recorte):
        a2.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=10,
                color="white" if v < 128 else C["primaria"])
    for lado in a2.spines.values():
        lado.set_color(C["destaque"])
        lado.set_linewidth(2.2)
    fig.tight_layout()
    fig.savefig(destino / "a02_pixels.pdf")
    plt.close(fig)

    # (5) Vizinhança: o mesmo gato deslocado 2 pixels para a direita
    desl = np.roll(g, 2, axis=1)
    desl[:, :2] = _FUNDO
    mudou = g != desl
    fig, axs = plt.subplots(1, 3, figsize=(8.4, 3.0))
    _mostrar(axs[0], g, "gato")
    _mostrar(axs[1], desl, "o mesmo gato, 2 pixels\npara a direita")
    mapa = np.where(mudou, 1.0, 0.0)
    axs[2].imshow(mapa, cmap=_cmap_destaque(), vmin=0, vmax=1, interpolation="nearest")
    _mostrar_eixos(axs[2])
    axs[2].set_title(f"pixels que mudaram:\n{mudou.sum()} de {g.size}")
    i, j = 12, 7                                           # borda do olho esquerdo
    for ax in axs[:2]:
        ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, ec=C["destaque"], lw=2))
    axs[0].set_xlabel(f"pixel ({i}, {j}) = {g[i, j]:.0f}")
    axs[1].set_xlabel(f"pixel ({i}, {j}) = {desl[i, j]:.0f}")
    fig.tight_layout()
    fig.savefig(destino / "a02_deslocamento.pdf")
    plt.close(fig)


def _cmap_destaque():
    from matplotlib.colors import ListedColormap

    return ListedColormap(["#F2F2F2", estilo.CORES["destaque"]])


def _mostrar_eixos(ax) -> None:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for lado in ax.spines.values():
        lado.set_visible(True)
        lado.set_color(estilo.CORES["cinza"])


AULAS = {"01": aula01, "02": aula02}


def main(argv: list[str]) -> None:
    estilo.aplicar("slides")
    selecionadas = argv or list(AULAS)
    for k in selecionadas:
        print(f"[figs] aula {k}")
        AULAS[k]()


if __name__ == "__main__":
    main(sys.argv[1:])
