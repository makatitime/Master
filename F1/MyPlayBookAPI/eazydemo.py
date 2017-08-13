#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Ansible API

import json
from ansible import constants as C
from collections import namedtuple
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
# from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor import playbook_executor
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.utils.ssh_functions import check_for_controlpersist
from ansible.plugins.callback.json import CallbackModule
from ansible.utils.display import Display
from ansible.plugins.callback import CallbackBase



class mycallback(CallbackBase):
    # 这里是状态回调，各种成功失败的状态,里面的各种方法其实都是从写于CallbackBase父类里面的，其实还有很多，可以根据需要拿出来用
    def __init__(self, *args):
        super(mycallback, self).__init__(display=None)
        self.status_ok = json.dumps({})
        self.status_fail = json.dumps({})
        self.status_unreachable = json.dumps({})
        self.status_playbook = ''
        self.status_no_hosts = False
        self.host_ok = {}
        self.host_failed = {}
        self.host_unreachable = {}

    def v2_runner_on_ok(self, result):
        #host = result._host.get_name()
        host = result._host
        self.runner_on_ok(host, result._result)
        #self.status_ok=json.dumps({host:result._result},indent=4)
        self.host_ok[host] = result

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        self.runner_on_failed(host, result._result, ignore_errors)
        self.status_fail=json.dumps({host:result._result},indent=4)
        self.host_failed[host] = result

    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        self.runner_on_unreachable(host, result._result)
        # self.status_unreachable=json.dumps({host:result._result},indent=4)
        self.host_unreachable[host] = result

    def v2_playbook_on_no_hosts_matched(self):
        self.playbook_on_no_hosts_matched()
        self.status_no_hosts = True

    def v2_playbook_on_play_start(self, play):
        self.playbook_on_play_start(play.name)
        self.playbook_path = play.name


class PlayBookApi(object):
    '''封装作为外放调用接口'''

    def __init__(self, playbooks, host_list, ssh_user, private_key_file, ext_vars, passwords='null', ack_pass=False,
                 forks=10, verbosity=0):
        '''
        :param playbook:
        :param host_list: 主机列表
        :param passwords: 存放认证信息
        :param data: 用于传递额外参数
        :param verbosity: 日志级别
        '''
        # 初始化一些自定义的变量
        self.playbooks = playbooks
        self.host_list = host_list
        self.ssh_user = ssh_user
        self.passwords = dict(vault_pass=passwords)
        self.ack_pass = ack_pass
        self.forks = forks
        self.connection = 'local'
        #self.connection = 'paramiko'
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
        # 回调返回格式Json值
        # self.callback = CallbackModule()
        # result_all = self.get_result()
        # return result_all

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
        self.pbex = PlaybookExecutor(
            playbooks=self.playbooks,
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.options,
            passwords=self.passwords
            #    stdout_callback=self.callback
        )
        self.results_callback = mycallback()
#        self.results_callback = CallbackModule()
        self.pbex._tqm._stdout_callback = self.results_callback
        results = self.pbex.run()
        return results
        print dir(results)


    def get_result(self):
#	print result._result
        self.result_all = {'success': {}, 'fail': {}, 'unreachable': {}}
        #print self.result_all
        #print dir(self.callback)
        for host, result in self.results_callback.host_ok.items():
            self.result_all['success'][host] = result._result
	    print  result._result
        for host, result in self.results_callback.host_failed.items():
            self.result_all['failed'][host] = result._result['msg']

        for host, result in self.results_callback.host_unreachable.items():
            self.result_all['unreachable'][host] = result._result['msg']

#        for i in self.result_all['success'].keys():
#            print i, self.result_all['success'][i]
        # print self.result_all['fail']
        # print self.result_all['unreachable']
        return self.result_all


web = ['127.0.0.1']
if __name__ == "__main__":
	playbook = PlayBookApi(playbooks=['test.yml'],
                           host_list=web,
                           ssh_user='automan',
                           private_key_file='/home/automan/.ssh/id_rsa',
                           verbosity=10,
                           ext_vars={'ansible_password': '123456'}
                           )
	stats = playbook.get_result()
    print stats
