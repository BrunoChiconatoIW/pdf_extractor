#!/usr/bin/env python3
"""
"""
__author__ = "Bruno Chiconato"
__version__ = "0.0.1"

import os

import camelot  # type: ignore
import matplotlib  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import pandas as pd  # type: ignore
import sqlalchemy  # type: ignore
from dotenv import load_dotenv

from funcs.pdf_extractor import (
    pdf_to_df,
    process_raw_pdf_model1,
    processed_pdf_to_csv,
    show_pdf_countour,
)


def main():
    file_name = "2024_10_02"
    output_path = "./data/"
    pages = "1"
    table_areas = ["65, 674, 390, 492"]
    columns = ["65, 138, 184, 232, 288, 338, 492"]

    # show_pdf_countour(file_name,pages,table_areas,columns)
    raw_pdf = pdf_to_df(file_name, pages, table_areas, columns)
    processed_pdf = process_raw_pdf_model1(file_name, raw_pdf)
    processed_pdf_to_csv(
        data_path=output_path, file_name=file_name, processed_pdf=processed_pdf
    )


if __name__ == "__main__":
    main()
