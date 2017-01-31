feature("some_feature")\
    .given(foo="foo")\
    .scenario("some_scenario")\
        .given(bar="bar")\
        .it("combines foo and bar into foobar")


###############3

@feature
def some_feature():

    @given
    def some_foo_data(my):
        my(foo="bar")

    @scenario
    def some_scenario(my):

        @given
        def some_bar_data(my):
            my(bar="bar")

        @it
        def combines_them_into_foobar(my):

            @given
            def some_extra_data(my):
                my(extra_data="extra_data")

            Expect(foobar(my("foo"), my("bar"), my("extra_data"))).to_be("foobar")

        @it
        def can_accept_an_string(my):
            expect(foobar(my("foo"), "")).toBe("foo")

    @scenario
    def some_other_scenario():

        @given
        def some_foobar_data(my):
            my(foobar="foobar")

        @it
        def does_stuff(my):
            expect(foo(my("foobar"))).toBe("something")
