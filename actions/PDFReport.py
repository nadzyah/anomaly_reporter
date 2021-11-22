#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from datetime import datetime
from datetime import timedelta
from fpdf import FPDF, HTMLMixin


from pymongo import MongoClient

class PDFReport(FPDF, HTMLMixin):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297

    def footer(self):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font('Arial', '', 10)
        self.set_text_color(128)
        self.cell(0, 10, str(self.page_no()), 0, 0, 'C')

    def page_body(self, logdata: dict, daysnum: int):
        # Determine how many plots there are per page and set positions
        # and margins accordingly

        # Create title
        header = f'Abnormal activity report for the last {daysnum} days'
        self.set_font('Arial', 'B', 20)
        w = self.get_string_width(header)
        self.set_x((self.WIDTH - w)/2)
        self.cell(w, 9, header, 0, 0, 'C')
        self.line(11, 20, self.WIDTH-11, 20)
        self.ln()

        for host, logs in logdata.items():
            self.ln()
            self.set_font('Arial', 'B', 14)
            self.cell(0, 10, f'Logs from {host}:')
            for log in logs:
                self.ln()
                self.set_font('Courier', '', 12)
                self.multi_cell(0, 5, log)


    def print_page(self, logdata, daterange):
        # Generates the report
        self.add_page()
        self.page_body(logdata, daterange)
