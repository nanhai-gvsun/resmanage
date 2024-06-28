# -*- coding: utf-8 -*-
import os
# 数据结构定义
class gsData(object):
    def __init__(self,**kargs):
        # 数据类型
        self.content_type=kargs.get("content_type","")
        # 数据内容
        self.content=kargs.get("content","")
        #获取数据内容的编码
        self.encoding=kargs.get("encoding","")
# 定义一个标准文件
class gsFile(gsData):
    # 定义一个gsFile类，继承自gsData类
    def __init__(self,**kargs):
        super().__init__(**kargs)
        # 调用父类的初始化方法
        self.path=kargs.get("path","")
        if self.path!="":self._t1()
    def _t1(self):
        # 获取传入的路径参数，如果没有则默认为空
        self.name=os.path.basename(self.path)
        # 获取路径的文件名
        self.dir=os.path.dirname(self.path)
        # 获取路径的目录
        self.ext=os.path.splitext(self.name)[1]
        self._get_content_type()
        # 获取文件的后缀名
        self.is_linked = os.path.exists(self.path)
        #判断路径是否存在
        if self.path!="":
            if os.path.exists(self.path):
                self.is_linked = True
            else:
                self.is_linked = False
        else:
            self.is_linked = False
    def _get_content_type(self):
        if not self.path:
            return None
        self.content_type = 'application/octet-stream'
        if self.ext.lower() == '.txt':
            self.content_type = 'text/plain'
        elif self.ext.lower() == '.md':
            self.content_type = 'text/plain'    
        elif self.ext.lower() == '.html':
            self.content_type = 'text/html'
        elif self.ext.lower() == '.jpg':
            self.content_type = 'image/jpeg'
        elif self.ext.lower() == '.json':
            self.content_type = 'application/json'
        elif self.ext.lower() == '.js':
            self.content_type = 'application/javascript'            
    def open(self,filename=None):
        if self.path=="":
            if not filename:
                self.path=filename
                self._t1()
            else:
                raise ValueError("File path cannot be empty")
        return self
    def close(self):
        return self
    def read(self):
        if not os.path.exists(self.path):
            return self.content
        with open(self.path, 'r') as f:
            self.content = f.read()
        return self.content
    def write(self,data=None):
        if data:self.content=data
        if self.encoding!="":data=self.content.encode(self.encoding)
        if os.path.exists(self.path):
            with open(self.path, 'w') as f:
                f.write(data)
                
        return self

# 定义一个文档
class gsDocument(gsFile):
    def convert_to_html(self,filepath=None):
        if self.ext.lower() == '.md':
            if self.content!="":
                import markdown
                data=markdown.markdown(self.content)
                if filepath:
                    # 如果有文件路径参数，则将转换后的内容写入文件
                    _file=gsDocument(path=filepath)
                    _file.write(data)
                    return _file
                else:data
        else:
            raise ValueError("File extension is not .md")
        return self
    def convert_to_pdf(self, filepath=None):
        if self.ext.lower() == '.html':
            if filepath is None:
                filepath = self.name.replace('.html', '.pdf')
            import pdfkit
            if self.content=="":pdfkit.from_file(self.path, filepath)
            else:pdfkit.from_string(self.content, filepath)
            return self
        else:
            raise ValueError("File extension is not .html")
        
# 使用示例
# 创建一个gsFile对象，传入文件路径
if __name__ == '__main__':
    gsDocument(path="D:\\test\\test.md").write(data="") \
        .convert_to_html(filepath="D:\\test\\test.html")  \
            .convert_to_pdf(filepath="D:\\test\\test.pdf")

