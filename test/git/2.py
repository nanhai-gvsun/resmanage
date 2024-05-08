# -*- coding: utf-8 -*-
import requests,json,sys,argparse,os,gitlab,types

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

g1=gitlab.Gitlab(args["gitlab_url"], private_token=args["token"])
project=g1.projects.get(args["project_id"])
path=os.path.abspath(os.path.join(args.get("path"),"./"+str(args.get("project_id"))))
if not os.path.exists(path):
    os.makedirs(path)
# 遍历问题
i=0

# 设置你的 GitLab API 访问参数
API_URL = "{gitlab_url}/api/v4/projects/{project_id}/issues".format(**args)
HEADERS = {'PRIVATE-TOKEN': args["token"]}

# 发送请求
response = requests.get(API_URL, headers=HEADERS, params={'scope': 'all', 'per_page': 1})

# 检查请求是否成功
if response.status_code == 200:
    # 从响应头中获取问题总数
    total_issues = int(response.headers.get('X-Total', '0'))
    print("Total number of issues: ",total_issues)
    sys.stdout.write('\r正在读取问题列表...')
    sys.stdout.flush()
    issues=project.issues.list(all=True,iterate=True)
else:
    print(f"Failed to fetch data: Status code {response.status_code}, Response: {response.text}")
    sys.stdout.write('\r正在读取问题列表...')
    sys.stdout.flush()
    issues=project.issues.list(all=True)
    total_issues=len(issues)

for issue in issues:  
    # 打印进度条
    sys.stdout.write('\r')
    sys.stdout.flush()
    # sys.stdout.write("[{}.rjust(40,' ')]".format(i*"#")
    sys.stdout.write("[%-40s] %d%%" % ('='*int(i*40/total_issues), i*100/total_issues))
    sys.stdout.write("，当前处理：{}".format(str(issue.iid).rjust(7,"0")))
    sys.stdout.flush()
    i+=1
    # 获取issue对象实例的接口，将属性内容复制到字典变量data中
    data={key:getattr(issue,key) for key in dir(issue) \
          if key[:1]!="_" and key[:8]!="resource" \
            and type(getattr(issue,key))!=types.MethodType \
            and key not in ["awardemojis","discussions","notes","links","manager"]}
    data["notes"]=[]
    # 遍历评论
    for note in issue.notes.list(all=True):
        data1=dict(
            id=note.id,
            type=note.type,
            body=note.body,
            attachment=note.attachment,
            author=note.author,
            created_at=note.created_at,
            updated_at=note.updated_at,
            system=note.system,
            noteable_id=note.noteable_id,
            noteable_type=note.noteable_type,
            resolvable=note.resolvable,
            noteable_iid=note.noteable_iid
        )
        data["notes"].append(data1)
    data=json.dumps(data, indent=4, ensure_ascii=False)
    with open(path+"/"+str(issue.iid)+".json","w",encoding="utf-8") as f:
        f.write(data)
sys.stdout.write('\r')
sys.stdout.flush()
sys.stdout.write("[%-40s] %d%%" % ('='*int(i*40/total_issues), i*100/total_issues))
sys.stdout.flush()
