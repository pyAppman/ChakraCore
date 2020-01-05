from ctypes import *

JsValueType_JsUndefined = 0  # 公开,该值是未定义的值。
JsValueType_JsNull = 1  # 公开,值为空值。
JsValueType_JsNumber = 2  # 公开,该值是JavaScript数值。
JsValueType_JsString = 3  # 公开,该值是JavaScript字符串值。
JsValueType_JsBoolean = 4  # 公开,该值是JavaScript布尔值。
JsValueType_JsObject = 5  # 公开,该值是JavaScript对象值。
JsValueType_JsFunction = 6  # 公开,该值是JavaScript函数对象值。
JsValueType_JsError = 7  # 公开,该值是JavaScript错误对象值。
JsValueType_JsArray = 8  # 公开,该值是JavaScript数组对象值。
JsValueType_JsSymbol = 9  # 公开,该值是JavaScript符号值。
JsValueType_JsArrayBuffer = 10  # 公开,该值是JavaScriptArrayBuffer对象值。
JsValueType_JsTypedArray = 11  # 公开,该值是JavaScript类型的数组对象值。
JsValueType_JsDataView = 12  # 公开,该值是JavaScriptDataView对象值。


class ChaCore:

    def __init__(self):
        self.source = ''
        self.dll = windll.LoadLibrary('ChakraCore.dll')
        self.init_source = '''(function(){%s;return %s})()'''
        self.count = 0
        self.result = c_wchar_p('')
        self._runtime = c_long(0)
        self._context = c_long(0)
        self._result = c_long(0)
        self._type = c_long(0)
        self._res_ptr = c_long(0)
        self._length_ptr = c_long(0)

    def compile(self, source):
        self.source = source

    def create_runtime(self):
        return self.dll.JsCreateRuntime(0, None, pointer(self._runtime))

    def create_context(self):
        return self.dll.JsCreateContext(self._runtime, pointer(self._context))

    def set_current_context(self):
        return self.dll.JsSetCurrentContext(self._context)

    def value(self, value):
        if value == JsValueType_JsNumber:
            self.result = c_float(0)
        elif value == JsValueType_JsString:
            self.result = c_wchar_p('')
            if self.dll.JsConvertValueToString(self._result, pointer(self.result)):
                return 'JsConvertValueToString Error'
            str_ptr = c_wchar_p('')
            u_ptr = c_int(0)
            res = self.dll.JsStringToPointer(self.result, pointer(str_ptr), pointer(u_ptr))
            if res:
                return 'JsStringToPointer Error'
            else:
                return str_ptr.value
        elif value == JsValueType_JsArray:
            self.result = (c_wchar * 10)()
        elif value == JsValueType_JsObject:
            self.result = {}
        else:
            self.result = None

    def run(self, func, *args):
        if not self._runtime:
            self.create_runtime()
        self.create_context()
        self.set_current_context()

        target = '{name}{arg}'.format(name=func, arg=args)
        js = self.init_source % (self.source, target)
        self.count += 1
        _run = self.dll.JsRunScript(c_wchar_p(js), self.count, c_wchar_p(''), pointer(self._result))
        if _run:
            self.dispose()
            return 'JsRunScript Error!', False
        return_type = self.dll.JsGetValueType(self._result, pointer(self._type))
        if return_type:
            self.dispose()
            return 'Js Return Type Error!', False
        if self._type.value == JsValueType_JsArray:
            self.dispose()
            return 'List wait', False
        if self.dll.JsConvertValueToString(self._result, pointer(self.result)):
            self.dispose()
            return 'JsConvertValueToString Error', False
        str_ptr = c_wchar_p('')
        u_ptr = c_int(0)
        res = self.dll.JsStringToPointer(self.result, pointer(str_ptr), pointer(u_ptr))
        if res:
            self.dispose()
            return 'JsStringToPointer Error', False
        else:
            # print(str_ptr.value)
            # self.dispose()
            return str_ptr.value, True

    def dispose(self):
        # self.dll.JsSetCurrentContext(0)
        self.result = c_wchar_p('')
        self.count = 0
        self.dll.JsDisposeRuntime(self._runtime)
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.result = c_wchar_p('')
        self.count = 0
        self.dll.JsDisposeRuntime(self._runtime)



