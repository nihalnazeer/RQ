from fastapi import FastAPI
import logging

def setup_logging(app: FastAPI):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
