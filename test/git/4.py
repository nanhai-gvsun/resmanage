# -*- coding: utf-8 -*-
import requests,json,sys,argparse,os,gitlab,types,re,markdown,pdfkit

# 用您的访问令牌和项目ID替换这里的值
# TOKEN = 'TXs49vsikey2v48sjnGs'
# PROJECT_ID = 239
# GITLAB_URL = "http://192.168.1.139"
def makefile(file,data):
    with open(file,"w",encoding="utf-8") as f:
        f.write(data)
def downloadImage(path,data):
    image_url=re.findall(r'/uploads/\w+/\w+\.(?:jpg|jpeg|png|gif)', data)
    if len(image_url)>0:
        i=1
        for url in image_url:
            Progress_percentage=int(i*40/len(image_url))
            Remaining_percentage=40-Progress_percentage
            console_status("[{}{}] {}%,{}".format(
                '='*Progress_percentage, 
                " "*Remaining_percentage,
                str(int(i*100/total_issues)).rjust(3,"0"),
                "当前处理第{}个图片".format(str(i).rjust(7,"0"))
            ))
            i+=1
            filename=os.path.abspath(os.path.join(path,"."+url))
            urlpath=os.path.dirname(filename)
            # 如果urlpath不存在，则新建
            if not os.path.exists(urlpath):
                os.makedirs(urlpath)
            with open(filename,"wb") as f:
                f.write(requests.get("{}/{}{}".format(args["gitlab_url"],project.path_with_namespace,url)).content)

def makepdf(html_file,data,pdf_file=None):
    # print(html_file)
    # html_file=html_file.replace("{","").replace("}","")
    pdf_file=pdf_file.replace("{","").replace("}","")
    html_content = markdown.markdown(data)
    with open(html_file,"w", encoding='utf-8') as f:
        f.write(html_content)
    if pdf_file:pdfkit.from_file(html_file, pdf_file,options = {'encoding': 'UTF-8'})
def console_status(data):
    sys.stdout.write('\r'+data)
    sys.stdout.flush()
def append_data(data,list):
    list.append(data)

parser = argparse.ArgumentParser()
parser.add_argument('-token', help='Gitlab access token', default='TXs49vsikey2v48sjnGs')
parser.add_argument('-project_id', help='Gitlab project id', default=239)
parser.add_argument('-gitlab_url', help='Gitlab url', default="http://192.168.1.139")
parser.add_argument('-path', help='输出文件路径',default="./")
parser.add_argument('-count', help='读取问题数量',type=int,default=50)
parser.add_argument('-onefile', help='是否一个问题一个文件',action='store_true')
parser.add_argument('-downloadimage', help='是否下载图片',action='store_true')
parser.add_argument('-labels', help='标签过滤',type=str,default="")
parser.add_argument('-search', help='查询条件',type=str,default="")
parser.add_argument('-assignee', help='查询条件',type=str,default="")
parser.add_argument('-author', help='查询条件',type=str,default="")

args = vars(parser.parse_args(sys.argv[1:]))
headers = {'PRIVATE-TOKEN': args["token"]}

image_url=set()
g1=gitlab.Gitlab(args["gitlab_url"], private_token=args["token"])
project=g1.projects.get(args["project_id"])

# print(project.path_with_namespace)
if args.get("path")[:2]=="./":
    args["path"]=os.path.abspath(os.path.join(os.path.dirname(__file__),args.get("path")))
path=os.path.abspath(os.path.join(args.get("path"),"./"+project.path))
if not os.path.exists(path):
    os.makedirs(path)
if not os.path.exists(path+"/html"):
    os.makedirs(path+"/html")
if not os.path.exists(path+"/markdown"):
    os.makedirs(path+"/markdown")
if not os.path.exists(path+"/pdf"):
    os.makedirs(path+"/pdf")
args["path_with_namespace"]=project.path_with_namespace
print("正在处理项目[{}:{}]的问题...".format(args["project_id"],project.path_with_namespace))

# 遍历问题
i=0

# 设置你的 GitLab API 访问参数
API_URL = "{gitlab_url}/api/v4/projects/{project_id}/issues".format(**args)
HEADERS = {'PRIVATE-TOKEN': args["token"]}

# 获取记录数
params={'scope': 'all', 'per_page': 1,'page':1}
if args["labels"]!="":params.update({'labels': args["labels"]})
if args["search"]!="":params.update({'search':args['search']})
if args["assignee"]!="":params.update({'assignee':args['assignee']})
if args["author"]!="":params.update({'author':args['author']})
response = requests.get(API_URL, headers=HEADERS, params=params)
# 检查请求是否成功
if response.status_code == 200:
    # 从响应头中获取问题总数
    total_issues = int(response.headers.get('X-Total', '0'))
    print("问题数量: ",total_issues)

if args.get("count")>0 and total_issues>=args.get("count"):
    total_issues=args.get("count")
    print("读取数量: ",total_issues)
else:console_status("正在读取问题列表...")

# 读取问题列表
data=[]
for i in range(1,total_issues+1):
    params["page"]=i
    issue=project.issues.list(**params)[0]
    # 当前进度
    Progress_percentage=int(i*40/total_issues)
    Remaining_percentage=40-Progress_percentage
    console_status("[{}{}] {}%,{}".format(
        '='*Progress_percentage, 
        " "*Remaining_percentage,
        str(int(i*100/total_issues)).rjust(3,"0"),
        "当前处理第{}个问题".format(str(i).rjust(7,"0"))
    ))
    data.append("## 问题编号:{}".format(issue.iid))
    # if issue.author:data.append("- 发起人:{}".format(issue.author["name"]))
    # if issue.assignee:data.append("- 负责人:{}".format(issue.assignee["name"]))
    
    # if len(issue.assignees)!=0:data.append("- 指定人员:{}".format(issue.assignees[0]["name"]))
    data.append("- 标题:{}".format(issue.attributes["title"]))
    data.append("- 描述:\n{}\n".format(issue.attributes["description"]))
    if issue.attributes["labels"]:data.append("- 标签:{}".format(issue.attributes["labels"]))
    data.append("- 状态:{}".format(issue.state))
    data.append("- 回复:")
    for note in issue.notes.list(all=True):
        data.append("    - 时间:{}".format(note.created_at))
        data.append("      操作人:{}".format(note.author["name"]))
        data.append("      内容:{}".format(note.body.replace("\n","")))
    if args["onefile"]:
        file_data="\n".join(data)
        if args["downloadimage"]==False:
            issue_data=file_data.replace("/uploads","{gitlab_url}/{path_with_namespace}/uploads".format(**args))
        else:
            issue_data=file_data.replace("/uploads","./uploads")
            downloadImage(path,file_data)
        makefile(path+"/markdown/"+str(issue.iid)+".md",issue_data)
        makepdf(path+"/html/{}.html".format(issue.iid),issue_data,path+"/pdf/{}.pdf".format(issue.iid))
        data=[]
                    