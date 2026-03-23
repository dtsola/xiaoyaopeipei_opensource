<template>
  <div class="design-showcase">
    <!-- 导航页面 -->
    <div v-if="currentView === 'home'" class="showcase-home">
      <!-- 头部 -->
      <header class="showcase-header">
        <div class="header-content">
          <div class="brand">
            <span class="brand-emoji">🎨</span>
            <h1 class="brand-title">小遥配配 C端视觉设计</h1>
          </div>
          <p class="brand-subtitle">AI对话式电脑导购助手 · 十套风格方案</p>
        </div>
      </header>

      <!-- 设计方案卡片 -->
      <main class="showcase-main">
        <div class="cards-container">
          <!-- 方案1：科技蓝 -->
          <div class="design-card tech-blue" @click="openDesign('tech-blue')">
            <div class="card-preview">
              <div class="preview-header">
                <div class="preview-nav">
                  <span class="preview-back">‹</span>
                  <span class="preview-title">小遥配配</span>
                  <span class="preview-dots">···</span>
                </div>
              </div>
              <div class="preview-messages">
                <div class="preview-msg ai">
                  <div class="preview-avatar ai-avatar">小遥</div>
                  <div class="preview-bubble ai-bubble">您好！请问您的预算大概是多少呢？</div>
                </div>
                <div class="preview-msg user">
                  <div class="preview-bubble user-bubble">6000左右的游戏笔记本</div>
                  <div class="preview-avatar user-avatar">👤</div>
                </div>
              </div>
              <div class="preview-input">
                <div class="preview-input-bar">
                  <span>输入您的需求...</span>
                  <span class="preview-send">➤</span>
                </div>
              </div>
            </div>
            <div class="card-info">
              <div class="card-badge" style="background: linear-gradient(135deg, #4A90E2, #357ABD);">
                Style 1
              </div>
              <h3 class="card-title">科技蓝 · 经典商务</h3>
              <p class="card-desc">稳重专业，可信赖</p>
              <div class="card-colors">
                <span class="color-dot" style="background: #4A90E2;"></span>
                <span class="color-dot" style="background: #50C878;"></span>
                <span class="color-dot" style="background: #FFB84D;"></span>
                <span class="color-dot" style="background: #F5F7FA;"></span>
              </div>
              <div class="card-tags">
                <span class="tag">商务</span>
                <span class="tag">专业</span>
                <span class="tag">稳重</span>
              </div>
            </div>
            <div class="card-arrow">→</div>
          </div>

          <!-- 方案2：活力橙 -->
          <div class="design-card vibrant-orange" @click="openDesign('vibrant-orange')">
            <div class="card-preview">
              <div class="preview-header orange">
                <div class="preview-nav">
                  <span class="preview-back">‹</span>
                  <span class="preview-brand"><span class="brand-emoji">🔥</span>小遥配配</span>
                  <span class="preview-dots">···</span>
                </div>
              </div>
              <div class="preview-messages orange-bg">
                <div class="preview-msg ai">
                  <div class="preview-avatar ai-avatar-orange">🤖</div>
                  <div class="preview-bubble ai-bubble-orange">嗨~ 找我帮你选电脑！预算是多少呢？</div>
                </div>
                <div class="preview-msg user">
                  <div class="preview-bubble user-bubble-orange">6000左右的游戏本</div>
                  <div class="preview-avatar user-avatar-orange">😊</div>
                </div>
              </div>
              <div class="preview-input orange-input">
                <div class="preview-input-bar">
                  <span class="emoji-icon">😊</span>
                  <span>告诉我你想要什么样的电脑~</span>
                  <span class="preview-send-orange">✨</span>
                </div>
              </div>
            </div>
            <div class="card-info">
              <div class="card-badge" style="background: linear-gradient(135deg, #FF6B35, #FF8C42);">
                Style 2
              </div>
              <h3 class="card-title">活力橙 · 年轻时尚</h3>
              <p class="card-desc">活力四射，趣味十足</p>
              <div class="card-colors">
                <span class="color-dot" style="background: #FF6B35;"></span>
                <span class="color-dot" style="background: #00D9A5;"></span>
                <span class="color-dot" style="background: #7B68EE;"></span>
                <span class="color-dot" style="background: #FFF8F3;"></span>
              </div>
              <div class="card-tags">
                <span class="tag">年轻</span>
                <span class="tag">活力</span>
                <span class="tag">趣味</span>
              </div>
            </div>
            <div class="card-arrow">→</div>
          </div>

          <!-- 方案3：森系绿 -->
          <div class="design-card forest-green" @click="openDesign('forest-green')">
            <div class="card-preview">
              <div class="preview-header forest">
                <div class="preview-nav natural-nav">
                  <span class="preview-back">‹</span>
                  <span class="natural-brand"><span class="brand-leaf">🌿</span>小遥配配</span>
                  <span class="natural-status"><span class="status-dot"></span>在线</span>
                </div>
              </div>
              <div class="preview-messages forest-bg">
                <div class="preview-msg ai">
                  <div class="preview-avatar ai-avatar-forest">🍃</div>
                  <div class="preview-bubble ai-bubble-forest">你好，我是小遥。你的预算大概在什么范围？</div>
                </div>
                <div class="preview-msg user">
                  <div class="preview-bubble user-bubble-forest">6000左右的游戏本</div>
                  <div class="preview-avatar user-avatar-forest">你</div>
                </div>
              </div>
              <div class="preview-input forest-input">
                <div class="preview-input-bar natural-input">
                  <span>想找什么样的电脑呢...</span>
                  <span class="preview-send-forest">➤</span>
                </div>
              </div>
            </div>
            <div class="card-info">
              <div class="card-badge" style="background: linear-gradient(135deg, #5D8A66, #8FB996);">
                Style 3
              </div>
              <h3 class="card-title">森系绿 · 清新自然</h3>
              <p class="card-desc">舒适优雅，有温度</p>
              <div class="card-colors">
                <span class="color-dot" style="background: #5D8A66;"></span>
                <span class="color-dot" style="background: #8FB996;"></span>
                <span class="color-dot" style="background: #D4A574;"></span>
                <span class="color-dot" style="background: #FAF9F6;"></span>
              </div>
              <div class="card-tags">
                <span class="tag">清新</span>
                <span class="tag">自然</span>
                <span class="tag">优雅</span>
              </div>
            </div>
            <div class="card-arrow">→</div>
          </div>

          <!-- 方案4：赛博紫 -->
          <div class="design-card cyber-purple" @click="openDesign('cyber-purple')">
            <div class="card-preview dark-preview">
              <div class="preview-header cyber-header">
                <div class="preview-nav">
                  <span class="preview-back">◄</span>
                  <span class="preview-brand-cyber">XIAOYAO</span>
                  <span class="status-light"></span>
                </div>
              </div>
              <div class="preview-messages cyber-messages">
                <div class="preview-msg ai">
                  <div class="preview-avatar ai-avatar-cyber">◈</div>
                  <div class="preview-bubble ai-bubble-cyber">>> SYSTEM READY\n> Specify budget range</div>
                </div>
                <div class="preview-msg user">
                  <div class="preview-bubble user-bubble-cyber">6000 gaming laptop</div>
                  <div class="preview-avatar user-avatar-cyber">U</div>
                </div>
              </div>
              <div class="preview-input cyber-input">
                <div class="preview-input-bar">
                  <span class="prompt-sign">></span>
                  <span>ENTER COMMAND...</span>
                  <span class="send-cyber">►</span>
                </div>
              </div>
            </div>
            <div class="card-info">
              <div class="card-badge" style="background: linear-gradient(135deg, #9D4EDD, #10002B);">
                Style 4
              </div>
              <h3 class="card-title">赛博紫 · 暗夜朋克</h3>
              <p class="card-desc">未来科技，霓虹炫彩</p>
              <div class="card-colors">
                <span class="color-dot" style="background: #9D4EDD;"></span>
                <span class="color-dot" style="background: #00D9FF;"></span>
                <span class="color-dot" style="background: #FF006E;"></span>
                <span class="color-dot" style="background: #10002B;"></span>
              </div>
              <div class="card-tags">
                <span class="tag">赛博</span>
                <span class="tag">霓虹</span>
                <span class="tag">科技</span>
              </div>
            </div>
            <div class="card-arrow">→</div>
          </div>

          <!-- 方案5：糖果粉 -->
          <div class="design-card candy-pink" @click="openDesign('candy-pink')">
            <div class="card-preview">
              <div class="preview-header candy-header">
                <div class="preview-nav">
                  <span class="preview-back">🌸</span>
                  <span class="preview-brand-candy">🎀小遥配配</span>
                  <span class="menu-dots">•••</span>
                </div>
              </div>
              <div class="preview-messages candy-messages">
                <div class="preview-msg ai">
                  <div class="preview-avatar ai-avatar-candy">🤖</div>
                  <div class="preview-bubble ai-bubble-candy">嗨~ 预算有多少呢？💕</div>
                </div>
                <div class="preview-msg user">
                  <div class="preview-bubble user-bubble-candy">6000左右的游戏本</div>
                  <div class="preview-avatar user-avatar-candy">😊</div>
                </div>
              </div>
              <div class="preview-input candy-input">
                <div class="preview-input-bar">
                  <span>😄</span>
                  <span>告诉我你想要什么样的电脑吧~</span>
                  <span class="send-candy">🚀</span>
                </div>
              </div>
            </div>
            <div class="card-info">
              <div class="card-badge" style="background: linear-gradient(135deg, #FFB6D9, #FF8AB3);">
                Style 5
              </div>
              <h3 class="card-title">糖果粉 · 可爱甜美</h3>
              <p class="card-desc">萌系温馨，活泼可爱</p>
              <div class="card-colors">
                <span class="color-dot" style="background: #FFB6D9;"></span>
                <span class="color-dot" style="background: #B8E6FF;"></span>
                <span class="color-dot" style="background: #FFF5BA;"></span>
                <span class="color-dot" style="background: #FFF0F7;"></span>
              </div>
              <div class="card-tags">
                <span class="tag">可爱</span>
                <span class="tag">甜美</span>
                <span class="tag">温馨</span>
              </div>
            </div>
            <div class="card-arrow">→</div>
          </div>

          <!-- 方案6：极简灰 -->
          <div class="design-card minimal-gray" @click="openDesign('minimal-gray')">
            <div class="card-preview minimal-preview">
              <div class="preview-header minimal-header">
                <div class="preview-nav">
                  <span class="minimal-back-icon">←</span>
                  <span class="preview-brand-minimal">小遥配配</span>
                  <span class="spacer-mini"></span>
                </div>
              </div>
              <div class="preview-messages minimal-messages">
                <div class="preview-msg ai">
                  <div class="preview-avatar ai-avatar-minimal">X</div>
                  <div class="preview-bubble ai-bubble-minimal">您好，预算大概在什么范围？</div>
                </div>
                <div class="preview-msg user">
                  <div class="preview-bubble user-bubble-minimal">6000左右的游戏笔记本</div>
                  <div class="preview-avatar user-avatar-minimal">U</div>
                </div>
              </div>
              <div class="preview-input minimal-input">
                <div class="preview-input-bar minimal-input-bar">
                  <span>输入您的需求...</span>
                  <span class="send-minimal">➤</span>
                </div>
              </div>
            </div>
            <div class="card-info">
              <div class="card-badge" style="background: linear-gradient(135deg, #2C2C2C, #3A3A3A);">
                Style 6
              </div>
              <h3 class="card-title">极简灰 · 高级商务</h3>
              <p class="card-desc">克制优雅，极致简约</p>
              <div class="card-colors">
                <span class="color-dot" style="background: #2C2C2C;"></span>
                <span class="color-dot" style="background: #8A8A8A;"></span>
                <span class="color-dot" style="background: #E8E8E8;"></span>
                <span class="color-dot" style="background: #FAFAFA;"></span>
              </div>
              <div class="card-tags">
                <span class="tag">极简</span>
                <span class="tag">高级</span>
                <span class="tag">商务</span>
              </div>
            </div>
            <div class="card-arrow">→</div>
          </div>

          <!-- 方案7：日式和风 -->
          <div class="design-card japanese-zen" @click="openDesign('japanese-zen')">
            <div class="card-preview zen-preview">
              <div class="preview-header zen-header">
                <div class="preview-nav zen-nav">
                  <span class="zen-back">›</span>
                  <div class="zen-brand-preview">
                    <span class="zen-seal-preview">小</span>
                    <span class="zen-brand-vertical">小遥配配</span>
                  </div>
                  <span class="zen-dot"></span>
                </div>
              </div>
              <div class="preview-messages zen-messages">
                <div class="preview-msg ai">
                  <div class="preview-avatar ai-avatar-zen">遥</div>
                  <div class="preview-bubble ai-bubble-zen">初めまして。予算はどのくらいでしょうか？</div>
                </div>
                <div class="preview-msg user">
                  <div class="preview-bubble user-bubble-zen">6000円くらい</div>
                  <div class="preview-avatar user-avatar-zen">客</div>
                </div>
              </div>
              <div class="preview-input zen-input">
                <div class="preview-input-bar zen-input-bar">
                  <span>何でもお聞きください...</span>
                  <span class="send-zen">送</span>
                </div>
              </div>
            </div>
            <div class="card-info">
              <div class="card-badge" style="background: linear-gradient(135deg, #C8553D, #E07A5F);">
                Style 7
              </div>
              <h3 class="card-title">日式和风 · 禅意温暖</h3>
              <p class="card-desc">宁静致远，匠心独运</p>
              <div class="card-colors">
                <span class="color-dot" style="background: #C8553D;"></span>
                <span class="color-dot" style="background: #B8956B;"></span>
                <span class="color-dot" style="background: #6B5B4F;"></span>
                <span class="color-dot" style="background: #F5F0E8;"></span>
              </div>
              <div class="card-tags">
                <span class="tag">和风</span>
                <span class="tag">禅意</span>
                <span class="tag">温暖</span>
              </div>
            </div>
            <div class="card-arrow">→</div>
          </div>

          <!-- 方案8：复古棕 -->
          <div class="design-card retro-film" @click="openDesign('retro-film')">
            <div class="card-preview retro-preview">
              <div class="preview-header retro-header">
                <div class="preview-nav">
                  <span class="retro-back">◄</span>
                  <span class="retro-brand-preview">小遥配配</span>
                  <span class="retro-rec">● REC</span>
                </div>
              </div>
              <div class="preview-messages retro-messages">
                <div class="preview-msg ai">
                  <div class="preview-avatar ai-avatar-retro">遥</div>
                  <div class="preview-bubble ai-bubble-retro">您好！请问您的预算大概是多少呢？</div>
                </div>
                <div class="preview-msg user">
                  <div class="preview-bubble user-bubble-retro">6000左右的游戏本</div>
                  <div class="preview-avatar user-avatar-retro">客</div>
                </div>
              </div>
              <div class="preview-input retro-input">
                <div class="preview-input-bar retro-input-bar">
                  <span>输入您的需求...</span>
                  <span class="send-retro">➤</span>
                </div>
              </div>
            </div>
            <div class="card-info">
              <div class="card-badge" style="background: linear-gradient(135deg, #8B7355, #A89070);">
                Style 8
              </div>
              <h3 class="card-title">复古棕 · 胶片怀旧</h3>
              <p class="card-desc">温暖回忆，岁月如歌</p>
              <div class="card-colors">
                <span class="color-dot" style="background: #8B7355;"></span>
                <span class="color-dot" style="background: #C4A76C;"></span>
                <span class="color-dot" style="background: #4A3728;"></span>
                <span class="color-dot" style="background: #E8DCC8;"></span>
              </div>
              <div class="card-tags">
                <span class="tag">复古</span>
                <span class="tag">胶片</span>
                <span class="tag">怀旧</span>
              </div>
            </div>
            <div class="card-arrow">→</div>
          </div>

          <!-- 方案9：渐变虹 -->
          <div class="design-card gradient-future" @click="openDesign('gradient-future')">
            <div class="card-preview gradient-preview">
              <div class="preview-header gradient-header">
                <div class="preview-nav">
                  <span class="gradient-back">◄</span>
                  <div class="gradient-brand-preview">
                    <span class="gradient-hologram">✦</span>
                    <span class="gradient-brand-text">小遥配配</span>
                  </div>
                  <span class="gradient-pulse"></span>
                </div>
              </div>
              <div class="preview-messages gradient-messages">
                <div class="preview-msg ai">
                  <div class="preview-avatar ai-avatar-gradient">🤖</div>
                  <div class="preview-bubble ai-bubble-gradient">嗨~我是小遥！预算大概是多少呢？✨</div>
                </div>
                <div class="preview-msg user">
                  <div class="preview-bubble user-bubble-gradient">6000左右的游戏本</div>
                  <div class="preview-avatar user-avatar-gradient">😊</div>
                </div>
              </div>
              <div class="preview-input gradient-input">
                <div class="preview-input-bar gradient-input-bar">
                  <span>告诉我您的需求...</span>
                  <span class="send-gradient">✦</span>
                </div>
              </div>
            </div>
            <div class="card-info">
              <div class="card-badge" style="background: linear-gradient(135deg, #FF0080, #00D4FF);">
                Style 9
              </div>
              <h3 class="card-title">渐变虹 · 未来科技</h3>
              <p class="card-desc">梦幻前卫，科技无限</p>
              <div class="card-colors">
                <span class="color-dot" style="background: #FF0080;"></span>
                <span class="color-dot" style="background: #00D4FF;"></span>
                <span class="color-dot" style="background: #FFD700;"></span>
                <span class="color-dot" style="background: #1A0033;"></span>
              </div>
              <div class="card-tags">
                <span class="tag">渐变</span>
                <span class="tag">科技</span>
                <span class="tag">梦幻</span>
              </div>
            </div>
            <div class="card-arrow">→</div>
          </div>

          <!-- 方案10：科技白 -->
          <div class="design-card tech-white" @click="openDesign('tech-white')">
            <div class="card-preview white-preview">
              <div class="preview-header white-header">
                <div class="preview-nav">
                  <svg class="white-back" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M19 12H5M12 19l-7-7 7-7"/>
                  </svg>
                  <div class="white-brand">
                    <span class="white-dot"></span>
                    <span>小遥配配</span>
                  </div>
                  <span class="white-spacer"></span>
                </div>
              </div>
              <div class="preview-messages white-messages">
                <div class="preview-msg ai">
                  <div class="preview-avatar ai-avatar-white">遥</div>
                  <div class="preview-bubble ai-bubble-white">您好！我是小遥，您的AI电脑导购助手。预算大概是多少呢？</div>
                </div>
                <div class="preview-msg user">
                  <div class="preview-bubble user-bubble-white">6000左右的游戏本</div>
                  <div class="preview-avatar user-avatar-white">客</div>
                </div>
              </div>
              <div class="preview-input white-input">
                <div class="preview-input-bar white-input-bar">
                  <span>输入您的需求...</span>
                  <svg class="send-white" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 2L11 13"/>
                    <path d="M22 2L15 22L11 13"/>
                    <path d="M22 2L2 9L11 13"/>
                  </svg>
                </div>
              </div>
            </div>
            <div class="card-info">
              <div class="card-badge" style="background: linear-gradient(135deg, #FF6B35, #FF8C5A);">
                Style 10
              </div>
              <h3 class="card-title">科技白 · 现代清爽</h3>
              <p class="card-desc">纯净明亮，大众首选</p>
              <div class="card-colors">
                <span class="color-dot" style="background: #FFFFFF; border: 1px solid #E8E8EA;"></span>
                <span class="color-dot" style="background: #F7F7F8; border: 1px solid #E8E8EA;"></span>
                <span class="color-dot" style="background: #FF6B35;"></span>
                <span class="color-dot" style="background: #1A1A1A;"></span>
              </div>
              <div class="card-tags">
                <span class="tag">现代</span>
                <span class="tag">清爽</span>
                <span class="tag">大众</span>
              </div>
            </div>
            <div class="card-arrow">→</div>
          </div>
        </div>

        <!-- 底部说明 -->
        <footer class="showcase-footer">
          <div class="footer-content">
            <p class="footer-text">点击卡片预览完整设计</p>
            <div class="footer-info">
              <span>Vue 3 + TypeScript + Vite 5</span>
              <span>·</span>
              <span>10套独立视觉方案</span>
            </div>
          </div>
        </footer>
      </main>
    </div>

    <!-- 设计预览页面 -->
    <div v-else class="design-preview">
      <div class="preview-container">
        <!-- 预览头部 -->
        <header class="preview-header-bar">
          <button class="back-btn" @click="goHome">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            返回导航
          </button>
          <div class="preview-title-info">
            <span class="preview-badge" :class="currentDesign">{{ currentDesignName }}</span>
          </div>
          <div class="spacer"></div>
        </header>

        <!-- 设计内容 -->
        <div class="design-frame">
          <component :is="currentComponent" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineAsyncComponent } from 'vue'

