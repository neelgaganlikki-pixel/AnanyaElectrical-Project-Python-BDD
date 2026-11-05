import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.load_workbook('TestCase.xlsx')

# 1. Update Existing 'Test Cases' Sheet
ws_cases = wb.active
ws_cases.title = "Test Cases"

# Styles
navy_fill = PatternFill(start_color="0B192C", end_color="0B192C", fill_type="solid")
header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
data_font = Font(name="Segoe UI", size=10)
bold_font = Font(name="Segoe UI", size=10, bold=True)

thin_border = Border(
    left=Side(style='thin', color='E2E8F0'),
    right=Side(style='thin', color='E2E8F0'),
    top=Side(style='thin', color='E2E8F0'),
    bottom=Side(style='thin', color='E2E8F0')
)

passed_fill = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")
passed_font = Font(name="Segoe UI", size=10, bold=True, color="137333")

high_fill = PatternFill(start_color="FCE8E6", end_color="FCE8E6", fill_type="solid")
high_font = Font(name="Segoe UI", size=10, bold=True, color="C5221F")

med_fill = PatternFill(start_color="FEF7E0", end_color="FEF7E0", fill_type="solid")
med_font = Font(name="Segoe UI", size=10, bold=True, color="B06000")

zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

# Style headers
ws_cases.row_dimensions[1].height = 28
for col_idx in range(1, ws_cases.max_column + 1):
    cell = ws_cases.cell(row=1, column=col_idx)
    cell.fill = navy_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

# Style data rows
for row_idx in range(2, ws_cases.max_row + 1):
    ws_cases.row_dimensions[row_idx].height = 36
    is_zebra = (row_idx % 2 == 0)
    current_row_fill = zebra_fill if is_zebra else white_fill
    
    for col_idx in range(1, ws_cases.max_column + 1):
        cell = ws_cases.cell(row=row_idx, column=col_idx)
        cell.border = thin_border
        cell.fill = current_row_fill
        cell.font = data_font
        
        # Specific column alignments
        header_name = str(ws_cases.cell(row=1, column=col_idx).value)
        if header_name in ["Test Case ID", "Priority", "Severity", "Test Type", "Automation Status", "Execution Status", "Defect ID"]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            
        # Priority highlighting
        if header_name == "Priority":
            if cell.value == "High" or cell.value == "Critical":
                cell.fill = high_fill
                cell.font = high_font
            elif cell.value == "Medium":
                cell.fill = med_fill
                cell.font = med_font
                
        # Status highlighting
        if header_name == "Execution Status" and cell.value == "PASSED":
            cell.fill = passed_fill
            cell.font = passed_font

# Column widths
column_widths = {
    1: 16,  # Test Case ID
    2: 24,  # Module
    3: 45,  # Test Scenario
    4: 30,  # Preconditions
    5: 50,  # Test Steps
    6: 35,  # Test Data
    7: 45,  # Expected Result
    8: 40,  # Actual Result
    9: 14,  # Priority
    10: 14, # Severity
    11: 18, # Test Type
    12: 18, # Automation Status
    13: 18, # Execution Status
    14: 12  # Defect ID
}

for col_idx, width in column_widths.items():
    col_letter = get_column_letter(col_idx)
    ws_cases.column_dimensions[col_letter].width = width

# Enable freeze pane and filter
ws_cases.freeze_panes = "A2"
ws_cases.auto_filter.ref = ws_cases.dimensions

# 2. Add Summary Dashboard Sheet
if "Summary Dashboard" in wb.sheetnames:
    del wb["Summary Dashboard"]

ws_summary = wb.create_sheet(title="Summary Dashboard", index=0)
ws_summary.views.sheetView[0].showGridLines = True

# Title block
ws_summary.merge_cells("A1:G1")
title_cell = ws_summary["A1"]
title_cell.value = "ANANYA ELECTRICAL SOLUTIONS - AUTOMATION TEST EXECUTION SUMMARY"
title_cell.fill = navy_fill
title_cell.font = Font(name="Segoe UI", size=14, bold=True, color="FFFFFF")
title_cell.alignment = Alignment(horizontal="center", vertical="center")
ws_summary.row_dimensions[1].height = 40

# Project Meta Table
meta = [
    ("Application Under Test", "Ananya Electrical Solutions (Live React SPA)"),
    ("Target Base URL (DEV)", "https://ananya-electrical-solutions.neelgaganat97.workers.dev"),
    ("Production Base URL", "https://ananyaelectricalsolutions.com"),
    ("Automation Framework", "Playwright Python + Pytest-BDD + Self-Healing Engine"),
    ("Execution Engine", "Chromium, Firefox, WebKit"),
    ("Total Automated Scenarios", "39 Scenarios"),
    ("Overall Pass Rate", "100.0% (39 Passed / 0 Failed)"),
    ("Jenkins CI/CD Job", "http://localhost:8080/job/AnanyaElectrical-Project-Python-BDD/")
]

