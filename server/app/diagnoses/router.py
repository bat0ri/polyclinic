from fastapi import APIRouter, Depends, HTTPException
from app.diagnoses.repository import DiagnoseRepo
from config import get_async_session
from app.diagnoses.model import Diagnosis
from app.diagnoses.schemas import CreateDiagnose, UpdateDiagnose
from auth.security import JWTBearer, RoleBasedJWTBearer


diagnose_route = APIRouter()


@diagnose_route.post("/create_new", dependencies=[Depends(RoleBasedJWTBearer())])
async def create_new_diagnose(diagnose_data: CreateDiagnose, repo: DiagnoseRepo = Depends(DiagnoseRepo)):
    _new = Diagnosis(
            name=diagnose_data.name,
            description=diagnose_data.description
        )
    new_diagnose = await repo.insert(_new)
    await repo.close()
    return new_diagnose

@diagnose_route.get("/get_all")
async def get_all_diagnoses(repo: DiagnoseRepo = Depends(DiagnoseRepo)):
    return await repo.get_all()

@diagnose_route.get("/get_by_id/{item_id}")
async def get_diagnose_by_id(item_id: int, repo: DiagnoseRepo = Depends(DiagnoseRepo)):
    diagnose = await repo.get_by_id(item_id)
    if not diagnose:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return diagnose

@diagnose_route.patch("/update", dependencies=[Depends(RoleBasedJWTBearer())])
async def update_diagnose_by_id(item_id: int, values: UpdateDiagnose, repo: DiagnoseRepo = Depends(DiagnoseRepo)):
    try:
        values_dict = values.dict(exclude_unset=True)  
        await repo.update(item_id=item_id, values=values_dict) 
        await repo.close()
        return {"status_code": 200, "detail": "обновлен"}
    except Exception as e:
        return {"status_code": 500, "detail": f"Не удалось обновить: {str(e)}"}

@diagnose_route.delete("/delete", dependencies=[Depends(RoleBasedJWTBearer())])
async def delete_diagnose_by_id(item_id: int, repo: DiagnoseRepo = Depends(DiagnoseRepo)):
    try:
        await repo.drop(item_id=item_id)
        await repo.close()
        return HTTPException(status_code=200, detail="диагноз удален")
    except:
        return HTTPException(status_code=500, detail="не удалось удалить дигноз")
