from fastapi import APIRouter, HTTPException
from repository.mongo_client import get_connection, DocumentDBClient
from service.save_info import SaveInfo
from service.get_info import GetInfo
from uuid import uuid4
from typing import Dict
from pydantic import BaseModel
import asyncio

router = APIRouter()

websites_db = DocumentDBClient(get_connection(), 'scraping_similarweb')

# Como é um teste, mock apenas para simular o banco de dados das operações
operations_db: Dict[str, Dict[str, str]] = {}


class OperationStatus(BaseModel):
    status: str


async def async_save_info(url: str, operation_id: str):
    try:
        simlar_url = f"https://www.similarweb.com/website/{url}"
        s_info = SaveInfo(simlar_url, websites_db)
        await s_info.save()
        operations_db[operation_id] = {"status": "Concluído com sucesso"}
    except Exception as e:
        operations_db[operation_id] = {"status": f"Falhou: {str(e)}"}


@router.post("/salve_info/{url}", status_code=201)
async def save_info(url: str):
    operation_id = str(uuid4())
    operations_db[operation_id] = {"status": "Em Progresso"}

    asyncio.create_task(async_save_info(url, operation_id))

    return {
        "operation_id": operation_id,
        "check_status": f"/operation_status/{operation_id}"
    }


@router.post("/get_info/{url}")
async def get_info(url: str):
    try:
        g_info = GetInfo(websites_db)
        return g_info.get_info(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting data: {e}")


@router.get("/operation_status/{operation_id}", response_model=OperationStatus)
def get_operation_status(operation_id: str):
    operation_status = operations_db.get(operation_id)
    if not operation_status:
        raise HTTPException(status_code=404, detail="ID não encontrato")
    return operation_status
