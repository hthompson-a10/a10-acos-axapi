## Exercise 3: Create virtual server

### Step 1
Use your favorite text editor to create and open the file `a10_virtual_server_create.yaml`

Add the following to the playbook:
```yaml
- hosts: localhost
  name: "Create virtual server"
  connection: local
```

As perviously discussed in Exercise 2 (insert linke here), our architecture is different than what is standard to Ansible. As we are communicating with a device through its API instead of an ssh connection, we must set `connection: local` to execute on the controller instead of a remote host.

### Step 2: XXX

### Step 3: XXX

### Conclusion
