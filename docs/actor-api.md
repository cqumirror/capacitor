API
===

##Schema
1. 数据返回格式统一使用 `json`
2. HTTP Method: `GET`
3. 时间格式: yyyy-MM-dd HH:mm:ss
4. 返回值为单个对象:


```
{
    "count": 10,
    "targets": []
}
```

参数说明:

|参数|意义|备注|
|----|----|----|
|count|对象个数||
|targets|对象列表||


##获取镜像列表
```
GET    /api/mirrors
```

返回列表中对象:
```
{
      "comment": "",
      "has_comment": false,
      "has_help": true,
      "muted_at": null,
      "is_muted": false,
      "sync_status": null,
      "created_at": null,
      "help_url": "https://mirrors.cqu.edu.cn/wiki/index.php?title=CentOS",
      "url": "https://b.mirrors.lanunion.org/centos",
      "cname": "centos",
      "upstream_url": null,
      "full_name": "CentOS",
      "synced_at": null,
      "size": null
}
```

参数说明:

|参数|意义|备注|
|----|----|----|
|cname|权威名称 全局 ID|应仅包含 [a-z] 和 -|
|full_name|显示名字|参见镜像官方|
|url|镜像链接|现需完整 url|
|help_url|镜像使用帮助链接|现链接到相应 wiki 页|
|comment|镜像备注||
|synced_at|最后同步时间||
|size|镜像大小||
|sync_status|镜像更新状态|具体代码含义参加下表|
|upstream_url|用于更新该镜像的上游 url||
|muted_at|镜像冻结时间||
|created_at|镜像创建时间||

`sync_status` 状态说明:

|状态码|含义|备注|
|----|----|----|
|100|Syncing|正在更新|
|200|Success|更新成功|
|300|Freeze|镜像冻结|
|400|Failed|更新失败|
|500|Unknown|状态不明|



##获取镜像站公告
```
GET    /api/notices
```

返回列表中的对象:
```
{
    "is_muted": false,
    "created_at": "2015-1-1 11:11:11",
    "muted_at": null,
    "id": 1,
    "github_issue_url": null
}
```
