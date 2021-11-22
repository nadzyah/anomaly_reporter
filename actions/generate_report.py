import os
from PDFReport import *
import datetime

from st2common.runners.base_action import Action

class GenerateReport(Action):

    def run(self, logdata, clientname, report_store_dir, event_handler_period):
        report = PDFReport()
        report.print_page(logdata, event_handler_period)

        CLIENT_DIR = report_store_dir + clientname
        if os.path.exists(report_store_dir) and os.access(report_store_dir, os.W_OK):
            if not os.path.exists(CLIENT_DIR):
                os.mkdir(CLIENT_DIR)
            now = datetime.datetime.now().strftime("%d.%m.%Y")

            filepath = CLIENT_DIR + "/" + now + ".pdf"
            report.output(filepath)

            return (True, filepath)

        return (False, "Cannot access the directory")
