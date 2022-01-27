from pathlib import Path

from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# for postgresql
PG_USER = env.str("PG_USER")
PG_PASSWORD = env.str("PG_PASSWORD")
PG_NAME = env.str("PG_NAME")
PG_HOST = env.str("PG_HOST")

# GINO
DATABASE = env.str("DATABASE")
POSTGRES_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{IP}/{DATABASE}"
