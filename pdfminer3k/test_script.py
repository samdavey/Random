# Runs a simple test of the PDF_Parser to extract the DPF text into a text file

# requires library pdfminer3k
# get it with:
# cmd> pip install pdfminer3k
print('Importing the parser')
from PDF_Parser import Parser

# open a pdf file to read in
# 'r+b' means open for reading (r) in binary mode (+b) so we don't have to worry about charactermaps (utf-8 etc)
print('Opening the test input file ', 'test.pdf.')
infile = open('test.pdf', 'r+b')

# Open an output file - where we're going to save the text
print('Opening the file to extract the pdf text to ', 'test_output1.txt')
outfile = open('test_output1.txt', 'w', encoding='utf-16')

# make a new parser class onbject
p = Parser()

# load the pdf into the parser
print('Parsing the PDF.')
p.load(infile)

# Once loaded, extract the text to the specified file
print('Extracting the PDF text to file.')
p.save_text_to_file(outfile)

# close the output file to write the text and clear the buffer
outfile.close()

# job done.
print('Done! Exiting.')
