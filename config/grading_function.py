def grading_function(correct, incorrect, unanswered):
    return max((correct - 4) * 1.25, 0)