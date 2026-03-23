<template>
  <div class="terms-view">
    <!-- 头部 -->
    <AppHeader title="用户协议" show-back />

    <!-- 内容区域 -->
    <div class="content-container">
      <div class="document-content">
        <!-- 重要提示 -->
        <div class="alert-box warning">
          <div class="alert-icon">⚠️</div>
          <div class="alert-content">
            <div class="alert-title">重要提示</div>
            <div class="alert-text">
              本应用为开源演示项目，仅供学习、研究和技术交流使用，非商业产品。
            </div>
          </div>
        </div>

        <!-- 协议内容 -->
        <section class="doc-section">
          <h1>用户协议</h1>
          <div class="meta-info">
            <span>生效日期：2026年1月1日</span>
            <span>更新日期：2026年2月25日</span>
          </div>
        </section>

        <section class="doc-section">
          <h2>一、协议的性质与适用范围</h2>
          <h3>1.1 开源演示性质</h3>
          <p>本应用是基于开源协议发布的演示项目，旨在展示AI对话式推荐系统的技术实现。本应用非商业产品，不提供任何商业服务或商业保证。</p>

          <h3>1.2 协议的接受</h3>
          <p>当您下载、安装、访问或使用本应用时，即表示您已阅读、理解并同意接受本协议的全部内容。</p>

          <h3>1.3 协议的修改</h3>
          <p>我们保留随时修改本协议的权利，修改后的协议一旦公布即代替原协议。恕不另行通知。</p>
        </section>

        <section class="doc-section">
          <h2>二、使用说明</h2>
          <h3>2.1 使用资格</h3>
          <ul>
            <li>您必须具备完全民事行为能力才能使用本应用</li>
            <li>未成年人使用本应用应在监护人的指导和监督下进行</li>
          </ul>

          <h3>2.2 许可范围</h3>
          <ul>
            <li>查看、研究本应用的源代码</li>
            <li>学习本应用的技术实现方式</li>
            <li>在遵循开源协议的前提下进行二次开发</li>
          </ul>

          <h3>2.3 使用限制</h3>
          <p>未经明确授权，您不得：</p>
          <ul>
            <li>将本应用用于任何商业目的</li>
            <li>声称本应用是您自己开发的</li>
            <li>利用本应用从事任何违法违规活动</li>
          </ul>
        </section>

        <section class="doc-section">
          <h2>三、用户行为规范</h2>
          <h3>3.1 合法使用</h3>
          <p>您在使用本应用时应遵守中华人民共和国相关法律法规，不得利用本应用从事以下行为：</p>
          <ul>
            <li>发布任何违法、有害、虚假、侮辱、诽谤、淫秽、色情、暴力等信息</li>
            <li>侵犯他人知识产权、商业秘密、隐私权等合法权益</li>
            <li>干扰或破坏本应用的正常运行</li>
          </ul>

          <h3>3.2 信息提交</h3>
          <p>如您在本应用中提交任何信息，您保证所提交信息真实、准确、完整，不包含任何违法或侵权内容。</p>
        </section>

        <section class="doc-section">
          <h2>四、知识产权</h2>
          <p>本应用的全部知识产权归原作者所有，受中华人民共和国法律及相关国际条约保护。</p>
          <p>本应用的开源授权以项目根目录的 LICENSE 文件为准。</p>
        </section>

        <section class="doc-section highlight">
          <h2>五、免责声明</h2>
          <div class="highlight-box">
            <h3>5.1 "按原样"提供</h3>
            <p>本应用按原样（AS IS）提供，不提供任何形式的明示或暗示保证。</p>

            <h3>5.2 责任限制</h3>
            <p>在法律允许的最大范围内，对于因使用或无法使用本应用而导致的任何直接、间接、附带、特殊或后果性的损害，我们不承担任何责任。</p>

            <h3>5.3 AI推荐结果</h3>
            <p>本应用提供的电脑配置推荐仅供参考，不构成任何购买建议。实际购买决策请自行判断。</p>
          </div>
        </section>

        <section class="doc-section">
          <h2>六、数据与隐私</h2>
          <h3>6.1 数据收集</h3>
          <p>作为演示项目，本应用可能收集：</p>
          <ul>
            <li>对话记录（用于AI理解您的需求）</li>
            <li>您主动提交的联系方式（用于商家联系）</li>
            <li>设备信息（用于改善用户体验）</li>
          </ul>

          <h3>6.2 数据保护</h3>
          <p>我们采取合理的技术措施保护您的数据安全，但由于本应用为开源演示项目，不能保证数据的绝对安全。请勿在本应用中提交任何敏感个人信息。</p>

          <h3>6.3 数据共享</h3>
          <p>我们不会出售、出租或以其他方式向第三方披露您的个人信息。</p>
        </section>

        <section class="doc-section">
          <h2>七、争议解决</h2>
          <p>本协议的订立、执行、解释及争议解决均适用中华人民共和国法律。</p>
          <p>因本协议引起的任何争议，双方应友好协商解决。</p>
        </section>

        <section class="doc-section">
          <h2>八、开源特别说明</h2>
          <h3>8.1 演示目的</h3>
          <p>本应用为技术演示项目，展示以下技术能力：</p>
          <ul>
            <li>AI对话式需求收集</li>
            <li>基于LangChain的智能推荐</li>
            <li>Vue3 + FastAPI全栈开发</li>
          </ul>

          <h3>8.2 自部署风险</h3>
          <p>如您选择自行部署本应用，您需要自行承担服务器、数据库等成本，并自行保障数据安全。</p>

          <h3>8.3 社区支持</h3>
          <p>本应用的开源支持以社区形式提供。欢迎提交Issue反馈问题、提交Pull Request贡献代码。</p>
        </section>

        <!-- 联系方式 -->
        <section class="doc-section contact-section">
          <h2>联系我们</h2>
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
        </section>

        <!-- 底部提示 -->
        <div class="footer-note">
          感谢您使用「小遥配配」开源演示项目！
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { AppHeader } from '@/components'
</script>

<style lang="less" scoped>
.terms-view {
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

.alert-box.warning .alert-title {
  color: #92400e;
}

.alert-box.warning .alert-text {
  color: #b45309;
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

// 高亮章节
.doc-section.highlight {
  .highlight-box {
    background: var(--color-bg-secondary);
    border-radius: var(--radius-md);
    padding: var(--spacing-lg);

    h3 {
      color: var(--color-primary);
      margin-top: var(--spacing-md);
      &:first-child {
        margin-top: 0;
      }
    }
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