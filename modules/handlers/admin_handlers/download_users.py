from openpyxl.reader.excel import load_workbook

wb = load_workbook(filename="all_users.xlsx")


def upload_all_data(data: list):
    x = 1
    bad = 0
    worksheet = wb['1']
    worksheet[f'A{x}'] = f'ID'
    worksheet[f'B{x}'] = f'tg_id'
    worksheet[f'C{x}'] = f'User_name'
    worksheet[f'D{x}'] = f'Language'
    worksheet[f'E{x}'] = f'Lust active'
    worksheet[f'F{x}'] = f'First reg data'
    x = 2
    for i in data:
        try:
            worksheet[f'A{x}'] = f'{i[0]}'
            worksheet[f'B{x}'] = f'{i[1]}'
            worksheet[f'C{x}'] = f'{i[2]}'
            worksheet[f'D{x}'] = f'{i[4]}'
            worksheet[f'E{x}'] = f'{i[5]}'
            worksheet[f'F{x}'] = f'{i[6]}'
            x += 1
        except:
            x += 1
            bad += 1
    wb.save('all_users.xlsx')
    return x-2, bad


def upload_all_users_id(data: list):
    x = 1
    bad = 0
    worksheet = wb['1']
    worksheet[f'A{x}'] = f'tg_id'
    x = 2
    for i in data:
        try:
            worksheet[f'A{x}'] = f'{i[1]}'
            x += 1
        except:
            x += 1
            bad += 1
    wb.save('all_users.xlsx')

    return x-2, bad
