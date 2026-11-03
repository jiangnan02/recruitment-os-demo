"""Synthetic, session-local sample data for the public Recruitment OS demo."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


def initial_state() -> dict[str, Any]:
    """Return a fresh, entirely fictional demo dataset."""
    return {
        "jobs": [
            {
                "title": "AI 产品经理（演示岗位）",
                "department": "示例产品组",
                "location": "上海 / 远程",
                "headcount": 2,
                "status": "招聘中",
                "summary": "规划 AI 助手体验，协同设计、研发与数据团队交付产品。",
                "requirements": "产品方案设计、需求分析、跨团队协作；了解生成式 AI 应用。",
            },
            {
                "title": "机器学习工程师（演示岗位）",
                "department": "示例技术组",
                "location": "杭州 / 远程",
                "headcount": 1,
                "status": "招聘中",
                "summary": "参与模型应用与评估工具建设，推动原型走向稳定服务。",
                "requirements": "熟悉 Python 与机器学习基础；具备实验复现和工程协作意识。",
            },
            {
                "title": "商业运营分析师（演示岗位）",
                "department": "示例运营组",
                "location": "北京 / 远程",
                "headcount": 1,
                "status": "暂停",
                "summary": "用数据分析支持虚构示例产品的运营策略与效果复盘。",
                "requirements": "具备数据分析、结构化表达和项目协作能力。",
            },
        ],
        "candidates": [
            {"id": "DEMO-001", "role": "AI 产品经理（演示岗位）", "score": 92, "experience": "应届 / 项目实践", "stage": "待初筛", "summary": "虚构画像：完成过智能问答原型，能描述用户研究与迭代过程。", "skills": ["产品设计", "用户研究", "AI 应用"]},
            {"id": "DEMO-002", "role": "AI 产品经理（演示岗位）", "score": 86, "experience": "应届 / 校园项目", "stage": "待初筛", "summary": "虚构画像：参与校园信息助手项目，关注可用性与指标定义。", "skills": ["需求分析", "原型设计", "数据意识"]},
            {"id": "DEMO-003", "role": "机器学习工程师（演示岗位）", "score": 94, "experience": "应届 / 研究项目", "stage": "面试中", "summary": "虚构画像：实现过小型文本分类实验，重视评估与可复现性。", "skills": ["Python", "模型评估", "实验设计"]},
            {"id": "DEMO-004", "role": "机器学习工程师（演示岗位）", "score": 81, "experience": "应届 / 开源练习", "stage": "待初筛", "summary": "虚构画像：熟悉基础训练流程，正在积累部署和监控经验。", "skills": ["Python", "机器学习", "工程基础"]},
            {"id": "DEMO-005", "role": "商业运营分析师（演示岗位）", "score": 78, "experience": "应届 / 课程项目", "stage": "人才库", "summary": "虚构画像：通过课程案例分析用户转化，表达清晰、重视验证。", "skills": ["SQL", "分析表达", "运营研究"]},
            {"id": "DEMO-006", "role": "AI 产品经理（演示岗位）", "score": 73, "experience": "应届 / 社团实践", "stage": "待初筛", "summary": "虚构画像：组织过团队协作项目，具备初步需求梳理经验。", "skills": ["协作", "需求梳理", "文档"]},
            {"id": "DEMO-007", "role": "机器学习工程师（演示岗位）", "score": 89, "experience": "应届 / 毕设项目", "stage": "已录用（模拟）", "summary": "虚构画像：比较过多种基线方法，能解释实验结论和局限。", "skills": ["Python", "机器学习", "技术表达"]},
            {"id": "DEMO-008", "role": "商业运营分析师（演示岗位）", "score": 84, "experience": "应届 / 校园实践", "stage": "待初筛", "summary": "虚构画像：参与活动复盘，擅长将观察转成可检验的问题。", "skills": ["数据分析", "项目协作", "结构化思考"]},
        ],
        "interviews": [],
    }


def reset_state() -> dict[str, Any]:
    """Return a new session state without mutating any shared data."""
    return deepcopy(initial_state())


def funnel_counts(candidates: list[dict[str, Any]]) -> dict[str, int]:
    stages = ("待初筛", "面试中", "已录用（模拟）", "人才库")
    return {stage: sum(item["stage"] == stage for item in candidates) for stage in stages}
