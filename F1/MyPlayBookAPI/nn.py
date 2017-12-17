#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Ansible API

import json
from ansible import constants as C
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
#from ansible.playbook.play import Play
#from ansible.executor import playbook_executor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.utils.ssh_functions import check_for_controlpersist
from ansible.plugins.callback.json import CallbackModule
from ansible.utils.display import Display

class Options(object):
    """
    Options class to replace Ansible OptParser
    """
    def __init__(self, verbosity=None, inventory=None, listhosts=None, subset=None, module_paths=None, extra_vars=None,
                 forks=None, ask_vault_pass=None,  output_file=None, tags="", skip_tags="", one_line=None, tree=None, ask_sudo_pass=None, ask_su_pass=None,
                 sudo=None, sudo_user=None, become=None, become_method='sudo', become_user='root', become_ask_pass=None,
                 ask_pass=None, private_key_file=None, remote_user=None, connection=None, timeout=None, ssh_common_args=None,
                 sftp_extra_args=None, scp_extra_args=None, ssh_extra_args=None, poll_interval=None, seconds=None, check=None,
                 syntax=None, diff=None, force_handlers=None, flush_cache=None, listtasks=None, listtags=None, module_path=None):
        self.verbosity = verbosity
        self.inventory = inventory
        self.listhosts = listhosts
        self.subset = subset
        self.module_paths = module_paths
        self.extra_vars = extra_vars
        self.forks = forks
        self.ask_vault_pass = ask_vault_pass
        self.output_file = output_file
        self.tags = tags
        self.skip_tags = skip_tags
        self.one_line = one_line
        self.tree = tree
        self.ask_sudo_pass = ask_sudo_pass
        self.ask_su_pass = ask_su_pass
        self.sudo = sudo
        self.sudo_user = sudo_user
        self.become = become
        self.become_method = become_method
        self.become_user = become_user
        self.become_ask_pass = become_ask_pass
        self.ask_pass = ask_pass
        self.private_key_file = private_key_file
        self.remote_user = remote_user
        self.connection = connection
        self.timeout = timeout
        self.ssh_common_args = ssh_common_args
        self.sftp_extra_args = sftp_extra_args
        self.scp_extra_args = scp_extra_args
        self.ssh_extra_args = ssh_extra_args
        self.poll_interval = poll_interval
        self.seconds = seconds
        self.check = check
        self.syntax = syntax
        self.diff = diff
        self.force_handlers = force_handlers
        self.flush_cache = flush_cache
        self.listtasks = listtasks
        self.listtags = listtags
        self.module_path = module_path

class NewPlaybookExecutor(PlaybookExecutor):

    '''重写PlayBookExecutor 加入回调参数(不是很明白原作者心里想法这个剧本函数居然不加回调参数）'''
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


class PlaybookAPI(object):
    '''此类作为外放调用接口'''
    def __init__(self,playbooks,host_list,ssh_user,private_key_file,ext_vars,passwords='null', ack_pass=False,forks=10,verbosity=5):
        '''
        :param playbook:
        :param host_list: 主机列表
        :param passwords: 存放认证信息
        :param data: 用于传递额外参数
        :param verbosity: 日志级别
        '''
        #初始化一些自定义的变量
        self.options = Options()
        self.playbooks = playbooks
        self.ext_vars = ext_vars
        self.host_list = host_list

        self.options.remote_user = ssh_user
        self.options.become = True
        self.options.private_key_file = private_key_file
        self.options.ack_pass = ack_pass
        self.options.forks = forks
        self.options.connection = 'paramiko'
        self.options.verbosity = verbosity

        #展示
        self.display = Display()
        self.display.verbosity = self.options.verbosity
        
        self.passwords = dict(conn_pass='123123')
        self.passwords = dict(vault_pass=passwords)
        # DataLoader, 负责数据解析
        # VariableManager, 负责存储各类变量
        # Inventory, 负责初始化hosts
        # Play, 负责初始化playbook
        # TaskQueueManager, 负责初始化执行对象, 其run()函数负责执行play
        # 用来加载解析yaml文件或JSON内容,并且支持vault的解密
        self.loader = DataLoader()
        # 管理变量的类，包括主机，组，扩展等变量，之前版本是在 inventory中的
        self.variable_manager = VariableManager()
        #加载额外配置 目前解决的是密钥带密码问题
        self.variable_manager.extra_vars = self.ext_vars
        # 根据inventory加载对应变量
        self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager, host_list=self.host_list)
        #设置以上全部变量
        self.variable_manager.set_inventory(self.inventory)
        #生成回调参数
        self.callback = CallbackModule()
        #直接运行
        self.Runner()

    def Runner(self):
        pbex = None
        pbex = NewPlaybookExecutor(
            playbooks=self.playbooks,
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.options,
            passwords=self.passwords,
            stdout_callback=self.callback
        )
        pbex.run()


web = ['119.28.72.51']
#demo
if __name__ == "__main__":
    PlaybookAPI(playbooks = ['xx.yml'],
                host_list = web,
                ssh_user = 'automan',
                private_key_file = '/home/automan/.ssh/id_rsa',
                verbosity=10,
                ext_vars = {'ansible_password':'123'}
    )

