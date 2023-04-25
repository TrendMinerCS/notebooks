# Suggested data science package imports
import pandas as pd
import numpy as np

from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt

# TrendMiner package import
import trendminer
from trendminer.trendminer_client import TrendMinerClient

import os

token = os.environ["KERNEL_USER_TOKEN"]
serverUrl = os.environ["KERNEL_SERVER_URL"]

# Create TrendMiner API object
client = TrendMinerClient(token, serverUrl)

!pip install reportlab

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import matplotlib.pyplot as plt
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen import canvas
import requests

# # # # # # # # # # # # MODIFY CONTEXT_ITEM ID AND DATA BELOW # # # # # # # # # # # # # # # # # # # 

context_item = '228173ad-d8b8-40cf-8b0b-29abaedf26c1'

df = pd.DataFrame({'Name': ['John', 'Mary', 'Peter'], 'Age': [30, 25, 35], 'City': ['New York', 'London', 'Paris']})
data = df.values.tolist()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

dt_string = (datetime.now()).strftime("%d-%m-%Y--%H-%M-%S")

extension = 'pdf'
pdf_filename = f'daily-report-date-{dt_string}.{extension}'
name, extension = pdf_filename.split(".")

# Create a PDF file
doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
elements = []

# Add the table to the PDF file
style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)])

table = Table(data)
table.setStyle(style)
elements.append(table)

# Build the PDF file
doc.build(elements)

try:
    files = {'file': (pdf_filename, open(pdf_filename, 'rb'), f'application/{extension}')}
    os.remove(pdf_filename)
    auth_header = {'Authorization':("Bearer " + token), 'Content-type':'application/octet-stream'}
    r = requests.post(f"{serverUrl}/context/data/{context_item}/attachments", headers=auth_header, files=files, params={"name": name, "extension": extension})
except:
    print(f"File '{pdf_filename}' does not exist.")
