#!/usr/bin/env python3
"""
"""
__author__ = "Bruno Chiconato"
__version__ = "0.0.1"

import os
import sys

import camelot  # type: ignore
import matplotlib  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import pandas as pd

python_base = sys.base_prefix

os.environ["TCL_LIBRARY"] = os.path.join(python_base, "tcl", "tcl8.6")
os.environ["TK_LIBRARY"] = os.path.join(python_base, "tcl", "tk8.6")


def show_pdf_countour(
    file_name: str, pages: str, table_areas: list[str], columns: list[str]
) -> None:
    """
    Reads a PDF file, extracts table data using Camelot's "stream" flavor, and
    plots the contour of the detected table.

    Args:
        file_name (str): The name of the PDF file (without extension) to process.
                         The file is assumed to be located in a folder named 'pdf'.
        pages (str): A string specifying the pages of the PDF to process (e.g., "1", "1,3", "1-5").
        table_areas (list[str]): A list of table areas specified in the format ["x1,y1,x2,y2"].
                                 Each entry defines the bounding box of a table on the page.
        columns (list[str]): A list of strings specifying the column separators in the format ["x1,x2,..."].

    Returns:
        None: This function displays the parsing report and a contour plot of the detected table.

    Raises:
        FileNotFoundError: If the specified PDF file does not exist in the 'pdf' folder.
        CamelotError: If Camelot fails to process the PDF.

    Notes:
        - The function uses Camelot's "stream" flavor for table detection.
        - The contour plot provides a visual representation of the detected table's structure.
        - Requires the `Camelot` and `matplotlib` libraries to be installed.
    """
    path = os.path.abspath(f"pdf/{file_name}.pdf")

    pages = camelot.read_pdf(
        path, pages=pages, flavor="stream", table_areas=table_areas, columns=columns
    )

    print(pages[0].parsing_report)

    camelot.plot(pages[0], kind="contour")
    plt.show()


def pdf_to_df(
    file_name: str, pages: str, table_areas: list[str], columns: list[str]
) -> pd.DataFrame:
    """
    Extracts table data from a specified PDF file and returns it as a pandas DataFrame.

    Args:
        file_name (str): The name of the PDF file (without extension) to process.
                         The file is assumed to be located in a folder named 'pdf'.
        pages (str): A string specifying the pages of the PDF to process (e.g., "1", "1,3", "1-5").
        table_areas (list[str]): A list of table areas specified in the format ["x1,y1,x2,y2"].
                                 Each entry defines the bounding box of a table on the page.
        columns (list[str]): A list of strings specifying the column separators in the format ["x1,x2,..."].

    Returns:
        pd.DataFrame: A pandas DataFrame containing the extracted table data from the first detected table.

    Raises:
        FileNotFoundError: If the specified PDF file does not exist in the 'pdf' folder.
        CamelotError: If Camelot fails to process the PDF.

    Notes:
        - The function uses Camelot's "stream" flavor for table detection.
        - Only the first detected table is returned as a DataFrame.
        - Requires the `Camelot` and `pandas` libraries to be installed.
    """
    path = os.path.abspath(f"pdf/{file_name}.pdf")

    pages = camelot.read_pdf(
        path, pages=pages, flavor="stream", table_areas=table_areas, columns=columns
    )

    return pages[0].df


def process_raw_pdf_model1(file_name: str, raw_pdf: pd.DataFrame) -> pd.DataFrame:
    """
    Processes a raw DataFrame extracted from a PDF into a structured format, adding segment headers,
    values, and categorized date labels.

    Args:
        file_name (str): The name of the PDF file (used to generate date labels).
        raw_pdf (pd.DataFrame): The raw DataFrame extracted from the PDF, where each row corresponds
                                to data extracted from the PDF.

    Returns:
        pd.DataFrame: A processed DataFrame with the following columns:
            - "Segmentos": Repeated headers indicating segments in the data.
            - "Valor": Values extracted from valid lines of the raw DataFrame.
            - "Data e categoria": Date labels concatenated with predefined categories.

    Process:
        1. Extracts valid lines from the raw DataFrame, skipping every alternate line.
        2. Strips and processes headers from the second column of the raw DataFrame.
        3. Generates values by extracting non-empty data from valid lines.
        4. Constructs a "Segmentos" column by repeating headers to match the number of values.
        5. Generates date labels by combining the file name's date prefix with predefined labels.
        6. Assembles the processed data into a new DataFrame.

    Raises:
        ValueError: If the raw DataFrame does not contain data in the expected format.

    Notes:
        - The function assumes specific patterns for segment headers and data rows.
        - Requires `pandas` to be installed.
    """
    pdf_total_lines = raw_pdf.shape[0]
    valid_lines_indexes = list(range(0, pdf_total_lines, 2))

    headers = [header.strip() for header in raw_pdf[1] if header != ""]
    values = []
    labels = ["(A)", "(B)", "(C)", "(D)", "(E)"]
    date_labels = [f"{file_name[:8]}" + label for label in labels]

    for valid_line_index in valid_lines_indexes:
        for valid_lines in raw_pdf.iloc[valid_line_index]:
            if valid_lines != "":
                values.append(valid_lines)

    values_per_headers = len(values) // len(headers)
    date_labels_per_rows = len(values) // len(date_labels)

    segments = [header for header in headers for _ in range(values_per_headers)]

    date_labels_column = date_labels * date_labels_per_rows

    processed_pdf = pd.DataFrame(
        {"Segmentos": segments, "Valor": values, "Data e categoria": date_labels_column}
    )

    return processed_pdf


def processed_pdf_to_csv(
    data_path: str, file_name: str, processed_pdf: pd.DataFrame
) -> None:
    """
    Saves a processed DataFrame to a CSV file in a specified directory.

    Args:
        data_path (str): The directory where the CSV file will be saved.
                         If the directory does not exist, it will be created.
        file_name (str): The name of the CSV file (without extension).
        processed_pdf (pd.DataFrame): The processed DataFrame to be saved.

    Returns:
        None: The function saves the DataFrame to a CSV file but does not return any value.

    Raises:
        ValueError: If the DataFrame is empty or any of the inputs are invalid.
        OSError: If there is an issue creating the directory or writing the file.
    """
    if not isinstance(data_path, str) or not data_path.strip():
        raise ValueError("The 'data_path' must be a non-empty string.")
    if not isinstance(file_name, str) or not file_name.strip():
        raise ValueError("The 'file_name' must be a non-empty string.")
    if processed_pdf.empty:
        raise ValueError("The DataFrame 'processed_pdf' is empty and cannot be saved.")

    try:
        os.makedirs(data_path, exist_ok=True)
    except OSError as e:
        raise OSError(f"Failed to create directory {data_path}: {e}")

    file_path = os.path.join(data_path, f"{file_name}.csv")

    try:
        processed_pdf.to_csv(file_path, sep=",", encoding="utf-8", index=False)
        print(f"File saved successfully at: {file_path}")
    except Exception as e:
        raise OSError(f"Failed to save file {file_path}: {e}")
