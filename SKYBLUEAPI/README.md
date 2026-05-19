# SKYBLUEAPI

基于 FastAPI 的异步 API 脚手架`fast-boiler`项目骨架。


## 特性

- 异步 API：FastAPI + async/await
- 认证与用户系统：fastapi-users + JWT（Cookie Transport）
- ORM：SQLAlchemy（Async）+ SQLite（默认）
- 分页：fastapi-pagination
- 环境变量：python-dotenv（启动时加载 .env）

## 技术栈

- Web：FastAPI, Uvicorn
- Auth：fastapi-users, python-jose, passlib[bcrypt]
- DB：SQLAlchemy, aiosqlite（默认），asyncpg（可选）
- Utils：python-dotenv, pydantic

## 目录结构

```
app/
  auth/           认证相关（Strategy / Routers / UserManager）
  controllers/    路由层（Controller）
  services/       业务逻辑层（Service）
  repositories/   数据访问层（Repository）
  schemas/        Pydantic 模型（Schema）
  models/         SQLAlchemy 模型（Model）
  database.py     数据库引擎与 Session 依赖
  main.py         应用入口（FastAPI app）
```

## 前置要求

- Python 3.10+（建议）
- Windows 需要使用 PowerShell 或 Windows Terminal 执行命令

## 快速开始（Windows）

1. 创建并激活虚拟环境

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. 安装依赖

```powershell
pip install -r requirements.txt
```

3. 配置环境变量

- 复制示例文件并填写 SECRET_KEY（必须）

```powershell
copy .env.example .env
```

在 `.env` 中设置：

```
SECRET_KEY=your-secret-key
```

4. 启动开发服务

```powershell
uvicorn app.main:app --reload
```

访问：

- Swagger UI：`http://127.0.0.1:8000/docs`
- ReDoc：`http://127.0.0.1:8000/redoc`

## 快速开始（macOS/Linux）

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## 主要接口说明

认证、用户与业务路由在 [app/main.py](file:///d:/skyblue_file/GItHub/fastapi-study/SKYBLUEAPI/app/main.py) 中注册。当前主要接口如下：

- 认证
  - `PUT /auth/register`：用户注册，请使用 JSON body 提交 `account`、`password`、`mobile` 等参数。
  - `POST /auth/login`：用户登录，成功后返回 token，并写入 Cookie。
  - `POST /auth/logout`：退出登录，清除 Cookie。
- 当前用户
  - `GET /user/info`：获取当前登录用户信息，需要携带 token。
- 用户列表
  - `GET /users/list`：分页查询 `box_user` 用户列表，需要携带 token。
- AI 模型列表
  - `GET /model/list`：分页查询 `box_ai_api_model` 模型列表，只返回 `is_delete = 0` 的数据，需要携带 token。

说明：

- 本项目使用 Cookie 方式承载 JWT；本地调试可以先调用 `/auth/login` 获取登录态，再请求需要登录的接口。
- 分页接口支持 `page`、`size` 查询参数，例如：`GET /model/list?page=1&size=20`。

## 数据库

默认使用 SQLite（异步驱动 aiosqlite），数据库文件为项目根目录下 `app.db`：

- 配置位置：[app/database.py](file:///d:/skyblue_file/GItHub/fastapi-study/SKYBLUEAPI/app/database.py)
- 应用启动时会自动创建表（开发便利）；生产环境通常建议引入 Alembic 做迁移管理

## 代码生成（fast-boiler）

如果你使用 fast-boiler 生成资源模块，可参考以下约定（示例：product）：
`fast-boiler generate product`

- `app/controllers/product.py`：控制器（路由层）
- `app/services/product.py`：业务逻辑层
- `app/repositories/product.py`：数据访问层
- `app/schemas/product.py`：Pydantic 模型
- `app/models/product.py`：SQLAlchemy 模型

## 开发约定

- Controller 只负责参数解析、依赖注入、返回响应；业务逻辑放在 Service
- Repository 只负责与数据库交互；不要在路由层直接写 ORM 查询
- Schema 与 Model 分离，避免直接暴露数据库实体

## 常见问题

- 启动时报错 `SECRET_KEY environment variable not set`
  - 确认已创建 `.env` 文件并设置 `SECRET_KEY`
- PowerShell 无法激活虚拟环境
  - 可使用管理员 PowerShell 执行：`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
