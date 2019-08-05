## Exercise 2: Exploration
A10's Ansible modules are generated off of ACOS schema files. These schema files are also used to create the API

### Step 1: Explore the AXAPI
Navigate to https://documentation.a10networks.com/index.html. You'll need to sign in with your A10 networks support account.

Once you've signed in, scroll down the page and find list item with the text `View ACOS 4.1.4-GR1-P1 documentation.` Click on that link, and scroll down until you reach the `Documentation Matrix`.

Under the `Reference Documentation for User Interfaces Used to Configure the Device` table view the HTML version of the `aXAPIv3 Reference Guide`. This guide contains links to our API endpoints.

Under the `Configuration APIs` section, navigate to the `slb` and then `virtual-server` sections. The `virtual-server attributes` section of this page contains information regarding acceptable arguments to the AXAPI. As the A10 Ansible modules pass the information provided in each playbook onto the AXAPI, arguments found within the AXAPI documentation are also valid playbook arguments.

### Step 2: Explore the Schema
On the same page, under the `virtual-server specification` section, you'll find a table with a `schema` section. Download and open the `txt` schema file. This file has the same information as the `virtual-server attributes` section, but in a more consumable format.

### Step 3: Explore the Modules


### Conclusion
