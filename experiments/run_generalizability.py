"""泛化性测试：3 个不同领域的需求"""
import json
import httpx
import time

BASE_URL = "http://127.0.0.1:8000"

DOMAINS = {
    "finance": """银行转账系统

功能需求:
R1. 转账金额:
   - 单笔转账金额范围: 0.01-500000.00 元
   - 每日累计转账上限: 1000000.00 元
   - 每日转账笔数上限: 50 笔

R2. 手续费计算:
   - 同行转账: 免手续费
   - 跨行转账金额 <= 5000 元: 手续费 2 元/笔
   - 跨行转账金额 5000-50000 元: 手续费 5 元/笔
   - 跨行转账金额 > 50000 元: 手续费 10 元/笔

R3. 账户余额:
   - 转账后账户余额不能为负数
   - 余额不足时拒绝转账并提示

R4. 收款账号验证:
   - 账号为 16-19 位纯数字
   - 收款账号不能与转出账号相同""",

    "education": """学生成绩管理系统

功能需求:
R1. 成绩录入:
   - 分数范围: 0-100 分（整数）
   - 每门课程只能录入一次成绩，重复录入需先删除原成绩
   - 支持批量录入，每批最多 200 条

R2. GPA 计算:
   - A: 90-100 分, 绩点 4.0
   - B: 80-89 分, 绩点 3.0
   - C: 70-79 分, 绩点 2.0
   - D: 60-69 分, 绩点 1.0
   - F: 0-59 分, 绩点 0.0
   - GPA = 所有课程绩点的加权平均（按学分加权）

R3. 学分约束:
   - 每门课程学分范围: 1-6
   - 每学期最多选修 30 学分
   - 每学期最少选修 12 学分

R4. 成绩查询:
   - 支持按学号、课程名、学期查询
   - 学号为 10 位数字""",

    "game": """角色创建系统

功能需求:
R1. 角色名称:
   - 长度: 2-12 个字符
   - 允许中文、英文、数字
   - 不允许特殊字符和空格
   - 名称不能与已有角色重复

R2. 属性点分配:
   - 初始总属性点: 20 点
   - 四项属性: 力量、敏捷、智力、体质
   - 每项属性最低 1 点，最高 10 点
   - 分配完后总和必须等于 20

R3. 职业选择:
   - 战士: 要求力量 >= 5, 体质 >= 5
   - 法师: 要求智力 >= 7
   - 盗贼: 要求敏捷 >= 6
   - 牧师: 要求智力 >= 4, 体质 >= 4

R4. 等级限制:
   - 初始等级: 1
   - 最高等级: 100
   - 每升一级获得 5 点属性点""",
}


def run_domain(name, requirements):
    print(f"\n{'='*60}")
    print(f"Domain: {name}")
    print(f"{'='*60}")
    start = time.time()
    resp = httpx.post(
        f"{BASE_URL}/api/blackbox/analyze",
        json={"requirements": requirements, "techniques": ["EP", "BVA", "TestCases"]},
        timeout=180,
    )
    elapsed = time.time() - start
    data = resp.json()
    result = data["result"]

    with open(f"D:/code/EasyTest/experiments/gen_{name}_result.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    vars_count = len(result.get("input_variables", []))
    ep_count = len(result.get("equivalence_partitions", []))
    bv_count = len(result.get("boundary_values", []))
    tc_count = len(result.get("test_cases", []))

    print(f"  Status: {resp.status_code}, Time: {elapsed:.1f}s")
    print(f"  Variables: {vars_count}")
    print(f"  EP: {ep_count}, BVA: {bv_count}, TC: {tc_count}")
    print(f"  Tokens: prompt={data['usage']['prompt_tokens']}, completion={data['usage']['completion_tokens']}")

    # Quick quality check
    ep_valid = sum(1 for e in result.get("equivalence_partitions", []) if e.get("type") == "valid")
    ep_invalid = sum(1 for e in result.get("equivalence_partitions", []) if e.get("type") == "invalid")
    tc_high = sum(1 for t in result.get("test_cases", []) if t.get("priority") == "high")
    tc_has_ep = sum(1 for t in result.get("test_cases", []) if t.get("covers_ep"))
    tc_has_bv = sum(1 for t in result.get("test_cases", []) if t.get("covers_bv"))

    print(f"  EP: {ep_valid} valid + {ep_invalid} invalid")
    print(f"  TC priority: {tc_high} high / {tc_count} total")
    print(f"  TC with EP mapping: {tc_has_ep}/{tc_count}")
    print(f"  TC with BV mapping: {tc_has_bv}/{tc_count}")

    return {
        "domain": name,
        "time": round(elapsed, 1),
        "vars": vars_count,
        "ep": ep_count,
        "bv": bv_count,
        "tc": tc_count,
        "ep_valid": ep_valid,
        "ep_invalid": ep_invalid,
        "tc_high": tc_high,
        "tc_with_ep": tc_has_ep,
        "tc_with_bv": tc_has_bv,
    }


if __name__ == "__main__":
    results = []
    for name, req in DOMAINS.items():
        results.append(run_domain(name, req))

    print("\n\n=== GENERALIZABILITY SUMMARY ===")
    print(f"{'Domain':<12} {'Vars':<6} {'EP':<5} {'BV':<5} {'TC':<5} {'Time':<8}")
    for r in results:
        print(f"{r['domain']:<12} {r['vars']:<6} {r['ep']:<5} {r['bv']:<5} {r['tc']:<5} {r['time']:<8}")

    with open("D:/code/EasyTest/experiments/generalizability_summary.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\nDone!")
