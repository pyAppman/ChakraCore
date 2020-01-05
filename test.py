# 测试用例
# dll务必放在ChakraCore.py同一目录下
from ChakraCore import ChakraCore
if __name__ == '__main__':
    js = 'function add(a, b){return a+b}'
    js_obj = ChakraCore()
    js_obj.compile(js)
    res, is_suc = js_obj.run('add', 10, 11)
    if is_suc:
        print(res)  # 21
    
