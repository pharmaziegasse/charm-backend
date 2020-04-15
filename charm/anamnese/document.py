import json

# This generates a Excel sheet out of anamnese data
import xlsxwriter

def handle_excel(form_data, path):
    # Get the raw form data from a submitted anamnese form page
    # json.loads converts it to a dictionary
    content = json.loads(form_data)

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet('Anamnesedaten')

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})
    align_left = workbook.add_format({'align': 'left'})

    # set the column width
    worksheet.set_column('A:A', 39)
    worksheet.set_column('B:B', 66)

    # Write some data headers.
    worksheet.write('A1', '#', bold)
    worksheet.write('B1', 'Antwort', bold)

    # Start from row 1, column 0.
    row = 1
    col = 0

    for k in content:
        # print(k, content[k])
        # print(type(content[k]))
        # print(content[k]['helpText'])
        if k != 'uid':
            worksheet.write(row, col, content[k]['helpText'], bold)
            if type(content[k]['value']) is str or type(content[k]['value']) is int:
                worksheet.write(row, col+1, content[k]['value'], align_left)
            if type(content[k]['value']) is list:
                litems = ", "
                # print(litems.join(content[k]['value']))
                worksheet.write(row, col+1, litems.join(content[k]['value']), align_left)
            if type(content[k]) is type(None):
                worksheet.write(row, col+1, "/")
            row += 1

    workbook.close()