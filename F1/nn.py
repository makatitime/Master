#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Ansible API

import json
from ansible import constants as C
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.utils.ssh_functions import check_for_controlpersist
from ansible.plugins.callback.json import CallbackModule

class NewPlaybookExecutor(PlaybookExecutor):

    '''重写PlayBookExecutor 加入回调参数'''
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
    def __init__(self,playbook,host_list,ssh_user='root',passwords='null',project_name='all',ack_pass=False,forks=10,ext_vars=None):
        '''
        :param playbook:
        :param host_list: 主机列表
        :param passwords: 存放认证信息
        :param data: 用于传递额外参数
        :param verbosity: 日志级别
        '''
