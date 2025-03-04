import numpy as np

def numpy_to_c_array(matrix):
    # 转为Python列表
    matrix_list = matrix.tolist()
    
    # 构造C语言数组字符串
    c_array = "{\n"
    for row in matrix_list:
        row_str = ", ".join(map(str, row))
        c_array += f"    {{ {row_str} }},\n"
    c_array = c_array.rstrip(",\n") + "\n};"
    
    return c_array