from processrepo.Process import ProcessStatus
from processrepo.repository.ProcessRepository import ProcessRepository

from processmanager.reporter.ProcessReporter import ProcessReporter


class ProcessBase:

    def __init__(self, options, market, process_name):
        self.options = options
        self.market = market
        self.process_name = process_name
        self.process_state = ProcessStatus.STOPPED
        self.process_reporter = self.init_process_reporter()

    def init_process_reporter(self):
        process_repository = ProcessRepository(self.options)
        return ProcessReporter(process_repository)

    def running(self):
        self.process_state = ProcessStatus.RUNNING
        self.report_process_status()

    def error(self):
        self.process_state = ProcessStatus.ERROR
        self.report_process_status()

    def stopped(self):
        self.process_state = ProcessStatus.STOPPED
        self.report_process_status()

    def report_process_status(self):
        self.process_reporter.report(self.process_name, self.market, self.process_state)

    def should_run(self) -> bool:
        return self.process_state == ProcessStatus.STOPPED

    def run(self):
        if self.should_run():
            try:
                self.running()
                self.process_to_run()
                self.stopped()
            except Exception:
                self.error()

    def process_to_run(self):
        pass
