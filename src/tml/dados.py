"""Acesso a dados econômicos públicos usados nas aulas.

- sgs(codigo): séries do Sistema Gerenciador de Séries Temporais (SGS) do
  Banco Central.
- nsw(): o experimento NSW (LaLonde, 1986; subamostra de Dehejia e Wahba,
  1999) e os controles da CPS, da página de Rajeev Dehejia no NBER.

Exemplos de códigos SGS: Exemplos de códigos SGS:
    433   IPCA — variação % mensal
    432   Meta Selic definida pelo Copom (% a.a.)
    24369 Taxa de desocupação — PNAD Contínua (%)
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

URL_NSW = "https://users.nber.org/~rdehejia/data/{arquivo}.dta"
URL_SGS = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json"
CACHE = Path(__file__).resolve().parents[2] / "data" / "raw"


def sgs(codigo: int, inicio: str | None = None, fim: str | None = None,
        cache: bool = True) -> pd.Series:
    """Baixa uma série do SGS/BCB como pd.Series indexada por data.

    inicio/fim no formato 'dd/mm/aaaa'. Com cache=True salva um CSV em
    data/raw/ e reaproveita nas próximas chamadas (útil fora do Colab).
    """
    arquivo = CACHE / f"sgs_{codigo}_{(inicio or '').replace('/', '')}_{(fim or '').replace('/', '')}.csv"
    if cache and arquivo.exists():
        return pd.read_csv(arquivo, index_col=0, parse_dates=True).iloc[:, 0]

    url = URL_SGS.format(codigo=codigo)
    if inicio:
        url += f"&dataInicial={inicio}"
    if fim:
        url += f"&dataFinal={fim}"
    df = pd.read_json(url)
    serie = pd.Series(df["valor"].astype(float).values,
                      index=pd.to_datetime(df["data"], dayfirst=True),
                      name=f"sgs_{codigo}")
    if cache:
        CACHE.mkdir(parents=True, exist_ok=True)
        serie.to_csv(arquivo)
    return serie


def nsw(cache: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Devolve (nsw, cps): os 445 participantes do experimento NSW
    (185 tratados, 260 controles) e os 15.992 homens da CPS (treat = 0).

    Colunas: treat, age, education, black, hispanic, married, nodegree,
    re74, re75, re78 (renda anual em US$).
    """
    bases = []
    for arquivo in ("nsw_dw", "cps_controls"):
        local = CACHE / f"{arquivo}.csv"
        if cache and local.exists():
            df = pd.read_csv(local)
        else:
            df = pd.read_stata(URL_NSW.format(arquivo=arquivo)).drop(columns="data_id")
            if cache:
                CACHE.mkdir(parents=True, exist_ok=True)
                df.to_csv(local, index=False)
        bases.append(df)
    return bases[0], bases[1]
