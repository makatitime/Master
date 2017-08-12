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
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,A55165FEA87A9D2B3CD03EBA106AC21C

IaMRvLxfU0hOtXG7tkRtDVFnP6sswxQ+lCGI1z3TyrcVoOQby4XI8rwUx/EDd8YX
Uzk5/1bdj5opQYGBbcZtZhZuAakGe4J2qVBJEmjuH6qbWY3FYJF77ZCBcs5eDIyA
PJVyVFZyOk9RiIVLeIeGYxt77YE7IK6ewq2nrWfNduxgY7WyQcsvxeJaIXuwRrMe
2ztKiK/lkpjR31UAL6k2ZL1yoMUMPbT8MCmt3zCVlXnZyCtFk89Ypri0ZEccmk1p
rmVp52TDlg6wu++N+29zbmwZEdvOcESa1/O5TkxLUhJ0EXxs5OUBScKu/xZodb+r
bDFt81aqCDGoYNuEoahFDLqlqPkON0q9euaNjg5kUx4xxnnK7zy0SFnnpxi8PmuO
sjoIVt9wwKMMUrYz49TxL3u9jJeYTBay0FSLOVo6Cw2/fG3va3OPbk/6TOBzXN/j
ECVl84/dUxU3rRPqaXCFp9E3L/D8Bhfu/ZxjjaFympwrTx9dUafHLw3t03dNiC3Y
ltHC6zBxP/t5fqbnhrcfOeWRM0BUjJb8dIa02iYEjnmSizMPg05sQpk5r/W+cKmA
duCVJtzi56jwSACGuG2/t2J9VgqbUJr/WsewXNE3rJOz9B3tyIg1L9QlnA/2RMuY
b3XEfNd2igjkDL6PlYxktSfcTj3jg/SNeXoVTaJ7SvUxXbJ4QW17GwIwnMCldEVc
RiYJOv4qH09EqxYB5xJy7Zx8FrkI63641UGwO61qz8CdSzVd1LYjE/AGaG8rR36P
tLDdqb8ABPCUlJyq+Qi9ks3CR/3iFq88pPR1xKm+Ga2ye8rFUs2HUiY/vq9QE220
eN1rCOSErwRN2UdgS5QFIoJwMKC4okueolTJ3DOFZSLHgUMHM79zQNjrRUpaZwrn
oCE0OH4E5DlaOysDCgEznpmKAAl8HUBzxXtR8NlJb63nITIrW0gqCLiT6lQ5fVVy
DAlYJoo1V/IpkydmNweUMdZhfRPxSiR9a6r0+aFACqWfSafxgMh/GU5ZF/HfQwjJ
RanmMuU22OPb8hwdDYlDgTB6NKWnYrdPpdFyIyOrLIXV1LxPYMrmr2omKGfscVVl
xZNDjuw2bymGOyABsNo0OtIPt8nmXgx1Ev6uQmpgS/FzJH7Z8LfU5IDAin40ZpHu
h0a94ORRxi4UK087d+bl5PbKChv0Vs3yYIEqCcgezEE6lXjixxl9Nm3KKROf58fG
97M8qFXWk1alYlWsZsmHkRfzxgsI+lVO/ek7YK6nv+zpPAhLeeKJN8qlQjgY1tKo
i2omG0a0gaON2InNxE6BGuO6kkwfexZIK8qVdHrVWc8ZBvKisomqRw46+kb1m2CH
tZMFgJkMA8B5X0aJN/4Zpb/3/7WWKuCw+aBF5lzsyUEyF2F/N8ZHO0d0C3Uti50w
ZdPhdxP6Kcx1ATV5d6IOPGQMvTc1WbfAIAMZUcWNZ7OI4WwzlqS1pqnilWhmb6ZJ
D+k0WqREWk7ck7uVm2mUYCKg88gzAbgUyQ8NlUgYXFzQE5823ZiDkK9FlaI405Ix
7b5KcGccgG1C8GOgeH1cIAs4gJYWnn+wAo2K3imgPRQlI64xlt0VayzsxlrsLyJ2
-----END RSA PRIVATE KEY-----



'''