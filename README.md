# TC_QDISC

A template for an ansible role which configures some GNU/Linux subsystem or
service. A brief description of the role goes here.

## Role Variables


```yaml
tc_qdisc_status: status
tc_qdisc_inf_if: "enp0s3 root netem delay 200ms"
```

## Example Playbook


```yaml
---
- name: tc qdisc test
  hosts: all

  tasks:
  - name: Demonstrate tc qdisc present
    import_role:
      name: tc_qdisc
    vars:
      tc_qdisc_status: present
      tc_qdisc_inf_if: "enp0s3 root netem delay 200ms"
```

## License

Whenever possible, please prefer MIT.

## Author Information

2 hours POC for tc qdisc add/del command.

Jaroslav Fedor <fedorjaro@gmail.com>
