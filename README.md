# Jasper

An asynchronous behavior-driven development framework.

-

Simply define some steps

```python
from jasper import step, Expect
import asyncio


@step
def an_async_function(context):
    context.function = asyncio.sleep
    
    
@step
async def we_call_the_function(context):  # Can easily test async calls and run your steps asynchronously
    try:
        await context.function(1)
    except Exception as e:
        context.exception = e
    else:
        context.exception = None
    
    
@step
def nothing_should_go_wrong(context):
    Expect(context.exception).to_be(None)
```

Create Features and Scenarios

```python
from jasper import Feature, Scenario
from example_steps import *


feature = Feature(
    'Example Feature',
    scenarios=[
        Scenario(
            'Example Scenario',
            given=an_async_function(),
            when=we_call_the_function(),
            then=nothing_should_go_wrong()
        )
    ]
)
```

And run your features and see the results

![alt text](https://github.com/tylerlaberge/Jasper/blob/master/img/ExampleFeature.jpg)



## Motivation

Behavior-Driven Development (BDD) is a form of test-driven development where the tests descibe the behaviours of an application, and typically these behaviours are described in plain English sentences. BDD allows tests to be written in a highly composible, understandable, and easy to read way.

Jasper's main points that seperate it from other BDD frameworks suchs as [lettuce](https://github.com/gabrielfalcao/lettuce), and [behave](https://github.com/behave/behave) are that:

* Test's are run *asynchronously*, making it very easy and intuitave to write tests for asynchonous code.

* Features are described within .py files, exactly how you would write normal python code. No need to learn the syntax of a domain-specific language in order to define your features like other frameworks require.

* Small and simple built-in *optional* assertion library allows for easy to write and easy to read assertions.

* The structure of your features, scenarios, and steps is very unrestrictive. No requirements for any specific directory structures in order for Jasper to run you tests.

## Contents

- [Installation](https://github.com/tylerlaberge/Jasper#installation)
- [Getting Started](https://github.com/tylerlaberge/Jasper#getting-started)
  - [Brief Overview](https://github.com/tylerlaberge/Jasper#breif-overview) 
  - [Defining Steps](https://github.com/tylerlaberge/Jasper#defining-steps)
  - [Creating a Scenario](https://github.com/tylerlaberge/Jasper#creating-a-scenario)
  - [Creating a Feature](https://github.com/tylerlaberge/Jasper#creating-a-feature)
    - [Organizing Features](https://github.com/tylerlaberge/Jasper#organizing-features)
  - [Running a Feature](https://github.com/tylerlaberge/Jasper#running-a-feature)
- [Steps](https://github.com/tylerlaberge/Jasper#steps)
  - [Creating a simple step](https://github.com/tylerlaberge/Jasper#creating-a-simple-step)
  - [Passing data between steps](https://github.com/tylerlaberge/Jasper#passing-data-between-steps)
  - [Passing arguments to your steps](https://github.com/tylerlaberge/Jasper#passing-arguments-to-your-steps)
  - [Defining asynchronous steps](https://github.com/tylerlaberge/Jasper#defining-asynchronous-steps)
- [Scenarios](https://github.com/tylerlaberge/Jasper#scenarios)
  - [Creating a simple Scenario](https://github.com/tylerlaberge/Jasper#creating-a-simple-scenario)
  - [Hooks](https://github.com/tylerlaberge/Jasper#hooks)
  - [Defining multiple steps for the same hooks](https://github.com/tylerlaberge/Jasper#defining-multiple-steps-for-the-same-hooks)
- [Features](https://github.com/tylerlaberge/Jasper#features)
  - [Creating a simple Feature](https://github.com/tylerlaberge/Jasper#creating-a-simple-feature)
  - [Hooks](https://github.com/tylerlaberge/Jasper#hooks-1)
  - [Multiple Scenarios](https://github.com/tylerlaberge/Jasper#multiple-scenarios)
- [The Expect Object](https://github.com/tylerlaberge/Jasper#the-expect-object)
  - [Identity Comparison](https://github.com/tylerlaberge/Jasper#identity-comparison)
  - [Equality Comparison](https://github.com/tylerlaberge/Jasper#equality-comparison)
  - [Less than Comparison](https://github.com/tylerlaberge/Jasper#less-than-comparison)
  - [Greater than Comparison](https://github.com/tylerlaberge/Jasper#greater-than-comparison)
  - [Negation Operator](https://github.com/tylerlaberge/Jasper#negation-operator)
- [The Display](https://github.com/tylerlaberge/Jasper#the-display)
  - [Example Display](https://github.com/tylerlaberge/Jasper#example-display)
- [The Test Runner](https://github.com/tylerlaberge/Jasper#the-test-runner)
  - [jasper command-line tool](https://github.com/tylerlaberge/Jasper#jasper-command-line-tool)
  - [How your features are ran asynchronously](https://github.com/tylerlaberge/Jasper#how-your-features-a-ran-asynchronously)
- [Async Demonstration](https://github.com/tylerlaberge/Jasper#async-demonstration)
- [API Documentation](https://github.com/tylerlaberge/Jasper#api-documentation)
- [Contributing](https://github.com/tylerlaberge/Jasper#contributing)
  
## Installation

    pip install jasper
    
Supports Python 3.6+

## Getting Started

### Breif Overview

Jasper tests are composed of 3 main parts. Features, Scenarios, and Steps. 

Features are exactly what they sound like, the features of your applications that you are testing. A calculator application might have an addition feature, subtraction feature, and so on.

Features are composed of scenarios, which are essentially the cases that you are testing on a particular feature. An addition feature might have scenario's for adding two positive numbers or two negative numbers. Likewise for a multiplication feature. Maybe for a division feature you might also have a scenario for the case of dividing by 0.

Lastly, Scenarios are composed of Steps, which are the parts that actually implement the behavioural tests. A Scenario is made up of given, when, and then steps. First the 'given' steps are ran, which supply us with something to test. Next the 'when' steps are ran, which actually run the thing we are testing. And finally the 'then' steps are ran, which make assertions against the results of what we ran in the when steps and either pass or fail based on those results.

This is the essence of BDD and writing behavioural tests in Jasper.

### Defining Steps

As was stated above, steps are the actual implementation of our behavioural tests. Writing steps is very easy, simply use the step decorator provided by Jasper. 

Following our calculator application example, lets implement some steps.

We'll start with a 'given' step, which will provide us with something to test. We are going to want to test an addition feature to begin, so we will need an addition function.  

```python
#calculator.py

def add(a, b):
    return a + b
```

```python
  from jasper import step
  from calculator import add
  
  @step
  def an_adding_function(context):
      context.function = add
```

The main thing to note here is the mysterious 'context' parameter. Context is the way you can pass data between steps. It is a dictionary-like object so you can get and set attributes on it and it will be passed along to each of your steps in a scenario to use. Here we are setting our calculators add function to a 'function' attribute on the context. Any steps in the same scenario which are ran after this step will have access to this 'function' attribute.

Let's now write a 'when' step, where we will actually run something against the given function. We are going to want to test that adding two positive numbers results in a positive number, so lets write a step for calling our function with two positive numbers.

```python
  from jasper import step
  
  @step
  def we_call_it_with_two_positive_numbers(context):
      context.result = context.function(50, 7)
```

Again notice the use of 'context'. I am calling the 'function' attribute that will be set from the first step we defined above, and then I am setting the result of the function call to a new attribute I called 'result'. These attributes can be called anything you want. The only reason I use 'function' and 'result' as attribute names is simply because they adequately describe the values of those attribues and they are general enough to allow composibility down the road.

Let's finally write a 'then' step, where we will actually assert that the result of the 'when' step is correct. Again, we want to test that adding two positive numbers will result in a positive number so that is what we will assert. We will use Jasper's built-in assertion library 'Expect' to do these assertions, however you are free to use plain old assert statements if you'd prefer.

```python
  from jasper import step, Expect
  
  @step
  def the_result_should_be_positive(context):
      Expect(context.result).to_be.greater_than(0)
```

Here we are initializing an 'Expect' object with our actual data, the result of the function call in the previous step, and we are asserting that the actual data is greater than 0. It reads like english, "Expect 'the result' to be greater than 0". You can read more about the Expect object [here](https://github.com/tylerlaberge/Jasper#the-expect-object).

One thing you might have noticed is that all these steps use the same @step decorator. You might wonder, what seperates a 'given' step from a 'when' step or a 'then' step? The only difference between these steps is the way in which you use them. When you supply a scenario with a 'given' step, it simply means that step will be ran before the 'when' step. It is up to the User to define steps that do what they are meant to do (provide something (given), run something (when), check something (then)), and to use those steps accordingly in your scenarios.

With that said, now that we have our steps defined lets create a Scenario. 

More information on steps can be found in the [Steps](https://github.com/tylerlaberge/Jasper#steps) section.

### Creating a Scenario

Scenarios are essentially the different parts of our features that we are testing. They are composed of 'given', 'when', and 'then' steps which desribe the behaviours we expect.

With the steps we defined above we can create a scenario using Jasper's Scenario object.

```python
  from jasper import Scenario
  
  adding_two_positive_numbers_scenario = Scenario(
      'Adding two positive numbers',
      given=an_adding_function(),
      when=we_call_it_with_two_positive_numbers(),
      then=the_result_should_be_positive()
  )
```

Assuming our steps were defined in the same file, we can define a scenario as easy as that. 

The first argument to the Scenario object is a description of the scenario. This will be displayed in the report after running your tests.

The given, when, and then arguments refer to the steps we defined above. Notice that we are ***calling*** the functions. This is an important detail. The reason you call the functions is because the @step decorator actually wraps your function into a Step object that Jasper uses internally, and when you call a function decorated with @step, it returns a new instance of that Step object. You will see some nice functionality we get from this later on when we pass arguments into our steps, but for now just remember to call your step functions and don't worry about passing in a 'context' argument, Jasper will pass that in on its own.

So we have a scenario, lets finally create a feature that contains this scenario.

More information on Scenarios can be found in the [Scenarios](https://github.com/tylerlaberge/Jasper#scenarios) section.

### Creating a Feature

Features are the high level peices of our application that we are testing. They are made up of scenarios which test the behaviours of a feature.

With our scenario we defined above, we can create a feature for our applications addition functionality like so.

```python
from jasper import Feature

feature = Feature(
  'Addition',
  scenarios=[
      adding_two_positive_numbers_scenario
  ]
)
```

You can see its fairly self explanatory. The Feature object has a description, which we said is 'Addition' since its the addition feature, and it also has a list of scenarios and we just passed our scenario we defined above into this list. An important thing to note is that your feature object must be stored in a variable, above we called it 'feature'. You cannot just call the Feature object and be done with it. This is because Jasper's test runner searches through your test files for references to Feature objects. If you don't store your features in a variable then it will be lost and Jasper won't know they are there. Jasper does it this way so that it can collect all you features up, put them into an internal Suite object, and then run all your tests asynchronously.

#### Organizing Features

One thing I'd like to do is rewrite this feature a little bit to make it a bit cleaner. Typically the way I like to write my features and scenarios is to just create my scenarios as I'm constructing a feature.

```python
from jasper import Feature, Scenario

feature = Feature(
    'Addition',
    scenarios=[
        Scenario(
            'Adding two positive numbers',
            given=an_adding_function(),
            when=we_call_it_with_two_positive_numbers(),
            then=the_result_should_be_positive()
        )
    ]
)
```

Writing it this way is how I like to do it, however you are free to organize you steps, features, and scenarios however you like. You may wish to put all your scenarios into their own module, or all the steps into their own module, or seperate steps into given, when, and then modules. Here's an example of how I typically organize my features.

```
| - my_app   # Your application code

|     |- ...

| - features  # your Jasper features

|     |- addition  # The addition feature directory

|        |- steps  # The steps involved with the addition feature

|            |- given.py  # The given steps

|            |- when.py   # The when steps

|            |- then.py   # The then steps

|        |- feature.py  # The actual feature that was defined above
```


However you organize your files just make sure that your feature.py file can successfully import steps or scenarios from wherever you choose to define them, and that your steps can import code from your actual application (we want to test an actual app after all!).

Okay, we have succesfully written a feature. Lets run it.

More information on Features can be found in the [Features](https://github.com/tylerlaberge/Jasper#features) section.

### Running a Feature

Using the directory structure I showed above, my final feature.py, which I called 'addition_feature.py', looks like this.

```python
from jasper import Feature, Scenario
from features.addition.steps.given import an_adding_function
from features.addition.steps.when import we_call_it_with_two_positive_numbers
from features.addition.steps.then import the_result_should_be_positive

feature = Feature(
    'Addition',
    scenarios=[
        Scenario(
            'Adding two positive numbers',
            given=an_adding_function(),
            when=we_call_it_with_two_positive_numbers(),
            then=the_result_should_be_positive()
        )
    ]
)
```

You may think all these imports are a bit overkill, but as you create more and more scenarios the number of steps you define increases quickly and its quite handy to seperate the steps into their own modules.

**IMPORTANT:** The single contraint on how your features are defined is that your files which contain your features, like the one above, must be given a filename *which ends with feature.py*, so addition_feature.py is fine, feature_addition.py or foobar.py are not. They need to end with feature.py because these are the files Jasper's runner searches for.

Okay, with our feature defined lets run it. Open up a terminal and navigate to the directory containing your feature files. Using the directory structure above this directory is called 'features'.

The jasper command has the following signature

    jasper [OPTIONS] TEST_DIRECTORY

Don't worry about options for now.

So to use that command to run the tests in the 'features' directory, simply type

    $ jasper features
    
You should see the following output

![alt text](https://github.com/tylerlaberge/Jasper/blob/master/img/PassingRunV0.jpg)

That's pretty good, but maybe we want to see more detail. We can up the verbosity level using the '-v' option.

    $ jasper -v1 features
    
![alt text](https://github.com/tylerlaberge/Jasper/blob/master/img/PassingRunV1.jpg)

And even more detail.

    $ jasper -v2 features
    
![alt_text](https://github.com/tylerlaberge/Jasper/blob/master/img/PassingRunV2.jpg)

Verbosity level can range from 0 to 2. 

More information on the jasper command-line tool can be found [here](https://github.com/tylerlaberge/Jasper#jasper-command-line-tool)

If any errors occur the display will show the full detail of the feature that failed regardless of verbosity level. For example lets say I change the 'then' step so that it throws an exception.

```python
#feature.addition.steps.then
  
from jasper import step, Expect
  
@step
def the_result_should_be_positive(context):
    Expect(context.result).to_be.less_than(0) # So we can see an example exception we use 'less_than', this should fail.
```

Lets save everything and run again.

    jasper features
    
![alt text](https://github.com/tylerlaberge/Jasper/blob/master/img/FailingRun.jpg)

As you can see an exception occured. Jasper highlights in red the failing features, scenarios, and steps. All exceptions are display in yellow.

The 'FAILURE: Expected 55 to be less than 0' description is the message of the exception that occured. It is easy to read because it comes from Jasper's 'Expect' assertion library which will throw a clean exception when an assertion fails. You can see the exact line the exception occured is at the point in the 'then' step when we say 'Expect(context.result).to_be.less_than(0).

More information about the display can be found [here](https://github.com/tylerlaberge/Jasper#the-display)

**Note: If you are not seeing colored output try using the '--ansi' flag in your jasper command.**

    jasper --ansi features
    
The ansi flag forces Jasper to use ansi escape sequences during coloring. By default if you are on Window's Jasper does not use ansi escape sequences. Some terminals however support ansi even if you are on windows, such as git bash, and in those cases you would want to use the --ansi flag even if you are on windows so that you get colored output. Linux and mac will use ansi sequences no matter what.

At this point you should understand the basics of Jasper. You can define as many features as you want in as many files as you want so long as their filenames end in feature.py and you should be good to go.

More detail on Features, Scenarios, and Steps as well as on additional topics like asynchronous testing are explained in additional sections of this README.

## Steps

Steps are one of the most important part of our behavioural tests. They define the actual implementation of our tests and are used by scenarios and feaures to define expected behaviours.

### Creating a simple step

To create a step use jaspers @step decorator.

```python
from jasper import step

@step
def some_example_step(context):
    pass
```

### Passing data between steps

A context object is passed into each of your steps automatically by Jasper. It is a way of communicating and passing data between your steps. It supports simple getting and setting attribute operations using the '.' notation.

```python
from jasper import step

@step
def first_step(context):
    context.foobar = 'foobar'  # Set an attribute
    

@step
def later_step(context):
    assert context.foober == 'foobar'  # Get an attribute
```

Every feature gets its own context, and every scenario gets its own copy of the features context. This simple diagram shows how each scenario has its own context, which is a copy of its features context.

![alt text](https://github.com/tylerlaberge/Jasper/blob/master/img/ContextDiagram.jpg)

The order in which steps are called, and thus the order in which the context is passed around, is described further in the [Test Runner](https://github.com/tylerlaberge/Jasper#how-your-features-a-ran-asynchronously) section. 

### Passing arguments to your steps

To pass arguments to your steps, simply add additional arguments after the 'context' argument in your step function.

```python
from jasper import step

@step
def two_numbers(context, a, b):
    context.a = a
    context.b = b
```
And pass in the the parameters as ***keyword*** arguments. You cannot use positional arguments.

```python
from jasper import Feature, Scenario
from features.example.steps.given import two_numbers

feature = Feature(
    'Steps Example',
    scenarios=[
        Scenario(
            'Keyword arguments',
            given=two_numbers(a=5, b=17),  # here we call the step with the keyword arguments.
            when=..., 
            then=...
        )
    ]
)
```
You can use default values like normal if you wish.

```python
from jasper import step

@step
def two_numbers(context, a=5, b=10):
    context.a = a
    context.b = b
```

### Defining asynchronous steps

Jasper makes testing asynchronous code a breeze. Simply define your step as an async function like normal and you are good to go.

```python
from jasper import step
import asyncio


@step
async def we_call_an_async_function(context):
    await asyncio.sleep(1)  # this is just an example async function, you dont need to use asyncio.
```

And then use the step like normal.

```python
from jasper import Feature, Scenario
from features.example.steps.when import we_call_an_async_function

feature = Feature(
    'Steps Example',
    scenarios=[
        Scenario(
            'Keyword arguments',
            given=...,
            when=we_call_an_async_function(), 
            then=...
        )
    ]
)
```

The step you defined will safely run asynchronously alongside other steps located within other scenarios. This also makes testing async functions very easy.

More information on the way Jasper runs your tests asynchronously can be found [here](https://github.com/tylerlaberge/Jasper#how-your-features-a-ran-asynchronously).

## Scenarios

Scenarios are the aspects of our features that we are testing. They are made up of steps which are passed into the various hooks of a Scenario.

### Creating a simple Scenario

To create a Scenario use jaspers Scenario object.

```python
from jasper import Scenario
from example_steps import *

scenario = Scenario(
    'Example Scenario',
    given=some_example_function(),
    when=we_run_it(),
    then=something_should_happen()
)
```

### Hooks

Hooks are used to define the order in which your steps are run.

Any step you define using the step decorator can be used in any of the following hooks.

####*given:* steps that should supply a scenario with something to test with.
####*when:* steps that should run whatever it is we are testing, ran after the 'given' step.
####*then:* steps that should make assertions upon the results of the 'when' step.

####*before_all:* steps that run exactly once before every other step in the scenario.
####*before_each:* steps that run before each of the 'given', 'when', and 'then' steps.
####*after_each:* steps that run after each of the 'given', 'when', and 'then' steps.
####*after_all:* steps that run exactly once after every other step in the scenario.

In actual code you can access these hooks with keyword arguments.

```python
from jasper import Scenario
from example_steps import *

scenario = Scenario(
    'All hooks',
    before_all=do_something_before_all_other_steps(),
    before_each=do_something_before_each_step(),
    after_each=do_something_after_each_step(),
    after_all=do_something_after_all_other_steps(),
    given=something_to_test(),
    when=we_test_it(), 
    then=something_should_happen()
)
```

The only required steps that all scenarios must define are the 'given', 'when', and 'then' steps.

The other steps are generally for setting up and tearing down the environment to test in, and are not required.

### Defining multiple steps for the same hooks

If you want to pass multiple steps into a single hook for a scenario, such as multiple given or then steps, just pass in a list of steps.

```python
from jasper import Feature, Scenario
from example_steps import *

scenario = Scenario(
    'Multiple steps',
    given=[something_to_test(), something_else_to_test()],
    when=we_test_it(), 
    then=[something_should_happen(), something_else_should_happen()]
)
```

You can pass in a list of steps into any of the hooks. 

When you run a feature with multiple steps for a single hook the additional steps will be prepended by an 'And' within the report.

![alt text](https://github.com/tylerlaberge/Jasper/blob/master/img/MultipleStepsScenario.jpg)


## Features

Features describe the high level parts of an application that we are testing. They are made up of scenarios which test different parts of the same feature.

### Creating a simple Feature

To create a Feature use jasper's Feature object.

```python
from jasper import Feature, Scenario
from example_steps import *

feature = Feature(
    'Example Feature'
    scenarios = [
        Scenario(
            'Example Scenario',
            given=something_to_test(),
            when=we_test_it(), 
            then=something_should_happen()
        )
    ]
)
```

### Hooks

Just like scenarios, features have various hooks that you can pass steps into.

####*before_all:* steps that run exactly once before every other step in the feature.
####*before_each:* steps that run before each scenario in the feature.
####*after_each:* steps that run after each scenario in the feature.
####*after_all:* steps that run exactly once after every other step in the feature.

Again just like with scenarios, to access these hooks just use keyword arguments.

```python
from jasper import Feature, Scenario
from example_steps import *

feature = Feature(
    'Example',
    before_all=do_something_before_all_other_steps(),
    before_each=do_something_before_each_scenario(),
    after_each=do_something_after_each_scenario(),
    after_all=do_something_after_all_other_steps(),
    scenarios=[
        ...
    ]
)
```

### Multiple scenarios

Most features will have more than one scenario which tests it's behaviour. Simply pass your scenarios in as a list to define them.

```python
from jasper import Feature, Scenario
from example_steps import *

feature = Feature(
    'Example',
    scenarios=[
        Scenario(
            'scenario one',
            given=...,
            when=...,
            then=...
        ),
        Scenario(
            'scenario two',
            given=...,
            when=...,
            then=...
        )
    ]
)
```

## The Expect Object

The expect object comes built-in with Jasper. It allows for easy to read and understand assertions.

### Identity Comparison

```python
from jasper import Expect

some_dict = {'foo':'bar'}

Expect(some_dict).to_be(some_dict) # some_dict 'is' some_dict
```

### Equality Comparison

```python
from jasper import Expect

Expect({'foo':'bar'}).to_equal({'foo':'bar'}) # {'foo':'bar'} == {'foo':'bar'}
```

### Less than Comparison

```python
from jasper import Expect

Expect(5).to_be.less_than(10) # 5 < 10
```

### Greater than Comparison

```python
from jasper import Expect

Expect(10).to_be.greater_than(5) # 10 > 5
```

### Negation Operator

```python
from jasper import Expect

Expect(True).not_.to_be(False) # not (True == False)
```

## The Display

While your tests are running a progress bar and elapsed time will show the progress of the tests. Once Jasper finishes your tests a color coded report will display the results.

The different colors that are used in the display are:

**blue:** The feature/scenario/step was ran and it passed.

**red:** The feature/scenario/step was ran and it did not pass.

**grey:** The step was skipped. (because a previous step failed)

**yellow:** An exception that occured and its traceback.

### Example Display

![alt text](https://github.com/tylerlaberge/Jasper/blob/master/img/DisplayExample.jpg)

## The Test Runner

Required setup for running tests:

* Your files which define your features must have filenames which end with 'feature.py'. i.e 'some_feature.py'
* Your feature files must contain a reference to a jasper 'Feature' object. i.e 

```python
    feature = Feature(
        '...', 
        scenarios=[
            ...
        ]
    )
```

### jasper command line tool
 
The jasper command line tool is what you will use to run your tests. The signature of the tool is as follows.

    Usage: jasper [OPTIONS] TEST_DIRECTORY

    Options:
      --ansi            Flag to force display to use ansi escape sequences for
                        coloring.
      -v INTEGER RANGE  Verbosity level from 0 to 2. default is 0.
      --help            Show this message and exit.

Where TEST_DIRECTORY is the direcotry containing the feature.py files you wish to run.

The --ansi flag is for coloring purposes if you are on a windows machine using a terminal that actually supports ansi escape sequences.

Level 0 verbosity only shows you the statistics of running your features.

Level 1 verbosity also shows the descriptions of each feature as well as the descriptions of each scenario.

Level 2 verbosity also shows the names of each of your steps. (These are derived from the function names of your steps)

#### Example Usage 

With a directory called 'features' containing your feature.py files, if you wish to run the features with verbosity level 2 type the following command in the same directory that the 'features' directory is located in.

    $ jasper -v2 features
    
And you should see the output of your tests running.

### How your Features a ran asynchronously.
 
 In Jasper everything is run asynchronously. With that said there are certain caveats to that to ensure saftey, for example we would never want our 'then' steps running before our 'given' steps in some scenario. Here is a (somewhat crude) diagram of how your tests are run. 
 
 ![alt text](https://github.com/tylerlaberge/Jasper/blob/master/img/RunOrderDiagram.jpg)
 
 The arrows show the order that steps/scenarios are run in, they do not represent a caller -> callee relationship. 
 
 The blue bars represent something that is being run asynchronously. If multiple blocks are covered by the same blue bar, then they can be run next to each using async, meaning either can finish before the other, etc. 
 
 The green bars are essentially just groups of asynchronous functions. Blocks covered by the same green bar will run in order, but also asynchronously. So before each steps run asynchronously, but they will awlays run before a scenario. Not after, and not during.

Basically, 

All features run asynchronouusly next to each other.

All scenarios run asynchronously next to each other.

All steps are run in order, but are still awaitable if you defined an async step. This way other scenarios can run while a step of another scenario is awaiting.

Steps are guarenteed to always run in this order within a feature.

1. BeforeAll
2. BeforeEach (ran for each scenario)
3. Scenario(s)
4. AfterEach (ran for each scenario)
5. AfterAll

And Steps are guarenteed to always run in this order with a scenario.

1. BeforeAll
2. BeforeEach
3. Given
4. AfterEach
5. BeforeEach
6. When
7. AfterEach
8. BeforeEach
9. Then
10. AfterEach
11. AfterAll

To take full advantage of the way Jasper runs your tests, you should try to write any slow steps as async functions. This way Jasper can await your slow step and run another scenario or feature which can work more on their steps in the meantime.

### Async demonstration

To show how much of an effect asynchronous steps can have on your tests, lets do a comparison.

First we'll write normal, non-asynchronous steps.

```python
from jasper import step
import time


@step
def a_slow_function(context):
    context.function = lambda: time.sleep(2)


@step
def we_call_it(context):
    context.function()


@step
def we_do_nothing(context):
    pass
```

and our features

```python
from jasper import Feature, Scenario
from example_steps import *

slow_feature_one = Feature(
    'Slow Feature One',
    scenarios=[
        Scenario(
            'Slow scenario',
            given=a_slow_function(),
            when=we_call_it(),
            then=we_do_nothing()
        ),
        Scenario(
            'Slow scenario two',
            given=a_slow_function(),
            when=we_call_it(),
            then=we_do_nothing()
        )
    ]
)

slow_feature_two = Feature(
    'Slow Feature Two',
    scenarios=[
        Scenario(
            'Slow scenario',
            given=a_slow_function(),
            when=we_call_it(),
            then=we_do_nothing()
        ),
        Scenario(
            'Slow scenario two',
            given=a_slow_function(),
            when=we_call_it(),
            then=we_do_nothing()
        )
    ]
)
```

Basically, we have 2 features, each of which has 2 scenarios, each of which calls one slow function which takes 2 seconds to complete.

We can expect this to take 8 seconds. 2 seconds per scenario, 4 scenarios.

    $ jasper features
    
![alt text](https://github.com/tylerlaberge/Jasper/blob/master/img/NonAsyncDemo.jpg)

As expected, it toook 8 seconds. Now lets change our steps to take advantage of async.

```python
from jasper import step
import asyncio


@step
def a_slow_function(context):
    context.function = lambda: asyncio.sleep(2)


@step
async def we_call_it(context):
    await context.function()


@step
def we_do_nothing(context):
    pass
```

The only changes are that the slow function now uses asyncio's sleep function, and that we await it when we call it. No changes to our feature or scenarios are needed.

Now that we are using async, we can expect all of our scenarios to run along side each other. Each scenario takes 2 seconds to complete, if they run at the same time we can expect the tests to take 2 seconds total.

    $ jasper features
    
![alt text](https://github.com/tylerlaberge/Jasper/blob/master/img/AsyncDemo.jpg)

And as suspected, it took 2 seconds. Async is awesome!

## API Documentation

API documentation can be found [here](https://tylerlaberge.github.io/Jasper/api/build/html/index.html)

## Contributing

All pull requests are welcome.

Feel free to open an issue if you found a bug or have thoughts on any missing features you think should be added.

