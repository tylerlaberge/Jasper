import asyncio
import tqdm


class Suite(object):

    def __init__(self):
        self.features = []
        self.successes = []
        self.failures = []
        self.passed = True

    @property
    def num_features_passed(self):
        return len(self.successes)

    @property
    def num_features_failed(self):
        return len(self.failures)

    @property
    def num_scenarios_passed(self):
        return sum([feature.num_scenarios_passed for feature in self.features])

    @property
    def num_scenarios_failed(self):
        return sum([feature.num_scenarios_failed for feature in self.features])

    def add_feature(self, feature):
        self.features.append(feature)

    async def run(self):
        await self.wait_with_progress([self.__run_feature(feature) for feature in self.features])

    async def __run_feature(self, feature):
        await feature.run()
        if feature.passed:
            self.successes.append(feature)
        else:
            self.failures.append(feature)
            self.passed = False

        return feature

    async def wait_with_progress(self, coros):
        with tqdm.tqdm(
                total=sum([len(feature.scenarios) for feature in self.features]),
                desc=f'Running {len(self.features)} features and '
                     f'{sum([len(feature.scenarios) for feature in self.features])} scenarios',
                ncols=100, bar_format='{desc}{percentage:3.0f}%|{bar}|'
        ) as progress_bar:
            for future in asyncio.as_completed(coros):
                completed_feature = await future
                progress_bar.update(len(completed_feature.scenarios))
