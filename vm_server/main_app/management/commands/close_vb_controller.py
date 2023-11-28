from django.core.management.base import BaseCommand
# from vm_server.main_app.vb_controller import VBController

from controllers.vb_controller_instance import vb_controller
# from vm_server.settings import vb_controller


class Command(BaseCommand):
    help = 'Closes the VM controller'

    def handle(self, *args, **kwargs):
        vb_controller.power_down()
