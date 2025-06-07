# utils_csv.py  --------------------------------------------------------------
import re
from pathlib import Path
import pandas as pd
import chardet
import unidecode

# ---------------------------------------------------------------------------
def detectar_encoding_robusto(arquivo: Path) -> str:
    """Tenta descobrir o encoding lendo os primeiros bytes do arquivo."""
    provavel = chardet.detect(arquivo.read_bytes(2048))["encoding"]
    encodings = [provavel, "utf-8", "iso-8859-1", "cp1252", "latin1"]
    for enc in filter(None, encodings):
        try:
            with open(arquivo, "r", encoding=enc) as f:
                f.read(100)
            return enc
        except Exception:
            continue
    return "utf-8"  # fallback seguro

# ---------------------------------------------------------------------------
def detectar_separador_automatico(arquivo: Path, encoding: str) -> str:
    """Retorna o separador que gerar mais de uma coluna no header."""
    for sep in [";", ",", "\t", "|"]:
        try:
            df = pd.read_csv(arquivo, sep=sep, encoding=encoding, nrows=1)
            if len(df.columns) > 1:
                return sep
        except Exception:
            pass
    return ","  # fallback

# ---------------------------------------------------------------------------
_rx_parenteses = re.compile(r"\([^)]*\)")
_rx_normaliza  = re.compile(r"\W+")

def normalizar_campo(s: str) -> str:
    """Remove acentos, parênteses, pontuação e converte para minúsculas."""
    s = unidecode.unidecode(s)
    s = _rx_parenteses.sub("", s)
    s = _rx_normaliza.sub("", s.lower())
    return s.strip()

# ---------------------------------------------------------------------------
def campos_similares_flex(c1: str, c2: str) -> bool:
    """Verifica se os campos são equivalentes de forma flexível."""
    n1, n2 = normalizar_campo(c1), normalizar_campo(c2)
    return (n1 == n2) or (n1 in n2) or (n2 in n1)
# ---------------------------------------------------------------------------
