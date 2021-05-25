#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright 2021 A10 Networks
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")

DOCUMENTATION = r'''
module: a10_vcs_vblades_stat
description:
    - Show aVCS vBlade box statistics information
author: A10 Networks 2021
options:
    state:
        description:
        - State of the object to be created.
        choices:
          - noop
        type: str
        required: True
    ansible_host:
        description:
        - Host for AXAPI authentication
        type: str
        required: True
    ansible_username:
        description:
        - Username for AXAPI authentication
        type: str
        required: True
    ansible_password:
        description:
        - Password for AXAPI authentication
        type: str
        required: True
    ansible_port:
        description:
        - Port for AXAPI authentication
        type: int
        required: True
    a10_device_context_id:
        description:
        - Device ID for aVCS configuration
        choices: [1-8]
        type: int
        required: False
    a10_partition:
        description:
        - Destination/target partition for object/command
        type: str
        required: False
    vblade_id:
        description:
        - "vBlade-id"
        type: int
        required: True
    uuid:
        description:
        - "uuid of the object"
        type: str
        required: False
    sampling_enable:
        description:
        - "Field sampling_enable"
        type: list
        required: False
        suboptions:
            counters1:
                description:
                - "'all'= all; 'slave_recv_err'= vBlade Receive Errors counter of aVCS election;
          'slave_send_err'= vBlade Send Errors counter of aVCS election;
          'slave_recv_bytes'= vBlade Received Bytes counter of aVCS election;
          'slave_sent_bytes'= vBlade Sent Bytes counter of aVCS election; 'slave_n_recv'=
          vBlade Received Messages counter of aVCS election; 'slave_n_sent'= vBlade Sent
          Messages counter of aVCS election; 'slave_msg_inval'= vBlade Invalid Messages
          counter of aVCS election; 'slave_keepalive'= vBlade Received Keepalives counter
          of aVCS election; 'slave_cfg_upd'= vBlade Received Configuration Updates
          counter of aVCS election; 'slave_cfg_upd_l1_fail'= vBlade Local Configuration
          Update Errors (1) counter of aVCS election; 'slave_cfg_upd_r_fail'= vBlade
          Remote Configuration Update Errors counter of aVCS election;
          'slave_cfg_upd_l2_fail'= vBlade Local Configuration Update Errors (2) counter
          of aVCS election; 'slave_cfg_upd_notif_err'= vBlade Configuration Update Notif
          Errors counter of aVCS election; 'slave_cfg_upd_result_err'= vBlade
          Configuration Update Result Errors counter of aVCS election;"
                type: str
    stats:
        description:
        - "Field stats"
        type: dict
        required: False
        suboptions:
            slave_recv_err:
                description:
                - "vBlade Receive Errors counter of aVCS election"
                type: str
            slave_send_err:
                description:
                - "vBlade Send Errors counter of aVCS election"
                type: str
            slave_recv_bytes:
                description:
                - "vBlade Received Bytes counter of aVCS election"
                type: str
            slave_sent_bytes:
                description:
                - "vBlade Sent Bytes counter of aVCS election"
                type: str
            slave_n_recv:
                description:
                - "vBlade Received Messages counter of aVCS election"
                type: str
            slave_n_sent:
                description:
                - "vBlade Sent Messages counter of aVCS election"
                type: str
            slave_msg_inval:
                description:
                - "vBlade Invalid Messages counter of aVCS election"
                type: str
            slave_keepalive:
                description:
                - "vBlade Received Keepalives counter of aVCS election"
                type: str
            slave_cfg_upd:
                description:
                - "vBlade Received Configuration Updates counter of aVCS election"
                type: str
            slave_cfg_upd_l1_fail:
                description:
                - "vBlade Local Configuration Update Errors (1) counter of aVCS election"
                type: str
            slave_cfg_upd_r_fail:
                description:
                - "vBlade Remote Configuration Update Errors counter of aVCS election"
                type: str
            slave_cfg_upd_l2_fail:
                description:
                - "vBlade Local Configuration Update Errors (2) counter of aVCS election"
                type: str
            slave_cfg_upd_notif_err:
                description:
                - "vBlade Configuration Update Notif Errors counter of aVCS election"
                type: str
            slave_cfg_upd_result_err:
                description:
                - "vBlade Configuration Update Result Errors counter of aVCS election"
                type: str
            vblade_id:
                description:
                - "vBlade-id"
                type: int

'''

EXAMPLES = """
"""

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'community',
    'status': ['preview']
}

# Hacky way of having access to object properties for evaluation
AVAILABLE_PROPERTIES = [
    "sampling_enable",
    "stats",
    "uuid",
    "vblade_id",
]

from ansible_collections.a10.acos_axapi.plugins.module_utils import \
    errors as a10_ex
from ansible_collections.a10.acos_axapi.plugins.module_utils.axapi_http import \
    client_factory
from ansible_collections.a10.acos_axapi.plugins.module_utils.kwbl import \
    KW_OUT, translate_blacklist as translateBlacklist


