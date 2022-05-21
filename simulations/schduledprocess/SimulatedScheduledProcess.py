from time import sleep

from processrepo.ProcessRunProfile import RunProfile

from processmanager.ScheduledProcess import ScheduledProcess


class SimulatedScheduledProcess(ScheduledProcess):

    def __init__(self, options, market, process_name):
        self.process_count = 0
        super().__init__(options, market, process_name)

    def init_process_run_profile(self):
        return RunProfile.ASAP

    def process_to_run(self):
        self.process_count += 1
        print(f'process count:{self.process_count}')
        # simulating long-running process
        sleep(10)
