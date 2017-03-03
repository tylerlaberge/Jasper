from unittest import TestCase, mock
from click.testing import CliRunner
from jasper.entrypoints import jasper
import os


class JasperTestCase(TestCase):

    def setUp(self):
        self.test_directory = os.path.abspath('.\mock_features')

    @mock.patch('jasper.entrypoints.Display')
    @mock.patch('jasper.entrypoints.Runner')
    def test_jasper_without_options(self, mock_runner_class, mock_display_class):
        mock_runner = mock.MagicMock()
        mock_runner.run.return_value = 'foobar'
        mock_runner_class.return_value = mock_runner

        mock_display = mock.MagicMock()
        mock_display_class.return_value = mock_display

        click_runner = CliRunner()
        result = click_runner.invoke(jasper, [self.test_directory])

        self.assertEqual(result.exit_code, 0)
        mock_runner_class.assert_called_once_with(self.test_directory)
        mock_runner.run.assert_called_once()
        mock_display_class.assert_called_once_with(force_ansi=False, verbosity_level=0)
        mock_display.prepare_suite.assert_called_once_with(mock_runner.run.return_value)
        mock_display.display.assert_called_once()

    @mock.patch('jasper.entrypoints.Display')
    @mock.patch('jasper.entrypoints.Runner')
    def test_jasper_with_options(self, mock_runner_class, mock_display_class):
        mock_runner = mock.MagicMock()
        mock_runner.run.return_value = 'foobar'
        mock_runner_class.return_value = mock_runner

        mock_display = mock.MagicMock()
        mock_display_class.return_value = mock_display

        click_runner = CliRunner()
        result = click_runner.invoke(jasper, [self.test_directory, '--ansi', '-v 2'])

        self.assertEqual(result.exit_code, 0)
        mock_runner_class.assert_called_once_with(self.test_directory)
        mock_runner.run.assert_called_once()
        mock_display_class.assert_called_once_with(force_ansi=True, verbosity_level=2)
        mock_display.prepare_suite.assert_called_once_with(mock_runner.run.return_value)
        mock_display.display.assert_called_once()

    @mock.patch('jasper.entrypoints.Display')
    @mock.patch('jasper.entrypoints.Runner')
    def test_jasper_with_missing_directory(self, mock_runner_class, mock_display_class):
        click_runner = CliRunner()
        result = click_runner.invoke(jasper, ['foobar'])

        self.assertEqual(result.exit_code, 2)

    @mock.patch('jasper.entrypoints.Display')
    @mock.patch('jasper.entrypoints.Runner')
    def test_jasper_with_missing_required_arguments(self, mock_runner_class, mock_display_class):
        click_runner = CliRunner()
        result = click_runner.invoke(jasper, [])

        self.assertEqual(result.exit_code, 2)
