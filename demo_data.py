"""Deterministic, wholly fictional fixtures for the original-style public demo."""
from __future__ import annotations

from copy import deepcopy
from typing import Any

ROLES = ("AI产品经理", "AI算法工程师", "企业销售经理")
STATUSES = ("待HR审核", "推荐面试", "进入面试", "待候选人选择时间", "面试已预约", "人才库", "淘汰")


def _resume(candidate_id: str, role: str, years: int, index: int) -> dict[str, Any]:
    role_skills = {
        ROLES[0]: ["需求分析", "产品规划", "用户研究", "AI应用评估"],
        ROLES[1]: ["Python", "模型评测", "数据处理", "实验复现"],
        ROLES[2]: ["客户研究", "方案沟通", "销售流程", "数据复盘"],
    }[role]
    return {
        "name": candidate_id,
        "phone": "未提供（虚构样例）",
        "email": "未提供（虚构样例）",
        "city": ("上海", "杭州", "北京", "成都")[index % 4],
        "target_position": role,
        "education": [{"时间": "2022.09—2026.06", "学校": "示例大学", "专业": ("信息管理", "计算机科学", "工商管理")[index % 3], "学历": "本科（虚构）"}],
        "work": [{"时间": f"{2025-years}.07—2026.06", "公司": "示例科技（虚构）", "职位": f"{role}项目实践", "职责": [f"在模拟项目中参与{role_skills[index % len(role_skills)]}相关工作。", "依据虚构样例数据记录过程与复盘结论。"]}],
        "projects": [{"项目名称": f"校招演示项目 {index:02d}", "项目背景": "完全虚构的课程与项目练习，不对应真实企业或客户。", "个人职责": f"练习{role_skills[index % len(role_skills)]}及跨职能协作。", "项目成果": "形成可复现的演示原型与复盘文档（合成样例）。"}],
        "technical_skills": role_skills[:3],
        "industry_skills": ["结构化表达", "团队协作"],
        "self_evaluation": "虚构演示画像，仅用于展示页面，不代表真实求职者。",
        "raw_markdown": f"# {candidate_id}\n\n> 全部内容为虚构演示样例，不包含个人联系方式。\n\n## 基本信息\n- 姓名：{candidate_id}\n- 手机号：未提供\n- 邮箱：未提供\n- 城市：{('上海', '杭州', '北京', '成都')[index % 4]}\n- 求职意向：{role}\n\n## 教育背景\n### 2022.09—2026.06\n- 学校：示例大学（虚构）\n- 专业：{('信息管理', '计算机科学', '工商管理')[index % 3]}｜本科\n\n## 工作经历\n### {2025-years}.07—2026.06\n**示例科技（虚构）｜{role}项目实践**\n工作职责：\n- 参与{role_skills[index % len(role_skills)]}相关演示练习。\n- 依据虚构样例数据完成过程记录与复盘。\n\n## 项目经历\n### 校招演示项目 {index:02d}\n- 项目背景：完全虚构的课程与项目练习。\n- 个人职责：练习{role_skills[index % len(role_skills)]}与跨职能协作。\n- 项目成果：形成可复现的演示原型与复盘文档。\n\n## 专业技能\n" + "".join(f"- {skill}\n" for skill in role_skills),
    }


def initial_state() -> dict[str, Any]:
    candidates = []
    # Fixed per-role counts preserve the original display scale without reusing its records.
    for role_index, role in enumerate(ROLES):
        for local_index in range(20):
            number = role_index * 20 + local_index + 1
            candidate_id = f"DEMO-{number:03d}"
            if number == 21:
                score, level, status = 95, "A", "推荐面试"
            elif number <= 38:
                score, level, status = 70 + ((number * 13) % 20), "B", "待HR审核"
            else:
                score, level, status = 60 + ((number * 7) % 10), "C", "淘汰"
            years = (local_index % 5) + 1
            resume = _resume(candidate_id, role, years, number)
            candidates.append({
                "key": candidate_id, "name": candidate_id, "position": role, "years": years,
                "score": score, "level": level,
                "recommendation": {"A": "推荐面试", "B": "待人工复核", "C": "暂不推荐"}[level],
                "ai_summary": f"虚构画像：具备{resume['technical_skills'][0]}相关项目练习；建议核实问题拆解、个人贡献与复盘过程。",
                "status": status, "application_date": "2026-11-03",
                "resume": resume,
            })
    jobs = []
    for index, role in enumerate(ROLES):
        jobs.append({
            "job_id": f"DEMO-JOB-{index+1:02d}", "岗位名称": role, "部门": f"示例团队{index+1}（虚构）",
            "工作地点": ("上海", "杭州", "北京")[index], "岗位类型": "全职", "招聘人数": [2, 3, 2][index],
            "招聘状态": "招聘中", "创建时间": "2026-08-01", "最后更新时间": "2026-08-01", "当前版本": "1.0",
            "薪资范围": "演示数据，不代表真实薪酬", "奖金": "演示福利", "股票期权": "未设置（演示）", "福利标签": "演示福利",
            "学历要求": "本科及以上（演示）", "工作年限": "应届或项目经验（演示）", "年龄要求": "不限",
            "必须技能": "岗位相关基础能力与沟通协作", "加分技能": "项目实践与复盘能力", "行业背景": "虚构示例场景",
            "外部发布JD": f"参与{role}相关产品或业务项目；与团队协作完成需求、方案和复盘。此岗位描述为虚构演示内容。",
            "内部HR JD备注": "虚构的内部画像示例，仅用于界面演示。",
            "versions": [{"版本": "1.0", "修改时间": "2026-08-01", "创建时间": "2026-08-01", "修改人": "Demo 用户", "修改原因": "虚构岗位初始化", "修改内容摘要": "生成公开演示用岗位数据"}],
        })
    return {"candidates": candidates, "jobs": jobs, "interviews": [], "questions": [], "risk_reviews": {}, "risk_reports": []}


def reset_state() -> dict[str, Any]:
    return deepcopy(initial_state())
