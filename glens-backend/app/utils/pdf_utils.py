import camelot
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=2)

def _extract_pdf(file_path, pages='all'):
    tables = camelot.read_pdf(file_path, pages=pages)
    all_rows = []
    for table in tables:
        df = table.df
        for i in range(len(df)):
            row = {str(j): df.iloc[i, j] for j in range(len(df.columns))}
            all_rows.append(row)
    return all_rows

async def extract_table_data(file_path, pages='all'):
    if isinstance(file_path, list):
        file_path = file_path[0] if file_path else None
    if not file_path:
        raise ValueError("File path must be a valid PDF path.")
    
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, _extract_pdf, file_path, pages)
