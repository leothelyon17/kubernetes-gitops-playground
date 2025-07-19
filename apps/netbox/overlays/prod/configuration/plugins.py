PLUGINS = ['netbox_bgp','netbox_lifecycle','netbox_slm','netbox_secrets','slurpit_netbox','netbox_diode_plugin','netbox_branching']

PLUGINS_CONFIG = {
    'netbox_bgp': {},
    'netbox_lifecycle': {},
    'netbox_slm': {},
    'netbox_secrets': {},
    'slurpit_netbox': {},
    'netbox_branching': {},
    'netbox_diode_plugin': {
        # # Auto-provision users for Diode plugin
        # "auto_provision_users": False,

        # Diode gRPC target for communication with Diode server
        "diode_target": "grpc://diode-marathon-srvc.lib-nauto-apps.lab.aheadaviation.com/diode",

        # # User allowed for Diode to NetBox communication
        # "diode_to_netbox_username": "diode-to-netbox",

        # # User allowed for NetBox to Diode communication
        # "netbox_to_diode_username": "netbox-to-diode",

        # User allowed for data ingestion
        #"diode_username": "diode-ingestion",
        "diode_username": "diode",
    }
}
