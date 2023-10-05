import pandas as pd

def transform_columns_to_numbers(input_csv_path, output_csv_path, columns_to_encode):
    column_code = {}
    df = pd.read_csv(input_csv_path, encoding='utf-8')
    
    for column_name in columns_to_encode:
        current_code = 1
        column_code[column_name] = {}
        for i in range(len(df)):
            column_value = df[column_name][i]
            if column_value not in column_code[column_name]:
                column_code[column_name][column_value] = str(current_code) 
                current_code += 1

            df.at[i, column_name] = column_code[column_name][column_value]
    df.to_csv(output_csv_path, index=False)

# 主程式
if __name__ == '__main__':
    import datetime
    start_time = datetime.datetime.now()
    
    columns_to_encode = ['縣市', '鄉鎮市區', '使用分區' ,'路名','主要用途', '主要建材']
    transform_columns_to_numbers('./CSV_DataSet/public_dataset.csv', './Save_CSV/Output_CSV/Output_CSV_Version1.csv', columns_to_encode)

    end_time = datetime.datetime.now()
    execution_time = (end_time - start_time).total_seconds() * 1000
    print('\n')
    print("程式運行時長：", execution_time, "ms",'\n')
