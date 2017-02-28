# Jasper

An async friendly behavior-driven development framework.

![alt text](https://github.com/tylerlaberge/Jasper/blob/master/img/PassingExample.jpg)

## Motivation

Jasper is a behaviour-driven development(BDD) framework. BDD is a form of test-driven development where the tests descibe the behaviours of an application, typically behaviours are described in plain English sentences. BDD allows tests to be written in a highly composible, and easy to read way.

Jasper's main points that seperate it from other BDD frameworks suchs as lettuce, and behave are that:

* Test's are run *asynchronously*, making it very easy and intuitave to write tests for asynchonous code.

* Features are described within .py files, exactly how you would write normal python code. No need to learn the syntax of a domain-specific language (DSL) in order to define your features like other frameworks require.

* The structure of your features, scenarios, and steps is very unrestrictive. No requirements for any specific directory structures in order for Jasper to run you tests.

* Very easy to read testing reports of various verbosity levels. It is very clear which features, scenarios, and steps failed, along with a clear traceback of where a failure occured.

