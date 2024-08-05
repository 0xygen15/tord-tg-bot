from aiogram import Bot
from data.config import API_TOKEN

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

bot = Bot(token=API_TOKEN) #create bot instance