#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)

import threading as th
import socket

from ansible.module_utils.basic import AnsibleModule
__metaclass__ = type

DOCUMENTATION = r'''
---
module: knock

short_description: 'Knocks' at the ports specified

version_added: "1.0.0"

description: The module will sequentially try to open a connection to each port for each host. Each host will be processed in a separate thread.

options:
    knock_at:
        description: List of dictionaries containing the keys host and ports.
        required: true
        type: list
    timeout:
        description: Max time in seconds the program will knock at each port (default 10).
        required: false
        type: int

author:
    - Lucas Arbiza (@arbiza)
'''

EXAMPLES = r'''
- name: Knock, knock, knock
  arbiza.firewall.knock:
    knock_at:
      - host: "{{ hostvars['container_1'].ansible_host }}"
        ports: "{{ hostvars['container_1'].knocking_list[0].ports }}"
      - host: "{{ hostvars['container_2'].ansible_host }}"
        ports: "{{ hostvars['container_2'].knocking_list[0].ports }}"
    timeout: 2 # can be omitted; default is 10s
  delegate_to: localhost
  become: false
'''

RETURN = r'''
message:
    description: Message informing success or failure
    type: str
    returned: always
    sample: 'Successfully knocked <host 1>,<host 2>,...<host N>'
'''


def knock_at(host: str, ports: list, timeout: int, lock: th.Lock, output: list):

    message = dict(
        ok=True,
        host=host,
        error=''
    )

    for p in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(False)
            s.settimeout(timeout)
            s.connect((host, p))
        except socket.timeout:
            # timeout is the expected result
            pass
        except socket.error as se:
            message['ok'] = False
            message['error'] = 'port {} - {}'.format(p, se)
        else:
            message['ok'] = False
            message['error'] = 'port {} - unknown error'.format(p)
        finally:
            s.close()

    lock.acquire()
    output.append(message)
    lock.release()


def run_module():
    # Arguments
    module_args = dict(
        knock_at=dict(type='list', required=True),
        timeout=dict(type='int', required=False)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Return
    result = dict(
        changed=False
    )

    # For when the user runs with 'check mode' - returns without modifications
    if module.check_mode:
        module.exit_json(**result)

    threads = list()
    lock = th.Lock()
    output = list()

    timeout = module.params['timeout'] if module.params['timeout'] is not None else 10

    for i in module.params['knock_at']:
        t = th.Thread(target=knock_at, args=(
            i['host'], i['ports'], timeout, lock, output,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    failed_hosts = ','.join(['{}: {}'.format(o['host'], o['error'])
                            for o in output if o['ok'] is False])
    if failed_hosts != '':
        module.fail_json(msg='Knocking failed for ' + failed_hosts, **result)

    result['msg'] = 'Successfully knocked {}'.format(
        ','.join([o['host'] for o in output]))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
