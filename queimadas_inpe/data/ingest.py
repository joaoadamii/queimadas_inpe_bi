from pathlib import Path
from zipfile import ZipFile
import requests
import pandas as pd
from loguru import logger


# Caminho raiz do projeto.
# __file__ aponta para queimadas_inpe/data/ingest.py
# parents[2] sobe até a pasta principal queimadas_inpe_bi
PROJECT_DIR = Path(__file__).resolve().parents[2]

# Onde os arquivos originais serão armazenados.
# Aqui ficam os ZIPs exatamente como vieram do INPE.
RAW_DIR = PROJECT_DIR / "data" / "raw" / "inpe" / "focos"

# Onde salvaremos dados intermediários já convertidos para Parquet.
INTERIM_DIR = PROJECT_DIR / "data" / "interim" / "inpe" / "focos"

# URL base dos arquivos anuais do INPE para Brasil, todos os satélites.
BASE_URL = (
    "https://dataserver-coids.inpe.br/queimadas/queimadas/"
    "focos/csv/anual/Brasil_todos_sats"
)


def download_file(url: str, output_path: Path) -> None:
    """
    Baixa um arquivo da internet e salva localmente.

    Se o arquivo já existir, o download é ignorado para evitar baixar
    o mesmo dado várias vezes.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        logger.info(f"Arquivo já existe, pulando download: {output_path}")
        return

    logger.info(f"Baixando arquivo: {url}")

    response = requests.get(url, timeout=120)
    response.raise_for_status()

    output_path.write_bytes(response.content)

    logger.info(f"Arquivo salvo em: {output_path}")


def ingest_year(year: int) -> Path:
    """
    Baixa o arquivo ZIP anual de focos de queimadas do INPE.
    """
    filename = f"focos_br_todos-sats_{year}.zip"
    url = f"{BASE_URL}/{filename}"
    output_path = RAW_DIR / filename

    download_file(url, output_path)

    return output_path


def extract_csv_from_zip(zip_path: Path) -> Path:
    """
    Extrai o CSV de dentro do arquivo ZIP baixado do INPE.
    """
    extract_dir = zip_path.parent / zip_path.stem
    extract_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Extraindo ZIP: {zip_path}")

    with ZipFile(zip_path, "r") as zip_file:
        csv_files = [
            file_name
            for file_name in zip_file.namelist()
            if file_name.lower().endswith(".csv")
        ]

        if not csv_files:
            raise FileNotFoundError(f"Nenhum CSV encontrado em {zip_path}")

        csv_name = csv_files[0]
        zip_file.extract(csv_name, extract_dir)

    csv_path = extract_dir / csv_name

    logger.info(f"CSV extraído em: {csv_path}")

    return csv_path


def convert_csv_to_parquet(csv_path: Path) -> Path:
    """
    Lê o CSV extraído, padroniza os nomes das colunas e salva em Parquet.
    """
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)

    logger.info(f"Lendo CSV: {csv_path}")

    df = pd.read_csv(csv_path)

    # Padroniza os nomes das colunas para facilitar o tratamento posterior.
    # Exemplo: "DataHora" -> "datahora", "Estado" -> "estado"
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    output_path = INTERIM_DIR / f"{csv_path.stem}.parquet"

    df.to_parquet(output_path, index=False)

    logger.info(f"Parquet salvo em: {output_path}")
    logger.info(f"Total de linhas: {len(df):,}")
    logger.info(f"Total de colunas: {len(df.columns)}")

    return output_path


def main() -> None:
    """
    Executa a ingestão dos anos definidos.
    """
    years = range(2020, 2026)

    for year in years:
        logger.info(f"Iniciando ingestão do ano {year}")

        zip_path = ingest_year(year)
        csv_path = extract_csv_from_zip(zip_path)
        parquet_path = convert_csv_to_parquet(csv_path)

        logger.info(f"Ingestão concluída para {year}: {parquet_path}")


if __name__ == "__main__":
    main()