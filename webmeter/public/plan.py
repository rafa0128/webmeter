import os
import shutil
from loguru import logger
from public.utils import Utils

class TestPlan(object):

    def __init__(self):
        self.file_dir = os.path.join(Utils.STATICPATH, 'file')
        self.template_jmx_path = os.path.join(self.file_dir, 'template.jmx')
        self.root_dir = Utils.make_dir(os.path.join(os.getcwd(), 'webmeter'))


    def create(self, plan_name: str) -> str:
        """create new plan"""
        content = Utils.read_file_content(self.template_jmx_path)
        plan_dir = Utils.make_dir(os.path.join(self.root_dir, plan_name))
        plan_path = Utils.make_dir_file(dir=plan_dir, filename='plan.jmx', content=content)
        Utils.write_jmxfile_testname(jmx_path_or_name=os.path.join(self.root_dir, plan_name, 'plan.jmx'),
                                     tag='TestPlan', attr='TestPlan', testname=plan_name)
        logger.info('create plan success: {}'.format(plan_path))
        return plan_path
    
    def isexist(self, plan_name: str) -> bool:
        if os.path.exists(os.path.join(self.root_dir, plan_name)):
            return True
        return False
    
    def edit(self, content: dict) -> None:
        """edit plan content"""
        old_dir = os.path.join(self.root_dir, content['old_name'])
        new_dir = os.path.join(self.root_dir, content['new_name'])
        os.rename(old_dir, new_dir)
        # edit plan info
        element_dict = dict()
        element_dict['TestPlan.comments'] = content['comments']
        element_dict['TestPlan.functional_mode'] = content['functional_mode']
        element_dict['TestPlan.tearDown_on_shutdown'] = content['tearDown_on_shutdown']
        element_dict['TestPlan.serialize_threadgroups'] = content['serialize_threadgroups']
        for key in element_dict.keys():
            Utils.write_jmxfile_text(new_dir, 'stringProp', key, element_dict[key])

    def remove(self, plan: str) -> None:
        """remove one plan"""
        shutil.rmtree(os.path.join(self.root_dir, plan), True)
        logger.info('remove {} success'.format(plan))
    
    def remove_all(self) -> None:
        """remove all plan"""
        dirs = os.listdir(self.root_dir)
        for plan in dirs:
            shutil.rmtree(os.path.join(self.root_dir, plan), True)
            logger.info('remove {} success'.format(plan))

    def get_all_plan(self) -> list:
        """get all plan"""
        dirs = os.listdir(self.root_dir)
        dir_list = reversed(sorted(dirs, key=lambda x: os.path.getmtime(os.path.join(self.root_dir, x))))
        plan_sorted_list = [plan for plan in dir_list]
        plan_list = list()
        for plan in plan_sorted_list:
            plan_dict = dict()
            plan_dict['name'] = plan
            plan_dict['checked'] =True if plan_sorted_list.index(plan) == 0 else False
            plan_list.append(plan_dict)
        return plan_list
    
    def checked_one_plan(self, plan_name) -> list:
        """checked one plan"""
        dirs = os.listdir(self.root_dir)
        dir_list = reversed(sorted(dirs, key=lambda x: os.path.getmtime(os.path.join(self.root_dir, x))))
        plan_sorted_list = [plan for plan in dir_list]
        plan_list = list()
        for plan in plan_sorted_list:
            plan_dict = dict()
            plan_dict['name'] = plan
            plan_dict['checked'] =True if plan == plan_name else False
            plan_list.append(plan_dict)
        return plan_list


    def get_plan_info(self, plan: str) -> dict:
        """get one plan info"""
        plan_jmx_path = os.path.join(self.root_dir, plan, 'plan.jmx')
        result = dict()
        result['name'] = Utils.read_jmxfile_testname(plan_jmx_path, 'TestPlan', 'TestPlan')
        result['comments'] = Utils.read_jmxfile_text(plan_jmx_path, 'stringProp', 'TestPlan.comments')
        result['functional_mode'] = Utils.MAPPING.get(
            Utils.read_jmxfile_text(
            jmx_path_or_name=plan_jmx_path, 
            tag='boolProp', 
            name='TestPlan.functional_mode'))
        result['tearDown_on_shutdown'] = Utils.MAPPING.get(
            Utils.read_jmxfile_text(
            jmx_path_or_name=plan_jmx_path,
            tag='boolProp', 
            name='TestPlan.tearDown_on_shutdown'))
        result['serialize_threadgroups'] = Utils.MAPPING.get(
            Utils.read_jmxfile_text(
            jmx_path_or_name=plan_jmx_path, 
            tag='boolProp', 
            name='TestPlan.serialize_threadgroups'))
        return result