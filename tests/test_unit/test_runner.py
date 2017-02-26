from unittest import TestCase, mock
from jasper.runner import Runner


class RunnerTestCase(TestCase):

    def setUp(self):
        self.test_directory = '.\mock_features'

    @mock.patch('jasper.runner.Suite')
    def test_init(self, mock_suite):
        runner = Runner(self.test_directory)

        self.assertEqual(runner.test_directory, self.test_directory)
        self.assertEqual(runner.test_file_paths, [])
        self.assertTrue(isinstance(runner.suite, mock.MagicMock))

    @mock.patch('jasper.runner.Suite')
    def test_discover(self, mock_suite):
        runner = Runner(self.test_directory)
        runner.discover()

        self.assertEqual(runner.test_file_paths, [
            ".\\mock_features\\runner\\runner_feature.py",
            ".\\mock_features\\runner_two\\runner_two_feature.py"
        ])

    @mock.patch('jasper.runner.Suite')
    def test_build_suite(self, mock_suite):

        added_features = []

        def save_feature(feature):
            added_features.append(feature)

        runner = Runner(self.test_directory)
        runner.suite.add_feature.side_effect = save_feature
        runner.test_file_paths = [
            ".\\mock_features\\runner\\runner_feature.py",
            ".\\mock_features\\runner_two\\runner_two_feature.py"
        ]
        runner.build_suite()

        self.assertEqual(runner.suite.add_feature.call_count, 2)
        self.assertEqual(len(added_features), 2)
        self.assertTrue(type(added_features[0]), mock.MagicMock)
        self.assertTrue(type(added_features[1]), mock.MagicMock)
        self.assertEqual(added_features[0].name, 'runner_feature')
        self.assertEqual(added_features[1].name, 'runner_two_feature')

    @mock.patch.object(Runner, 'build_suite')
    @mock.patch.object(Runner, 'discover')
    @mock.patch('jasper.runner.Suite')
    def test_run(self, mock_suite, mock_discover_method, mock_build_suite_method):
        runner = Runner(self.test_directory)

        mock_run_called = False
        async def mock_run():
            nonlocal mock_run_called
            mock_run_called = True

        runner.suite.run = mock_run

        completed_suite = runner.run()

        # noinspection PyUnresolvedReferences
        runner.discover.assert_called_once()
        # noinspection PyUnresolvedReferences
        runner.build_suite.assert_called_once()
        self.assertTrue(mock_run_called)
        self.assertEqual(runner.suite, completed_suite)
