import fitz
from tkinter import PhotoImage

class PDFMiner:
	def __init__(self, filepath):
		self.filepath = filepath
		self.pdf = fitz.open(self.filepath)

	def get_metadata(self):
		metadata = self.pdf.metadata
		numPages = self.pdf.pageCount

		return metadata, numPages