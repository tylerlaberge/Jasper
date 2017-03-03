from unittest import TestCase, mock
from jasper.display import Display
from jasper.utility import extract_traceback
import colorama
from termcolor import colored


class DisplayTestCase(TestCase):

    @mock.patch.object(colorama, 'deinit')
    def test_init(self, mock_deinit):
        display = Display()

        self.assertEqual(display.display_string, '')
        self.assertEqual(display.indentation_level, 0)
        self.assertEqual(display.verbosity_level, 0)
        self.assertEqual(display.colored, True)
        self.assertEqual(display.force_ansi, True)
        mock_deinit.assert_called_once()

    def test_cyan_with_colored_on(self):
        display = Display()
        display.colored = True

        self.assertEqual(display.cyan('foobar'), colored('foobar', 'cyan'))

    def test_cyan_without_colored_on(self):
        display = Display()
        display.colored = False

        self.assertEqual(display.cyan('foobar'), 'foobar')

    def test_yellow_with_colored_on(self):
        display = Display()
        display.colored = True

        self.assertEqual(display.yellow('foobar'), colored('foobar', 'yellow'))

    def test_yellow_without_colored_on(self):
        display = Display()
        display.colored = False

        self.assertEqual(display.yellow('foobar'), 'foobar')

    def test_red_with_colored_on(self):
        display = Display()
        display.colored = True

        self.assertEqual(display.red('foobar'), colored('foobar', 'red'))

    def test_red_without_colored_on(self):
        display = Display()
        display.colored = False

        self.assertEqual(display.red('foobar'), 'foobar')

    def test_grey_with_colored_on(self):
        display = Display()
        display.colored = True

        self.assertEqual(display.grey('foobar'), colored('foobar', 'white'))

    def test_grey_without_colored_on(self):
        display = Display()
        display.colored = False

        self.assertEqual(display.grey('foobar'), 'foobar')

    @mock.patch.object(colorama, 'deinit')
    @mock.patch.object(colorama, 'init')
    @mock.patch('jasper.display.sys')
    @mock.patch('builtins.print')
    def test_display_windows(self, mock_print, mock_sys, mock_init, mock_deinit):
        mock_sys.platform = 'win32'

        display = Display()
        display.display_string = 'foobar'
        display.force_ansi = False

        display.display()

        mock_init.assert_called_once()
        mock_print.assert_called_once_with('foobar')
        mock_deinit.assert_called()

    @mock.patch.object(colorama, 'deinit')
    @mock.patch.object(colorama, 'init')
    @mock.patch('jasper.display.sys')
    @mock.patch('builtins.print')
    def test_display_windows_with_ansi(self, mock_print, mock_sys, mock_init, mock_deinit):
        mock_sys.platform = 'win32'

        display = Display()
        display.display_string = 'foobar'
        display.force_ansi = True

        display.display()

        mock_init.assert_not_called()
        mock_print.assert_called_once_with('foobar')
        mock_deinit.assert_called()

    @mock.patch.object(colorama, 'deinit')
    @mock.patch.object(colorama, 'init')
    @mock.patch('jasper.display.sys')
    @mock.patch('builtins.print')
    def test_display_non_windows(self, mock_print, mock_sys, mock_init, mock_deinit):
        mock_sys.platform = 'foobarbaz'

        display = Display()
        display.display_string = 'foobar'
        display.force_ansi = False

        display.display()

        mock_init.assert_not_called()
        mock_print.assert_called_once_with('foobar')
        mock_deinit.assert_called()

    @mock.patch.object(Display, 'grey')
    @mock.patch.object(Display, 'red')
    @mock.patch.object(Display, 'cyan', side_effect=lambda text: text)
    @mock.patch('jasper.Step')
    def test_prepare_passing_step(self, step_mock, cyan_mock, red_mock, grey_mock):
        step_mock.ran = True
        step_mock.passed = True
        step_mock.kwargs = {'mock': 'kwargs'}

        def mock_function():
            pass

        step_mock.function = mock_function

        display = Display()
        display.prepare_step(step_mock, 'MockStep')

        self.assertEqual(display.indentation_level, 0)
        self.assertEqual(display.display_string, "MockStep: mock_function {'mock': 'kwargs'}\n")
        display.cyan.assert_called_once_with("MockStep: mock_function {'mock': 'kwargs'}")
        display.red.assert_not_called()
        display.grey.assert_not_called()

    @mock.patch.object(Display, 'grey')
    @mock.patch.object(Display, 'red', side_effect=lambda text: text)
    @mock.patch.object(Display, 'cyan')
    @mock.patch('jasper.Step')
    def test_prepare_failing_step(self, step_mock, cyan_mock, red_mock, grey_mock):
        step_mock.ran = True
        step_mock.passed = False
        step_mock.kwargs = {'mock': 'kwargs'}

        def mock_function():
            pass

        step_mock.function = mock_function

        display = Display()
        display.prepare_step(step_mock, 'MockStep')

        self.assertEqual(display.indentation_level, 0)
        self.assertEqual(display.display_string, "MockStep: mock_function {'mock': 'kwargs'}\n")
        display.cyan.assert_not_called()
        display.red.assert_called_once_with("MockStep: mock_function {'mock': 'kwargs'}")
        display.grey.assert_not_called()

    @mock.patch.object(Display, 'grey', side_effect=lambda text: text)
    @mock.patch.object(Display, 'red')
    @mock.patch.object(Display, 'cyan')
    @mock.patch('jasper.Step')
    def test_prepare_skipped_step(self, step_mock, cyan_mock, red_mock, grey_mock):
        step_mock.ran = False
        step_mock.passed = False
        step_mock.kwargs = {'mock': 'kwargs'}

        def mock_function():
            pass

        step_mock.function = mock_function

        display = Display()
        display.prepare_step(step_mock, 'MockStep')

        self.assertEqual(display.indentation_level, 0)
        self.assertEqual(display.display_string, "MockStep: mock_function {'mock': 'kwargs'}\n")
        display.cyan.assert_not_called()
        display.red.assert_not_called()
        display.grey.assert_called_once_with("MockStep: mock_function {'mock': 'kwargs'}")

    @mock.patch.object(Display, 'yellow', side_effect=lambda text: text)
    def test_prepare_exception(self, yellow_mock):
        try:
            raise Exception('FooBarException')
        except Exception as e:
            display = Display()
            display.prepare_exception(e)

            self.assertEqual(display.indentation_level, 0)
            self.assertEqual(display.display_string, "FooBarException\n" + extract_traceback(e))
            display.yellow.assert_called_once_with(("FooBarException\n" + extract_traceback(e)).rstrip())

    @mock.patch.object(Display, 'yellow', side_effect=lambda text: text)
    def test_prepare_exception_without_str_representation(self, yellow_mock):
        try:
            class FooBarException(Exception):

                def __str__(self):
                    return ''

            raise FooBarException
        except FooBarException as e:
            display = Display()
            display.prepare_exception(e)

            self.assertEqual(display.indentation_level, 0)
            self.assertEqual(display.display_string, "FooBarException\n" + extract_traceback(e))
            display.yellow.assert_called_once_with(("FooBarException\n" + extract_traceback(e)).rstrip())

    @mock.patch.object(Display, 'cyan', side_effect=lambda text: text)
    def test_prepare_border(self, cyan_mock):
        display = Display()
        border = display.prepare_border(cyan_mock, 50)

        self.assertEqual(border, '='*50)
        display.cyan.assert_called_once_with('='*50)

    @mock.patch('jasper.scenario.Scenario')
    def test_prepare_passing_scenario_verbose_0(self, scenario):
        display = Display()
        display.prepare_scenario(scenario)

        self.assertEqual(display.display_string, "")

    @mock.patch.object(Display, 'grey')
    @mock.patch.object(Display, 'red')
    @mock.patch.object(Display, 'cyan', side_effect=lambda text: text)
    @mock.patch('jasper.scenario.Scenario')
    def test_prepare_passing_scenario_verbose_1(self, scenario, cyan_mock, red_mock, grey_mock):
        display = Display()
        display.verbosity_level = 1

        scenario.description = 'Mock Scenario'
        scenario.ran = True
        scenario.passed = True

        display.prepare_scenario(scenario)

        cyan_mock.assert_called_once_with("Scenario: Mock Scenario")
        red_mock.assert_not_called()
        grey_mock.assert_not_called()
        self.assertEqual(display.indentation_level, 0)
        self.assertEqual(display.display_string, "Scenario: Mock Scenario\n")

    @mock.patch.object(Display, 'grey', side_effect=lambda text: text)
    @mock.patch.object(Display, 'red')
    @mock.patch.object(Display, 'cyan')
    @mock.patch('jasper.scenario.Scenario')
    def test_prepare_skipped_scenario_verbose_1(self, scenario, cyan_mock, red_mock, grey_mock):
        display = Display()
        display.verbosity_level = 1

        scenario.description = 'Mock Scenario'
        scenario.ran = False
        scenario.passed = True

        display.prepare_scenario(scenario)

        cyan_mock.assert_not_called()
        red_mock.assert_not_called()
        grey_mock.assert_called_once_with("Scenario: Mock Scenario")
        self.assertEqual(display.indentation_level, 0)
        self.assertEqual(display.display_string, "Scenario: Mock Scenario\n")

    @mock.patch.object(Display, 'grey')
    @mock.patch.object(Display, 'red')
    @mock.patch.object(Display, 'cyan', side_effect=lambda text: text)
    @mock.patch.object(Display, 'prepare_exception')
    @mock.patch.object(Display, 'prepare_step')
    @mock.patch('jasper.scenario.Scenario')
    def test_prepare_passing_scenario_verbose_2(self, scenario, prepare_step_mock, prepare_exception_mock, cyan_mock, red_mock, grey_mock):
        display = Display()
        display.verbosity_level = 2

        scenario.description = 'Mock Scenario'
        scenario.ran = True
        scenario.passed = True
        scenario.exception = None
        scenario.before_all = ['before_all_one', 'before_all_two']
        scenario.after_all = ['after_all']
        scenario.before_each = ['before_each']
        scenario.after_each = ['after_each_one', 'after_each_two']
        scenario.given = ['given_one', 'given_two']
        scenario.when = ['when_one', 'when_two']
        scenario.then = ['then_one', 'then_two']

        display.prepare_scenario(scenario)

        cyan_mock.assert_called_once_with('Scenario: Mock Scenario')
        red_mock.assert_not_called()
        grey_mock.assert_not_called()

        display.prepare_step.assert_any_call('before_all_one', 'BeforeAll')
        display.prepare_step.assert_any_call('before_all_two', 'BeforeAll')
        display.prepare_step.assert_any_call('after_all', 'AfterAll')
        display.prepare_step.assert_any_call('before_each', 'BeforeEach')
        display.prepare_step.assert_any_call('after_each_one', 'AfterEach')
        display.prepare_step.assert_any_call('after_each_two', 'AfterEach')
        display.prepare_step.assert_any_call('given_one', 'Given')
        display.prepare_step.assert_any_call('given_two', 'And')
        display.prepare_step.assert_any_call('when_one', 'When')
        display.prepare_step.assert_any_call('when_two', 'And')
        display.prepare_step.assert_any_call('then_one', 'Then')
        display.prepare_step.assert_any_call('then_two', 'And')

        display.prepare_exception.assert_not_called()

        self.assertEqual(display.display_string, 'Scenario: Mock Scenario\n')

    @mock.patch.object(Display, 'grey')
    @mock.patch.object(Display, 'red', side_effect=lambda text: text)
    @mock.patch.object(Display, 'cyan')
    @mock.patch.object(Display, 'prepare_exception')
    @mock.patch.object(Display, 'prepare_step')
    @mock.patch('jasper.scenario.Scenario')
    def test_prepare_failing_scenario_verbose_0(self, scenario, prepare_step_mock, prepare_exception_mock, cyan_mock, red_mock, grey_mock):
        display = Display()
        display.verbosity_level = 0

        scenario.description = 'Mock Scenario'
        scenario.ran = True
        scenario.passed = False
        scenario.exception = 'FooBarException'
        scenario.before_all = ['before_all_one', 'before_all_two']
        scenario.after_all = ['after_all']
        scenario.before_each = ['before_each']
        scenario.after_each = ['after_each_one', 'after_each_two']
        scenario.given = ['given_one', 'given_two']
        scenario.when = ['when_one', 'when_two']
        scenario.then = ['then_one', 'then_two']

        display.prepare_scenario(scenario)

        cyan_mock.assert_not_called()
        red_mock.assert_called_once_with('Scenario: Mock Scenario')
        grey_mock.assert_not_called()

        display.prepare_step.assert_any_call('before_all_one', 'BeforeAll')
        display.prepare_step.assert_any_call('before_all_two', 'BeforeAll')
        display.prepare_step.assert_any_call('after_all', 'AfterAll')
        display.prepare_step.assert_any_call('before_each', 'BeforeEach')
        display.prepare_step.assert_any_call('after_each_one', 'AfterEach')
        display.prepare_step.assert_any_call('after_each_two', 'AfterEach')
        display.prepare_step.assert_any_call('given_one', 'Given')
        display.prepare_step.assert_any_call('given_two', 'And')
        display.prepare_step.assert_any_call('when_one', 'When')
        display.prepare_step.assert_any_call('when_two', 'And')
        display.prepare_step.assert_any_call('then_one', 'Then')
        display.prepare_step.assert_any_call('then_two', 'And')

        display.prepare_exception.assert_called_once_with('FooBarException')

        self.assertEqual(display.display_string, 'Scenario: Mock Scenario\n')

    @mock.patch('jasper.feature.Feature')
    def test_prepare_passing_feature_verbose_0(self, mock_feature):
        display = Display()
        display.prepare_feature(mock_feature)

        self.assertEqual(display.display_string, "")

    @mock.patch.object(Display, 'red')
    @mock.patch.object(Display, 'cyan', side_effect=lambda text: text)
    @mock.patch.object(Display, 'prepare_exception')
    @mock.patch.object(Display, 'prepare_scenario')
    @mock.patch.object(Display, 'prepare_border', side_effect=lambda _, amount: '='*amount)
    @mock.patch('jasper.feature.Feature')
    def test_prepare_passing_feature_verbose_1(self, mock_feature, mock_prepare_border,
                                               mock_prepare_scenario, mock_prepare_exception, cyan_mock, red_mock):
        display = Display()
        display.verbosity_level = 1

        mock_feature.description = 'Mock Feature'
        mock_feature.passed = True
        mock_feature.exception = None
        mock_feature.scenarios = ['scenario_one', 'scenario_two']

        display.prepare_feature(mock_feature)

        cyan_mock.assert_called_once_with("Feature: Mock Feature")
        red_mock.assert_not_called()
        display.prepare_scenario.assert_any_call('scenario_one')
        display.prepare_scenario.assert_any_call('scenario_two')
        display.prepare_exception.assert_not_called()

        self.assertEqual(display.display_string,
                         "="*150 + "\n" + "Feature: Mock Feature\n" + "="*150 + "\n")

    @mock.patch.object(Display, 'red')
    @mock.patch.object(Display, 'cyan', side_effect=lambda text: text)
    @mock.patch.object(Display, 'prepare_exception')
    @mock.patch.object(Display, 'prepare_scenario')
    @mock.patch.object(Display, 'prepare_step')
    @mock.patch.object(Display, 'prepare_border', side_effect=lambda _, amount: '='*amount)
    @mock.patch('jasper.feature.Feature')
    def test_prepare_passing_feature_verbose_2(self, mock_feature, mock_prepare_border,
                                               mock_prepare_step, mock_prepare_scenario, mock_prepare_exception, cyan_mock, red_mock):
        display = Display()
        display.verbosity_level = 2

        mock_feature.description = 'Mock Feature'
        mock_feature.passed = True
        mock_feature.exception = None
        mock_feature.scenarios = ['scenario_one', 'scenario_two']
        mock_feature.before_all = ['before_all_one', 'before_all_two']
        mock_feature.after_all = ['after_all']
        mock_feature.before_each = ['before_each']
        mock_feature.after_each = ['after_each_one', 'after_each_two']

        display.prepare_feature(mock_feature)

        cyan_mock.assert_called_once_with("Feature: Mock Feature")
        red_mock.assert_not_called()

        display.prepare_step.assert_any_call('before_all_one', 'BeforeAll')
        display.prepare_step.assert_any_call('before_all_two', 'BeforeAll')
        display.prepare_step.assert_any_call('after_all', 'AfterAll')
        display.prepare_step.assert_any_call('before_each', 'BeforeEach')
        display.prepare_step.assert_any_call('after_each_one', 'AfterEach')
        display.prepare_step.assert_any_call('after_each_two', 'AfterEach')

        display.prepare_scenario.assert_any_call('scenario_one')
        display.prepare_scenario.assert_any_call('scenario_two')
        display.prepare_exception.assert_not_called()

        self.assertEqual(display.display_string,
                         "="*150 + "\n" + "Feature: Mock Feature\n" + "="*150 + "\n")

    @mock.patch.object(Display, 'red', side_effect=lambda text: text)
    @mock.patch.object(Display, 'cyan')
    @mock.patch.object(Display, 'prepare_exception')
    @mock.patch.object(Display, 'prepare_scenario')
    @mock.patch.object(Display, 'prepare_step')
    @mock.patch.object(Display, 'prepare_border', side_effect=lambda _, amount: '='*amount)
    @mock.patch('jasper.feature.Feature')
    def test_prepare_failing_feature_verbose_0(self, mock_feature, mock_prepare_border,
                                               mock_prepare_step, mock_prepare_scenario, mock_prepare_exception, cyan_mock, red_mock):
        display = Display()
        display.verbosity_level = 0

        mock_feature.description = 'Mock Feature'
        mock_feature.passed = False
        mock_feature.exception = 'FooBarException'
        mock_feature.scenarios = ['scenario_one', 'scenario_two']
        mock_feature.before_all = ['before_all_one', 'before_all_two']
        mock_feature.after_all = ['after_all']
        mock_feature.before_each = ['before_each']
        mock_feature.after_each = ['after_each_one', 'after_each_two']

        display.prepare_feature(mock_feature)

        cyan_mock.assert_not_called()
        red_mock.assert_called_once_with("Feature: Mock Feature")

        display.prepare_step.assert_any_call('before_all_one', 'BeforeAll')
        display.prepare_step.assert_any_call('before_all_two', 'BeforeAll')
        display.prepare_step.assert_any_call('after_all', 'AfterAll')
        display.prepare_step.assert_any_call('before_each', 'BeforeEach')
        display.prepare_step.assert_any_call('after_each_one', 'AfterEach')
        display.prepare_step.assert_any_call('after_each_two', 'AfterEach')

        display.prepare_scenario.assert_any_call('scenario_one')
        display.prepare_scenario.assert_any_call('scenario_two')
        display.prepare_exception.assert_called_once_with('FooBarException')

        self.assertEqual(display.display_string,
                         "="*150 + "\n" + "Feature: Mock Feature\n" + "="*150 + "\n")

    @mock.patch.object(Display, 'red')
    @mock.patch.object(Display, 'cyan', side_effect=lambda text: text)
    @mock.patch.object(Display, 'prepare_statistics')
    @mock.patch.object(Display, 'prepare_border', side_effect=lambda _, n: '='*150)
    @mock.patch.object(Display, 'prepare_feature')
    @mock.patch('jasper.suite.Suite')
    def test_prepare_passing_suite_verbose_0(self, mock_suite, mock_prepare_feature,
                                             mock_prepare_border, mock_prepare_statistics,
                                             mock_cyan, mock_red):

        display = Display()
        display.verbosity_level = 0

        mock_suite.passed = True

        display.prepare_suite(mock_suite)

        display.prepare_border.assert_called_with(mock_cyan, 150)
        display.prepare_feature.assert_not_called()
        display.prepare_statistics.assert_called_with(mock_suite)
        self.assertEqual(display.display_string, "="*150 + "\n" + "="*150 + "\n")

    @mock.patch.object(Display, 'red')
    @mock.patch.object(Display, 'cyan', side_effect=lambda text: text)
    @mock.patch.object(Display, 'prepare_statistics')
    @mock.patch.object(Display, 'prepare_border', side_effect=lambda _, n: '='*150)
    @mock.patch.object(Display, 'prepare_feature')
    @mock.patch('jasper.suite.Suite')
    def test_prepare_passing_suite_verbose_1(self, mock_suite, mock_prepare_feature,
                                             mock_prepare_border, mock_prepare_statistics,
                                             mock_cyan, mock_red):

        display = Display()
        display.verbosity_level = 1

        mock_suite.passed = True
        mock_suite.features = ['feature_one', 'feature_two']

        display.prepare_suite(mock_suite)

        display.prepare_border.assert_called_with(mock_cyan, 150)
        display.prepare_feature.assert_any_call('feature_one')
        display.prepare_feature.assert_any_call('feature_two')
        display.prepare_statistics.assert_called_with(mock_suite)
        self.assertEqual(display.display_string, "="*150 + "\n" + "="*150 + "\n")

    @mock.patch.object(Display, 'red', side_effect=lambda text: text)
    @mock.patch.object(Display, 'cyan')
    @mock.patch.object(Display, 'prepare_statistics')
    @mock.patch.object(Display, 'prepare_border', side_effect=lambda _, n: '='*150)
    @mock.patch.object(Display, 'prepare_feature')
    @mock.patch('jasper.suite.Suite')
    def test_prepare_failing_suite_verbose_0(self, mock_suite, mock_prepare_feature,
                                             mock_prepare_border, mock_prepare_statistics,
                                             mock_cyan, mock_red):

        display = Display()
        display.verbosity_level = 0

        mock_suite.passed = False
        mock_suite.features = ['feature_one', 'feature_two']

        display.prepare_suite(mock_suite)

        display.prepare_border.assert_called_with(mock_red, 150)
        display.prepare_feature.assert_any_call('feature_one')
        display.prepare_feature.assert_any_call('feature_two')
        display.prepare_statistics.assert_called_with(mock_suite)
        self.assertEqual(display.display_string, "="*150 + "\n" + "="*150 + "\n")

    @mock.patch.object(Display, 'red')
    @mock.patch.object(Display, 'cyan', side_effect=lambda text: text)
    @mock.patch('jasper.suite.Suite')
    def test_prepare_passing_statistics(self, mock_suite, mock_cyan, mock_red):
        display = Display()

        mock_suite.passed = True
        mock_suite.num_features_passed = 5
        mock_suite.num_features_failed = 0
        mock_suite.num_scenarios_passed = 20
        mock_suite.num_scenarios_failed = 0

        display.prepare_statistics(mock_suite)

        display.red.assert_not_called()
        display.cyan.assert_called_once_with(
            "5 Features passed, 0 failed.\n"
            "20 Scenarios passed, 0 failed."
        )

        self.assertEqual(
            display.display_string,
            "5 Features passed, 0 failed.\n20 Scenarios passed, 0 failed.\n"
        )

    @mock.patch.object(Display, 'red', side_effect=lambda text: text)
    @mock.patch.object(Display, 'cyan')
    @mock.patch('jasper.suite.Suite')
    def test_prepare_failing_statistics(self, mock_suite, mock_cyan, mock_red):
        display = Display()

        mock_suite.passed = False
        mock_suite.num_features_passed = 4
        mock_suite.num_features_failed = 1
        mock_suite.num_scenarios_passed = 15
        mock_suite.num_scenarios_failed = 5

        display.prepare_statistics(mock_suite)

        display.cyan.assert_not_called()
        display.red.assert_called_once_with(
            "4 Features passed, 1 failed.\n"
            "15 Scenarios passed, 5 failed."
        )

        self.assertEqual(
            display.display_string,
            "4 Features passed, 1 failed.\n15 Scenarios passed, 5 failed.\n"
        )
