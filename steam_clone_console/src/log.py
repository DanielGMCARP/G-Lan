import logging

def configurar_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("steam_clone.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()