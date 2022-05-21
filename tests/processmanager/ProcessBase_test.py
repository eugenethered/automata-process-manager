import time
import unittest

from processrepo.Process import ProcessStatus

from processmanager.ProcessBase import ProcessBase
from processmanager.reporter.ProcessReporter import ProcessReporter
from tests.helper.ProcessRepositoryHelper import ProcessRepositoryHelper


class ProcessBaseTestCase(unittest.TestCase):

    def test_process_should_report_status_to_completion(self):
        process_repository = ProcessRepositoryHelper()

        class ProcessRunner(ProcessBase):
            def init_process_reporter(self):
                self.process_count = 0
                return ProcessReporter(process_repository)

            def process_to_run(self):
                self.process_count += 1

        process_to_run = ProcessRunner(options={}, market='test', process_name='conductor')
        process_to_run.run()

        process = process_repository.help_get_current_state()
        self.assertEqual(process.status, ProcessStatus.STOPPED)
        process_history = process_repository.help_get_process_state_history()
        self.assertEqual(len(process_history), 2)
        self.assertEqual(process_history[0].status, ProcessStatus.RUNNING)
        self.assertEqual(process_history[1].status, ProcessStatus.STOPPED)

    def test_process_should_not_run_when_busy_running(self):
        process_repository = ProcessRepositoryHelper()

        class ProcessRunner(ProcessBase):
            def init_process_reporter(self):
                self.process_count = 0
                return ProcessReporter(process_repository)

            def run(self):
                # (override) hack to never stop the process
                if self.should_run():
                    self.running()
                    self.process_to_run()

            def process_to_run(self):
                self.process_count += 1

        process_to_run = ProcessRunner(options={}, market='test', process_name='conductor')
        process_to_run.run()
        process = process_repository.help_get_current_state()
        self.assertEqual(process.status, ProcessStatus.RUNNING, 'confirm process is running')
        self.assertEqual(process_to_run.process_count, 1)
        process_to_run.run()
        self.assertEqual(process_to_run.process_count, 1)
        process_history = process_repository.help_get_process_state_history()
        self.assertEqual(len(process_history), 1)
        self.assertEqual(process_history[0].status, ProcessStatus.RUNNING)

    def test_process_should_report_status_as_error(self):
        process_repository = ProcessRepositoryHelper()

        class ProcessRunner(ProcessBase):
            def init_process_reporter(self):
                self.process_count = 0
                return ProcessReporter(process_repository)

            def process_to_run(self):
                raise ValueError('some error')

        process_to_run = ProcessRunner(options={}, market='test', process_name='conductor')
        process_to_run.run()

        process = process_repository.help_get_current_state()
        self.assertEqual(process.status, ProcessStatus.ERROR)
        process_history = process_repository.help_get_process_state_history()
        self.assertEqual(len(process_history), 2)
        self.assertEqual(process_history[0].status, ProcessStatus.RUNNING)
        self.assertEqual(process_history[1].status, ProcessStatus.ERROR)

    def test_process_should_not_run_when_process_in_error(self):
        process_repository = ProcessRepositoryHelper()

        class ProcessRunner(ProcessBase):
            def init_process_reporter(self):
                return ProcessReporter(process_repository)

            def process_to_run(self):
                raise ValueError('some error')

        process_to_run = ProcessRunner(options={}, market='test', process_name='conductor')
        process_to_run.run()
        process = process_repository.help_get_current_state()
        self.assertEqual(process.status, ProcessStatus.ERROR, 'confirm process is running')
        process_to_run.run()
        process_history = process_repository.help_get_process_state_history()
        self.assertEqual(len(process_history), 2)
        self.assertEqual(process_history[0].status, ProcessStatus.RUNNING)
        self.assertEqual(process_history[1].status, ProcessStatus.ERROR)



if __name__ == '__main__':
    unittest.main()