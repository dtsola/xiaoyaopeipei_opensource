<template>
  <div class="privacy-view">
    <!-- 头部 -->
    <AppHeader title="隐私政策" show-back />

    <!-- 内容区域 -->
    <div class="content-container">
      <div class="document-content">
        <!-- 更新提示 -->
        <div class="alert-box info">
          <div class="alert-icon">🔒</div>
          <div class="alert-content">
            <div class="alert-title">我们重视您的隐私</div>
            <div class="alert-text">
              本隐私政策向您说明我们如何收集、使用、存储和保护您的个人信息。
            </div>
          </div>
        </div>

        <!-- 协议内容 -->
        <section class="doc-section">
          <h1>隐私政策</h1>
          <div class="meta-info">
            <span>生效日期：2026年1月1日</span>
            <span>更新日期：2026年2月25日</span>
          </div>
        </section>

        <section class="doc-section">
          <h2>引言</h2>
          <p>「小遥配配」非常重视用户的隐私保护。本隐私政策旨在向您说明我们如何收集、使用、存储和保护您的个人信息。</p>
          <div class="highlight-box">
            <p><strong>本应用为开源演示项目，请在使用前仔细阅读本隐私政策。</strong></p>
          </div>
        </section>

        <section class="doc-section">
          <h2>一、信息收集</h2>
          <h3>1.1 我们收集的信息</h3>

          <div class="info-card">
            <div class="card-icon">💬</div>
            <div class="card-content">
              <div class="card-title">对话记录</div>
              <div class="card-text">您与AI助手的对话内容，用于理解您的电脑配置需求和提供个性化推荐</div>
            </div>
          </div>

          <div class="info-card">
            <div class="card-icon">📱</div>
            <div class="card-content">
              <div class="card-title">联系信息</div>
              <div class="card-text">您主动提供的姓名、电话、微信等，用于商家与您联系</div>
            </div>
          </div>

          <div class="info-card">
            <div class="card-icon">🖥️</div>
            <div class="card-content">
              <div class="card-title">设备信息</div>
              <div class="card-text">设备类型、操作系统、浏览器类型等，用于改善应用兼容性</div>
            </div>
          </div>

          <h3>1.2 我们不收集的信息</h3>
          <ul>
            <li>生物识别信息（指纹、人脸等）</li>
            <li>银行卡号等支付信息</li>
            <li>精确地理位置信息</li>
            <li>社交账号密码</li>
          </ul>
        </section>

        <section class="doc-section">
          <h2>二、信息使用</h2>
          <p>我们使用收集的信息用于：</p>
          <ul>
            <li><strong>提供核心服务</strong>：理解您的电脑配置需求，生成个性化推荐方案</li>
            <li><strong>改善服务体验</strong>：优化AI推荐算法，修复技术问题</li>
            <li><strong>安全保障</strong>：防止欺诈行为，检测和防范安全威胁</li>
          </ul>
          <div class="promise-box">
            <div class="promise-title">🤝 我们的承诺</div>
            <ul>
              <li>不会将您的信息用于营销推广</li>
              <li>不会出售您的个人信息</li>
              <li>不会向第三方共享您的敏感信息</li>
            </ul>
          </div>
        </section>

        <section class="doc-section">
          <h2>三、信息共享与披露</h2>
          <p><strong>我们不会主动共享、出售或出租您的个人信息</strong>，仅在以下情况下披露：</p>
          <ul>
            <li>获得您的明确同意</li>
            <li>在您提交联系方式后，分享给合作商家（以便提供进一步服务）</li>
            <li>根据法律法规、政府主管部门要求</li>
            <li>委托的第三方服务提供商（如云服务、API服务）</li>
          </ul>
        </section>

        <section class="doc-section highlight">
          <h2>四、信息存储</h2>
          <div class="highlight-box">
            <h3>存储说明</h3>
            <table class="storage-table">
              <thead>
                <tr>
                  <th>信息类型</th>
                  <th>存储期限</th>
                  <th>说明</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>对话记录</td>
                  <td>30天</td>
                  <td>超期自动删除</td>
                </tr>
                <tr>
                  <td>联系信息</td>
                  <td>永久</td>
                  <td>直到您要求删除</td>
                </tr>
                <tr>
                  <td>使用日志</td>
                  <td>90天</td>
                  <td>超期自动删除</td>
                </tr>
              </tbody>
            </table>

            <h3>存储安全</h3>
            <p>我们采取以下措施保护您的信息：</p>
            <ul>
              <li>HTTPS加密传输</li>
              <li>数据库加密存储</li>
              <li>定期安全审计</li>
              <li>访问权限控制</li>
            </ul>

            <div class="warning-box">
              <p><strong>⚠️ 开源项目特别说明</strong></p>
              <p>由于本应用为开源项目，您可以自行查看源代码，了解数据处理逻辑。如自行部署，数据由您自行控制。</p>
            </div>
          </div>
        </section>

        <section class="doc-section">
          <h2>五、您的权利</h2>
          <p>根据《中华人民共和国个人信息保护法》，您享有以下权利：</p>
          <div class="rights-grid">
            <div class="right-item">
              <div class="right-icon">🔍</div>
              <div class="right-title">访问权</div>
              <div class="right-desc">要求提供您的个人信息副本</div>
            </div>
            <div class="right-item">
              <div class="right-icon">✏️</div>
              <div class="right-title">更正权</div>
              <div class="right-desc">要求更正不准确的信息</div>
            </div>
            <div class="right-item">
              <div class="right-icon">🗑️</div>
              <div class="right-title">删除权</div>
              <div class="right-desc">要求删除您的个人信息</div>
            </div>
            <div class="right-item">
              <div class="right-icon">↩️</div>
              <div class="right-title">撤回同意</div>
              <div class="right-desc">随时撤回对信息处理的同意</div>
            </div>
          </div>
        </section>

        <section class="doc-section">
          <h2>六、Cookie的使用</h2>
          <p>我们使用Cookie和类似技术用于：</p>
          <ul>
            <li>保持您的登录状态</li>
            <li>记住您的偏好设置</li>
            <li>分析网站使用情况</li>
          </ul>
          <p>您可以通过浏览器设置管理Cookie（接受、拒绝或删除）。请注意，禁用Cookie可能影响部分功能的使用。</p>
        </section>

        <section class="doc-section">
          <h2>七、未成年人的保护</h2>
          <p>本应用主要面向成年用户。如果您是未成年人：</p>
          <ul>
            <li>请在监护人的指导和监督下使用</li>
            <li>请勿提交任何个人信息</li>
          </ul>
        </section>

        <section class="doc-section">
          <h2>八、隐私政策的修订</h2>
          <p>我们可能适时修订本隐私政策，修订后的政策将在应用内公布。</p>
          <p>如您在隐私政策修订后继续使用本应用，视为您接受修订后的政策。</p>
        </section>

        <section class="doc-section">
          <h2>九、法律依据</h2>
          <p>本隐私政策的制定依据包括但不限于：</p>
          <ul>
            <li>《中华人民共和国个人信息保护法》</li>
            <li>《中华人民共和国网络安全法》</li>
            <li>《中华人民共和国数据安全法》</li>
            <li>《信息安全技术 个人信息安全规范》（GB/T 35273-2020）</li>
          </ul>
        </section>

        <!-- 联系方式 -->
        <section class="doc-section contact-section">
          <h2>联系我们</h2>
          <p>如您对本隐私政策有任何疑问、意见或建议，请通过以下方式联系我们：</p>
          <div class="contact-links">
            <a href="https://github.com/dtsola/xiaoyaopeipei" target="_blank" rel="noopener">
              <span class="contact-icon">📦</span>
              <span>GitHub 仓库</span>
            </a>
            <a href="mailto:dtsola@163.com">
              <span class="contact-icon">📧</span>
              <span>联系邮箱</span>
            </a>
          </div>
          <p class="response-time">我们会在收到您的请求后 <strong>15个工作日</strong> 内予以回复。</p>
        </section>

        <!-- 底部提示 -->
        <div class="footer-note">
          感谢您信任「小遥配配」！
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { AppHeader } from '@/components'
</script>

