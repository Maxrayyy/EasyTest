"""一致性测试：对「用户登录系统」运行 3 次，比较输出差异"""
import json
import httpx
import time

BASE_URL = "http://127.0.0.1:8000"

LOGIN_REQ = """用户登录系统

功能需求:
R1. 用户名验证：
   - 长度为 4-20 个字符
   - 只允许字母、数字和下划线
   - 不能以数字开头

R2. 密码验证：
   - 长度为 8-32 个字符
   - 必须包含至少一个大写字母、一个小写字母、一个数字
   - 可选包含特殊字符（!@#$%^&*）

R3. 登录尝试限制：
   - 连续失败 3 次后锁定账户 15 分钟
   - 连续失败 5 次后锁定账户 24 小时

R4. 验证码：
   - 连续失败 2 次后需要输入验证码
   - 验证码为 4 位数字，有效期 60 秒"""


def run_once(run_id):
    print(f"\n--- Run {run_id} ---")
    start = time.time()
    resp = httpx.post(
        f"{BASE_URL}/api/blackbox/analyze",
        json={"requirements": LOGIN_REQ, "techniques": ["EP", "BVA", "TestCases"]},
        timeout=180,
    )
    elapsed = time.time() - start
    data = resp.json()
    result = data["result"]

    with open(f"D:/code/EasyTest/experiments/consistency/consistency_run{run_id}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    vars_count = len(result.get("input_variables", []))
    ep_count = len(result.get("equivalence_partitions", []))
    bv_count = len(result.get("boundary_values", []))
    tc_count = len(result.get("test_cases", []))

    var_names = sorted([v["name"] for v in result.get("input_variables", [])])
    ep_ids = sorted([e["id"] for e in result.get("equivalence_partitions", [])])
    tc_ids = sorted([t["id"] for t in result.get("test_cases", [])])

    print(f"  Time: {elapsed:.1f}s")
    print(f"  Vars: {vars_count} -> {var_names}")
    print(f"  EP: {ep_count}")
    print(f"  BV: {bv_count}")
    print(f"  TC: {tc_count}")
    print(f"  Tokens: prompt={data['usage']['prompt_tokens']}, completion={data['usage']['completion_tokens']}")

    return {
        "run_id": run_id,
        "time": round(elapsed, 1),
        "vars": vars_count,
        "var_names": var_names,
        "ep": ep_count,
        "bv": bv_count,
        "tc": tc_count,
        "ep_ids": ep_ids,
        "tc_ids": tc_ids,
        "prompt_tokens": data["usage"]["prompt_tokens"],
        "completion_tokens": data["usage"]["completion_tokens"],
    }


if __name__ == "__main__":
    results = []
    for i in range(1, 4):
        results.append(run_once(i))

    print("\n\n=== CONSISTENCY SUMMARY ===")
    print(f"{'Run':<5} {'Vars':<6} {'EP':<5} {'BV':<5} {'TC':<5} {'Time':<8} {'Tokens':<12}")
    for r in results:
        print(f"{r['run_id']:<5} {r['vars']:<6} {r['ep']:<5} {r['bv']:<5} {r['tc']:<5} {r['time']:<8} {r['prompt_tokens']+r['completion_tokens']:<12}")

    # Check variable name consistency
    all_var_sets = [set(r["var_names"]) for r in results]
    common_vars = all_var_sets[0].intersection(*all_var_sets[1:])
    all_vars = all_var_sets[0].union(*all_var_sets[1:])
    print(f"\nVariable name consistency: {len(common_vars)}/{len(all_vars)} common")
    print(f"  Common: {sorted(common_vars)}")
    if all_vars - common_vars:
        print(f"  Varying: {sorted(all_vars - common_vars)}")

    # Save summary
    with open("D:/code/EasyTest/experiments/consistency/consistency_summary.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\nDone!")
