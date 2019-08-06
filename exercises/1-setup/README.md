## Excercise 1: Setup Lab
For this workshop you'll need:
- A bare-metal server or virtual machine running Ansible
- An A10 Thunder device running ACOS v4.1.4

### Step 1: Install Ansible
Please refer to the following guide: https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html

### Step 2: Clone git repo
Run the following commands on the Ansible server:
```
git clone git@github.com:a10networks/a10-ansible.git && sudo pip install -e a10-ansible/
```

### Step 3: Configure library
1. Run the following command to check the location of the config file:
```
ansible --version
```
The output should be as follows:
```
ansible 2.8.3
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/ubuntu/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.15+ (default, Nov 27 2018, 23:36:35) [GCC 7.3.0]
```

2. Open the `ansible.cfg` file indicated by the `config file` variable above.
3. Replace the add the following line under the `defaults` sections:
```
library        = /path/to/a10-ansible/a10_ansible/library
```

### Conclusion
At this stage, you now have a fully setup lab. In the next lesson (hyperlink to next lesson), we'll cover writing playbooks.
