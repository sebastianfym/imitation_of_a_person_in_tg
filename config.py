import os
from dotenv import load_dotenv
from pyrogram import Client
from loguru import logger


load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")


api_hash = os.environ.get("API_HASH")
api_id = os.environ.get("API_ID")

client = Client(name="my_account", api_hash=api_hash, api_id=api_id)

logger.add("message.log", rotation="500 MB", level="INFO")