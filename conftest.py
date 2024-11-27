# Adds option for pytest to wait for debugger to attach before running tests


def pytest_addoption(parser):
    parser.addoption(
        "--wait-for-debugger",
        action="store_true",
        help="Wait for debugpy attach before running tests",
    )


def pytest_configure(config):
    if config.getoption("--wait-for-debugger"):
        import debugpy

        debugpy.listen(("0.0.0.0", 3001))
        debugpy.wait_for_client()
