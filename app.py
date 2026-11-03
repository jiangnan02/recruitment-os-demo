from __future__ import annotations

from datetime import date, timedelta

import streamlit as st

from demo_data import funnel_counts, reset_state

st.set_page_config(page_title="Recruitment OS · Public Demo", page_icon="◈", layout="wide")
st.markdown("""
<style>
:root { color-scheme: light; }
.stApp { background: #f5f7fb; }
[data-testid="stSidebar"] { background: #101827; }
[data-testid="stSidebar"] * { color: #e5e7eb; }
.block-container { max-width: 1440px; padding-top: 2rem; padding-bottom: 3rem; }
.demo-banner { padding: .8rem 1rem; border: 1px solid #bfdbfe; border-radius: 12px; background: #eff6ff; color: #1e3a8a; margin: .4rem 0 1.1rem; }
.hero { padding: 1.5rem 1.6rem; border-radius: 18px; color: white; background: linear-gradient(120deg,#111827,#1d4ed8); margin: .6rem 0 1.2rem; }
.hero h1 { color: white; margin: 0 0 .35rem; font-size: 2rem; }
.hero p { color: #dbeafe; margin: 0; }
.metric { background:white; border:1px solid #e6ebf2; border-radius:14px; padding:16px; min-height:100px; }
.metric-label { color:#64748b; font-size:.84rem; }
.metric-value { color:#0f172a; font-size:1.75rem; font-weight:800; margin-top:.3rem; }
.small-note { color:#64748b; font-size:.86rem; }
</style>
""", unsafe_allow_html=True)

if "demo_state" not in st.session_state:
    st.session_state.demo_state = reset_state()

state = st.session_state.demo_state
with st.sidebar:
    st.markdown("<div class='hero'><h1>Recruitment OS</h1><p>校招招聘流程 · 公开演示版</p></div>", unsafe_allow_html=True)
    page = st.radio("演示模块", ["总览", "JD 管理", "候选人池", "招聘漏斗", "AI 行业报告", "面试协调"], label_visibility="collapsed")
    st.divider()
    st.caption("数据仅存于当前浏览器会话")
    if st.button("重置本会话演示", use_container_width=True):
        st.session_state.demo_state = reset_state()
        st.rerun()

st.markdown("<div class='demo-banner'><b>安全演示模式</b> · 所有资料均为虚构示例；不会读取或修改原项目文件，也不会发送邮件、飞书消息或平台请求。交互数据只保存在当前会话，关闭会话后不保证保留。</div>", unsafe_allow_html=True)
st.title(page)


def metric(label: str, value: str | int) -> None:
    st.markdown(f"<div class='metric'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div></div>", unsafe_allow_html=True)


if page == "总览":
    candidates = state["candidates"]
    counts = funnel_counts(candidates)
    st.markdown("<div class='hero'><h1>从岗位到面试，一站式招聘工作台</h1><p>浏览虚构校招候选人、岗位与流程数据，体验安全的模拟招聘操作。</p></div>", unsafe_allow_html=True)
    cols = st.columns(4)
    for col, label, value in zip(cols, ["演示岗位", "候选人样例", "进行中岗位", "面试安排"], [len(state["jobs"]), len(candidates), sum(j["status"] == "招聘中" for j in state["jobs"]), len(state["interviews"]) ]):
        with col:
            metric(label, value)
    st.subheader("招聘流程概览")
    cols = st.columns(len(counts))
    for col, (stage, count) in zip(cols, counts.items()):
        with col:
            metric(stage, count)
    st.info("选择左侧模块查看 JD、候选人样例、漏斗分析、虚构行业报告及模拟面试协调。")

elif page == "JD 管理":
    st.caption("岗位变更仅影响当前会话，页面不连接招聘平台。")
    with st.expander("新增演示岗位", expanded=False):
        with st.form("add_job_form"):
            title = st.text_input("岗位名称", placeholder="例如：数据产品实习生（演示岗位）")
            department = st.text_input("团队", value="示例团队")
            location = st.text_input("工作地点", value="远程")
            summary = st.text_area("岗位职责摘要")
            requirements = st.text_area("任职要求摘要")
            headcount = st.number_input("招聘人数", min_value=1, max_value=20, value=1)
            submitted = st.form_submit_button("添加到本会话")
        if submitted:
            if not title.strip():
                st.error("请填写岗位名称。")
            elif any(job["title"] == title.strip() for job in state["jobs"]):
                st.warning("该演示岗位已存在。")
            else:
                state["jobs"].append({"title": title.strip(), "department": department, "location": location, "headcount": int(headcount), "status": "招聘中", "summary": summary or "演示岗位职责摘要。", "requirements": requirements or "演示岗位要求摘要。"})
                st.success("岗位已添加到当前会话。")
                st.rerun()
    for index, job in enumerate(state["jobs"]):
        with st.container(border=True):
            left, right = st.columns([4, 1])
            with left:
                st.subheader(job["title"])
                st.caption(f"{job['department']} · {job['location']} · {job['headcount']} 人 · {job['status']}")
                st.write(job["summary"])
                st.write("**任职要求：** " + job["requirements"])
            with right:
                new_status = st.selectbox("招聘状态", ["招聘中", "暂停", "关闭"], index=["招聘中", "暂停", "关闭"].index(job["status"]), key=f"job_status_{index}")
                job["status"] = new_status

