#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright 2021 A10 Networks
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")

DOCUMENTATION = r'''
module: a10_scaleout_cluster
description:
    - Configure scaleout cluster
author: A10 Networks 2021
options:
    state:
        description:
        - State of the object to be created.
        choices:
          - noop
          - present
          - absent
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
    cluster_id:
        description:
        - "Scaleout cluster-id"
        type: int
        required: True
    follow_vcs:
        description:
        - "Field follow_vcs"
        type: bool
        required: False
    uuid:
        description:
        - "uuid of the object"
        type: str
        required: False
    local_device:
        description:
        - "Field local_device"
        type: dict
        required: False
        suboptions:
            priority:
                description:
                - "Field priority"
                type: int
            id:
                description:
                - "Field id"
                type: int
            action:
                description:
                - "'enable'= enable; 'disable'= disable;"
                type: str
            start_delay:
                description:
                - "Field start_delay"
                type: int
            uuid:
                description:
                - "uuid of the object"
                type: str
            l2_redirect:
                description:
                - "Field l2_redirect"
                type: dict
            session_sync_interface:
                description:
                - "Field session_sync_interface"
                type: dict
            tracking_template:
                description:
                - "Field tracking_template"
                type: dict
    cluster_devices:
        description:
        - "Field cluster_devices"
        type: dict
        required: False
        suboptions:
            uuid:
                description:
                - "uuid of the object"
                type: str
            minimum_nodes:
                description:
                - "Field minimum_nodes"
                type: dict
            cluster_discovery_timeout:
                description:
                - "Field cluster_discovery_timeout"
                type: dict
            device_id_list:
                description:
                - "Field device_id_list"
                type: list
    device_groups:
        description:
        - "Field device_groups"
        type: dict
        required: False
        suboptions:
            uuid:
                description:
                - "uuid of the object"
                type: str
            device_group_list:
                description:
                - "Field device_group_list"
                type: list
    tracking_template:
        description:
        - "Field tracking_template"
        type: dict
        required: False
        suboptions:
            template_list:
                description:
                - "Field template_list"
                type: list
    service_config:
        description:
        - "Field service_config"
        type: dict
        required: False
        suboptions:
            uuid:
                description:
                - "uuid of the object"
                type: str
            template_list:
                description:
                - "Field template_list"
                type: list
    db_config:
        description:
        - "Field db_config"
        type: dict
        required: False
        suboptions:
            uuid:
                description:
                - "uuid of the object"
                type: str

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
    "cluster_devices",
    "cluster_id",
    "db_config",
    "device_groups",
    "follow_vcs",
    "local_device",
    "service_config",
    "tracking_template",
    "uuid",
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
        state=dict(type='str',
                   default="present",
                   choices=['noop', 'present', 'absent']),
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
        'cluster_id': {
            'type': 'int',
            'required': True,
        },
        'follow_vcs': {
            'type': 'bool',
        },
        'uuid': {
            'type': 'str',
        },
        'local_device': {
            'type': 'dict',
            'priority': {
                'type': 'int',
            },
            'id': {
                'type': 'int',
            },
            'action': {
                'type': 'str',
                'choices': ['enable', 'disable']
            },
            'start_delay': {
                'type': 'int',
            },
            'uuid': {
                'type': 'str',
            },
            'l2_redirect': {
                'type': 'dict',
                'redirect_eth': {
                    'type': 'str',
                },
                'ethernet_vlan': {
                    'type': 'int',
                },
                'redirect_trunk': {
                    'type': 'int',
                },
                'trunk_vlan': {
                    'type': 'int',
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'session_sync_interface': {
                'type': 'dict',
                'eth_cfg': {
                    'type': 'list',
                    'ethernet': {
                        'type': 'str',
                    }
                },
                'trunk_cfg': {
                    'type': 'list',
                    'trunk': {
                        'type': 'int',
                    }
                },
                've_cfg': {
                    'type': 'list',
                    've': {
                        'type': 'int',
                    }
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'tracking_template': {
                'type': 'dict',
                'template_list': {
                    'type': 'list',
                    'template': {
                        'type': 'str',
                        'required': True,
                    },
                    'threshold_cfg': {
                        'type': 'list',
                        'threshold': {
                            'type': 'int',
                        },
                        'action': {
                            'type': 'str',
                            'choices': ['down', 'exit-cluster']
                        }
                    },
                    'uuid': {
                        'type': 'str',
                    },
                    'user_tag': {
                        'type': 'str',
                    }
                }
            }
        },
        'cluster_devices': {
            'type': 'dict',
            'uuid': {
                'type': 'str',
            },
            'minimum_nodes': {
                'type': 'dict',
                'minimum_nodes_num': {
                    'type': 'int',
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'cluster_discovery_timeout': {
                'type': 'dict',
                'timer_val': {
                    'type': 'int',
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'device_id_list': {
                'type': 'list',
                'device_id': {
                    'type': 'int',
                    'required': True,
                },
                'ip': {
                    'type': 'str',
                },
                'action': {
                    'type': 'str',
                    'choices': ['enable', 'disable']
                },
                'uuid': {
                    'type': 'str',
                },
                'user_tag': {
                    'type': 'str',
                }
            }
        },
        'device_groups': {
            'type': 'dict',
            'uuid': {
                'type': 'str',
            },
            'device_group_list': {
                'type': 'list',
                'device_group': {
                    'type': 'int',
                    'required': True,
                },
                'device_id_list': {
                    'type': 'list',
                    'device_id_start': {
                        'type': 'int',
                    },
                    'device_id_end': {
                        'type': 'int',
                    }
                },
                'uuid': {
                    'type': 'str',
                },
                'user_tag': {
                    'type': 'str',
                }
            }
        },
        'tracking_template': {
            'type': 'dict',
            'template_list': {
                'type': 'list',
                'template': {
                    'type': 'str',
                    'required': True,
                },
                'threshold_cfg': {
                    'type': 'list',
                    'threshold': {
                        'type': 'int',
                    },
                    'action': {
                        'type': 'str',
                        'choices': ['down', 'exit-cluster']
                    }
                },
                'uuid': {
                    'type': 'str',
                },
                'user_tag': {
                    'type': 'str',
                }
            }
        },
        'service_config': {
            'type': 'dict',
            'uuid': {
                'type': 'str',
            },
            'template_list': {
                'type': 'list',
                'name': {
                    'type': 'str',
                    'required': True,
                },
                'bucket_count': {
                    'type': 'int',
                },
                'device_group': {
                    'type': 'int',
                },
                'uuid': {
                    'type': 'str',
                },
                'user_tag': {
                    'type': 'str',
                }
            }
        },
        'db_config': {
            'type': 'dict',
            'uuid': {
                'type': 'str',
            }
        }
    })
    return rv


def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/scaleout/cluster/{cluster-id}"

    f_dict = {}
    f_dict["cluster-id"] = module.params["cluster_id"]

    return url_base.format(**f_dict)


def list_url(module):
    """Return the URL for a list of resources"""
    ret = existing_url(module)
    return ret[0:ret.rfind('/')]


def get(module):
    return module.client.get(existing_url(module))


def get_list(module):
    return module.client.get(list_url(module))


def exists(module):
    try:
        return get(module)
    except a10_ex.NotFound:
        return None


def _to_axapi(key):
    return translateBlacklist(key, KW_OUT).replace("_", "-")


def _build_dict_from_param(param):
    rv = {}

    for k, v in param.items():
        hk = _to_axapi(k)
        if isinstance(v, dict):
            v_dict = _build_dict_from_param(v)
            rv[hk] = v_dict
        elif isinstance(v, list):
            nv = [_build_dict_from_param(x) for x in v]
            rv[hk] = nv
        else:
            rv[hk] = v

    return rv


def build_envelope(title, data):
    return {title: data}


def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/scaleout/cluster/{cluster-id}"

    f_dict = {}
    f_dict["cluster-id"] = ""

    return url_base.format(**f_dict)


def validate(params):
    # Ensure that params contains all the keys.
    requires_one_of = sorted([])
    present_keys = sorted([
        x for x in requires_one_of if x in params and params.get(x) is not None
    ])

    errors = []
    marg = []

    if not len(requires_one_of):
        return REQUIRED_VALID

    if len(present_keys) == 0:
        rc, msg = REQUIRED_NOT_SET
        marg = requires_one_of
    elif requires_one_of == present_keys:
        rc, msg = REQUIRED_MUTEX
        marg = present_keys
    else:
        rc, msg = REQUIRED_VALID

    if not rc:
        errors.append(msg.format(", ".join(marg)))

    return rc, errors


def build_json(title, module):
    rv = {}

    for x in AVAILABLE_PROPERTIES:
        v = module.params.get(x)
        if v is not None:
            rx = _to_axapi(x)

            if isinstance(v, dict):
                nv = _build_dict_from_param(v)
                rv[rx] = nv
            elif isinstance(v, list):
                nv = [_build_dict_from_param(x) for x in v]
                rv[rx] = nv
            else:
                rv[rx] = module.params[x]

    return build_envelope(title, rv)


def report_changes(module, result, existing_config, payload):
    if existing_config:
        for k, v in payload["cluster"].items():
            if isinstance(v, str):
                if v.lower() == "true":
                    v = 1
                else:
                    if v.lower() == "false":
                        v = 0
            elif k not in payload:
                break
            else:
                if existing_config["cluster"][k] != v:
                    if result["changed"] is not True:
                        result["changed"] = True
                    existing_config["cluster"][k] = v
            result.update(**existing_config)
    else:
        result.update(**payload)
    return result


def create(module, result, payload):
    try:
        post_result = module.client.post(new_url(module), payload)
        if post_result:
            result.update(**post_result)
        result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result


def update(module, result, existing_config, payload):
    try:
        post_result = module.client.post(existing_url(module), payload)
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


def present(module, result, existing_config):
    payload = build_json("cluster", module)
    changed_config = report_changes(module, result, existing_config, payload)
    if module.check_mode:
        return changed_config
    elif not existing_config:
        return create(module, result, payload)
    elif existing_config and not changed_config.get('changed'):
        return update(module, result, existing_config, payload)
    else:
        result["changed"] = True
        return result


def delete(module, result):
    try:
        module.client.delete(existing_url(module))
        result["changed"] = True
    except a10_ex.NotFound:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result


def absent(module, result, existing_config):
    if module.check_mode:
        if existing_config:
            result["changed"] = True
            return result
        else:
            result["changed"] = False
            return result
    else:
        return delete(module, result)


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

    if state == 'present':
        result = present(module, result, existing_config)

    if state == 'absent':
        result = absent(module, result, existing_config)

    if state == 'noop':
        if module.params.get("get_type") == "single":
            result["result"] = get(module)
        elif module.params.get("get_type") == "list":
            result["result"] = get_list(module)
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
