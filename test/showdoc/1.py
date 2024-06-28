# -*- coding: utf-8 -*-
import requests,json,sys,argparse,os,markdown,pdfkit

parser = argparse.ArgumentParser()
parser.add_argument('-token', help='Gitlab access token', default='fea892ba02a14105a2775e3f89bd21ea')
parser.add_argument('-path', help='输出文件路径',default="./")
parser.add_argument('-page_id', help='showdoc页面id',type=str,default="")
parser.add_argument('-module', help='子系统',type=str,default="")
parser.add_argument('-onefile', help='是否一个问题一个文件',action='store_true')
parser.add_argument('-file', help='文件名',type=str,default="")
args = vars(parser.parse_args(sys.argv[1:]))
headers = {'Authorization': args["token"]}

# 检查目录是否存在，不存在则创建
if not os.path.exists(args["path"]):
    os.makedirs(args["path"])

if args["onefile"]==False:
    # 检查子目录markdown是否存在，不存在则创建
    if not os.path.exists(args["path"]+"\\markdown"):os.makedirs(args["path"]+"\\markdown")
    # 检查子目录html是否存在，不存在则创建
    if not os.path.exists(args["path"]+"\\html"):os.makedirs(args["path"]+"\\html")
    # 检查子目录pdf是否存在，不存在则创建
    if not os.path.exists(args["path"]+"\\pdf"):os.makedirs(args["path"]+"\\pdf")
if args["page_id"]!="":
    mdfilepath=args["path"] if args["onefile"] else "{}\\markdown".format(args["path"]) 
    htmlfilepath=args["path"] if args["onefile"] else "{}\\html".format(args["path"])
    pdffilepath=args["path"] if args["onefile"] else "{}\\pdf".format(args["path"])
    for pageid in args["page_id"].split(","):
        url="https://www.lubanlou.com/showdocserver/v1/api/page/info?page_id={}".format(pageid)    
        response=requests.post(url,headers=headers)
        # 检查请求是否成功
        if response.status_code == 200:
            data=response.json()
            if data['error_code']==0:
                filename=data["data"]["page_title"].replace("|","-")
                fileconetent=data["data"]["page_content"]
                if args["file"]=="":
                    mdfile="{}\\{}_{}_{}.md".format(mdfilepath,args["module"],pageid,filename)
                    htmlfile="{}\\{}_{}_{}.html".format(htmlfilepath,args["module"],pageid,filename)
                    pdffile="{}\\{}_{}_{}.pdf".format(pdffilepath,args["module"],pageid,filename)
                else:
                    mdfile="{}\\{}.md".format(mdfilepath,args["file"])
                    htmlfile="{}\\{}.html".format(htmlfilepath,args["file"])
                    pdffile="{}\\{}.pdf".format(pdffilepath,args["file"])
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