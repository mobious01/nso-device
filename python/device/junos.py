def configure(
    cb, tctx, root, service, plan, component, state, proplist, component_proplist
):
    device = root.ncs__devices.device[service.device]
    config_top = device.config.junos__configuration

    del config_top.system
    config_system = config_top.system

    if service.host_name is not None:
        config_system.host_name = service.host_name

    config_system.root_authentication.encrypted_password = "$6$R./dmSMU$O/Z/MwEwrEowNHhsv2xONh97PGimZV6HSPx.eQA6L6CjuDfsVw8dyo5dShUqtlzJP5Pd.yabaRPkwoUgGbRAp/"

    config = config_system.services.create()

    config = config_system.services.ssh.create()
    config.root_login = "allow"

    config = config_system.services.netconf
    config.ssh.create()

    if service.domain_name is not None:
        config_system.domain_name = service.domain_name

    config_system.management_instance.create()

    config = config_system.syslog

    config.user.create("*")
    config.user["*"].contents.create("any")
    config.user["*"].contents["any"].emergency.create()

    config.file.create("interactive-commands")
    config.file["interactive-commands"].contents.create("interactive-commands")
    config.file["interactive-commands"].contents["interactive-commands"].any.create()

    config.file.create("messages")
    config.file["messages"].contents.create("any")
    config.file["messages"].contents["any"].notice.create()
    config.file["messages"].contents.create("authorization")
    config.file["messages"].contents["authorization"].info.create()

    del config_top.chassis
    config_chassis = config_top.chassis

    if device.platform.model == "vmx":
        config_chassis.aggregated_devices.ethernet.device_count = 480
    else:
        config_chassis.aggregated_devices.ethernet.device_count = 1000

    if device.platform.model == "vmx":
        config_chassis.fpc.create("0")
        config_chassis.fpc["0"].pic.create("0")
        config_chassis.fpc["0"].pic["0"].tunnel_services.create()
        config_chassis.fpc["0"].pic["0"].inline_services.create()
        config_chassis.fpc["0"].flexible_queuing_mode.create()

    config_chassis.network_services = "enhanced-ip"
