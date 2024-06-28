# -*- coding: utf-8 -*-
import requests,json,sys,argparse,os

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
url = "{gitlab_url}/api/v4/projects/{project_id}/issues".format(**args)
def getNotes(id):
    data=args.copy()
    data["id"]=id
    url="{gitlab_url}/api/v4/projects/{project_id}/issues/{id}/notes".format(**data)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
response = requests.get(url, headers=headers)
if response.status_code == 200:
    issues = response.json()
    if args.get("fileformat")=="json":print("[")
    elif args.get("fileformat")=="single":
        # 建立目录
        path=os.path.abspath(os.path.join(args.get("path"),"./"+str(args.get("project_id"))))
        if not os.path.exists(path):
            os.makedirs(path)
    for issue in issues:
        issue["notes"]=getNotes(issue["iid"])
        if args.get("fileformat")=="json":print(json.dumps(issue, indent=4, ensure_ascii=False)+","  if issue != issues[-1] else "")
        elif args.get("fileformat")=="txt":
            print("添加到知识库:",json.dumps(issue, ensure_ascii=False),"-r=n")
        elif args.get("fileformat")=="single":
            # 写入文件
            with open(path+"/"+str(issue["iid"])+".json","w",encoding="utf-8") as f:
                f.write(json.dumps(issue, indent=4, ensure_ascii=False))
    if args.get("fileformat")=="json":print("]")
else:
    print("Failed to retrieve issues:", response.status_code)