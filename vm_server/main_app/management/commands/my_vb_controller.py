from django.core.management.base import BaseCommand
# from vm_server.settings import vb_controller


from controllers.vb_controller_instance import vb_controller


class Command(BaseCommand):
    help = 'Runs the VM controller'

    def handle(self, *args, **kwargs):
        vb_controller.initiate()
        vb_controller.start_machine_in_window()
