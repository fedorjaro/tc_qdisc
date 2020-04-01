#!/usr/bin/python

# Copyright: (c) 2020, Jaroslav Fedor <fedorjaro@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: tc_qdisc

short_description: This is module to manage trafic control

version_added: "2.9.2"

description:
    - "qdisc is short for 'queueing discipline' and it is elementary to understanding traffic control. Whenever the kernel needs to send a packet to an interface, it is enqueued to the qdisc configured for that interface."

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
original_message:
    description: The requests parameters for tc qdisc command
    type: str
    returned: always

message:
    description: The output message that the module generates
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import subprocess



def add_tc_qdisc(run_command, dev):
    cmd_output = run_command(['/usr/sbin/tc', 'qdisc','add','dev'] + ''.join(list(dev)).split(' '))
    return cmd_output

def remove_tc_qdisc(run_command, dev):
    cmd_output = run_command(['/usr/sbin/tc', 'qdisc','del','dev'] + ''.join(list(dev)).split(' '))
    return cmd_output

def get_tc_qdiscs(run_command):
    cmd_output = run_command(['/usr/sbin/tc', 'qdisc','show'])[1]
    _qdiscs_list = []
    for line in cmd_output.splitlines():
        if not line:
            continue
        _qdisc_list = line.split(" ")
        _qdiscs_list.append({
            "interface": _qdisc_list[4],
            "protocol": _qdisc_list[1]
            })
    return _qdiscs_list 

def qdics_exists(interface, protocol, qdiscs):
    for qdisc in qdiscs:
        if (
                qdisc['interface'] == interface and 
                qdisc['protocol'] == protocol
            ):
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
        original_message='',
        message=''
    )

    _tc_qdisc_protocol = module.params['dev'].split(' ')[2]
    _tc_qdisc_interface = module.params['dev'].split(' ')[0]
    result['original_message'] = module.params['dev']
    tc_qdiscs = get_tc_qdiscs(run_command)

    if module.params['status'] == 'present':
        if not qdics_exists(_tc_qdisc_interface, _tc_qdisc_protocol, tc_qdiscs):
            output = add_tc_qdisc(run_command, module.params['dev'])
            result['message'] = 'qdisc added' if output[0] == 0 else output[1] == ''
            if output[0] > 0:
                module.fail_json(msg=output[2], **result)
            result['changed'] = True
        else:
            result['message'] = 'qdisc is present'
   
    if module.params['status'] == 'absent':
        if qdics_exists(_tc_qdisc_interface, _tc_qdisc_protocol, tc_qdiscs):
            output = remove_tc_qdisc(run_command, module.params['dev'])
            result['message'] = 'OK' if output[0] == 0 else output[1] == ''
            if output[0] > 0:
                module.fail_json(msg=output[2], **result)
            result['changed'] = True
        else:
            result["message"] = 'qdisc is absent'


    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()
