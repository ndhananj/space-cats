import fitz  # PyMuPDF

input_file = 'A_Hybrid_Air_Quality_Prediction_Model_Based_on_Empirical_Mode_Decomposition.pdf'


def extract_text_from_pdf(input_file_path):
	doc = fitz.open(input_file_path)
	out = open("output.txt", "wb")
	for page in doc:
		text = page.get_text().encode("utf8")
		out.write(text)
		out.write(bytes((12,)))  # write page delimiter (form feed 0x0C)
	out.close()


# extract_text_from_pdf(input_file)

