# import userInterface
# import controllers

# def mockGetUserInputFactory(answers):
#     def mockGetUserInput(prompt="", default=""):
#         return next(answers)

#     return mockGetUserInput

# # def test_multiple_inputs(monkeypatch):
# #     answers = iter(["first", "second"])
# #     monkeypatch.setattr(userInterface, "getUserInput", mockGetUserInputFactory(answers))

# #     result = my_function_that_calls_input_twice()
# #     assert result == ("first", "second")

# def testViewAllTasksByCategory():
