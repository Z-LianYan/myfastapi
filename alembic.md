# 集成 alembic

### 安装
```commandline
pip install alembic
```

### 根目录执行
```commandline
alembic init alembic
```
    会生成：
        alembic
        ├── versions
        ├── env.py
        ├── script.py.mako
        
        alembic.ini

    配置数据库 
        alembic.ini 找到 sqlalchemy.url =
        修改 sqlalchemy.url = mysql+pymysql://root:123456@127.0.0.1:3306/admin_py_tpl

### 生成第一次迁移
```commandline
alembic revision --autogenerate -m "init"
```
    生成文件 alembic/versions/xxxxx_init.py

### 执行迁移
```commandline
alembic upgrade head
```
    数据库表就创建了
    包括 
        alembic_version

### 新增字段
```bash
email = Column(String(100))
# 生成迁移
alembic revision --autogenerate -m "add email"
# 执行迁移
alembic upgrade head
# 数据库自动更新 执行 ALTER TABLE users ADD email VARCHAR(100)
```

### 回滚
```bash
# 回退一步
alembic downgrade -1
# 回退指定版本
alembic downgrade 版本号
```
### 查看历史
```bash
alembic history
```

### 查看当前版本
```bash
alembic current
```
