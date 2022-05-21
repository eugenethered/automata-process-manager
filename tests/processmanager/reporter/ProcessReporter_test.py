import unittest

from processrepo.Process import ProcessStatus
from processrepo.ProcessRunProfile import RunProfile

from processmanager.reporter.ProcessReporter import ProcessReporter
from tests.helper.ProcessRepositoryHelper import ProcessRepositoryHelper


class ProcessReporterTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.repository = ProcessRepositoryHelper()
        self.process_reporter = ProcessReporter(self.repository)

    def test_should_report_process(self):
        self.process_reporter.report('conductor', 'test', RunProfile.MINUTE, ProcessStatus.RUNNING)
        process_state_history = self.repository.help_get_process_state_history()
        self.assertEqual(len(process_state_history), 1)


if __name__ == '__main__':
    unittest.main()
