# SQLAlchemy 的使用例子

#### 查询
```
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

```

### 新增
```
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
        
