from pypdf import PdfReader
from app.core.airlogger import logger
from io import BytesIO


class FileLogic:
    @staticmethod
    def validate_file_offline(filename: str, savepath: str) -> int:
        number_of_pages = -1
        try:
            reader = PdfReader(savepath + "/" + filename)
            number_of_pages = len(reader.pages)
        except Exception as ex:
            logger.error(f"File Could not be opened {filename}")
            number_of_pages = -1
        logger.info(f"PDF File uploaded contains {number_of_pages} pages")
        return number_of_pages

    @staticmethod
    def validate_file_online(filename: str, filestream: BytesIO) -> int:
        try:
            _pdf = PdfReader(filestream)
            number_of_pages = len(_pdf.pages)
        except Exception as ex:
            logger.error(f"File Could not be opened {filename}")
            number_of_pages = -1
        logger.info(f"PDF File uploaded contains {number_of_pages} pages")
        return number_of_pages
