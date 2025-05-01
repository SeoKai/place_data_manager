import mysql.connector
from config.db_config import DB_CONFIG

def get_connection():
    """MySQL 연결"""
    return mysql.connector.connect(**DB_CONFIG)
