#!/usr/bin/python

# Copyright: (c) 2020, Jaroslav Fedor <fedorjaro@gmail.com>
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: tc_qdisc

short_description: This is module to manage trafic control

version_added: "2.6"

description:
    - "qdisc is short for 'queueing discipline' and it is
       elementary to understanding traffic control. Whenever
       the kernel needs to send a packet to an interface, it
       is enqueued to the qdisc configured for that interface."

options:
    status:
        description:
            - This is a operation for tc qdisc comamnd present / absent
        required: true
    dev:
        description:
            - Interdace and classful or classless qdisc plus adition params
        required: false

author:
    - Jaroslav Fedor (@fedorajro)
'''

EXAMPLES = '''
# Pass in a message
- name: TC_QDISC | Adjusting tc qdisc configuration
  tc_qdisc:
    status: present
    dev: "enp0s3 root netem delay 200ms"

'''

RETURN = '''
message:
    description: The output message that the module generates
    type: str
    returned: always
'''


def add_tc_qdisc(run_command, dev):
    cmd_output = run_command(
            [
                '/usr/sbin/tc',
                'qdisc',
                'add',
                'dev'
                ] + ''.join(list(dev)).split(' '))
    return cmd_output


def remove_tc_qdisc(run_command, dev):
    cmd_output = run_command(
            [
                '/usr/sbin/tc',
                'qdisc',
                'del',
                'dev'
            ] + ''.join(list(dev)).split(' '))
    return cmd_output


def get_tc_qdiscs(run_command):
    cmd_output = run_command(['/usr/sbin/tc', 'qdisc', 'show'])[1]
    __qdiscs_list = []
    for line in cmd_output.splitlines():
        if not line:
            continue
        __qdisc_list = line.split(" ")
        __qdiscs_list.append({
            "interface": __qdisc_list[4],
            "protocol": __qdisc_list[1]
            })
    return __qdiscs_list


def qdics_exists(__interface, __protocol, __qdiscs):
    for __qdisc in __qdiscs:
        if (__qdisc['interface'] == __interface and
           __qdisc['protocol'] == __protocol):
            return True

    return False


def run_module():
    module_args = dict(
        status=dict(type='str', required=True),
        dev=dict(type='str', required=False)
    )

    module = AnsibleModule(
        argument_spec=module_args,
    )

    run_command = module.run_command

    result = dict(
        changed=False,
        message=''
    )
    if module.params['status'] not in ['present', 'absent']:
        module.fail_json(msg='Status must be present or absent', **result)

    if len(module.params['dev'].split(' ')) < 3:
        module.fail_json(msg='You need to specify also protocol', **result)

    __tc_qdisc_protocol = module.params['dev'].split(' ')[2]
    __tc_qdisc_interface = module.params['dev'].split(' ')[0]
    __tc_qdiscs = get_tc_qdiscs(run_command)
    message = ""
    if module.params['status'] == 'present':
        if (not qdics_exists(
              __tc_qdisc_interface,
              __tc_qdisc_protocol,
              __tc_qdiscs)):
            __output = add_tc_qdisc(run_command, module.params['dev'])
            message = 'qdisc added' if __output[0] == 0 else __output[1]
            if __output[0] > 0:
                module.fail_json(msg=__output[2], **result)
            result['changed'] = True
        else:
            message = 'qdisc is present'

    if module.params['status'] == 'absent':
        if qdics_exists(
                __tc_qdisc_interface,
                __tc_qdisc_protocol,
                __tc_qdiscs):
            __output = remove_tc_qdisc(run_command, module.params['dev'])
            message = 'qdisc deleted' if __output[0] == 0 else __output[1]
            if __output[0] > 0:
                module.fail_json(msg=__output[2], **result)
            result['changed'] = True
        else:
            message = 'qdisc is absent'
    result['message'] = message
    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()
