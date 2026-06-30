# uv 是 python 版本管理工具

### uv 操作命令
```bash
  uv python list # 查看可安装的版本/查看已安装版本
  uv python install 3.11.15 # 安装指定版本
  
  # 项目中切换 Python 版本
  ① 修改或创建 .python-version
    uv python pin 3.11.15 # 会修改（或创建）.python-version
  ② 需要重新创建虚拟环境
    rm -rf .venv
    uv venv
    #或者直接指定
    uv venv --python 3.11.15
  ③ 验证
    source .venv/bin/activate
    python -V
   完成了这3步即可更换版本成功
   
  # 删除某个版本
    uv python uninstall 3.11.15
    
  # 查看python版本号，项目根目录执行
    uv run python -V # 每个虚拟环境下（.venv）都有不一样的版本号
```



```bash
  # 部署到 Linux 时要上传 .venv 吗？ 答案是：不需要
  
  #正确流程是：
    本地
    ├── app/
    ├── main.py
    ├── pyproject.toml
    └── uv.lock
   uv sync # uv 会自动创建新的 .venv 并安装所有依赖。
```
# uv.lock
```bash
   uv sync # 会生成 uv.lock 文件

```

## 如果使用 requirements.txt，则执行：
```bash
    uv venv # 会生成 python 虚拟环境目录 .venv
    source .venv/bin/activate
    uv pip install -r requirements.txt # 安装 requirements.txt 中包依赖
```
## 导入 requirements.txt 中依赖到 pyproject.toml
```bash
    # 可以逐个添加
    uv add fastapi
    uv add uvicorn
    ...
    #直接导入所有
    uv add -r requirements.txt

```

## 现有的项目生成 pyproject.toml、 uv.lock
```bash
    # 进入项目根目录
    uv init
    # uv 不会删除你的代码，只会在没有这些文件时创建
    pyproject.toml
    README.md（可能）
    .gitignore（可能）

```

 ## .python-version
    这是一个非常简单的文本文件，里面通常只有一行：
    3.11
    这个项目希望使用哪个 Python 版本。
    它是怎么生成的？
    uv python pin 3.11.15 # 就可以生成.python-version文件了
    作用：
        假设你安装了多个版本：
                Python 3.9
                Python 3.11
                Python 3.12
        uv 会读取 .python-version，如果里面是 3.11.15，那么 uv run python 会自动使用 Python 3.11.15， 不用手动指定 uv run --python 3.9 python