<style lang="less" scoped>
.privacy-view {
  min-height: 100vh;
  background: var(--color-bg-secondary);
}

.content-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 76px var(--spacing-lg) var(--spacing-xl);
  animation: fadeIn 0.4s ease-out;
}

.document-content {
  background: var(--color-bg-primary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-sm);
}

// 警告框
.alert-box {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-xl);

  &.info {
    background: #dbeafe;
    border-left: 3px solid #3b82f6;
  }

  &.warning {
    background: #fef3c7;
    border-left: 3px solid #f59e0b;
  }

  .alert-icon {
    font-size: var(--font-size-2xl);
    flex-shrink: 0;
  }

  .alert-content {
    flex: 1;
  }

  .alert-title {
    font-size: var(--font-size-base);
    font-weight: 600;
    margin-bottom: var(--spacing-xs);
  }

  .alert-text {
    font-size: var(--font-size-sm);
    line-height: 1.6;
  }
}

.alert-box.info .alert-title {
  color: #1e40af;
}

.alert-box.info .alert-text {
  color: #3b82f6;
}

// 文档章节
.doc-section {
  margin-bottom: var(--spacing-xl);

  &:last-child {
    margin-bottom: 0;
  }

  h1 {
    font-size: var(--font-size-3xl);
    font-weight: 700;
    color: var(--color-text-primary);
    margin-bottom: var(--spacing-md);
  }

  h2 {
    font-size: var(--font-size-xl);
    font-weight: 600;
    color: var(--color-text-primary);
    margin-bottom: var(--spacing-md);
    padding-bottom: var(--spacing-sm);
    border-bottom: 1px solid var(--color-border-light);
  }

  h3 {
    font-size: var(--font-size-base);
    font-weight: 600;
    color: var(--color-text-primary);
    margin: var(--spacing-md) 0 var(--spacing-sm);
  }

  p {
    font-size: var(--font-size-sm);
    line-height: 1.8;
    color: var(--color-text-secondary);
    margin-bottom: var(--spacing-sm);
  }

  ul {
    margin-left: var(--spacing-lg);
    margin-bottom: var(--spacing-sm);

    li {
      font-size: var(--font-size-sm);
      line-height: 1.8;
      color: var(--color-text-secondary);
      margin-bottom: var(--spacing-xs);
    }
  }
}

