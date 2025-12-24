# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import re
import logging
from typing import Dict, List, Optional, Tuple
import json
app = FastAPI(
    title="Игра «Найди свой ОКВЭД по номеру телефона»",
    description="API для поиска ОКВЭД по окончанию российского мобильного номера.",
    version="1.0.0"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_okved_data() -> None:
    global OKVED_DATA
    try:
        with open("okved.json", "r", encoding="utf-8") as f:
            OKVED_DATA = json.load(f)
        logger.info(f"Загружено {len(OKVED_DATA)} записей ОКВЭД")
    except Exception as e:
        logger.error(f"Ошибка загрузки okved.json: {e}")
        raise RuntimeError("Не удалось загрузить данные ОКВЭД")


def normalize_phone(phone: str) -> Optional[str]:

    # Удаляем все нецифровые символы
    digits = re.sub(r'\D', '', phone.strip())

    # Возможные префиксы
    if digits.startswith('79') and len(digits) == 11:
        return '+7' + digits[1:]
    elif digits.startswith('9') and len(digits) == 10:
        return '+79' + digits
    elif digits.startswith('89') and len(digits) == 11:
        return '+7' + digits[1:]
    elif digits.startswith('8') and len(digits) == 11:
        return '+7' + digits[1:]
    elif digits.startswith('7') and len(digits) == 11:
        return '+' + digits
    else:
        return None


def find_best_okved(suffix: str) -> Optional[Tuple[str, str, int]]:

    best_match: Optional[Tuple[str, str, int]] = None
    max_len = 0

    for entry in OKVED_DATA:
        phone_end = entry.get("phone_end", "")
        if suffix.endswith(phone_end):
            length = len(phone_end)
            if length > max_len or (length == max_len and length == len(suffix)):  # приоритет полному совпадению
                max_len = length
                best_match = (entry.get("code", ""), entry.get("name", ""), length)

    return best_match


def fallback_strategy() -> Tuple[str, str, int]:

    return ("62.01", "Разработка компьютерного ПО (вы загадочный программист!)", 0)


class PhoneInput(BaseModel):
    phone: str


class OkvedResponse(BaseModel):
    normalized_phone: Optional[str] = None
    okved_code: str
    okved_name: str
    match_length: int
    error: Optional[str] = None


@app.on_event("startup")
def startup_event():
    load_okved_data()


@app.post("/find-okved", response_model=OkvedResponse)
def find_okved(request: PhoneInput):

    normalized = normalize_phone(request.phone)

    if not normalized:
        raise HTTPException(status_code=400,
                            detail="Не удалось нормализовать номер телефона. Убедитесь, что это российский мобильный номер.")

    suffix = normalized[2:]

    match = find_best_okved(suffix)

    if match:
        code, name, length = match
    else:
        code, name, length = fallback_strategy()

    return OkvedResponse(
        normalized_phone=normalized,
        okved_code=code,
        okved_name=name,
        match_length=length
    )


@app.get("/")
def root():
    return {
        "message": "Добро пожаловать в игру «Найди свой ОКВЭД по номеру телефона»! Отправьте POST /find-okved с полем 'phone'."}