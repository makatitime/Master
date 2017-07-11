#!/usr/bin/env  python
# --*-- coding:utf-8 --*--

import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
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


class YunweiPlaybookExecutor(PlaybookExecutor):
    '''重写PlayBookExecutor'''

    def __init__(self, playbooks, inventory, variable_manager, loader, options, passwords, stdout_callback=None):
        self._playbooks = playbooks
        self._inventory = inventory
        self._variable_manager = variable_manager
        self._loader = loader
        self._options = options
        self.passwords = passwords
        self._unreachable_hosts = dict()

        if options.listhosts or options.listtasks or options.listtags or options.syntax:
            self._tqm = None
        else:
            self._tqm = TaskQueueManager(inventory=inventory, variable_manager=variable_manager, loader=loader,
                                         options=options, passwords=self.passwords, stdout_callback=stdout_callback)

            # Note: We run this here to cache whether the default ansible ssh
            # executable supports control persist.  Sometime in the future we may
            # need to enhance this to check that ansible_ssh_executable specified
            # in inventory is also cached.  We can't do this caching at the point
            # where it is used (in task_executor) because that is post-fork and
            # therefore would be discarded after every task.


web = ['222.186.169.220', '222.186.169.221', '222.186.169.222']
# web = ['222.186.169.220']

Options = namedtuple('Options',
                     ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check',
                      'private_key_file', 'listhosts', 'listtasks', 'listtags', 'syntax'])

# initialize needed objects
variable_manager = VariableManager()
variable_manager.extra_vars = {'ansible_password': '123456', 'ansible_ssh_user': 'automan'}
loader = DataLoader()
options = Options(connection='paramiko', module_path='/usr/lib/python2.7/site-packages/ansible/modules/', forks=100,
                  become=True, become_method='sudo', become_user='root', check=False,
                  private_key_file='/home/automan/.ssh/id_rsa', listhosts=None, listtasks=None, listtags=None,
                  syntax=None)
passwords = dict(vault_pass='')

# Instantiate our ResultCallback for handling results as they come in
results_callback = ResultCallback()

# create inventory and pass to var manager
inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=web)
variable_manager.set_inventory(inventory)


playbook = YunweiPlaybookExecutor(playbooks=['/opt/xx.yml'], inventory=inventory,
                                  variable_manager=variable_manager,
                                  loader=loader, options=options,
                                  passwords=passwords,
                                  stdout_callback=results_callback)

playbook.run()


