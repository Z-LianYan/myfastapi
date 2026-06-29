# SQLAlchemy


## 这是 SQLAlchemy 最容易混淆的地方。返回什么类型，不是由 select 或 query 决定，而是由你查询的内容决定。
### 可以记住一个规则：
    查询模型（Model）→ 返回对象（Object）
    查询字段（Column）→ 返回元组（Tuple）或映射（Mapping）

# 一、query() 
## 1. 查询整个模型 → 返回对象
```bash
    data = db.query(Admin).all()
    #返回
    [
        <Admin object>,
        <Admin object>,
    ]
    #可以
    for item in data:
      print(item.name)
```
## 2.查询多个字段 → 返回元组
```bash
    data = db.query(
        Admin.id,
        Admin.name
    ).all()
    #返回
    [
        (1, "张三"),
        (2, "李四"),
    ]
    #访问
    row[0]
    row[1]
    #返回客户端
    result = [
        dict(row._mapping)
        for row in data
    ]
```
## 3.查询模型 + 字段
```bash
    data = db.query(
        Admin,
        AdminRole.role_name
    ).all()
    #返回
    [
        (<Admin object>, "财务"),
        (<Admin object>, "管理员"),
    ]
    #可以
    for admin, role_name in data
      print(admin.name,role_name)

```
# 二、select()
① 查询整个模型
```bash
  conditions = [Admin.delete_time.is_(None)]
  stmt = select(Admin).where(*conditions)
  
  data = db.execute(stmt).scalars().all()
  #返回：
  [
    {
        "Admin": <Admin object>
    }
  ]
  #可以
  for item in data
     print(item.name)
```
② 查询多个字段
```bash
    stmt = select(
        Admin.id,
        Admin.name
    )
    data = db.execute(stmt).all()
    #返回原组
    [
        (1, "张三"),
        (2, "李四"),
    ]
    # 返回的是原组可以使用 mappings() 直接得到 [{"id": 1,"name": "张三"}]
    data = db.execute(stmt).mappings().all()
    #返回
    [
        {
            "id": 1,
            "name": "张三"
        },
        {
            "id": 2,
            "name": "李四"
        }
    ]
```
③ 查询模型 + 字段
```bash
    stmt = select(
        Admin,
        AdminRole.role_name
    )
    data = db.execute(stmt).all()
    #返回
    [
        (<Admin>, "财务"),
    ]
    # mappings()
    data = db.execute(stmt).mappings().all()
    #返回
    [
        {
            "Admin": <Admin>,
            "role_name": "财务"
        }
    ]
```


# 总结
写法	                                        返回类型
db.query(Admin)	                            Admin 对象
db.query(Admin.id, Admin.name)	            元组
db.query(Admin, AdminRole.role_name)        (Admin对象, 字段)
select(Admin) + scalars()	                 Admin 对象
select(Admin) + all()	                     (<Admin>,)
select(Admin) + mappings()	                 {"Admin": <Admin>}
select(Admin.id, Admin.name) + all()	     元组
select(Admin.id, Admin.name) + mappings()	 字典








# SQLAlchemy 的使用例子

#### 查询
```bash
     # 例1
    result = (db.query(User.username,func.count(User.username).label("count"))
          .filter(
                User.password == "1",
                User.id>=1,
                User.id.in_([8,9,10]),
                User.username.like("%Tom%")
            )
          .group_by(User.username)
          .having(User.username=="Tom")
          .order_by(User.username.desc())
          .offset(0)
          .limit(10)
          .all())
          
        data = [
            {
                "username": item.username,
                "count": item.count
            }
            for item in result
        ]

        print("sql===>>",data)
        
        
        # 例2
        admin = db.query(Admin).filter(
            Admin.phone == phone
        ).one()
        特点：
        查不到 → 抛异常
        查到多条 → 抛异常
        必须且仅有一条
        

```

### 新增
```bash
    # 例1
    user = User(
        username="Tom",
        password="1",
        created=datetime.datetime.now(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print("create===user", user.id) # 获取新增后的id
    
    # 例2 新增多条数据
    users = [
        User(
            username="老六1",
            password="1",
            created=datetime.datetime.now(),
        ),
        User(
            username="老六2",
            password="1",
            created=datetime.datetime.now(),
        ),
        User(
            username="老六3",
            password="1",
            created=datetime.datetime.now(),
        )
    ]
    db.add_all(users)
    db.commit()
```
### 修改
```bash
    # 例1
    user = (
        db.query(User)
        .filter(User.id == 12)
        .first()
    )
    if user:
        user.username = "Tom12"
        db.commit()
    # 例2
    db.query(User).filter(
        User.id == 12
    ).update({
        User.username: "Tom1212"
    })
    db.commit()
    
    
```

### 删除
```
    # 例1
    user = (
        db.query(User)
        .filter(User.id == 14)
        .first()
    )

    if user:
        db.delete(user)
        db.commit()

    # 例2
    db.query(User).filter(
        User.id == 15
    ).delete()
    db.commit()
```

### 事务回滚
```
    try:
    
        user = User(
            username="王五33",
            password="1",
            created=datetime.datetime.now(),
        )
    
        db.add(user)
        raise Exception('事务回滚')
        db.commit()
    
    except Exception:
        db.rollback()
        raise
```
        