def get_default_argspec():
    return dict(
        ansible_host=dict(type='str', required=True),
        ansible_username=dict(type='str', required=True),
        ansible_password=dict(type='str', required=True, no_log=True),
        state=dict(type='str', default="noop", choices=['noop']),
        ansible_port=dict(type='int', choices=[80, 443], required=True),
        a10_partition=dict(
            type='dict',
            name=dict(type='str', ),
            shared=dict(type='str', ),
            required=False,
        ),
        a10_device_context_id=dict(
            type='int',
            choices=[1, 2, 3, 4, 5, 6, 7, 8],
            required=False,
        ),
        get_type=dict(type='str', choices=["single", "list", "oper", "stats"]),
    )


def get_argspec():
    rv = get_default_argspec()
    rv.update({
        'vblade_id': {
            'type': 'int',
            'required': True,
        },
        'uuid': {
            'type': 'str',
        },
        'sampling_enable': {
            'type': 'list',
            'counters1': {
                'type':
                'str',
                'choices': [
                    'all', 'slave_recv_err', 'slave_send_err',
                    'slave_recv_bytes', 'slave_sent_bytes', 'slave_n_recv',
                    'slave_n_sent', 'slave_msg_inval', 'slave_keepalive',
                    'slave_cfg_upd', 'slave_cfg_upd_l1_fail',
                    'slave_cfg_upd_r_fail', 'slave_cfg_upd_l2_fail',
                    'slave_cfg_upd_notif_err', 'slave_cfg_upd_result_err'
                ]
            }
        },
        'stats': {
            'type': 'dict',
            'slave_recv_err': {
                'type': 'str',
            },
            'slave_send_err': {
                'type': 'str',
            },
            'slave_recv_bytes': {
                'type': 'str',
            },
            'slave_sent_bytes': {
                'type': 'str',
            },
            'slave_n_recv': {
                'type': 'str',
            },
            'slave_n_sent': {
                'type': 'str',
            },
            'slave_msg_inval': {
                'type': 'str',
            },
            'slave_keepalive': {
                'type': 'str',
            },
            'slave_cfg_upd': {
                'type': 'str',
            },
            'slave_cfg_upd_l1_fail': {
                'type': 'str',
            },
            'slave_cfg_upd_r_fail': {
                'type': 'str',
            },
            'slave_cfg_upd_l2_fail': {
                'type': 'str',
            },
            'slave_cfg_upd_notif_err': {
                'type': 'str',
            },
            'slave_cfg_upd_result_err': {
                'type': 'str',
            },
            'vblade_id': {
                'type': 'int',
                'required': True,
            }
        }
    })
    return rv


def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/vcs-vblades/stat/{vblade-id}"

    f_dict = {}
    f_dict["vblade-id"] = module.params["vblade_id"]

    return url_base.format(**f_dict)


def stats_url(module):
    """Return the URL for statistical data of and existing resource"""
    partial_url = existing_url(module)
    return partial_url + "/stats"


def list_url(module):
    """Return the URL for a list of resources"""
    ret = existing_url(module)
    return ret[0:ret.rfind('/')]


def get(module):
    return module.client.get(existing_url(module))


def get_list(module):
    return module.client.get(list_url(module))


def get_stats(module):
    if module.params.get("stats"):
        query_params = {}
        for k, v in module.params["stats"].items():
            query_params[k.replace('_', '-')] = v
        return module.client.get(stats_url(module), params=query_params)
    return module.client.get(stats_url(module))


def exists(module):
    try:
        return get(module)
    except a10_ex.NotFound:
        return None


def replace(module, result, existing_config, payload):
    try:
        post_result = module.client.put(existing_url(module), payload)
        if post_result:
            result.update(**post_result)
        if post_result == existing_config:
            result["changed"] = False
        else:
            result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result


def run_command(module):
    run_errors = []

    result = dict(changed=False, original_message="", message="", result={})

    state = module.params["state"]
    ansible_host = module.params["ansible_host"]
    ansible_username = module.params["ansible_username"]
    ansible_password = module.params["ansible_password"]
    ansible_port = module.params["ansible_port"]
    a10_partition = module.params["a10_partition"]
    a10_device_context_id = module.params["a10_device_context_id"]

    if ansible_port == 80:
        protocol = "http"
    elif ansible_port == 443:
        protocol = "https"

    valid = True

    if state == 'present':
        valid, validation_errors = validate(module.params)
        for ve in validation_errors:
            run_errors.append(ve)

    if not valid:
        err_msg = "\n".join(run_errors)
        result["messages"] = "Validation failure: " + str(run_errors)
        module.fail_json(msg=err_msg, **result)

    module.client = client_factory(ansible_host, ansible_port, protocol,
                                   ansible_username, ansible_password)

    if a10_partition:
        module.client.activate_partition(a10_partition)

    if a10_device_context_id:
        module.client.change_context(a10_device_context_id)

    existing_config = exists(module)

    if state == 'noop':
        if module.params.get("get_type") == "single":
            result["result"] = get(module)
        elif module.params.get("get_type") == "list":
            result["result"] = get_list(module)
        elif module.params.get("get_type") == "stats":
            result["result"] = get_stats(module)
    module.client.session.close()
    return result


def main():
    module = AnsibleModule(argument_spec=get_argspec(),
                           supports_check_mode=True)
    result = run_command(module)
    module.exit_json(**result)


# standard ansible module imports
from ansible.module_utils.basic import AnsibleModule

if __name__ == '__main__':
    main()
