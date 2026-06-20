<script setup lang="ts">
type HighlightItem = {
  title: string
  description: string
}

defineProps<{
  title: string
  description: string
  caption: string
  highlights: HighlightItem[]
}>()
</script>

<template>
  <div class="auth-layout">
    <a
      class="auth-layout__intro-link"
      href="https://info.campustreex.com"
      target="_blank"
      rel="noopener noreferrer"
    >
      项目介绍
    </a>

    <section class="auth-layout__aside">
      <RouterLink class="auth-layout__brand" to="/" aria-label="CampusTree 首页">
        <span class="auth-layout__brand-mark">CT</span>
        <span class="auth-layout__brand-copy">
          <strong>CampusTree</strong>
          <small>匿名校园树洞</small>
        </span>
      </RouterLink>

      <div class="auth-layout__hero">
        <p class="auth-layout__caption">{{ caption }}</p>
        <h1 class="auth-layout__title">{{ title }}</h1>
        <p class="auth-layout__description">{{ description }}</p>
      </div>

      <div class="auth-layout__highlights">
        <article v-for="item in highlights" :key="item.title" class="auth-layout__highlight">
          <h2>{{ item.title }}</h2>
          <p>{{ item.description }}</p>
        </article>
      </div>
    </section>

    <main class="auth-layout__main">
      <div class="auth-layout__panel">
        <slot />
      </div>
    </main>
  </div>
</template>

<style scoped>
.auth-layout {
  position: relative;
  min-height: 100vh;
  display: grid;
  grid-template-columns: minmax(320px, 520px) minmax(0, 1fr);
  background:
    radial-gradient(circle at top left, rgba(16, 185, 129, 0.18), transparent 30%),
    radial-gradient(circle at bottom right, rgba(59, 130, 246, 0.12), transparent 28%),
    linear-gradient(180deg, #f5fbf8 0%, #f9fafb 100%);
}

.auth-layout__intro-link {
  position: absolute;
  top: var(--space-24);
  right: var(--space-24);
  z-index: 2;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
  padding: 0 var(--space-16);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: var(--radius-8);
  color: var(--color-primary);
  font-size: 14px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.86);
  box-shadow: var(--shadow-card);
  backdrop-filter: blur(14px);
  transition:
    color 200ms ease,
    border-color 200ms ease,
    background-color 200ms ease,
    transform 120ms ease,
    box-shadow 200ms ease;
}

.auth-layout__intro-link:hover,
.auth-layout__intro-link:focus-visible {
  color: #059669;
  border-color: rgba(5, 150, 105, 0.48);
  background: #ffffff;
  box-shadow: var(--shadow-hover);
  transform: translateY(-1px);
}

.auth-layout__aside {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: var(--space-32);
  padding: var(--space-32);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.72) 0%, rgba(235, 250, 244, 0.92) 100%);
  border-right: 1px solid rgba(229, 231, 235, 0.76);
}

.auth-layout__brand {
  display: inline-flex;
  align-items: center;
  gap: var(--space-12);
  width: fit-content;
}

.auth-layout__brand-mark {
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border-radius: 16px;
  color: #ffffff;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.08em;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 12px 28px rgba(16, 185, 129, 0.24);
}

.auth-layout__brand-copy {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.auth-layout__brand-copy strong {
  color: var(--color-text-primary);
  font-size: 20px;
  font-weight: 700;
}

.auth-layout__brand-copy small {
  color: var(--color-text-secondary);
  font-size: 12px;
}

.auth-layout__hero {
  display: flex;
  flex-direction: column;
  gap: var(--space-12);
}

.auth-layout__caption {
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.auth-layout__title {
  color: var(--color-text-primary);
  font-size: 40px;
  line-height: 1.2;
}

.auth-layout__description {
  max-width: 34ch;
  color: var(--color-text-secondary);
  font-size: 16px;
  line-height: 1.75;
}

.auth-layout__highlights {
  display: grid;
  gap: var(--space-16);
}

.auth-layout__highlight {
  padding: var(--space-16);
  border: 1px solid rgba(229, 231, 235, 0.72);
  border-radius: var(--radius-12);
  background: rgba(255, 255, 255, 0.74);
  box-shadow: var(--shadow-card);
}

.auth-layout__highlight h2 {
  margin-bottom: var(--space-8);
  color: var(--color-text-primary);
  font-size: 18px;
  font-weight: 600;
  line-height: 1.5;
}

.auth-layout__highlight p {
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.7;
}

.auth-layout__main {
  display: grid;
  place-items: center;
  padding: var(--space-24);
}

.auth-layout__panel {
  width: min(100%, 520px);
}

@media (max-width: 1023px) {
  .auth-layout {
    grid-template-columns: minmax(0, 1fr);
  }

  .auth-layout__aside {
    padding: var(--space-24);
    border-right: 0;
    border-bottom: 1px solid rgba(229, 231, 235, 0.76);
  }

  .auth-layout__description {
    max-width: 100%;
  }
}

@media (max-width: 767px) {
  .auth-layout__intro-link {
    top: var(--space-16);
    right: var(--space-16);
    min-height: 36px;
    padding: 0 var(--space-12);
    font-size: 13px;
  }

  .auth-layout__aside,
  .auth-layout__main {
    padding: var(--space-16);
  }

  .auth-layout__title {
    font-size: 32px;
  }
}
</style>