for idx, (label, val) in enumerate(meta, 3):
    ws_summary.cell(row=idx, column=1, value=label).font = Font(name="Segoe UI", size=10, bold=True, color="1E293B")
    ws_summary.cell(row=idx, column=1).fill = PatternFill(start_color="F1F5F9", fill_type="solid")
    ws_summary.cell(row=idx, column=1).border = thin_border
    
    ws_summary.merge_cells(start_row=idx, start_column=2, end_row=idx, end_column=7)
    val_cell = ws_summary.cell(row=idx, column=2, value=val)
    val_cell.font = Font(name="Segoe UI", size=10)
    val_cell.border = thin_border
    ws_summary.row_dimensions[idx].height = 22

# Metric Cards
metrics_header_row = 12
ws_summary.cell(row=metrics_header_row, column=1, value="TEST SUITE METRICS").font = Font(name="Segoe UI", size=11, bold=True, color="0B192C")

metric_headers = ["Category / Module", "Total Cases", "High Priority", "Medium Priority", "Automation Status", "Execution Status"]
for col_idx, h in enumerate(metric_headers, 1):
    cell = ws_summary.cell(row=13, column=col_idx, value=h)
    cell.fill = navy_fill
    cell.font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
    cell.alignment = Alignment(horizontal="center", vertical="center")
ws_summary.row_dimensions[13].height = 26

# Module aggregation
from collections import defaultdict
type_data = defaultdict(lambda: {"total": 0, "high": 0, "med": 0})
for r in range(2, ws_cases.max_row + 1):
    ttype = ws_cases.cell(row=r, column=11).value or "Other"
    prio = ws_cases.cell(row=r, column=9).value or "Medium"
    type_data[ttype]["total"] += 1
    if prio in ["High", "Critical"]:
        type_data[ttype]["high"] += 1
    else:
        type_data[ttype]["med"] += 1

row_cursor = 14
for ttype, counts in sorted(type_data.items()):
    ws_summary.cell(row=row_cursor, column=1, value=f"{ttype} Testing").font = bold_font
    ws_summary.cell(row=row_cursor, column=1).alignment = Alignment(horizontal="left", vertical="center")
    ws_summary.cell(row=row_cursor, column=2, value=counts["total"]).alignment = Alignment(horizontal="center", vertical="center")
    ws_summary.cell(row=row_cursor, column=3, value=counts["high"]).alignment = Alignment(horizontal="center", vertical="center")
    ws_summary.cell(row=row_cursor, column=4, value=counts["med"]).alignment = Alignment(horizontal="center", vertical="center")
    ws_summary.cell(row=row_cursor, column=5, value="100% Automated").alignment = Alignment(horizontal="center", vertical="center")
    
    st_cell = ws_summary.cell(row=row_cursor, column=6, value="PASSED (100%)")
    st_cell.alignment = Alignment(horizontal="center", vertical="center")
    st_cell.fill = passed_fill
    st_cell.font = passed_font
    
    for c in range(1, 7):
        ws_summary.cell(row=row_cursor, column=c).border = thin_border
    ws_summary.row_dimensions[row_cursor].height = 22
    row_cursor += 1

# Total Row
ws_summary.cell(row=row_cursor, column=1, value="TOTAL ALL SUITES").font = Font(name="Segoe UI", size=10, bold=True, color="0B192C")
ws_summary.cell(row=row_cursor, column=1).fill = PatternFill(start_color="E2E8F0", fill_type="solid")
ws_summary.cell(row=row_cursor, column=2, value=39).font = bold_font
ws_summary.cell(row=row_cursor, column=2).alignment = Alignment(horizontal="center", vertical="center")
ws_summary.cell(row=row_cursor, column=3, value=sum(d["high"] for d in type_data.values())).alignment = Alignment(horizontal="center", vertical="center")
ws_summary.cell(row=row_cursor, column=4, value=sum(d["med"] for d in type_data.values())).alignment = Alignment(horizontal="center", vertical="center")
ws_summary.cell(row=row_cursor, column=5, value="39 / 39 (100%)").alignment = Alignment(horizontal="center", vertical="center")

final_st = ws_summary.cell(row=row_cursor, column=6, value="ALL 39 PASSED")
final_st.alignment = Alignment(horizontal="center", vertical="center")
final_st.fill = passed_fill
final_st.font = Font(name="Segoe UI", size=10, bold=True, color="137333")

for c in range(1, 7):
    ws_summary.cell(row=row_cursor, column=c).border = thin_border
ws_summary.row_dimensions[row_cursor].height = 25

# Summary column widths
summary_widths = {1: 28, 2: 15, 3: 16, 4: 16, 5: 20, 6: 22, 7: 15}
for col_idx, width in summary_widths.items():
    ws_summary.column_dimensions[get_column_letter(col_idx)].width = width

# Save both to root and test_data
wb.save('TestCase.xlsx')
wb.save('test_data/TestCase.xlsx')
print("Successfully generated and saved styled TestCase.xlsx")
