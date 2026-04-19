"""运行 3 个内置示例实验，保存完整 JSON 结果"""
import json
import httpx
import time

BASE_URL = "http://127.0.0.1:8000"

EXAMPLES = {
    "vending": """智能自动售货机系统

功能需求:
R1. 商品选择：售货机提供三类商品：
   - 饮料（价格范围：1.50-3.00元）
   - 零食（价格范围：2.00-4.50元）
   - 热食（价格范围：5.00-10.00元）

R2. 支付方式：接受以下支付方式：
   - 硬币：0.10元、0.25元、0.50元、1.00元
   - 纸币：5.00元、10.00元

R3. 支付约束：
   - 投入金额必须大于等于商品价格
   - 机器只能找零不超过5.00元，超过则拒绝交易

R4. 库存约束：
   - 商品可能在支付过程中售罄
   - 售罄时需提示用户并退还已投入金额""",

    "login": """用户登录系统

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
   - 验证码为 4 位数字，有效期 60 秒""",

    "shopping": """在线购物车系统

功能需求:
R1. 添加商品：
   - 每种商品数量范围为 1-99
   - 购物车最多容纳 50 种不同商品
   - 商品价格范围为 0.01-99999.99 元

R2. 优惠券：
   - 满 100 减 10
   - 满 300 减 50
   - 满 500 减 100
   - 每次结算只能使用一张优惠券

R3. 运费计算：
   - 订单金额 < 50 元：运费 10 元
   - 订单金额 50-199 元：运费 5 元
   - 订单金额 >= 200 元：免运费
   - 优惠券减免后的金额用于计算运费

R4. 库存检查：
   - 下单时检查库存，库存不足则提示用户
   - 支持部分发货""",
}


def run_example(name, requirements):
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print(f"{'='*60}")
    start = time.time()
    resp = httpx.post(
        f"{BASE_URL}/api/blackbox/analyze",
        json={"requirements": requirements, "techniques": ["EP", "BVA", "TestCases"]},
        timeout=120,
    )
    elapsed = time.time() - start
    print(f"Status: {resp.status_code}, Time: {elapsed:.1f}s")

    data = resp.json()
    # Save full response
    with open(f"D:/code/EasyTest/experiments/accuracy/{name}_result.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Print summary
    result = data.get("result", {})
    print(f"  Input Variables: {len(result.get('input_variables', []))}")
    print(f"  EP: {len(result.get('equivalence_partitions', []))}")
    print(f"  BVA: {len(result.get('boundary_values', []))}")
    print(f"  TC: {len(result.get('test_cases', []))}")
    print(f"  Tokens: prompt={data.get('usage',{}).get('prompt_tokens',0)}, completion={data.get('usage',{}).get('completion_tokens',0)}")
    return data


if __name__ == "__main__":
    for name, req in EXAMPLES.items():
        run_example(name, req)
    print("\nAll experiments complete!")
