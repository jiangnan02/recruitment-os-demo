# Recruitment OS · 原版风格公开 Demo

独立的 Streamlit 展示目录，以原版 Dashboard 的深色侧边栏、六模块导航、页面层级、卡片/表格样式和招聘工作流为界面基准。此版本自包含，不导入原项目 `dashboard/`、`data/`、`resumes/`、`reports/`、`simulation/` 或 `agents/`。

## 安全边界

- 60 份合成简历样例，按三个演示岗位各 20 份生成。候选人仅用 `DEMO-001` 至 `DEMO-060` 标识；不包含真实姓名、联系方式、真实教育/雇佣信息或原简历文本。
- 公司/团队及岗位画像均为“示例”虚构内容；行业 Mapping 是静态演示，不包含原项目内部资料。
- 所有操作（JD、HR 状态、风险复核、面试安排、问题草稿）仅写入当前 Streamlit 会话的 `session_state`，不写本地共享数据文件。关闭会话或重启后恢复初始合成数据。
- 面试协调仅生成本地模拟草稿，不访问日历、不创建会议、不发送邮件/飞书/招聘平台消息。
- 风险检测分数是稳定的演示计算值，不判断任何真实简历，不能用于真实招聘决策。
- 公开发布时只上传此目录，不上传原项目仓库或历史记录，不设置 Secrets。

## 本地运行

建议 Python 3.12。进入此目录后安装并启动：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8503
```

## 测试

```powershell
python -m unittest discover -s tests -v
```

## Streamlit Community Cloud

将本目录的**内容**复制到独立的新 GitHub 仓库根目录；Streamlit Cloud 的 Main file path 使用 `app.py`，并在部署的 Advanced settings 中选择 Python 3.12（Community Cloud 通过部署界面设置 Python 版本，不依赖 `runtime.txt`）。不要发布原项目仓库。此版本无 API Key、Secrets 或外部集成配置。
