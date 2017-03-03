"""
The suite module.
"""

import asyncio
import tqdm


class Suite(object):
    """
    An internal class for running a collection of Feature of objects and collecting results.
    """
    def __init__(self):
        """
        Initialize a new Suite object.
        """
        self.features = []
        self.successes = []
        self.failures = []
        self.passed = True

    @property
    def num_features_passed(self):
        """
        The number of features that passed after running this suite.
        """
        return len(self.successes)

    @property
    def num_features_failed(self):
        """
        The number of features that failed after running this suite.
        """
        return len(self.failures)

    @property
    def num_scenarios_passed(self):
        """
        The number of scenarios that passed running this suite.
        """
        return sum([feature.num_scenarios_passed for feature in self.features])

    @property
    def num_scenarios_failed(self):
        """
        The number of scenarios that failed after running this suite.
        """
        return sum([feature.num_scenarios_failed for feature in self.features])

    def add_feature(self, feature):
        """
        Add a feature to this suite.

        :param feature: The Feature object to add to this suite.
        """
        self.features.append(feature)

    async def run(self):
        """
        Run all the features of this suite.
        """
        await self.__wait_with_progress([self.__run_feature(feature) for feature in self.features])

    async def __run_feature(self, feature):
        await feature.run()
        if feature.passed:
            self.successes.append(feature)
        else:
            self.failures.append(feature)
            self.passed = False

        return feature

    async def __wait_with_progress(self, coros):
        with tqdm.tqdm(
                total=sum([len(feature.scenarios) for feature in self.features]),
                desc=f'Running {len(self.features)} features and '
                     f'{sum([len(feature.scenarios) for feature in self.features])} scenarios',
                ncols=100, bar_format='{desc}{percentage:3.0f}%|{bar}| {elapsed}'
        ) as progress_bar:
            for future in asyncio.as_completed(coros):
                completed_feature = await future
                progress_bar.update(len(completed_feature.scenarios))
