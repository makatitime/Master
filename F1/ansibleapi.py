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
DEK-Info: AES-128-CBC,23274BD3532CDEDFBD21D3C0E9B71093

bDCttZKJ4iHoCy6kE0ii1lmNkWJm74c14Wupoki0L8nAkUwE+OT5n+febqbpmqox
Na8ngLgQwlZhyaJpHO/W7NR8O5YkhXvu6u5LzvGKq+Uhkdjjskt12Zmi2OK7mLLe
ttwRb0g2n9IWAH9HvvjrP2Z45qOIETm4cuGs4yvk/jFEstm8q4R5Enf0po92zEdJ
QFAFSmnlupdtNBBhmwg+GhZBx1/numQZRdJ+RO/xFR7SO9/48TFeSq9mkHHkXm3f
+btGLQ/dp7ylOpmMTZ8OALn1ArC3r4Sl7Cjos5DSfl4PwqsKLONuNz2FIxTjjvW9
AXsUpCd+oTuPxGTUezWrh6pEyA7xcB/d+E9faouHF1A2jw0ECK+kydmY5JsK5zsD
9g8TO9ZQo4v8RdZFhfSRZG8Bvj+kq4j+SV4Ym7RcUt8BPKxT5ZnRfmiJXJFgbxTD
vpKCnqZ74zAtZ1sI6wMV8kqDjxX0+jFNXcjedTI4HQys7TNUOINiDnW9/SjoDkGp
HUXZsciUtc/xRb7vScHojFlOWHqeQvnXPrWAu2pL1SX6dTxcGihG1DoT+6rlGeSW
6bZCYKAHFc3Ziw1Gm02LwPKe8s+wt0vyS43/PtCgbp395tLi30Ei8ruRcTVmuTg2
oYvIiY6yZ5XhI+KWeRe0o9BUlGse3X27rG3FE5KkP3d2864ibiQnOyNWqmDup4gn
xDnNwzG5ZCmn6fPSc9sM7RbQFHk6LWgUKMYbapoJYKgiOFEyoP6v9mCAhDNQV9L6
DkZ8jZxBLeCg9ZY3DFTf20Jn+w1xFg07fwfOQg0pnLq+Ew4gr6gaYwjPd/cahE6n
DkgbKZtG6mRXfrrzANA+pgJA+YANxKhMYhhP/25sz9RHKWf3rLYoPE/wlq0jUBFd
ufyYmBnrUJoCfDZKPh/cq9YqJneLklugMcLnr4CspJo2to3KxdYT5H4N7tqjNHVa
kpbupE4yp81Z9ihEg17a1s/P9XNQjOfpzvWe05gO4trJYX8EaefMV+W1jitbm46p
NgvFuPP09liXrEF+IBgTfyiNzQH2eaW98rgWNMjzNWbjwgUwQc52zbt8VLw10pc4
wqR5+hE4XJgm15ygRrz3DnDcoOc2uOj/XhfmuRrFWvnm2LeP4UYspWAHY4kU/mAV
ASxMIMjc2JrrKmjKJi5XOWfJ1Lv2gOzEeUtj2Z4K3Vlpz5nMAKhCCzpWUzgfXa4r
yOcKQT+D9PJjCbKzCtUqpxcdJYb0gTCSkvk658NJtuCafx3qQsJf0ZCnmSm3T0u4
yn14R0VZDTsRQ4gjIKg0ZFFixAOY+tSknYjdMZ8ssu/3y8KcWpeKiMCVCwrshe5J
qjZX1GpKpka8L/HhiMytGZ3fxgHFvBjG7zEZDKOBUPdNoVvcnM7uV7ND+4zTsNP8
baK8n0Z4wyP5B2IV3zMt3CvEJGNReRbMjTRo0fmoZU+ryCAatstP/4bTrU74IAr1
0ClmL6f43uRNQ1ZMOzfb6caQ3udol7UVskosXn0/HTIvOKjptJguXFytjGdGZiFd
G7oRzrIBmFFLIjBDl+QcOTGHucYbiO4ICpOm/5K/AETaVAFX8JPvjcl3O+cqe9ub
-----END RSA PRIVATE KEY-----


'''