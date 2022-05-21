import unittest

from cache.holder.RedisCacheHolder import RedisCacheHolder
from processrepo.Process import ProcessStatus
from processrepo.repository.ProcessRepository import ProcessRepository

from processmanager.reporter.ProcessReporter import ProcessReporter


class ProcessReporterTestCase(unittest.TestCase):

    def setUp(self) -> None:
        options = {
            'REDIS_SERVER_ADDRESS': '192.168.1.90',
            'REDIS_SERVER_PORT': 6379,
            'PROCESS_KEY': '{}:process:status:{}'
        }
        self.cache = RedisCacheHolder(options)
        self.repository = ProcessRepository(options)
        self.process_reporter = ProcessReporter(self.repository)

    def tearDown(self):
        self.cache.delete('test:process:status:conductor')

    def test_should_report_process(self):
        self.process_reporter.report('conductor', 'test', ProcessStatus.RUNNING)
        process = self.repository.retrieve('test', 'conductor')
        self.assertEqual(process.market, 'test')
        self.assertEqual(process.name, 'conductor')
        self.assertEqual(process.status, ProcessStatus.RUNNING)
        self.assertGreater(process.instant, 0)


if __name__ == '__main__':
    unittest.main()
