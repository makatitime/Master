#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Ansible API

import json
from ansible import constants as C
from collections import namedtuple
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
#from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor import playbook_executor
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.utils.ssh_functions import check_for_controlpersist
from ansible.plugins.callback.json import CallbackModule
from ansible.utils.display import Display
from ansible.plugins.callback import CallbackBase

class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print json.dumps({host.name: result._result}, indent=4)

class NewPlaybookExecutor(PlaybookExecutor):

    '''重写PlayBookExecutor 加入回调(不是很明白原作者心里想法这个剧本函数居然不加回调参数）'''
    def __init__(self, playbooks, inventory, variable_manager, loader, options, passwords, stdout_callback=None):
        self._playbooks        = playbooks
        self._inventory        = inventory
        self._variable_manager = variable_manager
        self._loader           = loader
        self._options          = options
        self.passwords         = passwords
        self._unreachable_hosts = dict()

        if options.listhosts or options.listtasks or options.listtags or options.syntax:
            self._tqm = None
        else:
            self._tqm = TaskQueueManager(inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=self.passwords, stdout_callback=stdout_callback)

        # Note: We run this here to cache whether the default ansible ssh
        # executable supports control persist.  Sometime in the future we may
        # need to enhance this to check that ansible_ssh_executable specified
        # in inventory is also cached.  We can't do this caching at the point
        # where it is used (in task_executor) because that is post-fork and
        # therefore would be discarded after every task.
        check_for_controlpersist(C.ANSIBLE_SSH_EXECUTABLE)



class PlayBookApi(object):
    '''封装作为外放调用接口'''
    def __init__(self,playbooks,host_list,ssh_user,private_key_file,ext_vars,passwords='null',ack_pass=False,forks=10,verbosity=0):
        '''
        :param playbook:
        :param host_list: 主机列表
        :param passwords: 存放认证信息
        :param data: 用于传递额外参数
        :param verbosity: 日志级别
        '''
        #初始化一些自定义的变量
        self.playbooks = playbooks
        self.host_list = host_list
        self.ssh_user = ssh_user
        self.passwords = dict(vault_pass=passwords)
        self.ack_pass = ack_pass
        self.forks = forks
        self.connection = 'paramiko'
        self.ext_vars = ext_vars
        self.verbosity = verbosity
        self.display = Display()

        # 用来加载解析yaml文件或JSON内容,并且支持vault的解密
        self.loader = DataLoader()
        # 管理变量的类，包括主机，组，扩展等变量，之前版本是在 inventory中的
        self.variable_manager = VariableManager()
        self.variable_manager.extra_vars = self.ext_vars
        # 根据inventory加载对应变量
        self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager, host_list=self.host_list)

        self.variable_manager.set_inventory(self.inventory)
        #回调返回格式Json值
        self.callback = ResultCallback()

        # 初始化需要的对象1
        self.Options = namedtuple('Options',
                                  ['connection',
                                   'remote_user',
                                   'ask_sudo_pass',
                                   'verbosity',
                                   'ack_pass',
                                   'module_path',
                                   'forks',
                                   'become',
                                   'become_method',
                                   'become_user',
                                   'check',
                                   'listhosts',
                                   'listtasks',
                                   'listtags',
                                   'syntax',
                                   'sudo_user',
                                   'sudo'
                                   ])

        # 初始化需要的对象2
        self.options = self.Options(connection=self.connection,
                                    remote_user=self.ssh_user,
                                    ack_pass=self.ack_pass,
                                    sudo_user=self.ssh_user,
                                    forks=self.forks,
                                    sudo='yes',
                                    ask_sudo_pass=False,
                                    verbosity=self.verbosity,
                                    module_path=None,
                                    become=True,
                                    become_method='sudo',
                                    become_user='root',
                                    check=None,
                                    listhosts=None,
                                    listtasks=None,
                                    listtags=None,
                                    syntax=None
                                    )



        self.Runner()

    def Runner(self):
        pbex = PlaybookExecutor(
            playbooks=self.playbooks,
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.options,
            passwords=self.passwords,
            #            stdout_callback=self.callback
        )
        self.results_callback = ResultCallback()
        pbex._tqm._stdout_callback = self.results_callback

    def get_result(self):
        self.result_all = {'success': {}, 'fail': {}, 'unreachable': {}}
        # print result_all
        # print dir(self.results_callback)
        for host, result in self.results_callback.host_ok.items():
            self.result_all['success'][host] = result._result

        for host, result in self.results_callback.host_failed.items():
            self.result_all['failed'][host] = result._result['msg']

        for host, result in self.results_callback.host_unreachable.items():
            self.result_all['unreachable'][host] = result._result['msg']

        for i in self.result_all['success'].keys():
            print i, self.result_all['success'][i]

        print self.result_all
        print self.result_all['fail']
        print self.result_all['unreachable']




web = ['127.0.0.1']
if __name__ == "__main__":
    playbook = PlayBookApi(playbooks=['/opt/xx.yml'],
                           host_list=web,
                           ssh_user='automan',
                           private_key_file='/home/automan/.ssh/id_rsa',
                           verbosity = 10,
                           ext_vars={'ansible_password': '123456'}
                           )
    playbook.run()
    playbook.get_result()