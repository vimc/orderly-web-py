class ReportStatusResult:
    def __init__(self, response_data):
        self.status = response_data["status"]
        self.version = response_data["version"]
        self.output = response_data["output"]
        self.success = self.status == "success"
        self.fail = "error" in self.status.lower()
        self.finished = self.success or self.fail
