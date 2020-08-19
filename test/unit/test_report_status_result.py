from orderlyweb_api.result_models import ReportStatusResult

test_result_success = ReportStatusResult({"status": "success",
                                          "version": "test-version",
                                          "output": {"stdout": ["test-out"]}})

test_result_running = ReportStatusResult({"status": "running",
                                          "version": None, "output": {}})

test_result_error = ReportStatusResult({"status": "RuntimeError",
                                        "version": None, "output": {}})


def test_status():
    assert test_result_success.status == "success"


def test_version():
    assert test_result_success.version == "test-version"


def test_output():
    assert test_result_success.output["stdout"] == ["test-out"]


def test_success():
    assert test_result_success.success
    assert not test_result_running.success
    assert not test_result_error.success


def test_fail():
    assert not test_result_success.fail
    assert not test_result_running.fail
    assert test_result_error.fail


def test_finished():
    assert test_result_success.finished
    assert not test_result_running.finished
    assert test_result_error.finished
