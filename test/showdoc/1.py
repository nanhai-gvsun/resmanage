# -*- coding: utf-8 -*-
import requests,json,sys,argparse,os,markdown,pdfkit

parser = argparse.ArgumentParser()
parser.add_argument('-token', help='Gitlab access token', default='fea892ba02a14105a2775e3f89bd21ea')
parser.add_argument('-path', help='输出文件路径',default="./")
parser.add_argument('-page_id', help='showdoc页面id',type=int,default=-1)
parser.add_argument('-module', help='子系统',type=str,default="")
args = vars(parser.parse_args(sys.argv[1:]))
headers = {'Authorization': args["token"]}

if args["page_id"]!=-1:
    url="https://www.lubanlou.com/showdocserver/v1/api/page/info?page_id={}".format(args["page_id"])    
    response=requests.post(url,headers=headers)
    # 检查请求是否成功
    if response.status_code == 200:
        data=response.json()
        if data['error_code']==0:
            filename=data["data"]["page_title"]
            fileconetent=data["data"]["page_content"]
            mdfile="{}\\markdown\\{}_{}_{}.md".format(args["path"],args["module"],args["page_id"],filename)
            htmlfile="{}\\html\\{}_{}_{}.html".format(args["path"],args["module"],args["page_id"],filename)
            pdffile="{}\\pdf\\{}_{}_{}.pdf".format(args["path"],args["module"],args["page_id"],filename)
            print("正在生成文件：{}".format(mdfile))
            with open(mdfile,"w", encoding='utf-8') as f:
                f.write(fileconetent)
            print("正在生成文件：{}".format(htmlfile))
            html_content = markdown.markdown(fileconetent, extensions=['markdown.extensions.extra', 'markdown.extensions.toc','tables'])
            with open(htmlfile, "w", encoding='utf-8') as f:
                f.write(html_content)
            print("正在生成文件：{}".format(pdffile))
            pdfkit.from_string(html_content, pdffile,options = {'encoding': 'UTF-8'})
            print("文件已生成到")