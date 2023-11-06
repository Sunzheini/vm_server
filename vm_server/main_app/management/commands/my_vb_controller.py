from django.core.management.base import BaseCommand
from vm_server.main_app.vb_controller import VBController

from vm_server.main_app.vb_controller_instance import vb_controller


class Command(BaseCommand):
    help = 'Runs the VM controller'

    def handle(self, *args, **kwargs):
        # vb_controller = VBController()
        vb_controller.initiate()
        vb_controller.start_machine_in_window()