elif page == "候选人池":
    candidates = state["candidates"]
    all_roles = ["全部岗位"] + sorted({item["role"] for item in candidates})
    col1, col2 = st.columns([2, 1])
    with col1:
        role_filter = st.selectbox("目标岗位", all_roles)
    with col2:
        minimum_score = st.slider("最低匹配分", 0, 100, 0)
    shown = [item for item in candidates if (role_filter == "全部岗位" or item["role"] == role_filter) and item["score"] >= minimum_score]
    st.caption(f"显示 {len(shown)} 位虚构候选人。演示 ID 不对应真实个人，也不包含个人联系方式。")
    for candidate in shown:
        with st.container(border=True):
            top, score_col = st.columns([5, 1])
            with top:
                st.subheader(f"{candidate['id']}  ·  {candidate['role']}")
                st.caption(f"{candidate['experience']} · 流程阶段：{candidate['stage']}")
            with score_col:
                metric("模拟匹配分", candidate["score"])
            st.write(candidate["summary"])
            st.write("**能力标签：** " + " · ".join(candidate["skills"]))
            stages = ["待初筛", "面试中", "已录用（模拟）", "人才库"]
            candidate["stage"] = st.selectbox("更新演示阶段", stages, index=stages.index(candidate["stage"]), key=f"candidate_stage_{candidate['id']}")

elif page == "招聘漏斗":
    counts = funnel_counts(state["candidates"])
    total = max(1, len(state["candidates"]))
    st.caption("仅展示虚构样例数据；阶段调整只作用于你的当前会话。")
    for index, (stage, count) in enumerate(counts.items()):
        left, bar, number, ratio = st.columns([1.5, 5, 1, 1])
        with left:
            st.write(stage)
        with bar:
            st.progress(count / total)
        with number:
            st.write(f"**{count}**")
        with ratio:
            st.write(f"{count / total:.0%}")
        if index < len(counts) - 1:
            next_count = list(counts.values())[index + 1]
            st.caption(f"本阶段至下一阶段转化率：{next_count / count:.0%}" if count else "本阶段暂无样例")
    st.info("漏斗诊断（演示）：可进一步关注初筛反馈的一致性，并按岗位复盘面试阶段的转化情况。")

elif page == "AI 行业报告":
    st.caption("本页是静态虚构行业观察样例，不代表真实市场数据，也未连接外部 AI 服务。")
    st.subheader("生成式 AI 应用岗位 · 校招趋势观察")
    st.markdown("**样例周期：** 2026 年秋季校招（模拟）　　**样例范围：** 虚构岗位样本")
    st.warning("以下趋势、比例与建议均为演示用合成内容，不应用于真实招聘决策。")
    a, b, c = st.columns(3)
    for col, label, value in zip([a, b, c], ["样例岗位需求指数", "跨学科标签占比", "实践项目关注度"], ["↑ 12%", "约 46%", "较高"]):
        with col:
            metric(label, value)
    st.markdown("#### 演示观察")
    st.markdown("- **产品方向：** 更关注问题定义、用户验证与 AI 能力边界意识。\n- **技术方向：** 项目复现、实验设计与可靠评估是常见的演示能力标签。\n- **协作方式：** 产品、工程与运营的跨学科协同在样例场景中持续出现。")
    st.markdown("#### 演示建议")
    st.success("为校招岗位统一能力评价维度；结合结构化面试与人工判断，避免仅凭自动评分作出决定。")

elif page == "面试协调":
    st.caption("全流程为本地模拟：不创建真实日历事件，不发送通知、不生成可用预约链接。")
    candidate_options = [item["id"] for item in state["candidates"]]
    job_options = [job["title"] for job in state["jobs"]]
    with st.form("interview_form"):
        candidate_id = st.selectbox("演示候选人", candidate_options)
        job_title = st.selectbox("演示岗位", job_options)
        interviewer = st.selectbox("模拟面试官角色", ["用人团队代表（模拟）", "招聘伙伴（模拟）", "技术面试官（模拟）"])
        interview_day = st.date_input("意向日期", value=date.today() + timedelta(days=3))
        slot = st.selectbox("模拟时段", ["10:00–10:45", "14:00–14:45", "16:00–16:45"])
        submitted = st.form_submit_button("创建模拟安排")
    if submitted:
        state["interviews"].append({"candidate": candidate_id, "job": job_title, "interviewer": interviewer, "when": f"{interview_day.isoformat()} {slot}", "status": "待确认（模拟）"})
        st.success("模拟安排已加入当前会话；没有发送任何消息或调用外部服务。")
    if state["interviews"]:
        st.subheader("本会话模拟安排")
        st.dataframe(state["interviews"], use_container_width=True, hide_index=True)
    else:
        st.info("尚无安排。提交上方表单可创建一条仅对当前会话可见的模拟安排。")

st.divider()
st.caption("Recruitment OS Public Demo · Synthetic data only · No external integrations · Session-local state")
