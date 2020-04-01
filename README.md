# TC_QDISC

qdisc is short for 'queueing discipline' and it is elementary to understanding tr    affic control. Whenever the kernel needs to send a packet to an interface, it is enqueue    d to the qdisc configured for that interface.

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
  - name: Demonstrate tc qdisc absent
    import_role:
      name: tc_qdisc
    vars:
      tc_qdisc_status: absent
      tc_qdisc_inf_if: "enp0s3 root netem delay 200ms"
```

## License

MIT.

## Author Information

Jaroslav Fedor <fedorjaro@gmail.com>
