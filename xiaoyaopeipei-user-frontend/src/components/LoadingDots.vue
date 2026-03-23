<template>
  <div class="loading-dots">
    <span class="dot"></span>
    <span class="dot"></span>
    <span class="dot"></span>
  </div>
</template>

<style lang="less" scoped>
.loading-dots {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-md);
}

.dot {
  width: 8px;
  height: 8px;
  background: var(--gradient-primary);
  border-radius: 50%;
  animation: bounce 1.4s ease-in-out infinite both;
  box-shadow: 0 0 8px rgba(255, 107, 53, 0.4);

  &:nth-child(1) {
    animation-delay: -0.32s;
  }

  &:nth-child(2) {
    animation-delay: -0.16s;
  }
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
