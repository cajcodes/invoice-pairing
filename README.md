# PDF Merger and Text Extraction Tool

## Overview

I tasked GPT-4 with automating the tedious task of identifying and combining relevant pages from separate PDFs. 
This Python script it produced offers a solution to merge specific pages from two PDF files based on text extraction and pattern matching.

## Key Features:

Text Extraction: It employs pytesseract and pdf2image to extract text from PDF pages, enabling content analysis.
Pattern Matching: Leveraging regular expressions, the script identifies specific data patterns within the extracted text, such as location and work order numbers.
PDF Merging: Using PyPDF2, it merges targeted pages from two PDFs into a new file, facilitating organized record-keeping.
Multithreading: With concurrent.futures, the script processes multiple pages concurrently, enhancing efficiency for large documents.
