from vm_server.virtual_machines.models import Plc, Project


def find_plc_based_on_id(plc_id):
    """
    Find the plc object based on the id
    Result: object of Plc class
    @param plc_id: string
    @return: object of Plc class
    """
    try:
        plc = Plc.objects.get(pk=plc_id)
        return plc
    except Plc.DoesNotExist:
        return None


def find_project_based_on_plc_id(plc_id):
    """
    Find the latest project loaded on the PLC
    Result: object of Project class
    @param plc_id: string
    @return: object of Project class
    """
    try:
        plc = Plc.objects.get(pk=plc_id)
        if plc.loaded_project:
            latest_project = plc.loaded_project
            return latest_project
        else:
            return None
    except Plc.DoesNotExist:
        return None


def check_if_git_hash_exists(git_hash):
    try:
        Project.objects.get(git_hash=git_hash)
        return True
    except Project.DoesNotExist:
        return False
