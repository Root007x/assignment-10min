from pdf2image import convert_from_path
import pytesseract
import pdfplumber
import unicodedata
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.config.config import PY_TESSERACT_LOCATION, DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP
from src.utils.logger import logger
from src.utils.custom_exception import CustomException


pytesseract.pytesseract.tesseract_cmd = PY_TESSERACT_LOCATION

logger = logger(__name__)

class ProcessData:
    
    def __init__(self):
        pass
    
    # data extraction
    def extract_raw_data(self):
        # Convert PDF to Images
        try:
            logger.info("Converting PDF into Images.......")
            pages = convert_from_path(
                            pdf_path=DATA_PATH, 
                            dpi=300,
                            fmt = "png",
                            thread_count=4,
                            grayscale=False,
                            use_cropbox=False,
                            strict=False
                    )
            
            logger.info("PDF to Image process Done")
            logger.info("Converting Image to Text.........")
            # Convert Images to Text
            raw_text = ""
            table_number = [2, 41]

            for i,page in  enumerate(pages):
                if i in table_number:
                    with pdfplumber.open(DATA_PATH) as pdf:
                        table_page = pdf.pages[i - 1]  # select page
                        tables = table_page.extract_tables()

                        for table in tables:
                            raw_text += "উপরে দেওয়া প্রশ্নগুলোর সঠিক উত্তরগুলো প্রশ্ন নম্বর অনুযায়ী দেওয়া আছে, যেমন ‘১’, ‘ক’ (SL, ANS)" + '\n'
                            for row in table:
                                raw_text += str(row) + '\n'
                    
                text = pytesseract.image_to_string(page, lang ="ben+eng", config='--psm 6 --oem 1')
                raw_text += text
                
            logger.info("Image to Text process Done")
            
            return raw_text
        
        except Exception as e:
            error = CustomException("Failed to extract raw data",e)
            logger.error(str(error))
        
    
    # Data normalize
    def normalize_text(self,raw_text):
        return unicodedata.normalize("NFC",raw_text)
    
    # Make document object
    def convert_document_object(self, cleaned_text):
        cleaned_doc = Document(page_content=cleaned_text, metadata={"source": "HSC26-Bangla1st-Paper.pdf"})
        return cleaned_doc
        
    
    # convert into chunk
    def convert_into_chunk(self, cleaned_doc):
        text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size = CHUNK_SIZE,
                        chunk_overlap = CHUNK_OVERLAP,
                        separators=["\n\n", "\n", " ", ""]
                    )
        
        chunks = text_splitter.split_documents([cleaned_doc])
        
        return chunks