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

