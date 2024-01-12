import fitz  # PyMuPDF
import os
import re

INPUT_DIRECTORY = 'LABLAB'

file_one = 'A_Hybrid_Air_Quality_Prediction_Model_Based_on_Empirical_Mode_Decomposition.pdf'
file_two = 'Heating-Cooling_Monitoring_and_Power_Consumption_Forecasting_Using_LSTM_for_Energy-Efficient_Smart_Management_of_Buildings_A_Computational_Intelligence_Solution_for_Smart_Homes.pdf'
file_three = 'Malware_Evasion_Attacks_Against_IoT_and_Other_Devices_An_Empirical_Study.pdf'
file_four = 'UTF-8_Futech2024-03-01-02_Habib.pdf'
file_five = 'UTF-8_Futech2024-03-01-04_Safarishaal.pdf'


class TextExtractor:
    def __init__(self):
        self.text = ''
        self.file_name = ''

    def extract_text_from_pdf(self, input_pdf_path):
        self.file_name = os.path.basename(input_pdf_path)
        doc = fitz.open(input_pdf_path)
        for page in doc:
            self.text += page.get_text(sort=True).encode("utf8").decode("utf8")

    def save_txt(self, name):
        file_name = f'{name}.txt'
        save_location = os.path.join('postprocessing', file_name)
        try:
            with open(save_location, 'w+', encoding='utf-8') as file:
                file.write(self.text)
        except UnicodeDecodeError as e:
            print(e)

# input_file = os.path.join(INPUT_DIRECTORY, file_one)
# text_extractor = TextExtractor(input_file)
# text_extractor.extract_text_from_pdf()
# print(text_extractor.text)