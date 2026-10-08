<template>
  <header
    class="join-header"
    data-ws-part="home.header"
  >
    <div
      class="brand-lockup"
      data-ws-part="home.brand"
    >
      <img
        class="brand-mark"
        src="/网站图标.jpg"
        alt="WebSpeak"
      />
      <div>
        <strong :title="brandName">{{ brandName }}</strong>
        <small>{{ t("browserWorkspace") }}</small>
      </div>
    </div>
    <div
      class="header-tools"
      data-ws-part="home.header-tools"
    >
      <a
        class="github-link"
        href="https://github.com/c0febean/WebSpeak-client-for-TeamSpeak"
        target="_blank"
        rel="noreferrer"
        :title="t('githubRepository')"
        :aria-label="t('githubRepository')"
      >{{ t("githubRepository") }}</a>
      <button
        type="button"
        class="theme-toggle"
        data-ws-part="control"
        :aria-label="darkTheme ? t('switchToLightTheme') : t('switchToDarkTheme')"
        :title="darkTheme ? t('switchToLightTheme') : t('switchToDarkTheme')"
        :aria-pressed="darkTheme"
        @click="emit('themeToggle')"
      >
        <span
          class="theme-toggle-track"
          :class="{ dark: darkTheme }"
          aria-hidden="true"
        >
          <span class="theme-toggle-option theme-toggle-moon"><Icon name="moon" :size="12" /></span>
          <span class="theme-toggle-option theme-toggle-sun"><Icon name="sun" :size="12" /></span>
          <span class="theme-toggle-thumb"></span>
        </span>
      </button>
      <LanguageSwitcher
        v-model="language"
        class="join-language-switcher"
        compact
        :menu-label="t('languageMenu')"
        @change="emit('languageChange')"
      />
    </div>
  </header>
</template>

<script setup lang="ts">
import Icon from "../Icon.vue";
import LanguageSwitcher from "../LanguageSwitcher.vue";
import type { Language } from "../../i18n/web-client.js";

defineProps<{
  brandName: string;
  darkTheme: boolean;
  t: (key: string, variables?: Record<string, string | number>) => string;
}>();
const language = defineModel<Language>("language", { required: true });
const emit = defineEmits<{
  themeToggle: [];
  languageChange: [];
}>();
</script>

<style scoped>
.join-header { display: flex; align-items: center; justify-content: space-between; gap: 20px; }
.brand-lockup { min-width: 0; max-width: 100%; }
.brand-lockup > div { min-width: 0; }
.brand-mark { flex: 0 0 auto; }
.brand-lockup strong { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.header-tools { display: flex; align-items: center; justify-content: flex-end; gap: 13px; }
.github-link { color: inherit; font-size: 11px; text-decoration: none; transition: color .16s ease; }
.github-link:hover, .github-link:focus-visible { color: var(--terminal-accent, currentColor); }
.theme-toggle { display: inline-flex; padding: 0; color: inherit; background: transparent; border: 0; border-radius: 999px; cursor: pointer; }
.theme-toggle:focus-visible { outline: 2px solid var(--terminal-accent, currentColor); outline-offset: 4px; }
.theme-toggle-track { position: relative; display: grid; grid-template-columns: repeat(2, 22px); width: 46px; height: 24px; align-items: center; padding: 2px; overflow: hidden; background: rgba(127, 127, 127, .16); border: 1px solid currentColor; border-color: color-mix(in srgb, currentColor 22%, transparent); border-radius: 999px; }
.theme-toggle-option { position: relative; z-index: 1; display: grid; place-items: center; color: currentColor; opacity: .55; transition: color .16s ease, opacity .16s ease; }
.theme-toggle-track:not(.dark) .theme-toggle-sun,
.theme-toggle-track.dark .theme-toggle-moon { color: var(--terminal-accent, currentColor); opacity: 1; }
.theme-toggle-thumb { position: absolute; z-index: 0; top: 2px; left: 2px; width: 20px; height: 18px; background: currentColor; border-radius: 999px; opacity: .14; transition: transform .2s ease, background .16s ease; }
.theme-toggle-track:not(.dark) .theme-toggle-thumb { transform: translateX(20px); }
.theme-toggle-track.dark .theme-toggle-thumb { background: var(--terminal-accent, currentColor); opacity: .22; }
</style>