.meta-info {
  display: flex;
  gap: var(--spacing-lg);
  flex-wrap: wrap;
  margin-bottom: var(--spacing-lg);

  span {
    font-size: var(--font-size-sm);
    color: var(--color-text-tertiary);
  }
}

// 高亮框
.highlight-box {
  background: var(--color-bg-secondary);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  margin-top: var(--spacing-md);

  h3 {
    color: var(--color-primary);
    margin-top: var(--spacing-md);
    &:first-child {
      margin-top: 0;
    }
  }
}

// 信息卡片
.info-card {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-sm);

  .card-icon {
    font-size: var(--font-size-2xl);
    flex-shrink: 0;
  }

  .card-content {
    flex: 1;
  }

  .card-title {
    font-weight: 600;
    color: var(--color-text-primary);
    margin-bottom: var(--spacing-xs);
  }

  .card-text {
    font-size: var(--font-size-sm);
    color: var(--color-text-secondary);
    line-height: 1.6;
  }
}

// 承诺框
.promise-box {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  margin-top: var(--spacing-md);
  border-left: 3px solid #10b981;

  .promise-title {
    font-weight: 600;
    color: #065f46;
    margin-bottom: var(--spacing-sm);
  }

  ul {
    margin: 0;

    li {
      color: #047857;
    }
  }
}

// 警告框
.warning-box {
  background: #fef3c7;
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  margin-top: var(--spacing-md);
  border-left: 3px solid #f59e0b;

  p {
    margin: 0;
    color: #92400e;
  }
}

// 表格
.storage-table {
  width: 100%;
  border-collapse: collapse;
  margin: var(--spacing-md) 0;

  th,
  td {
    padding: var(--spacing-sm) var(--spacing-md);
    text-align: left;
    border-bottom: 1px solid var(--color-border-light);
    font-size: var(--font-size-sm);
  }

  th {
    background: var(--color-bg-secondary);
    font-weight: 600;
    color: var(--color-text-primary);
  }

  td {
    color: var(--color-text-secondary);
  }

  tbody tr:hover {
    background: var(--color-bg-secondary);
  }
}

// 权利网格
.rights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: var(--spacing-md);
  margin-top: var(--spacing-md);
}

.right-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: var(--spacing-md);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-md);
  transition: all 0.2s ease;

  &:hover {
    background: var(--color-bg-tertiary);
    transform: translateY(-2px);
  }

  .right-icon {
    font-size: var(--font-size-2xl);
    margin-bottom: var(--spacing-sm);
  }

  .right-title {
    font-weight: 600;
    color: var(--color-text-primary);
    margin-bottom: var(--spacing-xs);
  }

  .right-desc {
    font-size: var(--font-size-xs);
    color: var(--color-text-tertiary);
    line-height: 1.4;
  }
}

// 联系方式
.contact-section {
  margin-top: var(--spacing-2xl);
  padding-top: var(--spacing-xl);
  border-top: 1px solid var(--color-border-light);
}

.contact-links {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  margin: var(--spacing-md) 0;
  max-width: 400px;

  a {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    padding: var(--spacing-md);
    background: var(--color-bg-secondary);
    border-radius: var(--radius-md);
    text-decoration: none;
    color: var(--color-text-primary);
    transition: all 0.2s ease;

    &:hover {
      background: var(--color-bg-tertiary);
      transform: translateX(4px);
    }
  }
}

.contact-icon {
  font-size: var(--font-size-xl);
}

.response-time {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  background: var(--color-bg-secondary);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  display: inline-block;
  margin-top: var(--spacing-md);
}

// 底部提示
.footer-note {
  text-align: center;
  padding: var(--spacing-xl) 0;
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
  border-top: 1px solid var(--color-border-light);
  margin-top: var(--spacing-xl);
}

@media (max-width: 768px) {
  .content-container {
    padding: 70px var(--spacing-md) var(--spacing-lg);
  }

  .document-content {
    padding: var(--spacing-lg);
  }

  .doc-section {
    h1 {
      font-size: var(--font-size-2xl);
    }

    h2 {
      font-size: var(--font-size-lg);
    }
  }

  .rights-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .storage-table {
    font-size: var(--font-size-xs);

    th,
    td {
      padding: var(--spacing-xs) var(--spacing-sm);
    }
  }

  .contact-links {
    a {
      flex-direction: column;
      text-align: center;
    }
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
