#!/usr/bin/env  python
#--*-- coding:utf-8 --*--

import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
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

web = ['222.186.169.221','222.186.169.222']
Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'private_key_file'])

# initialize needed objects
variable_manager = VariableManager()
variable_manager.extra_vars = {'ansible_password':'123456','ansible_ssh_user':'automan'}
loader = DataLoader()
options = Options(connection='paramiko', module_path='/usr/lib/python2.7/site-packages/ansible/modules/', forks=100, become=True, become_method='sudo', become_user='automan', check=False, private_key_file='/home/automan/.ssh/id_rsa')
passwords = dict(vault_pass='')

# Instantiate our ResultCallback for handling results as they come in
results_callback = ResultCallback()

# create inventory and pass to var manager
inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=web)
variable_manager.set_inventory(inventory)
# create play with tasks
play_source =  dict(
        name = "Ansible Play",
        hosts = web,
        gather_facts = 'no',
        tasks = [
            dict(action=dict(module='setup', args=''), register='shell_out'),
            dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
         ]
    )
play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

# actually run it
tqm = None
try:
    tqm = TaskQueueManager(
              inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,
              options=options,
              passwords=passwords,
              stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
          )
    result = tqm.run(play)
finally:
    if tqm is not None:
        tqm.cleanup()


'''

'''