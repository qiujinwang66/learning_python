import os

from django.core.exceptions import ObjectDoesNotExist

from .models import TestCase, Module, Project, DebugTalk,TestConfig
from .utils import dump_python_file, dump_yaml_file


def run_by_single(index, base_url, path):
    """
    加载单个case用例信息
    :param index: int or str：用例索引
    :param base_url: str：环境地址
    :return: dict
    """
    config = {
        'config': {
            'name': '',
            'base_url': base_url
        }
    }
    testcase_list = []

    testcase_list.append(config)

    try:
        obj = TestCase.objects.get(id=index)
    except ObjectDoesNotExist:
        return testcase_list

    include = eval(obj.include)
    request = eval(obj.request)
    name = obj.name
    project = obj.belong_project
    module = obj.belong_module.module_name

    config['config']['name'] = name

    
    testcase_dir_path = path
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

        try:
            debugtalk = DebugTalk.objects.get(belong_project__project_name=project).debugtalk
        except ObjectDoesNotExist:
            debugtalk = ''

        dump_python_file(os.path.join(testcase_dir_path, 'debugtalk.py'), debugtalk)
    testcase_dir_path = os.path.join(path, project)
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
    testcase_dir_path = os.path.join(testcase_dir_path, module)

    if not os.path.exists(testcase_dir_path):
        os.mkdir(testcase_dir_path)

    for test_info in include:
        try:
            if isinstance(test_info, dict):
                config_id = test_info.pop('config')[0]
                config_request = eval(TestConfig.objects.get(id=config_id).request)
                print(base_url)
                config_request.get('config').setdefault('base_url', base_url)
                testcase_list[0] = config_request
            else:
                id = test_info[0]
                pre_request = eval(TestCase.objects.get(id=id).request)
                testcase_list.append(pre_request)

        except ObjectDoesNotExist:
            return testcase_list

    if request['test']['request']['url'] != '':
        testcase_list.append(request)

    dump_yaml_file(os.path.join(testcase_dir_path, name) +'.yml', testcase_list)






def run_by_batch(test_list, base_url, path, type=None, mode=False):
    """
    批量组装用例数据
    :param test_list:
    :param base_url: str: 环境地址
    :param type: str：用例级别
    :param mode: boolean：True 同步 False: 异步
    :return: list
    """
    if mode:           
        for index in range(len(test_list) - 2):
            form_test = test_list[index].split('=')
            value = form_test[1]
            if type == 'project':
                run_by_project(value, base_url, path)
            elif type == 'module':
                run_by_module(value, base_url, path)
            elif type == 'suite':
                run_by_suite(value, base_url, path)
            else:
                run_by_single(value, base_url, path)

    else:
        if type == 'project':
            for value in test_list.values():
                run_by_project(value, base_url, path)

        elif type == 'module':
            for value in test_list.values():
                run_by_module(value, base_url, path)
        elif type == 'suite':
            for value in test_list.values():
                run_by_suite(value, base_url, path)

        else:
            for index in range(len(test_list) - 1):
                form_test = test_list[index].split('=')
                index = form_test[1]
                run_by_single(index, base_url, path)


def run_by_module(id, base_url, path):
    """
    组装模块用例
    :param id: int or str：模块索引
    :param base_url: str：环境地址
    :return: list
    """
    obj = Module.objects.get(id=id)
    test_index_list = TestCase.objects.filter(belong_module=obj).values_list('id')
    for index in test_index_list:
        run_by_single(index[0], base_url, path)


def run_by_project(id, base_url, path):
    """
    组装项目用例
    :param id: int or str：项目索引
    :param base_url: 环境地址
    :return: list
    """
    
    obj = Project.objects.get(id=id)
    module_index_list = Module.objects.filter(belong_project=obj).values_list('id')
    for index in module_index_list:
        module_id = index[0]
        run_by_module(module_id, base_url, path)


def run_test_by_type(id, base_url, path, type):
    if type == 'project':
        run_by_project(id, base_url, path)
    elif type == 'module':
        run_by_module(id, base_url, path)
    else:
        run_by_single(id, base_url, path)
