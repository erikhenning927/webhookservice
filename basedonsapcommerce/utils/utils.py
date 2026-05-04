import os
from datetime import datetime
from zoneinfo import ZoneInfo  

BR_ZONE = ZoneInfo("America/Sao_Paulo")

def parse_order_date(raw_date):
    if not raw_date:
        return {"datetime": None}
    timestamp = int(raw_date.strip("/Date()\\/")) / 1000
    order_date = datetime.fromtimestamp(timestamp, tz=BR_ZONE)
    formatted_date = order_date.strftime("%Y-%m-%d %H:%M:%S")
    date_only = order_date.strftime("%Y-%m-%d")
    time_only = order_date.strftime("%H:%M:%S")
    return {
        "datetime": order_date,
        "formatted_date": formatted_date,
        "date_only": date_only,
        "time_only": time_only
    }

def commerce_date(creationTime, modifiedTime):
    parsed_creationDate = parse_order_date(creationTime)
    parsed_modifiedtime = parse_order_date(modifiedTime)
    creationDate_date = parsed_creationDate["date_only"]
    creationDate_time = parsed_creationDate["time_only"]
    modifiedtime_date = parsed_modifiedtime["date_only"]
    modifiedtime_time = parsed_modifiedtime["time_only"]
    return {
        "creationDate": creationDate_date,
        "modifiedDate": modifiedtime_date,
        "creationTime": creationDate_time,
        "modifiedTime": modifiedtime_time
    }

def load_sql(filename, folder):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sql_path = os.path.join(base_dir, 'SQL', folder, filename)
    
    with open(sql_path, 'r', encoding='utf-8') as file:
        return file.read()

def commerce_boolean(value):
    if value is not None:
        value = 1 if value else 0
    return value

def commerce_collection(atr, var1=None, var2=None):
    if atr is not None:
        collection = atr.get("localizedAttributes", {}).get("results", {})
        for col in collection:
            var1 = atr.get("code", None)
            var2 = col.get("name", None)
    return var1, var2

def load_events_from_txt(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as f:
        events = [line.strip() for line in f if line.strip()]  # remove espaços/linhas vazias
    return events