const currentView = ref('home')
const currentDesign = ref('')

// 动态导入设计组件
const designs = {
  'tech-blue': defineAsyncComponent(() => import('../style1-tech-blue/ChatPage.vue')),
  'vibrant-orange': defineAsyncComponent(() => import('../style2-vibrant-orange/ChatPage.vue')),
  'forest-green': defineAsyncComponent(() => import('../style3-forest-green/ChatPage.vue')),
  'cyber-purple': defineAsyncComponent(() => import('../style4-cyber-purple/ChatPage.vue')),
  'candy-pink': defineAsyncComponent(() => import('../style5-candy-pink/ChatPage.vue')),
  'minimal-gray': defineAsyncComponent(() => import('../style6-minimal-gray/ChatPage.vue')),
  'japanese-zen': defineAsyncComponent(() => import('../style7-japanese-zen/ChatPage.vue')),
  'retro-film': defineAsyncComponent(() => import('../style8-retro-film/ChatPage.vue')),
  'gradient-future': defineAsyncComponent(() => import('../style9-gradient-future/ChatPage.vue')),
  'tech-white': defineAsyncComponent(() => import('../style10-tech-white/ChatPage.vue'))
}

const designNames = {
  'tech-blue': '科技蓝风格',
  'vibrant-orange': '活力橙风格',
  'forest-green': '森系绿风格',
  'cyber-purple': '赛博紫风格',
  'candy-pink': '糖果粉风格',
  'minimal-gray': '极简灰风格',
  'japanese-zen': '日式和风风格',
  'retro-film': '复古棕风格',
  'gradient-future': '渐变虹风格',
  'tech-white': '科技白风格'
}

