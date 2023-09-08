from loguru import logger
from typing import Union
from fastapi import APIRouter, Response, Cookie, UploadFile, File, Form
from core.plan import TestPlan
from core.engine import EngineServie
from core.sqlhandle import crud, models, schemas
from core.sqlhandle.database import engine
router = APIRouter()
test_plan = TestPlan()
models.Base.metadata.create_all(bind=engine)


@router.post("/api/initialize")
async def initialize(keys: schemas.keyCreate):
   try:
      crud.create_key(keys=keys)
      result = {'status':1, 'msg': 'success'}
   except Exception as e:
      logger.exception(e)
      result = {'status':0, 'msg': str(e)}
   return result

# @router.post("/api/language/set")
# async def set_language(content: dict, response:Response):
#    try:
#       language = content.get('language')
#       response.set_cookie(key="language",value=language)
#       result = {'status':1, 'msg': 'Change the language to {}'.format(language)}
#    except Exception as e:
#       logger.exception(e)
#       result = {'status':0, 'msg': str(e)}
#    return result

@router.post("/api/language/set")
async def set_language(keys: schemas.keyUpdate):
   try:
      crud.update_value(keys=keys)
      result = {'status':1, 'msg': 'Change the language to {}'.format(keys.value)}
   except Exception as e:
      logger.exception(e)
      result = {'status':0, 'msg': str(e)}
   return result

# @router.post("/api/sql/language/get")
# async def get_sql_language(keys: schemas.keyQuery):
#    try:
#       value = crud.query_key(keys)
#       result = {'status':1, 'msg': 'success', 'language': value}
#    except Exception as e:
#       logger.exception(e)
#       result = {'status':0, 'msg': str(e)}
#    return result

@router.post("/api/language/get")
async def get_language(keys: schemas.keyQuery):
   try:
      value = crud.query_key(keys)
      result = {'status':1, 'msg': 'success', 'language': value}
   except Exception as e:
      logger.exception(e)
      result = {'status':0, 'msg': str(e)}
   return result

@router.post("/api/plan/all")
async def get_all_plan():
   try:
      plan_list = test_plan.get_all_plan()
      result = {'status':1, 'plan_list':plan_list, 'length':len(plan_list), 'msg': 'get success'}
   except Exception as e:
      logger.exception(e)
      result = {'status':0, 'msg': str(e)}
   return result

@router.post("/api/plan/checked")
async def checked_one_plan(content: dict):
   plan_name = content.get('plan_name')
   try:
      plan_list = test_plan.checked_one_plan(plan_name)
      result = {'status':1, 'plan_list':plan_list, 'length':plan_list.__len__(), 'msg': 'get success'}
   except Exception as e:
      logger.exception(e)
      result = {'status':0, 'msg': str(e)}
   return result


@router.post("/api/plan/info")
async def get_plan_info(content: dict):
   plan_name = content.get('plan_name')
   try:
      plan_info = test_plan.info(plan_name)
      result = {'status':1, 'plan_info':plan_info, 'msg': 'get success'}
   except Exception as e:
      logger.exception(e)
      result = {'status':0, 'msg': str(e)}
   return result

@router.post("/api/plan/create")
async def create_plan(content: dict):
   plan_name = content.get('plan_name')
   try:
      logger.info(plan_name)
      if not test_plan.isexist(plan_name):
         test_plan.create(plan_name)
         result = {'status':1, 'msg': 'create success'}
      else:
         result = {'status':0, 'msg': 'plan existed'}   
   except Exception as e:
      logger.exception(e)
      result = {'status':0, 'msg': str(e)}
   return result

@router.post("/api/plan/import")
async def import_plan(file:UploadFile = File(...), plan_name:str = Form(...)):
   try:
      if not test_plan.isexist(plan_name):
         test_plan.import_jmx(file, plan_name)
         result = {'status':1, 'msg': 'import success'}
      else:
         result = {'status':0, 'msg': 'plan existed'}   
   except Exception as e:
      logger.exception(e)
      result = {'status':0, 'msg': str(e)}
   return result

@router.post("/api/plan/remove")
async def remove_plan(content: dict):
   plan_name = content.get('plan_name')
   try:
      test_plan.remove(plan_name)
      result = {'status':1, 'msg': 'remove success'}   
   except Exception as e:
      logger.exception(e)
      result = {'status':0, 'msg': str(e)}
   return result

@router.post("/api/plan/removeall")
async def remove_all_plan():
   try:
      test_plan.remove_all()
      result = {'status':1, 'msg': 'remove success'}   
   except Exception as e:
      logger.exception(e)
      result = {'status':0, 'msg': str(e)}
   return result

@router.post("/api/plan/save")
async def save_plan(content: dict):
   try:
      test_plan.edit(content)
      result = {'status':1, 'msg': 'save success'}   
   except Exception as e:
      logger.exception(e)
      result = {'status':0, 'msg': str(e)}
   return result


@router.post("/api/plan/run")
async def run_plan(content: dict):
   try:
      EngineServie.run(content=content, remote=False)
      result = {'status':1, 'msg': 'run success'}   
   except Exception as e:
      logger.exception(e)
      result = {'status':0, 'msg': str(e)}
   return result