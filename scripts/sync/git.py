# -*- coding: utf-8 -*-
from sync import gsDocument

gsDocument(path="Z:\\reseach\\resmanage\\test\\showdoc\\1.md").write(data="hello world\n") \
    .convert_to_html(filepath="Z:\\reseach\\resmanage\\test\\showdoc\\2.html")  \
        .convert_to_pdf(filepath="Z:\\reseach\\resmanage\\test\\showdoc\\2.pdf")
# doc=gsDocument(path="Z:\\reseach\\resmanage\\test\\showdoc\\1.md",encoding="utf-8")
# doc.write(data="hello world\n")
# print(doc.content)