const currentComponent = computed(() => {
  return designs[currentDesign.value]
})

const currentDesignName = computed(() => {
  return designNames[currentDesign.value] || ''
})

const openDesign = (design) => {
  currentDesign.value = design
  currentView.value = 'preview'
}

const goHome = () => {
  currentView.value = 'home'
  currentDesign.value = ''
}
</script>

<style scoped>
/* ==================== 导航页面样式 ==================== */
.design-showcase {
  min-height: 100vh;
}

.showcase-home {
  min-height: 100vh;
  padding: 0;
}

/* 头部 */
.showcase-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  padding: 40px 20px;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.header-content {
  max-width: 1000px;
  margin: 0 auto;
}

.brand {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 16px;
}

.brand-emoji {
  font-size: 48px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.brand-title {
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-subtitle {
  font-size: 16px;
  color: #666;
  font-weight: 400;
}

/* 主内容 */
.showcase-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 32px;
  margin-bottom: 60px;
}

/* 设计卡片 */
.design-card {
  background: white;
  border-radius: 24px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  position: relative;
}

.design-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.card-arrow {
  position: absolute;
  right: 20px;
  bottom: 20px;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  opacity: 0;
  transform: scale(0.5);
  transition: all 0.3s ease;
}

.design-card:hover .card-arrow {
  opacity: 1;
  transform: scale(1);
}

/* 预览区域 */
.card-preview {
  height: 280px;
  background: #f5f7fa;
  position: relative;
  overflow: hidden;
}

.preview-header {
  background: white;
  padding: 12px 16px;
  border-bottom: 1px solid #e1e8ed;
}

.preview-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.preview-back {
  font-size: 24px;
  color: #333;
}

.preview-title {
  font-weight: 600;
  color: #333;
}

.preview-dots {
  font-size: 20px;
  color: #999;
}

.preview-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #333;
}

