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
  name: "Create virtual server"
  connection: local
  tasks:
  - name: Create service group
    a10_slb_virtual_server:
```

Note the action name `a10_slb_virtual_server`. Actions are named based paritally upon their URI and preceded by `a10`. In this case, the URI is `/axapi/v3/slb/virtual_server`. Another examle is `a10_health_monitor` which has the URI `/axapi/v3/health/monitor`.

### Step 3
Finally, it's time to add arguments to the playbook. First, make sure to refer to the AXAPI (insert link here).

### Conclusion

### Problems
***3.1: Disable the virtual server***

***3.2: Enable extended stats***

***3.3: Create a description for the virtual server***

See (insert link here) for solutions
