# src/reporter.py
import pandas as pd
import xlsxwriter

def generate_professional_excel(df, output_path):
    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
    sheet_name = 'Auditoria LGPD'
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    
    # Formatos de cor
    format_danger = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006', 'bold': True})
    format_safe = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100', 'bold': True})
    format_header = workbook.add_format({'bg_color': '#003366', 'font_color': '#FFFFFF', 'bold': True})

    # Cabeçalho bonito
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, format_header)
        
    # Encontra a coluna de status
    idx = df.columns.get_loc('Status_Predito') if 'Status_Predito' in df.columns else 1
    
    # PINTA O TEXTO: DADO PESSOAL -> VERMELHO
    worksheet.conditional_format(1, idx, len(df), idx, {
        'type': 'text', 'criteria': 'containing', 'value': 'DADO PESSOAL', 'format': format_danger
    })
    
    # PINTA O TEXTO: DADO PÚBLICO -> VERDE
    worksheet.conditional_format(1, idx, len(df), idx, {
        'type': 'text', 'criteria': 'containing', 'value': 'DADO PÚBLICO', 'format': format_safe
    })
    
    worksheet.set_column(0, 0, 80) # Largura texto
    worksheet.set_column(1, 1, 25) # Largura status
    
    writer.close()
    return output_path
