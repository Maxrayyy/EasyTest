// ============================================================
// EasyTest 前端交互逻辑
// 负责：发送分析请求、渲染结果表格、标签页切换、示例加载
// ============================================================

// 示例需求数据
const EXAMPLES = {
    vending: `智能自动售货机系统

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
   - 售罄时需提示用户并退还已投入金额`,

    login: `用户登录系统

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
   - 验证码为 4 位数字，有效期 60 秒`,

    shopping: `在线购物车系统

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
   - 支持部分发货`
};

/**
 * 加载示例需求到输入框
 */
function loadExample(name) {
    document.getElementById('requirements').value = EXAMPLES[name] || '';
}

/**
 * 发送分析请求到后端
 */
async function analyze() {
    const requirements = document.getElementById('requirements').value.trim();
    if (!requirements) {
        alert('请输入系统需求描述');
        return;
    }

    // 收集选中的测试技术
    const techniques = [];
    if (document.getElementById('tech-ep').checked) techniques.push('EP');
    if (document.getElementById('tech-bva').checked) techniques.push('BVA');
    if (document.getElementById('tech-tc').checked) techniques.push('TestCases');

    if (techniques.length === 0) {
        alert('请至少选择一种测试技术');
        return;
    }

    // 切换 UI 状态：显示加载中
    const btn = document.getElementById('analyzeBtn');
    btn.disabled = true;
    btn.textContent = '⏳ 分析中...';
    document.getElementById('loading').classList.add('active');
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('statsSection').classList.remove('active');
    document.getElementById('resultSection').classList.remove('active');

    try {
        const response = await fetch('/api/blackbox/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ requirements, techniques }),
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || '请求失败');
        }

        const data = await response.json();
        renderResults(data);
    } catch (error) {
        alert('分析失败: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = '🚀 开始分析';
        document.getElementById('loading').classList.remove('active');
    }
}

/**
 * 渲染所有分析结果
 */
function renderResults(data) {
    const result = data.result;

    // 显示统计概览
    document.getElementById('statsSection').classList.add('active');
    document.getElementById('statEP').textContent = (result.equivalence_partitions || []).length;
    document.getElementById('statBV').textContent = (result.boundary_values || []).length;
    document.getElementById('statTC').textContent = (result.test_cases || []).length;
    document.getElementById('statVars').textContent = (result.input_variables || []).length;

    // 渲染输入变量表
    renderVarsTable(result.input_variables || []);

    // 渲染等价类划分表
    renderEPTable(result.equivalence_partitions || []);

    // 渲染边界值分析表
    renderBVATable(result.boundary_values || []);

    // 渲染测试用例表
    renderTCTable(result.test_cases || []);

    // 显示 Prompt
    document.getElementById('systemPrompt').textContent = data.prompt_used?.system || '';
    document.getElementById('userPrompt').textContent = data.prompt_used?.user || '';

    // 显示原始 JSON
    document.getElementById('rawJson').textContent = JSON.stringify(result, null, 2);

    // 显示用量信息
    const usage = data.usage || {};
    document.getElementById('usageInfo').innerHTML =
        `模型: <strong>${data.model || 'unknown'}</strong> | ` +
        `输入 Token: ${usage.prompt_tokens || 0} | ` +
        `输出 Token: ${usage.completion_tokens || 0}`;

    // 显示结果区域
    document.getElementById('resultSection').classList.add('active');
}

/**
 * 渲染输入变量表格
 */
function renderVarsTable(vars) {
    const tbody = document.querySelector('#varsTable tbody');
    tbody.innerHTML = vars.map(v => `
        <tr>
            <td><strong>${v.name || ''}</strong></td>
            <td><span class="tag tag-low">${v.type || ''}</span></td>
            <td>${v.description || ''}</td>
            <td>${v.constraints || ''}</td>
        </tr>
    `).join('');
}

/**
 * 渲染等价类划分表格
 */
function renderEPTable(partitions) {
    const tbody = document.querySelector('#epTable tbody');
    tbody.innerHTML = partitions.map(ep => `
        <tr>
            <td>${ep.id || ''}</td>
            <td>${ep.variable || ''}</td>
            <td>${ep.partition || ''}</td>
            <td><span class="tag ${ep.type === 'valid' ? 'tag-valid' : 'tag-invalid'}">${ep.type || ''}</span></td>
            <td>${ep.representative_value || ''}</td>
        </tr>
    `).join('');
}

/**
 * 渲染边界值分析表格
 */
function renderBVATable(boundaries) {
    const tbody = document.querySelector('#bvaTable tbody');
    tbody.innerHTML = boundaries.map(bv => `
        <tr>
            <td>${bv.id || ''}</td>
            <td>${bv.variable || ''}</td>
            <td>${bv.boundary || ''}</td>
            <td>${Array.isArray(bv.test_values) ? bv.test_values.join(', ') : (bv.test_values || '')}</td>
            <td>${bv.expected_behavior || ''}</td>
        </tr>
    `).join('');
}

/**
 * 渲染测试用例表格
 */
function renderTCTable(testCases) {
    const tbody = document.querySelector('#tcTable tbody');
    tbody.innerHTML = testCases.map(tc => `
        <tr>
            <td>${tc.id || ''}</td>
            <td>${tc.description || ''}</td>
            <td style="font-family:monospace;font-size:0.85rem;">${formatInputs(tc.inputs)}</td>
            <td>${tc.expected_result || ''}</td>
            <td>${Array.isArray(tc.covers_ep) ? tc.covers_ep.join(', ') : (tc.covers_ep || '')}</td>
            <td>${Array.isArray(tc.covers_bv) ? tc.covers_bv.join(', ') : (tc.covers_bv || '')}</td>
            <td><span class="tag tag-${tc.priority || 'medium'}">${tc.priority || ''}</span></td>
        </tr>
    `).join('');
}

/**
 * 格式化输入参数为可读字符串
 */
function formatInputs(inputs) {
    if (!inputs) return '';
    if (typeof inputs === 'string') return inputs;
    return Object.entries(inputs).map(([k, v]) => `${k}: ${v}`).join('<br>');
}

/**
 * 标签页切换
 */
function switchTab(name) {
    // 更新标签页激活状态
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));

    // 找到对应标签页并激活
    const tabs = document.querySelectorAll('.tab');
    const tabNames = ['ep', 'bva', 'tc', 'prompt', 'json'];
    const idx = tabNames.indexOf(name);
    if (idx >= 0 && tabs[idx]) {
        tabs[idx].classList.add('active');
    }
    const content = document.getElementById('tab-' + name);
    if (content) content.classList.add('active');
}
