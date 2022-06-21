import ncs

from device import junos


class SelfInitCallbacks(ncs.application.NanoService):
    @ncs.application.NanoService.create
    def cb_nano_create(
        self, tctx, root, service, plan, component, state, proplist, component_proplist
    ):
        self.log.info("Service create(service=", service._path, ")")

        device = root.ncs__devices.device[service.device]

        if "http://tail-f.com/ned/cisco-ios-xr" in device.capability:
            os_family = "iosxr"
        elif "http://xml.juniper.net/xnm/1.1/xnm" in device.capability:
            junos.configure(
                self,
                tctx,
                root,
                service,
                plan,
                component,
                state,
                proplist,
                component_proplist,
            )
        else:
            raise RuntimeError("Device OS is not supported.")


class Main(ncs.application.Application):
    def setup(self):
        self.log.info("Main RUNNING")

        self.register_nano_service(
            "device-servicepoint",
            "ncs:self",
            "ncs:init",
            SelfInitCallbacks,
        )

    def teardown(self):
        self.log.info("Main FINISHED")
