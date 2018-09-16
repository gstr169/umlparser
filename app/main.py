#!ENV\Scripts\python

import sys
from lxml import etree
from io import StringIO, BytesIO


# функция открывает xml файл,
# забирает из него нужные поля
# и формирует словарь элементов [{тег1:значение1, тег2:значение2, ...}, {тег1:значение3, ...}]
def parse_xml(src_path, tags):
    dict_list = [{}]
    src_xml = etree.parse(src_path)
    i = 0
    for element in src_xml.iter():
        # print("%s - %s" % (element.tag, element.text))
        if element.tag.lower() in tags:
            if i < len(tags):
                dict_list[-1][element.tag] = element.text
                i = i + 1
            else:
                dict_list.append({element.tag: element.text})
                i = 1
    return dict_list

# функция открывает плоский файл, и забирает из него элементы по индексам
# формирует словарь элементов [{индекс1:значение1, индекс2:значение2, ...}, {индекс1:значение3, ...}]
def parse_flat(src_path, indexes):
    dict_list = [{}]
    src_flat = open(src_path)
    for str in src_flat:
        str = str.strip()
        elem_list = str.split('|')
        for ind in indexes:
            dict_list[-1][ind] = elem_list[ind]
        dict_list.append({})


def create_sql(dict_list):
    for record in dict_list:
        # print(record)
        pass

# забирает словарь элементов и парсит элементы
def parse_fields(dict_list):
    for record in dict_list:
        # rec['test'] = 'test'
        string = record['panel_attributes'].strip()
        list_ = string.split('--')
        for val in list_:
            val = val.strip()
            val = val.split('\n')
            # print(val)
            if 'dbo' in val[0]:
                record['tbl_name'] = val[0]
                record['tbl_comment'] = '/*' + val[1].replace('/', '') + '*/'
            elif '-' in val[0]:
                record[val[0].replace('-', '').replace(':', '')] = '/*' + val[1].replace('/', '') + '*/'
        record.pop('panel_attributes')
    return dict_list


def main():
    # if len(sys.argv) < 2:
    #     examples_path = "C:/work/umlparser/examples/"
    #     src_path = input("Enter path to *.uxf file: ")
    #     src_path = examples_path + src_path
    # else:
    #     src_path = sys.argv[1]
    # print(src_path)  # debug print
    src_path = "C:/work/umlparser/examples/VTB24_20171109_8002_uf.xml"
    tags_path = "C:/work/umlparser/template/tmpl_xml.txt"
    f = open(tags_path)
    tags = []
    for string in f:
        tags.append(string.strip())
    out = parse_xml(src_path, tags)
    print(out)
    #out = parse_fields(out)
    #print(out)

    # create_sql(out)


if __name__ == '__main__':
    main()
