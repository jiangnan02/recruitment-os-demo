"""Original-style Recruitment OS public demo, backed only by synthetic session data."""
from __future__ import annotations

import html
import json
from datetime import date, timedelta
from urllib.parse import quote

import streamlit as st

from demo_data import ROLES, STATUSES, reset_state

st.set_page_config(page_title="Recruitment OS", page_icon="◈", layout="wide", initial_sidebar_state="expanded")

CSS = """
<style>
:root { --navy:#111827; --blue:#2563eb; --muted:#64748b; --line:#e5e7eb; --bg:#f6f8fc; }
.stApp { background:var(--bg); } [data-testid="stSidebar"] { background:#101827; }
[data-testid="stSidebar"] * { color:#e5e7eb; } .stAppHeader,[data-testid="stHeader"] { background:rgba(246,248,252,.94); }
.block-container { padding-top:4.75rem; padding-bottom:3rem; max-width:1500px; }
.brand { color:white;font-size:1.2rem;font-weight:750;letter-spacing:.2px;padding:.35rem 0 1rem; }
.brand span { color:#60a5fa; } .side-nav { margin:.35rem 0 1rem; }
.side-nav a { display:block;color:#cbd5e1!important;text-decoration:none;padding:9px 11px;border-radius:8px;margin:3px 0;font-size:.9rem; }
.side-nav a:hover,.side-nav a.active { background:#1e293b;color:#fff!important; }
.page-title { color:#0f172a;font-size:2rem;font-weight:780;margin:.15rem 0 .15rem; }
.page-subtitle { color:#64748b;margin-bottom:1.3rem; }
.metric-card { background:white;border:1px solid #e8edf5;border-radius:14px;padding:18px 19px;box-shadow:0 3px 14px rgba(15,23,42,.045);min-height:112px; }
.metric-label { color:#64748b;font-size:.82rem;white-space:nowrap; }.metric-value { color:#0f172a;font-size:2rem;font-weight:780;margin-top:.3rem; }
.metric-accent { height:3px;width:34px;border-radius:4px;background:#2563eb;margin-top:.55rem; }
.section-card,.detail-section,.funnel-card,.report-card { background:white;border:1px solid #e5eaf1;border-radius:14px;padding:20px;margin-top:16px;box-shadow:0 3px 14px rgba(15,23,42,.035); }
.candidate-table,.job-table,.risk-table,.schedule-table,.mapping-table { width:100%;border-collapse:collapse;font-size:.86rem; }
.candidate-table th,.job-table th,.risk-table th,.schedule-table th,.mapping-table th { text-align:left;color:#64748b;font-weight:650;padding:12px 10px;border-bottom:1px solid #dfe5ee;background:#f8fafc;white-space:nowrap; }
.candidate-table td,.job-table td,.risk-table td,.schedule-table td,.mapping-table td { color:#334155;padding:13px 10px;border-bottom:1px solid #edf1f6;vertical-align:top; }
.candidate-table tr:hover td { background:#f8fbff; }.candidate-table a,.job-table a { color:#1d4ed8;font-weight:700;text-decoration:none; }
.score { font-weight:800;color:#0f172a; }.badge,.risk-pill { display:inline-block;padding:3px 9px;border-radius:999px;font-size:.75rem;font-weight:700;white-space:nowrap; }
.badge-A,.status-good { background:#dcfce7;color:#166534; }.badge-B,.status-pending { background:#fef3c7;color:#92400e; }.badge-C,.status-bad { background:#fee2e2;color:#991b1b; }.status-pool { background:#e0e7ff;color:#3730a3; }
.detail-hero,.public-jd { background:#fff;border:1px solid #e2e8f0;border-radius:16px;padding:24px 26px;margin:.5rem 0 1rem;box-shadow:0 3px 14px rgba(15,23,42,.045); }
.detail-topline,.mapping-head { display:flex;justify-content:space-between;align-items:flex-start;gap:24px; }.detail-hero h1 { color:#0f172a;font-size:1.8rem;margin:0 0 .25rem; }
.detail-role,.small-muted { color:#64748b;font-size:.9rem; }.info-row { display:flex;gap:24px;flex-wrap:wrap;color:#64748b;font-size:.88rem;margin-top:.85rem;padding-top:.75rem;border-top:1px solid #eef2f7; }
.ai-summary-grid,.diagnosis-grid,.report-grid,.risk-grid { display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px; }.ai-note,.diagnosis-box,.risk-box { background:#f8fafc;border:1px solid #e5eaf1;border-radius:10px;padding:13px 15px; }.ai-note.risk { background:#fffaf0;border-color:#fde7bd; }
.ai-note-label,.diagnosis-title { color:#64748b;font-size:.76rem;font-weight:750;margin-bottom:4px; }.ai-note-text { color:#334155;font-size:.9rem;line-height:1.6; }
.detail-section-title,.funnel-title { color:#0f172a;font-size:1.05rem;font-weight:800;padding-bottom:10px;border-bottom:1px solid #edf1f5;margin-bottom:14px; }
.detail-entry-card { border:1px solid #e7ebf1;border-radius:11px;padding:16px 18px;margin-top:10px;background:#fff; }.detail-entry-head { display:grid;grid-template-columns:145px 1fr;gap:20px;align-items:start; }
.detail-entry-time { color:#2563eb;font-size:.84rem;font-weight:750; }.detail-entry-company { color:#0f172a;font-weight:780; }.detail-entry-body { margin:12px 0 0 165px;color:#3f4b5d;font-size:.9rem;line-height:1.65; }
.education-line { display:grid;grid-template-columns:145px 1.4fr 1fr;gap:20px;padding:12px 4px;border-bottom:1px solid #f0f2f5; }.project-card { border-left:3px solid #2563eb;padding:4px 0 4px 16px;margin:15px 0; }.project-name { color:#0f172a;font-weight:780;margin-bottom:6px; }
.skill-pill,.mapping-tag { display:inline-block;background:#eff6ff;color:#1d4ed8;border:1px solid #dbeafe;padding:5px 10px;margin:3px;border-radius:8px;font-size:.82rem; }
.public-jd-head { padding-bottom:15px;margin-bottom:15px;border-bottom:1px solid #edf1f5; }.public-jd-title { color:#0f172a;font-size:1.35rem;font-weight:780;margin-bottom:7px; }.public-jd-section { margin-top:18px; }.public-jd-section-title { color:#17233a;font-weight:780;margin-bottom:8px; }
.job-status { background:#dcfce7;color:#166534;padding:4px 9px;border-radius:999px;font-size:.76rem;font-weight:700; }.job-version { color:#475569;background:#f1f5f9;border-radius:6px;padding:4px 8px; }
.funnel-row { display:grid;grid-template-columns:130px 1fr 70px 72px;gap:12px;align-items:center;margin:10px 0; }.funnel-track { height:10px;background:#eef2f7;border-radius:999px;overflow:hidden; }.funnel-fill { height:100%;background:linear-gradient(90deg,#2563eb,#60a5fa);border-radius:999px; }.funnel-value { color:#0f172a;font-weight:780;text-align:right; }.funnel-rate { color:#64748b;font-size:.8rem;text-align:right; }
.industry-header { margin-bottom:14px;padding-top:1rem; }.industry-title { color:#0f172a;font-size:1.75rem;font-weight:780; }.report-kpi { background:#fff;border:1px solid #e5eaf1;border-radius:11px;padding:13px 15px;min-height:76px; }.report-kpi-label { color:#64748b;font-size:.78rem; }.report-kpi-value { color:#0f172a;font-size:1.35rem;font-weight:780;margin-top:4px; }
.interview-panel { background:#fff;border:1px solid #e5eaf1;border-radius:13px;padding:18px 20px;margin-top:14px; }.interview-panel-title { color:#0f172a;font-size:1.05rem;font-weight:780;margin-bottom:8px; }.risk-notice { background:#f0f7ff;border:1px solid #bfdbfe;border-left:4px solid #3b82f6;border-radius:11px;padding:14px 16px;color:#294667;line-height:1.6;margin:10px 0 16px; }
.risk-low { background:#e8f5ee;color:#28704b; }.risk-medium { background:#fff4d8;color:#8a6215; }.risk-high { background:#fbe9e7;color:#9b3d36; }.risk-tag { display:inline-block;background:#f1f5f9;color:#475569;border-radius:6px;padding:3px 7px;margin:2px;font-size:.74rem; }
.resume-stage { background:#e9edf3;padding:28px 12px;border-radius:14px;margin-top:14px; }.resume-paper { width:min(900px,96%);margin:0 auto;background:#fff;color:#20242b;padding:48px 56px;box-shadow:0 8px 30px rgba(15,23,42,.13);font-family:'Microsoft YaHei','PingFang SC',sans-serif;line-height:1.65; }.resume-head { display:flex;justify-content:space-between;gap:28px;border-bottom:3px solid #1f3a5f;padding-bottom:18px; }.resume-name { font-size:2.1rem;font-weight:800;color:#17243a; }.resume-section { margin-top:25px; }.resume-section-title { color:#17243a;font-size:1.05rem;font-weight:800;border-bottom:1px solid #aab7c6;padding-bottom:6px;margin-bottom:13px; }
.stButton>button { border-radius:9px;font-weight:650; } @media(max-width:700px){.block-container{padding-top:4.25rem}.ai-summary-grid,.diagnosis-grid,.report-grid,.risk-grid{grid-template-columns:1fr}.detail-entry-head,.education-line{grid-template-columns:1fr;gap:4px}.detail-entry-body{margin-left:0}.funnel-row{grid-template-columns:110px 1fr 45px}.resume-paper{padding:28px 22px}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

PAGES = {"jd_management": "JD管理", "candidate_pool": "候选人池", "recruitment_funnel": "招聘漏斗", "industry_report": "AI行业报告", "interview_scheduling": "面试协调", "resume_risk": "简历风险检测"}
NAV = [("jd_management", "▤", "JD管理"), ("candidate_pool", "▣", "候选人池"), ("recruitment_funnel", "▽", "招聘漏斗"), ("industry_report", "◫", "AI行业报告"), ("interview_scheduling", "▣", "面试协调"), ("resume_risk", "◇", "简历风险检测")]


def esc(value: object) -> str:
    return html.escape(str(value))


def get_state() -> dict:
    if "demo_state" not in st.session_state:
        st.session_state.demo_state = reset_state()
    return st.session_state.demo_state


def page_title(title: str, subtitle: str = "") -> None:
    st.markdown(f'<div class="page-title">{esc(title)}</div><div class="page-subtitle">{esc(subtitle)}</div>', unsafe_allow_html=True)


def metric_cards(values: list[tuple[str, object]]) -> None:
    columns = st.columns(len(values))
    for col, (label, value) in zip(columns, values):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-label">{esc(label)}</div><div class="metric-value">{esc(value)}</div><div class="metric-accent"></div></div>', unsafe_allow_html=True)


def sidebar(active: str) -> None:
    with st.sidebar:
        st.markdown('<div class="brand"><span>◈</span> Recruitment OS</div>', unsafe_allow_html=True)
        st.caption("AI-Recruiter-OS · Dashboard v2")
        st.markdown("---")
        st.markdown("**招聘工作台**")
        links = "".join(f'<a class="{"active" if key == active else ""}" href="?page={key}" target="_self">{icon} {label}</a>' for key, icon, label in NAV)
        st.markdown(f'<div class="side-nav">{links}</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.caption("公开演示：全部为虚构数据；AI结论仅供人工复核")
        if st.button("重置本会话演示数据", use_container_width=True):
            st.session_state.demo_state = reset_state()
            st.query_params.clear()
            st.query_params["page"] = "candidate_pool"
            st.rerun()


def candidate_by_key(state: dict, key: str) -> dict | None:
    return next((x for x in state["candidates"] if x["key"] == key), None)


def candidate_table(items: list[dict]) -> None:
    rows = []
    for item in items:
        key = quote(item["key"], safe="")
        klass = {"推荐面试": "status-good", "进入面试": "status-good", "面试已预约": "status-good", "待HR审核": "status-pending", "待候选人选择时间": "status-pending", "人才库": "status-pool", "淘汰": "status-bad"}.get(item["status"], "status-pending")
        rows.append(f'<tr><td><a href="?page=candidate_detail&candidate={key}" target="_self">{esc(item["name"])}</a></td><td>{esc(item["position"])}</td><td>{item["years"]}年</td><td class="score">{item["score"]}</td><td><span class="badge badge-{item["level"]}">{item["level"]}</span></td><td>{esc(item["recommendation"])}</td><td>{esc(item["ai_summary"])}</td><td><span class="badge {klass}">{esc(item["status"])}</span></td></tr>')
    st.markdown('<div class="section-card" style="overflow-x:auto"><table class="candidate-table"><thead><tr><th>候选人姓名</th><th>应聘岗位</th><th>工作年限</th><th>AI评分</th><th>等级</th><th>AI推荐结果</th><th>AI分析备注</th><th>当前状态</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>', unsafe_allow_html=True)


def candidate_pool(state: dict) -> None:
    page_title("候选人池", "HR每日处理候选人的核心工作台，集中完成检索、筛选、查看与状态决策。")
    candidates = state["candidates"]
    latest = max(x["application_date"] for x in candidates)
    todays = sum(x["application_date"] == latest for x in candidates)
    metric_cards([("当前候选人总数", len(candidates)), ("最新批次新增", todays), ("AI完成筛选", len(candidates)), ("推荐面试", sum(x["level"] == "A" for x in candidates)), ("待HR确认", sum(x["status"] == "待HR审核" for x in candidates)), ("淘汰", sum(x["status"] == "淘汰" for x in candidates))])
    st.markdown("### 候选人列表")
    c1, c2, c3, c4 = st.columns([2.2, 1.3, 1, 1.2])
    search = c1.text_input("搜索候选人", placeholder="输入候选人ID或AI分析内容", label_visibility="collapsed")
    roles = c2.multiselect("岗位", list(ROLES), placeholder="全部岗位", label_visibility="collapsed")
    levels = c3.multiselect("等级", ["A", "B", "C"], placeholder="全部等级", label_visibility="collapsed")
    statuses = c4.multiselect("状态", list(STATUSES), placeholder="全部状态", label_visibility="collapsed")
    results = [x for x in candidates if (not search or search.lower() in (x["name"] + x["ai_summary"]).lower()) and (not roles or x["position"] in roles) and (not levels or x["level"] in levels) and (not statuses or x["status"] in statuses)]
    results.sort(key=lambda x: (-x["score"], x["name"]))
    st.caption(f"共 {len(results)} 名虚构候选人 · 点击演示ID进入简历详情")
    candidate_table(results)


def candidate_detail(state: dict, key: str) -> None:
    item = candidate_by_key(state, key)
    if not item:
        st.warning("未找到该演示候选人")
        return
    resume = item["resume"]
    left, right = st.columns([5, 1])
    with left:
        page_title(f"{item['name']} · 候选人详情", "合成简历样例，仅用于公开 Demo 页面展示")
    with right:
        if st.button("返回候选人池"):
            st.query_params.clear(); st.query_params["page"] = "candidate_pool"; st.rerun()
    st.markdown(f'<div class="detail-hero"><div class="detail-topline"><div><h1>{esc(item["name"])}</h1><div class="detail-role">{esc(item["position"])} · 演示候选人</div></div><div class="score">AI评分 {item["score"]}<br><span class="badge badge-{item["level"]}">等级 {item["level"]}</span></div></div><div class="info-row"><span>工作年限：{item["years"]} 年（模拟）</span><span>城市：{esc(resume["city"])}</span><span>申请批次：{item["application_date"]}</span><span>联系方式：不提供</span></div><div class="ai-summary-grid"><div class="ai-note"><div class="ai-note-label">AI分析摘要（模拟）</div><div class="ai-note-text">{esc(item["ai_summary"])}</div></div><div class="ai-note risk"><div class="ai-note-label">推荐说明</div><div class="ai-note-text">{esc(item["recommendation"])}；请结合结构化面试与人工判断。</div></div></div></div>', unsafe_allow_html=True)
    status = st.selectbox("HR处理状态", list(STATUSES), index=list(STATUSES).index(item["status"]), key=f"candidate_status_{key}")
    if st.button("保存状态（仅本会话）", type="primary"):
        item["status"] = status
        st.success("状态已更新至当前会话。")
    st.markdown('<div class="detail-section"><div class="detail-section-title">教育背景</div>' + "".join(f'<div class="education-line"><span>{esc(x["时间"])}</span><strong>{esc(x["学校"])}</strong><span>{esc(x["专业"])} · {esc(x["学历"])}</span></div>' for x in resume["education"]) + '</div>', unsafe_allow_html=True)
    st.markdown('<div class="detail-section"><div class="detail-section-title">工作经历</div>' + "".join(f'<div class="detail-entry-card"><div class="detail-entry-head"><div class="detail-entry-time">{esc(x["时间"])}</div><div><div class="detail-entry-company">{esc(x["公司"])}</div><div>{esc(x["职位"])}</div></div></div><div class="detail-entry-body">' + "".join(f"<p>{esc(duty)}</p>" for duty in x["职责"]) + '</div></div>' for x in resume["work"]) + '</div>', unsafe_allow_html=True)
    st.markdown('<div class="detail-section"><div class="detail-section-title">项目经历</div>' + "".join(f'<div class="project-card"><div class="project-name">{esc(x["项目名称"])}</div><p>{esc(x["项目背景"])}</p><p>{esc(x["个人职责"])}</p><p>{esc(x["项目成果"])}</p></div>' for x in resume["projects"]) + '</div>', unsafe_allow_html=True)
    st.markdown('<div class="detail-section"><div class="detail-section-title">专业技能与自我评价</div>' + "".join(f'<span class="skill-pill">{esc(skill)}</span>' for skill in resume["technical_skills"] + resume["industry_skills"]) + f'<p>{esc(resume["self_evaluation"])}</p></div>', unsafe_allow_html=True)
    with st.expander("查看模拟PDF简历版式"):
        project_html = "".join(f'<p>{esc(project["项目名称"])}：{esc(project["项目成果"])}</p>' for project in resume["projects"])
        st.markdown(f'<div class="resume-stage"><div class="resume-paper"><div class="resume-head"><div><div class="resume-name">{esc(item["name"])}</div><div>{esc(item["position"])} · 校招演示</div></div><div>虚构样例<br>无联系方式</div></div><div class="resume-section"><div class="resume-section-title">个人简介</div>{esc(resume["self_evaluation"])}</div><div class="resume-section"><div class="resume-section-title">项目经历</div>{project_html}</div></div></div>', unsafe_allow_html=True)


def job_manager(state: dict) -> None:
    page_title("JD管理", "管理岗位从创建、版本迭代到关闭的完整生命周期。所有岗位均为虚构演示数据。")
    jobs = state["jobs"]
    q = st.text_input("搜索岗位", placeholder="输入岗位名称或部门", label_visibility="collapsed")
    jobs = [job for job in jobs if not q or q.lower() in (job["岗位名称"] + job["部门"]).lower()]
    rows = []
    for job in jobs:
        count = sum(x["position"] == job["岗位名称"] for x in state["candidates"])
        rows.append(f'<tr><td><strong>{esc(job["岗位名称"])}</strong></td><td>{esc(job["部门"])}</td><td><span class="job-status">{esc(job["招聘状态"])}</span></td><td>{job["招聘人数"]}人</td><td>{count}人</td><td>{job["创建时间"]}</td><td>{job["最后更新时间"]}</td><td><span class="job-version">V{job["当前版本"]}</span></td></tr>')
    st.markdown('<div class="section-card" style="overflow-x:auto"><table class="job-table"><thead><tr><th>岗位名称</th><th>部门</th><th>状态</th><th>招聘人数</th><th>当前候选人数</th><th>创建时间</th><th>最后更新时间</th><th>JD版本</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>', unsafe_allow_html=True)
    st.markdown("### 岗位详情与生命周期")
    job = st.selectbox("选择演示岗位", state["jobs"], format_func=lambda x: x["岗位名称"], key="job_selected")
    tab_public, tab_internal, tab_history = st.tabs(["外部JD（Public JD）", "内部招聘画像（Internal Hiring Profile）", "版本记录"])
    with tab_public:
        st.markdown(f'<div class="public-jd"><div class="public-jd-head"><div class="public-jd-title">{esc(job["岗位名称"])}</div><div>{esc(job["工作地点"])} · {esc(job["薪资范围"])}</div></div><div class="public-jd-section"><div class="public-jd-section-title">岗位职责</div><p>{esc(job["外部发布JD"])}</p></div><div class="public-jd-section"><div class="public-jd-section-title">任职要求</div><p>{esc(job["学历要求"])} · {esc(job["工作年限"])} · {esc(job["必须技能"])}</p></div><div class="public-jd-section"><div class="public-jd-section-title">加分项 / 福利</div><p>{esc(job["加分技能"])} · {esc(job["福利标签"])}</p></div></div>', unsafe_allow_html=True)
    with tab_internal:
        st.warning("以下仅为虚构的 Demo 内部画像样例，不含企业真实策略。")
        st.write(job["内部HR JD备注"])
    with tab_history:
        for ver in reversed(job["versions"]):
            st.write(f"V{ver['版本']} · {ver['修改时间']} · {ver['修改原因']} · {ver['修改内容摘要']}")
    with st.expander("编辑岗位 / 创建新版本"):
        with st.form(f"edit_job_{job['job_id']}"):
            edit_title = st.text_input("岗位名称（编辑）", value=job["岗位名称"])
            edit_department = st.text_input("部门（编辑）", value=job["部门"])
            edit_location = st.text_input("工作地点（编辑）", value=job["工作地点"])
            edit_jd = st.text_area("外部发布JD（编辑）", value=job["外部发布JD"])
            edit_skills = st.text_area("必须技能（编辑）", value=job["必须技能"])
            edit_note = st.text_area("内部HR JD备注（虚构，仅当前会话）", value=job["内部HR JD备注"])
            reason = st.text_input("修改原因", value="演示岗位信息调整")
            saved = st.form_submit_button("保存并创建版本")
        if saved:
            if not edit_title.strip():
                st.error("岗位名称不能为空。")
            else:
                next_version = f"{int(float(job['当前版本'])) + 1}.0"
                job.update({"岗位名称": edit_title.strip(), "部门": edit_department, "工作地点": edit_location,
                            "外部发布JD": edit_jd, "必须技能": edit_skills, "内部HR JD备注": edit_note,
                            "最后更新时间": date.today().isoformat(), "当前版本": next_version})
                job["versions"].append({"版本": next_version, "修改时间": date.today().isoformat(),
                                        "修改人": "Demo 用户", "修改原因": reason or "岗位信息调整",
                                        "修改内容摘要": "当前会话内更新演示岗位资料"})
                st.success(f"岗位已更新为 V{next_version}（仅当前会话）。")
                st.rerun()
    with st.expander("新建演示岗位"):
        with st.form("new_job_form"):
            title = st.text_input("岗位名称")
            department = st.text_input("部门", "示例团队（虚构）")
            location = st.text_input("工作地点", "远程 / 演示")
            description = st.text_area("外部发布JD")
            requirement = st.text_area("必须技能")
            submitted = st.form_submit_button("新建岗位")
        if submitted:
            if not title.strip():
                st.error("请填写岗位名称")
            else:
                state["jobs"].append({**job.copy(), "job_id": f"DEMO-JOB-{len(state['jobs'])+1:02d}", "岗位名称": title.strip(), "部门": department, "工作地点": location, "外部发布JD": description or "虚构岗位职责演示内容。", "必须技能": requirement or "演示能力要求", "招聘状态": "招聘中", "创建时间": date.today().isoformat(), "最后更新时间": date.today().isoformat(), "当前版本": "1.0", "versions": [{"版本": "1.0", "修改时间": date.today().isoformat(), "修改人": "Demo 用户", "修改原因": "新建演示岗位", "修改内容摘要": "当前会话创建"}]})
                st.rerun()
    c1, c2, c3 = st.columns([1, 1, 3])
    with c1:
        new_status = st.selectbox("招聘状态", ["招聘中", "暂停", "关闭"], index=["招聘中", "暂停", "关闭"].index(job["招聘状态"]), key=f"job_state_{job['job_id']}")
        if st.button("保存岗位状态"):
            job["招聘状态"] = new_status
    with c2:
        if st.button("复制岗位"):
            clone = job.copy(); clone.update({"job_id": f"DEMO-JOB-{len(state['jobs'])+1:02d}", "岗位名称": job["岗位名称"] + "（副本）", "招聘状态": "暂停", "当前版本": "1.0", "versions": [dict(job["versions"][-1])]}); state["jobs"].append(clone); st.rerun()
    with c3:
        st.caption("岗位新建、复制与状态调整仅影响当前访问会话。")


def funnel_page(state: dict) -> None:
    page_title("招聘漏斗", "按岗位查看投递、AI筛选和HR决策转化，快速定位招聘瓶颈。")
    selected = st.selectbox("岗位", ["全部岗位", *ROLES])
    candidates = [x for x in state["candidates"] if selected == "全部岗位" or x["position"] == selected]
    stages = [("投递", len(candidates)), ("AI筛选完成", len(candidates)), ("AI推荐面试", sum(x["level"] == "A" for x in candidates)), ("HR确认进入面试", sum(x["status"] in ("推荐面试", "进入面试", "待候选人选择时间", "面试已预约") for x in candidates)), ("加入人才库", sum(x["status"] == "人才库" for x in candidates)), ("淘汰", sum(x["status"] == "淘汰" for x in candidates))]
    base = max(stages[0][1], 1)
    st.markdown(f'<div class="funnel-card"><div class="funnel-title">{esc(selected)}漏斗汇总</div>' + "".join(f'<div class="funnel-row"><div>{esc(name)}</div><div class="funnel-track"><div class="funnel-fill" style="width:{min(100, value/base*100):.1f}%"></div></div><div class="funnel-value">{value}人</div><div class="funnel-rate">{value/base*100:.1f}%</div></div>' for name, value in stages) + '</div>', unsafe_allow_html=True)
    recommends = stages[2][1] / base
    diagnosis = "AI推荐面试率偏低，可复核岗位要求和演示画像。" if recommends < .2 else "当前演示漏斗无明显异常，建议持续复盘各环节转化。"
    st.markdown(f'<div class="diagnosis-grid"><div class="diagnosis-box"><div class="diagnosis-title">问题诊断</div><p>{diagnosis}</p><p>所有计数均来自本页面虚构候选人样例。</p></div><div class="diagnosis-box"><div class="diagnosis-title">优化建议</div><p>统一岗位评价标准；将自动评分作为辅助信息，并由招聘人员复核。</p></div></div>', unsafe_allow_html=True)


def industry_page(state: dict) -> None:
    page_title("AI行业报告", "本地静态虚构行业观察与人才 Mapping 展示；不连接外部 AI 或市场数据服务。")
    role = st.selectbox("报告岗位", list(ROLES))
    st.markdown(f'<div class="industry-header"><div class="industry-title">{esc(role)}人才市场分析</div><div class="industry-subtitle">模拟报告 · 2026秋季校招（虚构样例）</div></div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for col, label, value in zip(cols, ["模拟需求指数", "样例岗位数", "技能关注度", "市场样本"], ["上行（示意）", "20 个合成候选人", "项目与实践", "虚构样例"]):
        with col:
            st.markdown(f'<div class="report-kpi"><div class="report-kpi-label">{esc(label)}</div><div class="report-kpi-value">{esc(value)}</div></div>', unsafe_allow_html=True)
    st.warning("报告中的观点与数字均为合成演示内容，不代表真实市场统计。")
    cards = [("行业近期变化", "演示观察：岗位能力描述逐步强调可验证的项目经验与协作过程。"), ("关键技术与业务趋势", "产品方向关注问题定义与AI能力边界；技术方向重视评估与可复现性。"), ("对人才需求的影响", "建议结合结构化面试核对候选人的个人贡献、方法和结果。"), ("未来30天招聘策略", "统一岗位画像、复盘漏斗转化、持续校准评价维度。")]
    st.markdown('<div class="report-grid">' + "".join(f'<div class="report-card"><div class="report-card-title">{esc(title)}</div><p>{esc(text)}</p></div>' for title, text in cards) + '</div>', unsafe_allow_html=True)
    st.markdown("### 目标公司 Mapping 方向（模拟）")
    mapping = [{"优先级": "P1", "公司": "示例科技甲（虚构）", "部门": "AI应用团队", "匹配依据": "能力方向匹配示例"}, {"优先级": "P2", "公司": "示例创新乙（虚构）", "部门": "数据产品团队", "匹配依据": "项目场景相近示例"}, {"优先级": "WATCH", "公司": "示例实验室丙（虚构）", "部门": "工程实践组", "匹配依据": "技能方向参考示例"}]
    st.markdown('<div class="mapping-table-wrap"><table class="mapping-table"><thead><tr><th>优先级</th><th>目标公司</th><th>目标部门</th><th>Mapping依据</th></tr></thead><tbody>' + "".join(f'<tr><td>{x["优先级"]}</td><td>{x["公司"]}</td><td>{x["部门"]}</td><td>{x["匹配依据"]}</td></tr>' for x in mapping) + '</tbody></table></div>', unsafe_allow_html=True)
    st.info("企业名称、部门与匹配理由均为虚构，不包含原项目映射资料。")


def risk_score(candidate: dict) -> int:
    number = int(candidate["key"].rsplit("-", 1)[1])
    return (number * 17 % 55) + 25


def risk_page(state: dict, candidate_key: str = "") -> None:
    if candidate_key:
        candidate = candidate_by_key(state, candidate_key)
        if candidate:
            score = risk_score(candidate)
            level = "高风险" if score >= 65 else "中风险" if score >= 45 else "低风险"
            page_title(f"{candidate['name']} · 简历风险详情", f"{candidate['position']} · 风险提示仅供人工复核")
            st.markdown('<div class="risk-notice"><strong>人工复核提示</strong><br>合成风险分仅用于演示UI，不表示简历存在真实性问题，不能作为淘汰依据。</div>', unsafe_allow_html=True)
            metric_cards([("AI评分", candidate["score"]), ("简历风险分（模拟）", score), ("风险等级", level)])
            for title, desc in [("AI润色痕迹", "演示算法提示：建议通过结构化提问了解项目过程。"), ("项目真实性", "样例维度用于展示风险详情布局，不对应真实个人。"), ("数据成果可信度", "此模块只显示合成说明，不读取或校验真实简历。")]:
                st.markdown(f'<div class="detail-section"><div class="detail-section-title">{title} · {score}/100（模拟）</div><p>{desc}</p><p>HR复核建议：要求候选人解释背景、职责边界、方法与结果。</p></div>', unsafe_allow_html=True)
            st.markdown("### HR复核问题")
            st.write("1. 请说明演示项目中的个人职责和协作边界。\n2. 如何验证项目结果？\n3. 哪些环节有待改进？")
            status = st.selectbox("复核状态", ["未复核", "已复核", "需进一步确认"], key=f"risk_review_{candidate_key}")
            if st.button("保存复核状态（本会话）"):
                state["risk_reviews"][candidate_key] = status
                st.success("已更新当前会话的演示复核状态")
            if st.button("返回风险列表"):
                st.query_params.clear(); st.query_params["page"] = "resume_risk"; st.rerun()
            return
    page_title("简历风险检测", "辅助HR复核文本风险信号；所有简历及评分均为合成演示数据。")
    st.markdown('<div class="risk-notice"><strong>人工复核提示</strong><br>风险分仅作演示说明，不能作为淘汰依据。所有候选人、简历和分析均为虚构样例。</div>', unsafe_allow_html=True)
    candidates = state["candidates"]
    scores = [risk_score(x) for x in candidates]
    high = sum(x >= 65 for x in scores); medium = sum(45 <= x < 65 for x in scores); low = len(scores)-high-medium
    metric_cards([("已检测简历数", len(candidates)), ("高风险样例", high), ("中风险样例", medium), ("低风险样例", low), ("高匹配且需复核", sum(x["score"] >= 85 and risk_score(x) >= 55 for x in candidates))])
    f1, f2, f3 = st.columns(3)
    search = f1.text_input("输入候选人姓名", placeholder="输入演示ID")
    roles = f2.multiselect("岗位筛选", list(ROLES), placeholder="全部岗位")
    risk_filter = f3.selectbox("风险等级筛选", ["全部风险", "高风险", "中风险", "低风险"])
    filtered = [x for x in candidates if (not search or search.lower() in x["key"].lower()) and (not roles or x["position"] in roles)]
    if risk_filter != "全部风险":
        filtered = [x for x in filtered if ("高风险" if risk_score(x) >= 65 else "中风险" if risk_score(x) >= 45 else "低风险") == risk_filter]
    rows = []
    for x in filtered:
        score = risk_score(x); level = "高风险" if score >= 65 else "中风险" if score >= 45 else "低风险"; klass = level.replace("风险", "")
        key = quote(x["key"], safe="")
        rows.append(f'<tr><td>{x["name"]}</td><td>{x["position"]}</td><td>{x["score"]}</td><td>{x["level"]}</td><td><strong>{score}</strong></td><td><span class="risk-pill risk-{klass}">{level}</span></td><td>{"重点复核" if x["score"] >= 85 and score >= 55 else "—"}</td><td>项目细节 · 数据口径</td><td>{x["status"]}</td><td><a href="?page=resume_risk&candidate={key}">查看风险详情</a></td></tr>')
    st.caption(f"共 {len(filtered)} 份合成简历检测结果")
    st.markdown('<div class="section-card" style="overflow-x:auto"><table class="risk-table"><thead><tr><th>候选人姓名</th><th>应聘岗位</th><th>AI评分</th><th>AI等级</th><th>风险分</th><th>风险等级</th><th>重点复核</th><th>主要风险标签</th><th>当前状态</th><th>操作</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>', unsafe_allow_html=True)


def interview_page(state: dict) -> None:
    page_title("面试协调", "灵活发起邀约，准备HR初面问题，并跟踪候选人预约状态。安全模拟，不发送真实消息。")
    candidates = state["candidates"]
    pending = sum(x["status"] in ("推荐面试", "进入面试") for x in candidates)
    waiting = sum(x["status"] == "待候选人选择时间" for x in state["interviews"])
    metric_cards([("待安排候选人", pending), ("待候选人选时", waiting), ("已预约面试", sum(x["status"] == "已预约（模拟）" for x in state["interviews"]))])
    tab1, tab2, tab3 = st.tabs(["发起面试协调", "生成HR面试问题", "面试安排列表"])
    with tab1:
        with st.container(border=True):
            st.markdown('<div class="interview-panel-title">创建邀约草稿（模拟）</div>', unsafe_allow_html=True)
            choices = [x for x in candidates if x["status"] in ("推荐面试", "进入面试")] or candidates
            selected = st.selectbox("候选人", choices, format_func=lambda x: f'{x["name"]} · {x["position"]} · {x["status"]}', key="interview_candidate")
            col1, col2 = st.columns(2)
            with col1:
                round_name = st.selectbox("面试轮次", ["第一轮面试", "第二轮面试", "终面", "HR面"])
                duration = st.selectbox("面试时长", [30, 45, 60, 90], index=2)
                interviewer = st.selectbox("面试官角色（模拟）", ["用人团队代表", "招聘伙伴", "技术面试官"])
            with col2:
                day = st.date_input("意向日期", value=date.today() + timedelta(days=3))
                time_slot = st.selectbox("建议时段", ["10:00–11:00", "14:00–15:00", "16:00–17:00"])
                mode = st.selectbox("面试方式", ["线上会议（模拟）", "线下面试（模拟）", "电话面试（模拟）"])
            if st.button("查询模拟日历并生成邀约", type="primary"):
                state["interviews"].append({"candidate": selected["key"], "name": selected["name"], "position": selected["position"], "round": round_name, "duration": duration, "interviewer": interviewer, "when": f"{day.isoformat()} {time_slot}", "mode": mode, "status": "草稿", "email_draft": f"主题：{selected['name']} · {selected['position']}（演示草稿）\n\n您好，\n\n此为虚构演示邀约，不会发送。建议时间：{day.isoformat()} {time_slot}。\n\nRecruitment OS Demo"})
                st.success("已创建仅当前会话可见的模拟邀约草稿。")
        drafts = [x for x in state["interviews"] if x["status"] == "草稿"]
        for draft in drafts:
            st.markdown('<div class="interview-panel"><div class="interview-panel-title">邀约预览 · 模拟</div></div>', unsafe_allow_html=True)
            st.code(draft["email_draft"])
            a, b = st.columns(2)
            if a.button("模拟发送邀约", key=f"send_{draft['candidate']}"):
                draft["status"] = "待候选人选择时间"
                cand = candidate_by_key(state, draft["candidate"])
                if cand: cand["status"] = "待候选人选择时间"
                st.success("模拟发送已完成；未发送邮件或消息。")
                st.rerun()
            if b.button("移除草稿", key=f"remove_{draft['candidate']}"):
                state["interviews"].remove(draft); st.rerun()
        waiting_items = [x for x in state["interviews"] if x["status"] == "待候选人选择时间"]
        if waiting_items:
            req = st.selectbox("待确认安排", waiting_items, format_func=lambda x: f"{x['name']} · {x['round']}")
            if st.button("模拟候选人确认时间"):
                req["status"] = "已预约（模拟）"
                cand = candidate_by_key(state, req["candidate"])
                if cand: cand["status"] = "面试已预约"
                st.rerun()
    with tab2:
        qs = st.multiselect("HR问题类型", ["求职动机", "项目经历核实", "工作经历核实", "团队协作", "岗位技能", "简历疑点追问", "职业规划"], default=["求职动机", "项目经历核实", "岗位技能"])
        candidate = st.selectbox("问题生成演示候选人", candidates, format_func=lambda x: f'{x["name"]} · {x["position"]}', key="question_candidate")
        if st.button("生成HR面试问题", type="primary"):
            state["questions"] = [f"请介绍一个与{candidate['position']}相关的项目，并说明你的具体贡献？", "遇到最重要的取舍或困难是什么？你如何处理？", "如何验证项目结果和数据口径？", "回顾这个项目，你会如何改进？"]
            state["question_candidate_name"] = candidate["name"]
        if state["questions"]:
            st.markdown(f"### {state.get('question_candidate_name', '演示候选人')} · 问题草稿")
            for index, question in enumerate(state["questions"], 1): st.write(f"{index}. {question}")
            st.download_button("下载Markdown（本地生成）", "\n".join(f"{i}. {q}" for i, q in enumerate(state["questions"], 1)), file_name="demo_interview_questions.md", mime="text/markdown")
    with tab3:
        if state["interviews"]:
            st.dataframe([{k: x[k] for k in ("name", "position", "round", "interviewer", "when", "mode", "status")} for x in state["interviews"]], use_container_width=True, hide_index=True)
        else:
            st.info("当前会话暂无模拟面试安排。")
        st.caption("不读取真实日历，不创建真实会议，不发送邮件、飞书消息或招聘平台通知。")


def main() -> None:
    state = get_state()
    page = st.query_params.get("page", "candidate_pool")
    if page not in {*PAGES.keys(), "candidate_detail"}: page = "candidate_pool"
    sidebar(page if page in PAGES else "candidate_pool")
    st.markdown('<div class="risk-notice" style="margin-top:0"><strong>安全演示模式</strong> · 60份简历、岗位、报告及评分均为自动生成的虚构样例；没有联系方式或真实企业资料。操作仅保存在当前会话，不发送外部消息。</div>', unsafe_allow_html=True)
    if page == "candidate_pool": candidate_pool(state)
    elif page == "candidate_detail": candidate_detail(state, st.query_params.get("candidate", ""))
    elif page == "jd_management": job_manager(state)
    elif page == "recruitment_funnel": funnel_page(state)
    elif page == "industry_report": industry_page(state)
    elif page == "interview_scheduling": interview_page(state)
    elif page == "resume_risk": risk_page(state, st.query_params.get("candidate", ""))
    st.divider()
    st.caption("Recruitment OS Original-style Public Demo · Synthetic data only · Session-local · No external integrations")


if __name__ == "__main__":
    main()
