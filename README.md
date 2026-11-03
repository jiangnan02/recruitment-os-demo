# Recruitment OS · 校招公开 Demo

这是独立的 Streamlit 展示应用。它不导入原项目模块、不读取原项目数据目录，使用的候选人和岗位均为代码内的虚构示例。适合单独复制到一个新的 GitHub 仓库后部署到 Streamlit Community Cloud。

## 安全边界

- 仅包含 `DEMO-xxx` 虚构候选人 ID，不包含个人姓名、联系方式、真实简历或企业资料。
- JD、候选人阶段和面试安排的变更仅保存在当前 Streamlit 会话的 `session_state` 中；不写入磁盘或原项目文件。每个访问会话相互隔离，关闭/重启后数据恢复为初始样例。
- “创建模拟安排”不会联系飞书、招聘平台、邮件或其他外部服务，不会发送真实通知。
- 行业报告为静态合成内容，不代表真实市场统计，不连接 AI 服务。
- 本目录适合作为公开演示，不应加入真实招聘数据或密钥。

## 本地运行

建议使用 Python 3.12。进入本目录后安装依赖并启动：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

浏览器通常会打开 `http://localhost:8501`。运行测试：

```powershell
python -m unittest discover -s tests -v
```

## 单独上传到 GitHub（不会自动上传）

1. 在本机新建一个空目录，例如 `recruitment-os-public-demo`。
2. **只将本 `public_demo` 目录里的内容复制到新目录根部**。不要复制仓库根目录中的 `data/`、`resumes/`、`reports/`、`simulation/`、`agents/`、原 `dashboard/` 或其他文件。
3. 检查新目录包含 `app.py`、`demo_data.py`、`requirements.txt`、`runtime.txt`、`.streamlit/config.toml` 和本 README；确认没有 `.env`、密钥或真实资料。
4. 在 GitHub 手动创建新的空仓库，选择公开前再次检查仓库文件清单。将新目录作为独立仓库提交并推送。**不要把原项目仓库直接改成公开，也不要提交本地 `.streamlit/secrets.toml`。**
5. 登录 Streamlit Community Cloud，选择 **Create app**，授权 GitHub 后选择刚创建的仓库和分支。
6. Main file path 填写 `app.py`（因为上传的是 `public_demo` 的目录内容，应用入口位于新仓库根目录）。如直接在当前原项目仓库的副本结构中选择，则路径为 `public_demo/app.py`，但不建议将含原始数据的完整仓库公开。
7. 选择 Python 3.12（若界面提供），点击部署。此应用无需配置 Secrets、API Key 或第三方服务权限。
8. 部署后检查六个模块、添加岗位/调整候选人阶段/创建模拟面试，以及侧边栏“重置本会话演示”是否正常。不要在 Community Cloud 中导入原项目数据。

## 功能清单

- 总览与校招流程指标
- JD 管理（添加岗位、切换模拟状态）
- 候选人池（岗位/匹配分筛选、会话内阶段调整）
- 招聘漏斗
- 虚构 AI 行业报告
- 面试协调模拟