.preview-messages {
  padding: 16px;
  height: calc(100% - 100px);
  overflow: hidden;
  background: #f5f7fa;
}

.preview-msg {
  display: flex;
  margin-bottom: 16px;
  gap: 8px;
}

.preview-msg.user {
  justify-content: flex-end;
}

.preview-avatar {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.ai-avatar {
  background: linear-gradient(135deg, #4A90E2, #357ABD);
  color: white;
}

.user-avatar {
  background: #e8f4fd;
  color: #4A90E2;
}

.preview-bubble {
  max-width: 200px;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 13px;
  line-height: 1.5;
}

.ai-bubble {
  background: white;
  color: #333;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.user-bubble {
  background: linear-gradient(135deg, #4A90E2, #357ABD);
  color: white;
}

.preview-input {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  padding: 12px 16px;
  border-top: 1px solid #e1e8ed;
}

.preview-input-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #f5f7fa;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 13px;
  color: #999;
}

.preview-send {
  margin-left: auto;
  color: #4A90E2;
  font-size: 16px;
}

/* 活力橙风格预览 */
.preview-header.orange {
  background: rgba(255, 255, 255, 0.95);
}

.preview-messages.orange-bg {
  background: linear-gradient(180deg, #FFF8F3 0%, #FFE8D6 100%);
}

.ai-avatar-orange {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.user-avatar-orange {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #7B68EE, #00D9A5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.ai-bubble-orange {
  background: white;
  color: #2D2D2D;
  border-radius: 18px 18px 18px 4px;
  padding: 10px 14px;
  box-shadow: 0 4px 15px rgba(255, 107, 53, 0.1);
}

.user-bubble-orange {
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
  color: white;
  border-radius: 18px 4px 18px 18px;
  padding: 10px 14px;
}

.preview-input.orange-input {
  background: rgba(255, 255, 255, 0.95);
}

.preview-input-bar .emoji-icon {
  font-size: 16px;
}

.preview-send-orange {
  margin-left: auto;
  font-size: 16px;
}

/* 森系绿风格预览 */
.preview-header.forest {
  background: rgba(250, 249, 246, 0.95);
  border-bottom-color: rgba(93, 138, 102, 0.15);
}

.natural-nav {
  align-items: center;
}

.natural-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  color: #3A3A3A;
  font-weight: 500;
}

.brand-leaf {
  font-size: 16px;
}

.natural-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #6B6B6B;
}

.natural-status .status-dot {
  width: 6px;
  height: 6px;
  background: #5D8A66;
  border-radius: 50%;
}

.preview-messages.forest-bg {
  background: #FAF9F6;
}

.ai-avatar-forest {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #8FB996, #B8D4BF);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.user-avatar-forest {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #F5E6D3, #E8B4A0);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 500;
  color: #D4A574;
}

.ai-bubble-forest {
  background: white;
  color: #3A3A3A;
  border-radius: 4px 14px 14px 14px;
  padding: 10px 14px;
  border: 1px solid rgba(93, 138, 102, 0.15);
  font-size: 13px;
}

.user-bubble-forest {
  background: linear-gradient(135deg, #5D8A66, #8FB996);
  color: white;
  border-radius: 14px 4px 14px 14px;
  padding: 10px 14px;
  font-size: 13px;
}

.preview-input.forest-input {
  background: rgba(250, 249, 246, 0.98);
  border-top-color: rgba(93, 138, 102, 0.15);
}

.preview-input-bar.natural-input {
  background: white;
  border: 1px solid rgba(93, 138, 102, 0.15);
  border-radius: 14px;
}

.preview-send-forest {
  margin-left: auto;
  color: #5D8A66;
}

/* 卡片信息 */
.card-info {
  padding: 24px;
  position: relative;
}

.card-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 20px;
  color: white;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.card-title {
  font-size: 22px;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
}

.card-desc {
  font-size: 14px;
  color: #999;
  margin-bottom: 16px;
}

.card-colors {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.color-dot {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tag {
  padding: 6px 12px;
  background: #f5f7fa;
  border-radius: 16px;
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

/* 底部 */
.showcase-footer {
  text-align: center;
  padding: 40px 20px;
}

.footer-content {
  max-width: 600px;
  margin: 0 auto;
}

.footer-text {
  font-size: 18px;
  color: white;
  font-weight: 500;
  margin-bottom: 16px;
}

.footer-info {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
}

.footer-info span {
  margin: 0 8px;
}

/* ==================== 预览页面样式 ==================== */
.design-preview {
  min-height: 100vh;
  background: #f5f7fa;
}

.preview-container {
  max-width: 600px;
  margin: 0 auto;
  min-height: 100vh;
  background: white;
  display: flex;
  flex-direction: column;
}

.preview-header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: white;
  border-bottom: 1px solid #e1e8ed;
  position: sticky;
  top: 0;
  z-index: 100;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid #e1e8ed;
  background: white;
  border-radius: 8px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: #f5f7fa;
  border-color: #4A90E2;
  color: #4A90E2;
}

.preview-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: white;
}

.preview-badge.tech-blue {
  background: linear-gradient(135deg, #4A90E2, #357ABD);
}

.preview-badge.vibrant-orange {
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
}

.preview-badge.forest-green {
  background: linear-gradient(135deg, #5D8A66, #8FB996);
}

.preview-badge.cyber-purple {
  background: linear-gradient(135deg, #9D4EDD, #10002B);
}

.preview-badge.candy-pink {
  background: linear-gradient(135deg, #FFB6D9, #FF8AB3);
}

.preview-badge.minimal-gray {
  background: linear-gradient(135deg, #2C2C2C, #3A3A3A);
}

.preview-badge.japanese-zen {
  background: linear-gradient(135deg, #C8553D, #E07A5F);
}

.preview-badge.retro-film {
  background: linear-gradient(135deg, #8B7355, #A89070);
}

.preview-badge.gradient-future {
  background: linear-gradient(135deg, #FF0080, #00D4FF);
}

.preview-badge.tech-white {
  background: linear-gradient(135deg, #FF6B35, #FF8C5A);
}

.spacer {
  width: 100px;
}

.design-frame {
  flex: 1;
  overflow: hidden;
}

/* ==================== 赛博紫预览样式 ==================== */
.dark-preview {
  background: #10002B;
  position: relative;
}

.cyber-header {
  background: rgba(16, 0, 43, 0.95);
  border-bottom: 2px solid #9D4EDD;
}

.preview-brand-cyber {
  font-family: 'Courier New', monospace;
  font-size: 14px;
  font-weight: 700;
  color: #E0AAFF;
  letter-spacing: 2px;
}

.cyber-messages {
  background: #10002B;
}

.ai-avatar-cyber {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #9D4EDD, #240046);
  border: 2px solid #9D4EDD;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.ai-bubble-cyber {
  background: rgba(157, 78, 221, 0.1);
  border: 1px solid rgba(157, 78, 221, 0.5);
  color: #E0AAFF;
  font-family: 'Courier New', monospace;
  font-size: 11px;
}

.user-bubble-cyber {
  background: rgba(0, 217, 255, 0.15);
  border: 1px solid rgba(0, 217, 255, 0.5);
  color: #00D9FF;
}

.user-avatar-cyber {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #240046, #00D9FF);
  border: 2px solid #00D9FF;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: #00D9FF;
}

.cyber-input {
  background: rgba(16, 0, 43, 0.95);
  border-top: 2px solid #9D4EDD;
}

.prompt-sign {
  color: #39FF14;
  font-size: 16px;
}

.send-cyber {
  color: #9D4EDD;
  font-size: 14px;
}

/* ==================== 糖果粉预览样式 ==================== */
.candy-header {
  background: rgba(255, 240, 247, 0.95);
  border-bottom: 3px solid #FFB6D9;
}

.preview-brand-candy {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 700;
  color: #FF8AB3;
}

.candy-messages {
  background: #FFF0F7;
}

.ai-avatar-candy {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #FFB6D9, #B8E6FF);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.ai-bubble-candy {
  background: white;
  border: 2px solid #FFCDE6;
  border-radius: 18px 18px 18px 6px;
  color: #5A5A5A;
  font-size: 12px;
}

.user-bubble-candy {
  background: linear-gradient(135deg, #FFB6D9, #FFCDE6);
  border-radius: 18px 6px 18px 18px;
  color: white;
  font-size: 12px;
}

.user-avatar-candy {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #B8E6FF, #C8F7DC);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.candy-input {
  background: rgba(255, 255, 255, 0.98);
  border-top: 3px solid #FFB6D9;
}

.send-candy {
  font-size: 16px;
}

/* ==================== 极简灰预览样式 ==================== */
.minimal-preview {
  background: #FAFAFA;
}

.minimal-header {
  background: white;
  border-bottom: 1px solid #E8E8E8;
}

.minimal-back-icon {
  font-size: 18px;
  color: #8A8A8A;
}

.preview-brand-minimal {
  font-size: 14px;
  font-weight: 500;
  color: #2C2C2C;
}

.spacer-mini {
  width: 18px;
}

.minimal-messages {
  background: #FAFAFA;
}

.ai-avatar-minimal {
  width: 32px;
  height: 32px;
  background: #2C2C2C;
  color: white;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.ai-bubble-minimal {
  background: white;
  border: 1px solid #E8E8E8;
  border-radius: 12px;
  color: #2C2C2C;
  font-size: 12px;
}

.user-bubble-minimal {
  background: #2C2C2C;
  border-radius: 12px;
  color: white;
  font-size: 12px;
}

.user-avatar-minimal {
  width: 32px;
  height: 32px;
  background: #E8E8E8;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 500;
  color: #8A8A8A;
}

.minimal-input {
  background: white;
  border-top: 1px solid #E8E8E8;
}

.minimal-input-bar {
  background: #FAFAFA;
  border: 1px solid #E8E8E8;
  border-radius: 12px;
  font-size: 12px;
  color: #8A8A8A;
}

.send-minimal {
  color: #2C2C2C;
}

/* ==================== 日式和风预览样式 ==================== */
.zen-preview {
  background: #F5F0E8;
}

.zen-header {
  background: rgba(245, 240, 232, 0.95);
  border-bottom: 1px solid #E8DFD1;
}

.zen-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.zen-back {
  font-size: 28px;
  color: #6B5B4F;
}

.zen-brand-preview {
  display: flex;
  align-items: center;
  gap: 12px;
}

.zen-seal-preview {
  width: 32px;
  height: 32px;
  background: #C8553D;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.zen-brand-vertical {
  font-size: 14px;
  color: #3D3D3D;
  letter-spacing: 2px;
  font-weight: 500;
}

.zen-dot {
  width: 8px;
  height: 8px;
  background: #C8553D;
  border-radius: 50%;
}

.zen-messages {
  background: #F5F0E8;
}

.ai-avatar-zen {
  width: 32px;
  height: 32px;
  background: white;
  border: 2px solid #C8553D;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #C8553D;
}

.user-avatar-zen {
  width: 32px;
  height: 32px;
  background: #E8DFD1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #6B5B4F;
}

.ai-bubble-zen {
  background: white;
  color: #3D3D3D;
  border-radius: 4px 14px 14px 14px;
  padding: 10px 14px;
  border: 1px solid #E8DFD1;
  font-size: 12px;
}

.user-bubble-zen {
  background: #C8553D;
  color: white;
  border-radius: 14px 4px 14px 14px;
  padding: 10px 14px;
  font-size: 12px;
}

.zen-input {
  background: rgba(245, 240, 232, 0.98);
  border-top: 1px solid #E8DFD1;
}

.zen-input-bar {
  background: white;
  border: 1px solid #B8956B;
  border-radius: 4px;
  font-size: 12px;
  color: #6B5B4F;
}

.send-zen {
  margin-left: auto;
  color: #C8553D;
}

/* ==================== 复古棕预览样式 ==================== */
.retro-preview {
  background: #E8DCC8;
}

.retro-header {
  background: rgba(232, 220, 200, 0.95);
  border-bottom: 2px solid #8B7355;
}

.retro-back {
  font-size: 18px;
  color: #4A3728;
}

.retro-brand-preview {
  font-size: 14px;
  font-weight: 600;
  color: #4A3728;
  font-family: 'Courier New', monospace;
}

.retro-rec {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #D32F2F;
  font-weight: 600;
}

.retro-messages {
  background: #E8DCC8;
}

.ai-avatar-retro {
  width: 36px;
  height: 36px;
  background: white;
  padding: 4px;
  box-shadow: 2px 2px 0 #8B7355;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #8B7355;
}

.user-avatar-retro {
  width: 36px;
  height: 36px;
  background: #C4A76C;
  padding: 4px;
  box-shadow: 2px 2px 0 #6B5544;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #4A3728;
}

.ai-bubble-retro {
  background: #F5F1E8;
  color: #4A3728;
  border-radius: 4px;
  padding: 10px 14px;
  box-shadow: 3px 3px 0 #8B7355;
  font-size: 12px;
  font-family: 'Courier New', monospace;
}

.user-bubble-retro {
  background: #8B7355;
  color: #F5F1E8;
  border-radius: 4px;
  padding: 10px 14px;
  box-shadow: 3px 3px 0 #6B5544;
  font-size: 12px;
}

.retro-input {
  background: rgba(232, 220, 200, 0.98);
  border-top: 2px solid #8B7355;
}

.retro-input-bar {
  background: #F5F1E8;
  border: 2px solid #8B7355;
  border-radius: 4px;
  font-size: 12px;
  color: #6B5544;
}

.send-retro {
  margin-left: auto;
  color: #8B7355;
}

/* ==================== 渐变虹预览样式 ==================== */
.gradient-preview {
  background: #1A0033;
  position: relative;
}

.gradient-preview::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 30% 20%, rgba(255, 0, 128, 0.4) 0%, transparent 50%),
    radial-gradient(circle at 70% 80%, rgba(0, 212, 255, 0.4) 0%, transparent 50%);
  pointer-events: none;
}

.gradient-header {
  background: rgba(45, 10, 78, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
}

.gradient-back {
  font-size: 18px;
  color: white;
}

.gradient-brand-preview {
  display: flex;
  align-items: center;
  gap: 8px;
}

.gradient-hologram {
  font-size: 20px;
  background: linear-gradient(135deg, #FF0080, #00D4FF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.gradient-brand-text {
  font-size: 14px;
  font-weight: 600;
  background: linear-gradient(135deg, white, #00D4FF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.gradient-pulse {
  width: 12px;
  height: 12px;
  background: #00D4FF;
  border-radius: 50%;
  box-shadow: 0 0 10px #00D4FF;
}

.gradient-messages {
  background: #1A0033;
  position: relative;
}

.ai-avatar-gradient {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #FF0080, #7928CA);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.user-avatar-gradient {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #00D4FF, #00FFF5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.ai-bubble-gradient {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  border-radius: 4px 16px 16px 16px;
  padding: 10px 14px;
  font-size: 12px;
}

.user-bubble-gradient {
  background: linear-gradient(135deg, rgba(255, 0, 128, 0.4), rgba(121, 40, 202, 0.3));
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  border-radius: 16px 16px 4px 16px;
  padding: 10px 14px;
  font-size: 12px;
}

.gradient-input {
  background: rgba(45, 10, 78, 0.8);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255, 255, 255, 0.15);
}

.gradient-input-bar {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
}

.send-gradient {
  margin-left: auto;
  background: linear-gradient(135deg, #FF0080, #00D4FF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* ==================== 科技白预览样式 ==================== */
.white-preview {
  background: #FFFFFF;
}

.white-header {
  background: white;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.white-back {
  color: #6B7280;
}

.white-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.white-dot {
  width: 8px;
  height: 8px;
  background: #FF6B35;
  border-radius: 50%;
}

.white-spacer {
  width: 20px;
}

.white-messages {
  background: white;
}

.ai-avatar-white {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #FF6B35, #FF8C5A);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: white;
  font-weight: 600;
}

.user-avatar-white {
  width: 36px;
  height: 36px;
  background: #F7F7F8;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #6B7280;
}

.ai-bubble-white {
  background: #F7F7F8;
  color: #1A1A1A;
  border-radius: 14px;
  padding: 10px 14px;
  font-size: 12px;
  line-height: 1.6;
}

.user-bubble-white {
  background: #FF6B35;
  color: white;
  border-radius: 14px;
  padding: 10px 14px;
  font-size: 12px;
}

.white-input {
  background: white;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}

.white-input-bar {
  background: #F7F7F8;
  border-radius: 20px;
  padding: 10px 14px;
  font-size: 12px;
  color: #9CA3AF;
}

.send-white {
  margin-left: auto;
  color: #FF6B35;
}

/* 响应式 */
@media (max-width: 768px) {
  .brand-title {
    font-size: 24px;
  }

  .cards-container {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .preview-header-bar {
    padding: 12px 16px;
  }

  .back-btn {
    padding: 6px 12px;
    font-size: 13px;
  }

  .spacer {
    width: 60px;
  }
}
</style>
