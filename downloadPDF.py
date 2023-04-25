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

import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
import base64
from IPython.display import HTML, display

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# create a sample dataframe
data = {'Name': ['John', 'Jane', 'Bob'], 'Age': [30, 25, 40], 'Gender': ['M', 'F', 'M']}
df = pd.DataFrame(data)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# create a buffer to hold the generated PDF
buffer = BytesIO()

# create a PDF object
pdf = SimpleDocTemplate(buffer, pagesize=letter)

# create a table from the dataframe
table_data = [df.columns.tolist()] + df.values.tolist()
table = Table(table_data)

# add the table to the PDF
pdf.build([table])

# reset the buffer position to the beginning
buffer.seek(0)

# encode the PDF in base64 for download
b64 = base64.b64encode(buffer.getvalue()).decode()

# create a link to download the PDF file
link = '<a href="data:application/pdf;base64,{0}" download="dataframe.pdf">Download PDF</a>'.format(b64)

# display the link
display(HTML(link))
