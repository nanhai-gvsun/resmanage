# -*- coding: utf-8 -*-
import requests,json,sys,argparse,os,markdown,pdfkit

parser = argparse.ArgumentParser()
parser.add_argument('-path', help='输出文件路径',default="./")
parser.add_argument('-mdfile', help='markdown文件名',type=str,default="")
args = vars(parser.parse_args(sys.argv[1:]))

if args["mdfile"]!="":
    file=os.path.basename(args["mdfile"])
    filename,extension = os.path.splitext(os.path.basename(file))

    htmlfile=os.path.abspath(os.path.join(args["path"],filename))+".html"
    pdffile=os.path.abspath(os.path.join(args["path"],filename))+".pdf"

    with open(args["mdfile"],"r", encoding='utf-8') as f:
        fileconetent=f.read()
    print("正在生成文件：{}".format(htmlfile))
    html_content = markdown.markdown(fileconetent, extensions=['markdown.extensions.extra', 'markdown.extensions.toc','tables'])
    with open(htmlfile, "w", encoding='utf-8') as f:
        f.write(html_content)
    print("正在生成文件：{}".format(pdffile))
    pdfkit.from_string(html_content, pdffile,options = {'encoding': 'UTF-8'})
    print("文件已生成到")

# python .\makefile.py -file="Z:\kb\14组\软著\人脸门禁\GVSUN人脸门禁管理系统V1.0_操作文档.md" -path=Z:\kb\14组\软著\人脸门禁