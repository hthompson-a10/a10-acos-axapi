## Exercise 3: Create virtual server

### Step 1
Use your favorite text editor to create and open the file `a10_virtual_server_create.yaml`.

Add the following to the playbook:
```yaml
- hosts: localhost
  name: "Create virtual server"
  connection: local
```

As perviously discussed in Exercise 2 (insert link here), our architecture is different than what is standard to Ansible. As we are communicating with a device through its API instead of an ssh connection, we must set `connection: local` to execute on the controller instead of a remote host.

### Step 2
Next, add a task section to the playbook:
```yaml
- hosts: localhost
  name: "Create virtual server instance"
  connection: local
  tasks:
  - name: Create virtual server
    a10_slb_virtual_server:
```

Note the action name `a10_slb_virtual_server`. Actions are named based paritally upon their URI and preceded by `a10`. In this case, the URI is `/axapi/v3/slb/virtual_server`. Another examle is `a10_health_monitor` which has the URI `/axapi/v3/health/monitor`.

### Step 3
Now, we must add connection information in order to talk with the AX device:
```yaml
- hosts: localhost
  name: "Create virtual server instance"
  connection: local
  tasks:
  - name: Create virtual server
    a10_slb_virtual_server:
      a10_host: "{{ a10_host }}"
      a10_username: "{{ a10_username }}"
      a10_password: "{{ a10_password }}"
      a10_port: "{{ a10_port }}"
      a10_protocol: "{{ a10_protocol }}"
```

### Step 4
Finally, it's time to add arguments to the playbook. First, make sure to refer to the AXAPI (insert link here) or schema. According to the schema, the only required argument is the `name`. For this exercise though, we will be also adding the `ip-address` and a `netmask`.

After these additions, your playbook should appear as follows:
```yaml
- hosts: localhost
  name: "Create virtual server instance"
  connection: local
  tasks:
  - name: Create virtual server
    a10_slb_virtual_server:
      a10_host: "{{ a10_host }}"
      a10_username: "{{ a10_username }}"
      a10_password: "{{ a10_password }}"
      a10_port: "{{ a10_port }}"
      a10_protocol: "{{ a10_protocol }}"
      name: vs1
      ip_address: 10.0.0.1
      netmask: 255.255.255.0
```

### Conclusion

### Problems
***3.1: Disable the virtual server***

***3.2: Enable extended stats***

***3.3: Create a description for the virtual server***

See (insert link here) for solutions
