from typing import Optional

from processrepo.Process import Process
from processrepo.repository.ProcessRepository import ProcessRepository


class ProcessRepositoryHelper(ProcessRepository):

    def __init__(self):
        self.processes = []

    def store(self, process: Process):
        self.processes.append(process)

    def help_get_process_state_history(self):
        return self.processes

    def help_get_current_state(self) -> Optional[Process]:
        if len(self.processes) == 0:
            return None
        return self.processes[-1:][0]
