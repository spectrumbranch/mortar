# test_jp.py is potentially long-running, so it is ignored by default.

# test_mort.py tests that mortar creates an OCR environment that matches MORT's
# and reproduces MORT's OCR result. This is currently not relevant to the goals
# of the mortar project. It may become relevant again later, so we'll keep the
# tests available to be run on demand.

collect_ignore = ["test_jp.py", "test_mort.py"]
