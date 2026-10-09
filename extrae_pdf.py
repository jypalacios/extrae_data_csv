#Leer archivo en pdf
import PyPDF2, pandas, fpdf, csv
from fpdf import FPDF


#Define los campos a extraer
fields = ['Paciente', 'Edad', 'Telefono']

pdf_file = open('PACIENTES.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)
num_pages = len(pdf_reader.pages)
for page_num in range(num_pages):
    page = pdf_reader.pages[page_num]
    print(page.extract_text())
pdf_file.close()
#Extrae los campos
for field in fields:
    print(field)
#Guarda los campos en un archivo csv
with open('datos.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(fields)
    
csv_file.close()
