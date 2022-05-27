import unittest

from processrepo.Process import ProcessStatus
from processrepo.ProcessRunProfile import RunProfile

from processmanager.ProcessRunner import ProcessRunner
from processmanager.reporter.ProcessReporter import ProcessReporter
from tests.helper.ProcessRepositoryHelper import ProcessRepositoryHelper


class ProcessRunnerTestCase(unittest.TestCase):

    def test_process_should_report_status_to_completion(self):
        process_repository = ProcessRepositoryHelper()

        class TestProcessRunner(ProcessRunner):
            def init_process_reporter(self):
                self.process_count = 0
                return ProcessReporter(process_repository)

            def init_process_run_profile(self):
                return RunProfile.MINUTE

            def process_to_run(self):
                self.process_count += 1

        process_to_run = TestProcessRunner(options={'VERSION':'0.0.1'}, market='test', process_name='conductor')
        process_to_run.run()

        process = process_repository.help_get_current_state()
        self.assertEqual(process.status, ProcessStatus.IDLE)
        process_history = process_repository.help_get_process_state_history()
        self.assertEqual(len(process_history), 3)
        self.assertEqual(process_history[0].status, ProcessStatus.INITIALIZED)
        self.assertEqual(process_history[1].status, ProcessStatus.RUNNING)
        self.assertEqual(process_history[2].status, ProcessStatus.IDLE)

    def test_process_should_not_run_when_busy_running(self):
        process_repository = ProcessRepositoryHelper()

        class TestProcessRunner(ProcessRunner):
            def init_process_reporter(self):
                self.process_count = 0
                return ProcessReporter(process_repository)

            def init_process_run_profile(self):
                return RunProfile.MINUTE

            def run(self):
                # (override) hack to never stop the process
                if self.should_run_process():
                    self.process_running()
                    self.process_to_run()

            def process_to_run(self):
                self.process_count += 1

        process_to_run = TestProcessRunner(options={'VERSION':'0.0.1'}, market='test', process_name='conductor')
        process_to_run.run()
        process = process_repository.help_get_current_state()
        self.assertEqual(process.status, ProcessStatus.RUNNING, 'confirm process is running')
        self.assertEqual(process_to_run.process_count, 1)
        process_to_run.run()
        self.assertEqual(process_to_run.process_count, 1)
        process_history = process_repository.help_get_process_state_history()
        self.assertEqual(len(process_history), 2)
        self.assertEqual(process_history[0].status, ProcessStatus.INITIALIZED)
        self.assertEqual(process_history[1].status, ProcessStatus.RUNNING)

    def test_process_should_report_status_as_error(self):
        process_repository = ProcessRepositoryHelper()

        class TestProcessRunner(ProcessRunner):
            def init_process_reporter(self):
                self.process_count = 0
                return ProcessReporter(process_repository)

            def init_process_run_profile(self):
                return RunProfile.MINUTE

            def process_to_run(self):
                raise ValueError('some error')

        process_to_run = TestProcessRunner(options={'VERSION':'0.0.1'}, market='test', process_name='conductor')
        process_to_run.run()

        process = process_repository.help_get_current_state()
        self.assertEqual(process.status, ProcessStatus.ERROR)
        process_history = process_repository.help_get_process_state_history()
        self.assertEqual(len(process_history), 3)
        self.assertEqual(process_history[0].status, ProcessStatus.INITIALIZED)
        self.assertEqual(process_history[1].status, ProcessStatus.RUNNING)
        self.assertEqual(process_history[2].status, ProcessStatus.ERROR)

    def test_process_should_not_run_when_process_in_error(self):
        process_repository = ProcessRepositoryHelper()

        class TestProcessRunner(ProcessRunner):
            def init_process_reporter(self):
                return ProcessReporter(process_repository)

            def init_process_run_profile(self):
                return RunProfile.MINUTE

            def process_to_run(self):
                raise ValueError('some error')

        process_to_run = TestProcessRunner(options={'VERSION':'0.0.1'}, market='test', process_name='conductor')
        process_to_run.run()
        process = process_repository.help_get_current_state()
        self.assertEqual(process.status, ProcessStatus.ERROR, 'confirm process is running')
        process_to_run.run()
        process_history = process_repository.help_get_process_state_history()
        self.assertEqual(len(process_history), 3)
        self.assertEqual(process_history[0].status, ProcessStatus.INITIALIZED)
        self.assertEqual(process_history[1].status, ProcessStatus.RUNNING)
        self.assertEqual(process_history[2].status, ProcessStatus.ERROR)

    def test_process_not_run_due_to_custom_pre_process_intervention(self):
        process_repository = ProcessRepositoryHelper()

        class TestProcessRunner(ProcessRunner):
            def init_process_reporter(self):
                self.process_count = 0
                return ProcessReporter(process_repository)

            def init_process_run_profile(self):
                return RunProfile.MINUTE

            def intervene_process(self) -> bool:
                return 1 == 1 and len('execute') > 0

            def process_to_run(self):
                self.process_count += 1

        process_to_run = TestProcessRunner(options={'VERSION':'0.0.1'}, market='test', process_name='conductor')
        process_to_run.run()

        process = process_repository.help_get_current_state()
        self.assertEqual(process.status, ProcessStatus.INITIALIZED)
        process_history = process_repository.help_get_process_state_history()
        self.assertEqual(len(process_history), 1)
        self.assertEqual(process_history[0].status, ProcessStatus.INITIALIZED)


if __name__ == '__main__':
    unittest.main()
