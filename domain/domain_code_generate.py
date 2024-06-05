import ast
from pathlib import Path

model_code = """
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Book(models.Model):
    id = fields.UUIDField(primary_key=True)

"""


def ast_to_text(node, indent=0):
    result = ' ' * indent + f'{node.__class__.__name__}:\n'
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    result += ast_to_text(item, indent + 1)
        elif isinstance(value, ast.AST):
            result += ' ' * (indent + 1) + f'{field}:\n'
            result += ast_to_text(value, indent)
        else:
            result += ' ' * (indent + 1) + f'{field}: {value}\n'
    return result


def get_assign(class_name, suffix='Dao'):
    param_name = class_name + suffix

    function_call = ast.Call(
        func=ast.Name(id='pydantic_model_creator', ctx=ast.Load()),
        args=[ast.Name(id=class_name)],
        keywords=[
            ast.keyword(arg='name', value=ast.Constant(param_name)),
        ]
    )
    dao_assign = ast.Assign(
        col_offset=0,
        lineno=19,
        targets=[ast.Name(id=param_name, ctx=ast.Store())],
        value=function_call
    )
    return dao_assign


def generate_class_from_string(class_string, class_name, fields, file_path):
    # 解析字符串为AST
    tree = ast.parse(class_string)
    body = tree.body
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # 替换class名
            node.name = class_name
            # break

            for index, field in enumerate(fields):
                function_call = ast.Call(
                    func=ast.Name(id='fields.TextField', ctx=ast.Load()),
                    args=[],
                    keywords=[]
                )
                field_assign = ast.Assign(
                    col_offset=4,
                    lineno=12 + index,
                    targets=[ast.Name(id=field, ctx=ast.Store())],
                    value=function_call
                )
                # 将field赋值节点添加到class body中
                node.body.insert(index, field_assign)

    body.insert(8, get_assign(class_name))
    body.insert(9, get_assign(class_name, 'Dto'))

    # 创建文件路径
    file_path = Path(file_path)
    # 创建文件目录
    file_path.parent.mkdir(parents=True, exist_ok=True)
    # 将AST写入文件
    with open(file_path, 'w') as f:
        f.write(ast.unparse(tree))


if __name__ == '__main__':
    # tree = ast.parse(model_code)
    # ast_text = ast_to_text(tree)
    # print(ast_text)
    generate_class_from_string(model_code, "Product", ['name', 'price', 'text'], "product.py")
