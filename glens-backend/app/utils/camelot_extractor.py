import camelot

def extract_table_data(file_path, pages='all'):
    # Ensure that file_path is a string (path to a single PDF file), not a list
    if isinstance(file_path, list):
        file_path = file_path[0] if file_path else None  # Use the first file path in the list

    # If file_path is None or an empty string, raise an error
    if not file_path:
        raise ValueError("File path must be a valid string representing the path to the PDF file.")

    # Extract tables from the PDF
    tables = camelot.read_pdf(file_path, pages=pages)

    all_rows = []

    # Loop through each table found
    for table in tables:
        df = table.df
        # Convert each row of the table to a dictionary (key = column index, value = cell content)
        for i in range(len(df)):
            row = {str(j): df.iloc[i, j] for j in range(len(df.columns))}
            all_rows.append(row)

    return all_rows


def main():
    file_path = r"input\GLE004264_CERIM-1.6KL.pdf"
    # file_path = r"input\GLE004106_AE-500L_JKTD VST.pdf"
    # file_path = r"input\GLE004156-2 R0_AERIM-1KL.pdf"
    # file_path = r"input\GLE004109_CERTM-10KL.pdf"
    tables = camelot.read_pdf(file_path,pages='all',parallel=True)
    
    tables.export(r"output\camelot_drawing.json", f='json',compress=False)  

if __name__ == "__main__":
    main()