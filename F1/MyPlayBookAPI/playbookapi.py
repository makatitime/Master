#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 描述:
# V1 WZJ 2016-12-19 PlayBook重写封装api基本功能

import json
from ansible import constants as C
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.utils.ssh_functions import check_for_controlpersist




class YunweiPlaybookExecutor(PlaybookExecutor):

    '''重写PlayBookExecutor'''
    def __init__(self, playbooks, inventory, variable_manager, loader, options, passwords):
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


class PlayBookJob(object):
  '''封装一个playbook接口,提供给外部使用'''
  def __init__(self,playbooks,host_list,ssh_user='bbs',passwords='null',project_name='all',ack_pass=False,forks=5,ext_vars=None):
    self.playbooks = playbooks
    self.host_list = host_list
    self.ssh_user  = ssh_user
    self.passwords = dict(vault_pass=passwords)
    self.project_name = project_name
    self.ack_pass  = ack_pass
    self.forks     = forks
    self.connection='smart'
    self.ext_vars  = ext_vars

    ## 用来加载解析yaml文件或JSON内容,并且支持vault的解密
    self.loader    = DataLoader()

    # 管理变量的类，包括主机，组，扩展等变量，之前版本是在 inventory中的
    self.variable_manager = VariableManager()

    # 根据inventory加载对应变量
    self.inventory = Inventory(loader=self.loader,
                               variable_manager=self.variable_manager,
                               group_name=self.project_name,  # 项目名对应组名,区分当前执行的内容
                               ext_vars=self.ext_vars,
                               host_list=self.host_list)

    self.variable_manager.set_inventory(self.inventory)

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
                                verbosity=5,
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

    # 初始化console输出
    self.callback = YunweiCallback()

    # 直接开始
    self.run()

  def run(self):
    pb = None
    pb = YunweiPlaybookExecutor(
        playbooks            = self.playbooks,
        inventory            = self.inventory,
        variable_manager     = self.variable_manager,
        loader               = self.loade                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        r,
        options              = self.options,
        passwords            = self.passwords
        #stdout_callback      = self.callback
    )
    result = pb.run()

# daemo
if __name__ == "__main__":
    PlayBookJob(playbooks=['xx.yml'],
                host_list=['10.45.176.2'],
                ssh_user='root',
                project_name="test",
                forks=20,
                ext_vars=None
                )
