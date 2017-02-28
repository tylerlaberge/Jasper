# Jasper

An async friendly behavior-driven development framework.

![alt text](https://github.com/tylerlaberge/Jasper/blob/master/img/PassingExample.jpg)

## Motivation

Jasper is a behaviour-driven development(BDD) framework. BDD is a form of test-driven development where the tests descibe the behaviours of an application, typically behaviours are described in plain English sentences. BDD allows tests to be written in a highly composible, and easy to read way.

Jasper's main points that seperate it from other BDD frameworks suchs as lettuce, and behave are that:

* Test's are run *asynchronously*, making it very easy and intuitave to write tests for asynchonous code.

* Features are described within .py files, exactly how you would write normal python code. No need to learn the syntax of a domain-specific language (DSL) in order to define your features like other frameworks require.

* Small and simple built-in *optional* assertion library allows for easy to write and easy to read assertions.

* The structure of your features, scenarios, and steps is very unrestrictive. No requirements for any specific directory structures in order for Jasper to run you tests.

* Very easy to read testing reports of various verbosity levels. It is very clear which features, scenarios, and steps failed, along with a clear traceback of where a failure occured.

## Getting Started

### Breif Overview

Jasper tests are composed of 3 main parts. Features, Scenarios, and Steps. 

Features are exactly what they are described as, the features of your applications that you are testing. A calculator application might have an addition feature, subtraction feature, and so on.

Features are composed of scenarios, which are essentially the cases that you are testing on a particular feature. An addition feature might have scenario's for adding two positive numbers or two negative numbers. Likewise for a multiplication feature. Maybe for a division feature you might also have a scenario for the case of dividing by 0.

Lastly, Scenarios are composed of Steps, which are the parts that actually implement the behavioural tests. A Scenario is made up of given, when, and then steps. First the 'given' steps are ran, which supply us with something to test. Next the 'when' steps are ran, which actually run the thing we are testing. And finally the 'then' steps are ran, which make assertions against the results of what we ran in the when steps and either pass or fail based on those results.

This is the essence of BDD and writing behavioural tests in Jasper.

### Defining Steps

As was stated above, steps are the actual implementations of our behavioural tests. Writing steps is very easy, simply use the step decorator provided by Jasper. 

Following our calculator application example, lets implement some steps.

We'll start with a 'given' step, which will provide us with something to test. We are going to want to test an addition feature to begin, so we will need an addition function.  

```python
  from jasper import step
  
  @step
  def an_adding_function(context):
      context.function = lambda a, b: a + b
      
```

The main thing to note here is the mysterious 'context' parameter. Context is the way you can pass data between steps, it is a dictionary-like object so you can get and set attributes on it and it will be passed along to each of your steps in a scenario to use. Here we are setting a 'function' attribute on the context, so any steps in the same scenario which are ran after this step will have access to this 'function' attribute.

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

Here we are initializing an 'Expect' object with our actual data, the result of the function call in the previous step, and we are asserting that the actual data is greater than 0. It reads like english, "Expect 'the result' to be greater than 0". Further details on the 'Expect' object will be discussed later.

One thing you might have noticed is that all these steps use the same @step decorator. You might wonder what seperates a 'given' step from a 'when' step or a 'then' step? The only difference between these steps is the way in which you use them. When you supply a scenario with a 'given' step, it simply means that step will be ran before the 'when' step. It is up to the User to define steps that do what they are meant to do (provide something (given), run something (when), check something (then)), and to use those steps accordingly in your scenarios.

With that said, now that we have our steps defined lets create a Scenario.

### Creating a Scenario

Scenarios are essentailly the test cases of our features. They are composed of 'given', 'when', and 'then' steps which desribe the behaviours we expect.

With our three scenario's we defined above we can define a scenario using Jasper's Scenario object.

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

The first argument to the Scenario object is a description of the scenario. This will be displayed in the report after runner your tests.

The given, when, and then arguments refer to the steps we defined above. Notice that we are *calling* the functions. This is an important detail. The reason you call the functions is because the @step decorator actually wraps you function into a Step object that Jasper uses internally, and when you call a function decorated with @step, it returns a new instance of that Step object. You will see some nice functionality we get from this later on when we pass arguments into our steps, but for now just remember to call your step functions and don't worry about passing in a 'context' argument, Jasper will pass that in on its own.

So we have a scenario, lets finally create feature that contains this scenario.

### Creating a Feature

Features are the features of our application that we are testing. They are made up of scenarios which test the behaviours of a feature.

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

You can see its fairly self explanatory. The Feature object has a description, which we said is 'Addition' since its the addition feature, and it also a list of scenarios, and we just passed our scenario we defined above into this list. An important not is that your feature object must be stored in a variable, above we called it 'feature'. You cannot just call the Feature object and be done with it. This is because Jasper's test runner searches through your test files for references to Feature objects. If you don't store your features in a variable then it will be lost and Jasper won't know they are there. Jasper does it this way so that it can collect all you features up, put them into an internal Suite object, and then run all your tests asynchronously (more on async later).


One thing I'd like to do is rewrite this feature a little bit to make it a bit cleaner. Typically the way I like to write my features and scenarios is to just create my scenarios as I'm constructing a feature. So if we did that we could instead write this as follows.

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

