import hashlib
import json
import os
import re

rootPath = os.path.dirname( os.path.dirname(os.path.realpath(__file__)) )

def makeMd5(raw):
    """计算出一个字符串的MD5值"""
    md5 = hashlib.md5()
    md5.update(raw.encode())
    return md5.hexdigest()

def jsonFormat(source):
    #rest = json.loads(source, encoding="utf-8")
    rest = json.loads(source, encoding="utf-8")
    return json.dumps(rest, ensure_ascii=False, indent=4, separators=(',', ':'))

# RGB格式颜色转换为16进制颜色格式
def RGB_to_Hex(rgb):
    RGB = rgb.split(',')  # 将RGB格式划分开来
    """
    color = ''
    for i in RGB[0:3]:
        num = int(i)
        # 将R、G、B分别转化为16进制拼接转换并大写  hex() 函数用于将10进制整数转换成16进制，以字符串形式表示
        color += str(hex(num))[-2:].replace('x', '0').upper()
    return color
    """
    #[-2:].replace('x', '0')是为了补零
    return ''.join(str(hex(int(i)))[-2:].replace('x', '0').upper() for i in RGB[0:3])

# 16进制颜色格式颜色转换为RGB格式
def Hex_to_RGB(hex):
    index = 0
    if hex[0] == "#":
        index = 1
    r = int(hex[index:index+2], 16)
    g = int(hex[index+2:index+4], 16)
    b = int(hex[index+4:index+6], 16)
    return r, g, b

def hex_convert(n, x):
    # n为待转换的十进制数，x为机制，取值为2-16
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'b', 'C', 'D', 'E', 'F']
    b = []
    while True:
        s = n // x  # 商
        y = n % x  # 余数
        b = b + [y]
        if s == 0:
            break
        n = s
    b.reverse()
    return "".join(str(x) for x in b)

def fieldname_camel2under(field):
    """驼峰命名转下划线命名
    小写和大写紧挨一起的地方,加上分隔符,然后全部转小写
    """
    sep = "_"
    # return name.replace(/([A-Z])/g,"_$1").toLowerCase();
    field_new = re.sub(r"([a-z])([A-Z])", r"\1{}\2".format(sep), field).lower()
    return field_new

def fieldname_under2camel(field, first_upper=False):
    """下划线命名转驼峰命名
    将字符串根据_分割成数组,再将每个单词首字母大写
    """
    #return "".join( [s.capitalize() for s in field.split("_")] )
    field_new = re.sub(r"_(\w)", lambda match:match.group(1).upper(), field)
    if first_upper:
        field_new = field_new[0].upper() + field_new[1:]
    return field_new

if __name__ == '__main__':
    print( fieldname_under2camel("table_body_lines", 1) )
    print(fieldname_camel2under("TableBodyLines"))