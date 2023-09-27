from loguru import logger
import json, os
from typing import Optional
from webmeter.core.utils import Common
from webmeter.core.sqlhandle import crud


class TaskBase(object):

    ROOT_DIR = Common.make_dir(os.path.join(os.getcwd(), 'webmeter'))

    @classmethod
    def read_statistics_file(cls, plan: str, task: str) -> dict:
        """read statistics.json content"""
        statistics_file_path = os.path.join(cls.ROOT_DIR, plan, 'report', task,'statistics.json')
        if os.path.exists(statistics_file_path):
            content = Common.read_file_content(statistics_file_path)
            return json.loads(content)
        else:
            logger.warning('No file found')
            return None
        
    @classmethod
    def read_result_file(cls, plan: str, task: str) -> list:
        """read result.jtl content"""
        result_file_path = os.path.join(cls.ROOT_DIR, plan, 'report', task,'result.jtl')
        if os.path.exists(result_file_path):
            content = Common.read_file_lines(result_file_path)
            return content
        else:
            logger.warning('No file found')
            return None

    @classmethod
    def read_log_file(cls, plan: str, task: str) -> Optional[str]:
        """read result.log content"""
        log_dir = os.path.join(cls.ROOT_DIR, plan, 'log')
        if os.path.exists(log_dir):
            log_file_path = os.path.join(log_dir, task,'result.log')
            content = Common.read_file_content(log_file_path)
            return content.strip()
        else:
            logger.warning('No file found')
            return None
        
class TaskDetail(TaskBase):
    
    @classmethod
    def getTestAndReportInfo(cls, plan: str, task: str) -> dict:
        result = dict()
        summary_dict = crud.query_task_one(plan, task)
        result['source_file'] = os.path.join(TaskBase.ROOT_DIR, plan, 'report', task, 'result.jtl')
        result['stime'] = summary_dict.get('stime')
        result['etime'] = summary_dict.get('etime')
        return result
    
    @classmethod
    def getRequestSummary(cls, plan: str, task: str) -> list:
        jtlContent = TaskBase.read_result_file(plan, task)
        jtlContent.pop(0)
        jtlList = [{'lable':item.split(',')[2], 
                    'responseCode':item.split(',')[3],
                    'responseMessage':item.split(',')[4], 
                    'threadName': item.split(',')[5],
                    'failureMessage':item.split(',')[8],
                    'bytes': item.split(',')[9],
                    'sentBytes': item.split(',')[10],
                    'allThreads':item.split(',')[12],
                    'URL': item.split(',')[13]}  for item in jtlContent]
        return jtlList
