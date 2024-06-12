# -*- coding: utf-8 -*-
import requests,json,sys,argparse,os,gitlab,types,re,markdown

# 用您的访问令牌和项目ID替换这里的值
# TOKEN = 'TXs49vsikey2v48sjnGs'
# PROJECT_ID = 239
# GITLAB_URL = "http://192.168.1.139"

parser = argparse.ArgumentParser()
parser.add_argument('-token', help='Gitlab access token', default='TXs49vsikey2v48sjnGs')
parser.add_argument('-project_id', help='Gitlab project id', default=239)
parser.add_argument('-gitlab_url', help='Gitlab url', default="http://192.168.1.139")
parser.add_argument('-fileformat', help='输出格式',default="json")
parser.add_argument('-path', help='输出文件路径',default="./")
args = vars(parser.parse_args(sys.argv[1:]))
headers = {'PRIVATE-TOKEN': args["token"]}
image_url=set()
g1=gitlab.Gitlab(args["gitlab_url"], private_token=args["token"])
project=g1.projects.get(args["project_id"])
# print(project.path_with_namespace)
if args.get("path")[:2]=="./":
    args["path"]=os.path.abspath(os.path.join(os.path.dirname(__file__),args.get("path")))
path=os.path.abspath(os.path.join(args.get("path"),"./"+project.path))
print(path)
if not os.path.exists(path):
    os.makedirs(path)
print("正在处理项目[{}:{}]的问题...".format(args["project_id"],project.path_with_namespace))
# 遍历问题
i=0

# 设置你的 GitLab API 访问参数
API_URL = "{gitlab_url}/api/v4/projects/{project_id}/issues".format(**args)
HEADERS = {'PRIVATE-TOKEN': args["token"]}

# 发送请求
response = requests.get(API_URL, headers=HEADERS, params={'scope': 'all', 'per_page': 1,'page':1})

# 检查请求是否成功
if response.status_code == 200:
    # 从响应头中获取问题总数
    total_issues = int(response.headers.get('X-Total', '0'))
    print("问题数量: ",total_issues)
    sys.stdout.write('\r正在读取问题列表...')
    sys.stdout.flush()
#     issues=project.issues.list(all=True,iterate=True)
data=[]
for i in range(1,total_issues+1):
    issue=project.issues.list(per_page=1,page=i)[0]
    sys.stdout.write('\r')
    sys.stdout.flush()
    # sys.stdout.write("[{}.rjust(40,' ')]".format(i*"#")
    sys.stdout.write("[%-40s]  %d%%" % ('='*int(i*40/total_issues), i*100/total_issues))
    sys.stdout.write("，当前处理第{}个问题".format(str(i).rjust(7,"0")))
    sys.stdout.flush()
    data.append("## 问题编号:{}".format(issue.iid))
    if issue.assignee:data.append("- 负责人:{}".format(issue.assignee["name"]))
    if len(issue.assignees)!=0:data.append("- 指定人员:{}".format(issue.assignees[0]["name"]))
    data.append("- 标题:{}".format(issue.attributes["title"]))
    data.append("- 描述:\n{}\n".format(issue.attributes["description"]))
    if issue.attributes["labels"]:data.append("- 标签:{}".format(issue.attributes["labels"]))
    data.append("- 状态:{}".format(issue.state))
    data.append("- 回复:")
    for note in issue.notes.list(all=True):
        data.append("    - 时间:{}".format(note.created_at))
        data.append("      操作人:{}".format(note.author["name"]))
        data.append("      内容:{}".format(note.body.replace("\n","")))
    del data[-1]
    data.append("==split line==")
print("")
body="\n".join(data)
image_url=re.findall(r'/uploads/\w+/\w+\.(?:jpg|jpeg|png|gif)', body)
print("需要下载的图片数量：",len(image_url))
i=0
if len(image_url)!=0:
    for url in image_url:
        filename=os.path.abspath(os.path.join(path,"."+url))
        urlpath=os.path.dirname(filename)
        # 如果urlpath不存在，则新建
        if not os.path.exists(urlpath):
            os.makedirs(urlpath)
        sys.stdout.write('\r')
        sys.stdout.flush()
        sys.stdout.write("[%-40s]  %d%%" % ('='*int(i*40/len(image_url)), i*100/len(image_url)))
        sys.stdout.write("，当前处理第{}张图片".format(str(i).rjust(7,"0")))
        sys.stdout.flush()
        i+=1
        with open(filename,"wb") as f:
            f.write(requests.get("{}/{}{}".format(args["gitlab_url"],project.path_with_namespace,url)).content)
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write("[%-40s] %d%%" % ('='*int(i*40/len(image_url)), i*100/len(image_url)))
    sys.stdout.write("，当前处理第{}张图片".format(str(i).rjust(7,"0")))
    sys.stdout.flush()
    body=body.replace("/uploads","./uploads")
with open(path+"/"+str(args["project_id"])+".txt","w",encoding="utf-8") as f:
    f.write(body)
with open(path+"/"+str(args["project_id"])+".md","w",encoding="utf-8") as f:
    f.write(body)
html_content = markdown.markdown(body)
with open(path+"/"+str(args["project_id"])+".html","w", encoding='utf-8') as f:
    f.write(html_content)
