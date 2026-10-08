<template>
  <div
    class="terminal-home"
    :data-theme="darkTheme ? 'dark' : 'light'"
    data-ws-part="home.terminal-shell"
    :data-ws-state="systemState"
  >
    <div
      class="terminal-ambient"
      data-ws-part="home.ambient"
      aria-hidden="true"
    ></div>

    <div
      class="terminal-corner terminal-corner-tl"
      data-ws-part="home.terminal-corner"
      data-ws-position="top-left"
    >
      <span class="terminal-corner-dot" aria-hidden="true"></span>
      {{ topLeftStatus }}
    </div>
    <div
      class="terminal-corner terminal-corner-tr"
      data-ws-part="home.terminal-corner"
      data-ws-position="top-right"
    >
      {{ topRightStatus }}
    </div>
    <div
      class="terminal-corner terminal-corner-bl"
      data-ws-part="home.terminal-corner"
      data-ws-position="bottom-left"
    >
      <span>{{ bottomLeftStatus }}</span>
      <span class="terminal-cursor" aria-hidden="true"></span>
    </div>
    <div
      class="terminal-corner terminal-corner-br"
      data-ws-part="home.terminal-corner"
      data-ws-position="bottom-right"
    >
      <span class="terminal-visitor-readout">
        <span>VISITORS</span>
        <strong>{{ visitorReadout }}</strong>
      </span>
      <span class="terminal-corner-separator" aria-hidden="true">//</span>
      <span class="terminal-corner-metric">
        RELAY_NODES: <strong>{{ accelerationRelays.length }}</strong>
      </span>
    </div>

    <WebClientHeader
      v-model:language="language"
      :brand-name="skinHomeCopy.brandName || siteName"
      :dark-theme="darkTheme"
      :t="t"
      @theme-toggle="emit('themeToggle')"
      @language-change="emit('languageChange')"
    />

    <main
      class="terminal-content"
      data-ws-part="home.content"
    >
      <section
        class="terminal-hero"
        data-ws-part="home.hero"
      >
        <div
          v-if="skinHomeCopy.eyebrow"
          class="terminal-kicker"
          data-ws-part="home.hero.eyebrow"
        >
          <span class="terminal-kicker-dot" aria-hidden="true"></span>
          {{ skinHomeCopy.eyebrow }}
        </div>
        <h1 data-ws-part="home.hero.title">{{ terminalTitle }}</h1>
        <p data-ws-part="home.hero.description">{{ terminalDescription }}</p>
      </section>

      <section
        :class="['terminal-launch-card', { 'has-error': hasConnectionError }]"
        data-ws-part="home.join-card"
        :data-ws-state="hasConnectionError ? 'error' : connecting ? 'connecting' : 'ready'"
      >
        <div
          v-if="errorMessage"
          class="terminal-notice terminal-notice-error"
          data-ws-part="home.notice"
          data-ws-state="error"
          role="alert"
        >
          <span class="terminal-notice-symbol">!</span>
          <span class="terminal-notice-copy">
            <span>{{ errorMessage }}</span>
            <code v-if="errorCode">{{ t("errorCode") }}: {{ errorCode }}</code>
          </span>
        </div>
        <div
          v-if="browserErrorMessage"
          class="terminal-notice terminal-notice-warning"
          data-ws-part="home.notice"
          data-ws-state="warning"
          role="alert"
        >
          <span class="terminal-notice-symbol">i</span>
          <span>{{ browserErrorMessage }}</span>
        </div>
        <div
          v-if="!serverConfigLoading && !initialized"
          class="terminal-notice terminal-notice-warning"
          data-ws-part="home.notice"
          data-ws-state="unconfigured"
          role="status"
        >
          <span class="terminal-notice-symbol">i</span>
          <span>{{ t("notConfigured") }} <a href="/admin">{{ t("configureNow") }}</a></span>
        </div>
        <div
          v-if="!localPersistenceAvailable"
          class="terminal-notice terminal-notice-warning"
          data-ws-part="home.notice"
          data-ws-state="storage-warning"
          role="status"
        >
          <span class="terminal-notice-symbol">i</span>
          <span>{{ t("localPersistenceUnavailable") }}</span>
        </div>

        <JoinForm
          v-if="initialized"
          layout="terminal"
          :autofocus-nickname="autofocusNickname"
          v-model:server-host="serverHost"
          v-model:server-port="serverPort"
          v-model:server-password="serverPassword"
          v-model:nickname="nickname"
          v-model:channel="channel"
          v-model:remember-identity="rememberIdentity"
          v-model:acceleration-relay-id="accelerationRelayId"
          :access-mode="accessMode"
          :open-target-prefill-blocked="openTargetPrefillBlocked"
          :acceleration-relays="accelerationRelays"
          :favorite-servers="favoriteServers"
          :recent-servers="recentServers"
          :is-favorite="isFavorite"
          :identity-export-busy="identityExportBusy"
          :has-identity="hasIdentity"
          :connecting="connecting"
          :join-disabled="joinDisabled"
          :t="t"
          @connect="emit('connect')"
          @disconnect="emit('disconnect')"
          @select-server="onSelectServer"
          @toggle-favorite="emit('toggleFavorite')"
          @import-identity="emit('importIdentity')"
          @export-identity="emit('exportIdentity')"
        />

        <div
          class="terminal-security-note"
          data-ws-part="home.security-note"
        >
          <span class="terminal-security-mark" aria-hidden="true">↯</span>
          {{ t("connectionAuthorized") }}
        </div>
      </section>

      <div
        class="terminal-facts"
        data-ws-part="home.terminal-facts"
        aria-live="polite"
      >
        <span>{{ targetFact }}</span>
        <span class="terminal-fact-separator" aria-hidden="true">·</span>
        <span>{{ storageFact }}</span>
      </div>
    </main>

    <footer
      class="terminal-footer"
      data-ws-part="home.footer"
    >
      <div class="terminal-footer-left">
        <span>v{{ appVersion || "—" }}</span>
        <span class="terminal-footer-separator" aria-hidden="true">·</span>
        <span>{{ t("browserWorkspace") }}</span>
        <span class="terminal-footer-separator" aria-hidden="true">·</span>
        <span class="terminal-footer-accent">CODEC: OPUS 48KHZ</span>
      </div>
      <div class="terminal-footer-right">
        <span>{{ footerLinkStatus }}</span>
        <span class="terminal-footer-separator" aria-hidden="true">·</span>
        <button
          type="button"
          data-ws-part="control"
          @click="emit('clearLocalData')"
        >
          {{ t("clearLocalData") }}
        </button>
        <span class="terminal-footer-separator" aria-hidden="true">·</span>
        <span>{{ t("browserSupport") }}</span>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import JoinForm from "./JoinForm.vue";
import WebClientHeader from "./WebClientHeader.vue";
import type { FavoriteServer, RecentServer } from "../../services/local-persistence.js";
import type { SkinHomeCopy } from "../../services/skin-pack.js";
import type { Language } from "../../i18n/web-client.js";

const language = defineModel<Language>("language", { required: true });
const serverHost = defineModel<string>("serverHost", { required: true });
const serverPort = defineModel<string>("serverPort", { required: true });
const serverPassword = defineModel<string>("serverPassword", { required: true });
const nickname = defineModel<string>("nickname", { required: true });
const channel = defineModel<string>("channel", { required: true });
const rememberIdentity = defineModel<boolean>("rememberIdentity", { required: true });
const accelerationRelayId = defineModel<string>("accelerationRelayId", { required: true });

const props = defineProps<{
  siteName: string;
  appVersion: string;
  darkTheme: boolean;
  skinHomeCopy: SkinHomeCopy;
  welcomeText: string;
  accessMode: "fixed" | "open";
  initialized: boolean;
  serverConfigLoading: boolean;
  openTargetPrefillBlocked: boolean;
  accelerationRelays: ReadonlyArray<{ id: string; name: string }>;
  favoriteServers: readonly FavoriteServer[];
  recentServers: readonly RecentServer[];
  isFavorite: boolean;
  identityExportBusy: boolean;
  hasIdentity: boolean;
  localPersistenceAvailable: boolean;
  visitorNumber: number | null;
  visitorTotal: number | null;
  connecting: boolean;
  joinDisabled: boolean;
  autofocusNickname: boolean;
  errorMessage: string;
  errorCode: string;
  browserErrorMessage: string;
  t: (key: string, variables?: Record<string, string | number>) => string;
}>();

const emit = defineEmits<{
  themeToggle: [];
  languageChange: [];
  connect: [];
  disconnect: [];
  selectServer: [address: string, nickname?: string];
  toggleFavorite: [];
  importIdentity: [];
  exportIdentity: [];
  clearLocalData: [];
}>();

function onSelectServer(address: string, selectedNickname?: string): void {
  emit("selectServer", address, selectedNickname);
}

const hasConnectionError = computed(() => Boolean(props.errorMessage || props.browserErrorMessage));
const terminalTitle = computed(() => props.skinHomeCopy.welcomeTitle || props.skinHomeCopy.title || props.t("welcomeBack"));
const terminalDescription = computed(() => props.t("browserVoiceLead"));
const systemState = computed(() => {
  if (props.serverConfigLoading) return "configuring";
  if (!props.initialized) return "unconfigured";
  if (props.errorMessage || props.browserErrorMessage) return "error";
  if (props.connecting) return "connecting";
  return "ready";
});
const systemCode = computed(() => systemState.value.toUpperCase());
const topLeftStatus = computed(() => `WEBSPEAK // ${props.accessMode === "fixed" ? "FIXED_TARGET" : "OPEN_TARGET"}`);
const topRightStatus = computed(() => `STATUS: ${systemCode.value} // ACCESS: ${props.accessMode === "fixed" ? "RESTRICTED" : "OPEN"}`);
const bottomLeftStatus = computed(() => `SYS_LOG: ${systemCode.value}`);
const visitorReadout = computed(() => {
  const visitors = props.visitorNumber == null
    ? "—"
    : props.visitorTotal == null
      ? String(props.visitorNumber)
      : `${props.visitorNumber}/${props.visitorTotal}`;
  return visitors;
});
const targetFact = computed(() => props.accessMode === "fixed" ? "TARGET: INSTANCE_DEFAULT" : "TARGET: USER_SELECTABLE");
const storageFact = computed(() => props.localPersistenceAvailable ? "STATE: PERSISTENT" : "STATE: SESSION_ONLY");
const footerLinkStatus = computed(() => {
  if (props.serverConfigLoading) return "GATEWAY: CONFIGURING";
  if (!props.initialized) return "GATEWAY: OFFLINE";
  if (props.errorMessage || props.browserErrorMessage) return "GATEWAY: ATTENTION";
  if (props.connecting) return "GATEWAY: CONNECTING";
  return "GATEWAY: READY";
});
</script>

<style scoped>
.terminal-home {
  --terminal-bg: #0b0c0e;
  --terminal-surface: #141619;
  --terminal-surface-hover: #1c1f24;
  --terminal-border: rgba(255, 255, 255, .08);
  --terminal-border-focus: rgba(45, 212, 191, .46);
  --terminal-border-error: rgba(239, 68, 68, .55);
  --terminal-text: #f4f4f5;
  --terminal-muted: #a0a0a9;
  --terminal-secondary: rgba(244, 244, 245, .68);
  --terminal-subtle: rgba(244, 244, 245, .53);
  --terminal-corner: rgba(244, 244, 245, .54);
  --terminal-error: #f87171;
  --terminal-error-bg: rgba(127, 29, 29, .16);
  --terminal-error-border: rgba(239, 68, 68, .22);
  --terminal-warning: #d8b66d;
  --terminal-warning-bg: rgba(117, 83, 25, .12);
  --terminal-warning-border: rgba(214, 169, 72, .2);
  --terminal-separator: rgba(244, 244, 245, .24);
  --terminal-accent: #2dd4bf;
  --terminal-accent-soft: rgba(45, 212, 191, .12);
  --terminal-focus-glow: rgba(45, 212, 191, .14);
  --terminal-error-glow: rgba(239, 68, 68, .14);
  --terminal-field-bg: rgba(0, 0, 0, .22);
  --terminal-field-bg-soft: rgba(0, 0, 0, .16);
  --terminal-button-text: #0b0c0e;
  --terminal-button-bg: #f4f4f5;
  --terminal-button-hover: #fff;
  --terminal-button-disabled-text: #71717a;
  --terminal-button-disabled-bg: #d4d4d8;
  --terminal-shadow: 0 28px 64px rgba(0, 0, 0, .56), 0 6px 16px rgba(0, 0, 0, .28), inset 0 1px 0 rgba(255, 255, 255, .04);
  --terminal-focus-shadow: var(--terminal-shadow), 0 0 0 3px var(--terminal-accent-soft), 0 0 30px var(--terminal-focus-glow);
  --terminal-ambient: radial-gradient(circle at 50% 0%, rgba(255, 255, 255, .07), transparent 58%), linear-gradient(135deg, transparent 0 49.5%, rgba(255, 255, 255, .036) 50%, transparent 50.5%);
  --terminal-ambient-sheen: linear-gradient(90deg, transparent, rgba(45, 212, 191, .03), transparent);
  --terminal-ambient-drift: radial-gradient(circle at 18% 14%, rgba(45, 212, 191, .09), transparent 31%), radial-gradient(circle at 84% 78%, rgba(255, 255, 255, .045), transparent 36%);
  position: relative;
  z-index: 0;
  display: flex;
  min-height: 0;
  flex: 1 1 auto;
  flex-direction: column;
  overflow: hidden;
  padding: 28px 48px;
  color: var(--terminal-text);
  background: var(--terminal-bg);
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
  isolation: isolate;
}

.terminal-home[data-theme="light"] {
  --terminal-bg: #f7f9f8;
  --terminal-surface: #fff;
  --terminal-surface-hover: #eef5f2;
  --terminal-border: rgba(25, 33, 32, .12);
  --terminal-border-focus: rgba(0, 135, 125, .42);
  --terminal-border-error: rgba(201, 90, 84, .48);
  --terminal-text: #192120;
  --terminal-muted: #657671;
  --terminal-secondary: rgba(25, 33, 32, .72);
  --terminal-subtle: rgba(25, 33, 32, .56);
  --terminal-corner: rgba(25, 33, 32, .66);
  --terminal-error: #b94f4a;
  --terminal-error-bg: rgba(201, 90, 84, .1);
  --terminal-error-border: rgba(185, 79, 74, .24);
  --terminal-warning: #9b6b2c;
  --terminal-warning-bg: rgba(200, 145, 67, .12);
  --terminal-warning-border: rgba(155, 107, 44, .22);
  --terminal-separator: rgba(25, 33, 32, .22);
  --terminal-accent: #006a64;
  --terminal-accent-soft: rgba(0, 106, 100, .12);
  --terminal-field-bg: rgba(25, 33, 32, .055);
  --terminal-field-bg-soft: rgba(25, 33, 32, .04);
  --terminal-button-text: #fff;
  --terminal-button-bg: #192120;
  --terminal-button-hover: #006a64;
  --terminal-button-disabled-text: #7b8885;
  --terminal-button-disabled-bg: #dfe8e5;
  --terminal-shadow: 0 26px 58px rgba(38, 76, 69, .15), 0 6px 16px rgba(38, 76, 69, .08), inset 0 1px 0 rgba(255, 255, 255, .78);
  --terminal-focus-glow: rgba(0, 106, 100, .14);
  --terminal-error-glow: rgba(185, 79, 74, .14);
  --terminal-focus-shadow: var(--terminal-shadow), 0 0 0 3px var(--terminal-accent-soft), 0 0 30px var(--terminal-focus-glow);
  --terminal-ambient: radial-gradient(circle at 50% 0%, rgba(0, 106, 100, .12), transparent 58%), linear-gradient(135deg, transparent 0 49.5%, rgba(0, 106, 100, .055) 50%, transparent 50.5%);
  --terminal-ambient-sheen: linear-gradient(90deg, transparent, rgba(0, 106, 100, .045), transparent);
  --terminal-ambient-drift: radial-gradient(circle at 18% 14%, rgba(0, 106, 100, .09), transparent 31%), radial-gradient(circle at 84% 78%, rgba(25, 33, 32, .055), transparent 36%);
}

.terminal-ambient {
  position: absolute;
  z-index: 0;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  background: var(--terminal-ambient);
  background-size: auto, 88px 88px;
}

.terminal-ambient::before {
  position: absolute;
  inset: -18%;
  background: var(--terminal-ambient-drift);
  content: "";
  opacity: .88;
  transform: translate3d(-1.5%, -1%, 0) scale(1.02);
  animation: terminal-ambient-drift 22s ease-in-out infinite alternate;
}

.terminal-ambient::after {
  position: absolute;
  inset: 0;
  background: var(--terminal-ambient-sheen);
  content: "";
  opacity: .84;
}

.terminal-corner {
  position: absolute;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 7px;
  color: var(--terminal-corner);
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  font-size: 11.5px;
  letter-spacing: .06em;
  line-height: 1.4;
  pointer-events: none;
  user-select: none;
}

.terminal-corner-tl { top: 76px; left: 48px; }
.terminal-corner-tr { top: 76px; right: 48px; }
.terminal-corner-bl { bottom: 72px; left: 48px; }
.terminal-corner-br { right: 48px; bottom: 72px; }
.terminal-corner-dot {
  width: 6px;
  height: 6px;
  flex: 0 0 6px;
  border-radius: 50%;
  background: var(--terminal-accent);
  box-shadow: 0 0 8px var(--terminal-accent);
}

.terminal-visitor-readout,
.terminal-corner-metric {
  display: inline-flex;
  align-items: baseline;
  gap: 5px;
}

.terminal-visitor-readout strong,
.terminal-corner-metric strong {
  color: var(--terminal-text);
  font-weight: 600;
}

.terminal-corner-separator {
  color: var(--terminal-separator);
}

.terminal-cursor {
  width: 5px;
  height: 12px;
  background: var(--terminal-accent);
  animation: terminal-cursor-blink 1s steps(1, end) infinite;
}

.terminal-home :deep(.join-header) {
  position: relative;
  z-index: 3;
  display: flex;
  width: 100%;
  min-height: 34px;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  margin: 0;
  color: var(--terminal-text);
}

.terminal-home :deep(.brand-lockup) {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.terminal-home :deep(.brand-mark) {
  display: none;
}

.terminal-home :deep(.brand-lockup strong) {
  color: var(--terminal-text);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: -.02em;
}

.terminal-home :deep(.brand-lockup > div) {
  display: flex;
  min-width: 0;
  align-items: baseline;
  gap: 8px;
}

.terminal-home :deep(.brand-lockup small) {
  display: inline;
  margin: 0;
  overflow: hidden;
  color: var(--terminal-muted);
  font-size: 9px;
  letter-spacing: .02em;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.terminal-home :deep(.header-tools) {
  display: flex;
  min-width: 0;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
}

.terminal-home :deep(.github-link) {
  color: var(--terminal-muted);
  font-size: 10px;
}

.terminal-home :deep(.github-link:hover),
.terminal-home :deep(.github-link:focus-visible) {
  color: var(--terminal-text);
}

.terminal-home :deep(.theme-toggle) {
  color: var(--terminal-muted);
}

.terminal-home :deep(.join-language-switcher) {
  color: var(--terminal-muted);
}

.terminal-home :deep(.language-trigger) {
  min-height: 24px;
  color: var(--terminal-muted);
  background: transparent;
  border-color: transparent;
  border-radius: 4px;
  box-shadow: none;
}

.terminal-home :deep(.language-trigger:hover),
.terminal-home :deep(.language-switcher.open .language-trigger) {
  color: var(--terminal-text);
  background: transparent;
  border-color: transparent;
  box-shadow: none;
}

.terminal-content {
  position: relative;
  z-index: 2;
  display: grid;
  width: min(520px, 100%);
  min-height: 0;
  margin: auto;
  align-content: center;
  gap: 14px;
}

.terminal-hero {
  text-align: left;
}

.terminal-kicker {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 12px;
  color: var(--terminal-secondary);
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  font-size: 10px;
  letter-spacing: .08em;
  text-transform: uppercase;
}

.terminal-kicker-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--terminal-accent);
  box-shadow: 0 0 8px var(--terminal-accent);
}

.terminal-hero h1 {
  margin: 0 0 6px;
  color: var(--terminal-text);
  font-size: 28px;
  font-weight: 600;
  letter-spacing: -.035em;
  line-height: 1.18;
}

.terminal-hero p {
  max-width: 460px;
  margin: 0;
  color: var(--terminal-secondary);
  font-size: 13px;
  line-height: 1.55;
}

.terminal-launch-card {
  padding: 8px;
  background: var(--terminal-surface);
  border: 1px solid var(--terminal-border);
  border-radius: 12px;
  box-shadow: var(--terminal-shadow);
  transition: border-color .2s ease, box-shadow .2s ease;
}

.terminal-launch-card:focus-within {
  border-color: var(--terminal-border-focus);
  box-shadow: var(--terminal-focus-shadow);
}

.terminal-launch-card.has-error {
  border-color: var(--terminal-border-error);
}

.terminal-launch-card.has-error:focus-within {
  border-color: var(--terminal-border-error);
  box-shadow: var(--terminal-shadow), 0 0 0 3px var(--terminal-error-glow), 0 0 30px var(--terminal-error-glow);
}

.terminal-home :deep(.terminal-join-form) {
  display: grid;
  gap: 9px;
  min-width: 0;
}

.terminal-home :deep(.terminal-entry-row) {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 8px;
  min-width: 0;
  align-items: stretch;
}

.terminal-home :deep(.terminal-nickname-field) {
  position: relative;
  display: flex;
  min-width: 0;
  align-items: center;
  gap: 0;
  padding: 0 8px 1px;
  background: transparent !important;
  border: 0 !important;
  border-radius: 0;
  box-shadow: none !important;
  outline: none !important;
  transition: color .2s ease;
}

.terminal-home :deep(.terminal-nickname-field)::after {
  position: absolute;
  right: 8px;
  bottom: 0;
  left: 8px;
  height: 1px;
  background: var(--terminal-accent);
  content: "";
  transform: scaleX(0);
  transform-origin: left center;
  transition: transform .2s ease;
}

.terminal-home :deep(.terminal-nickname-field:focus-within)::after {
  transform: scaleX(1);
}

.terminal-home :deep(.terminal-nickname-field input),
.terminal-home :deep(.terminal-nickname-field input:focus),
.terminal-home :deep(.terminal-nickname-field input:focus-visible),
.terminal-home :deep(.terminal-field-label input) {
  appearance: none;
  -webkit-appearance: none;
  min-width: 0;
  width: 100%;
  color: var(--terminal-text);
  background: transparent !important;
  border: 0 !important;
  border-radius: 0;
  box-shadow: none !important;
  outline: none !important;
  font-size: 13px;
  caret-color: var(--terminal-accent);
}

.terminal-home :deep(.terminal-nickname-field input) {
  flex: 1 1 auto;
  padding: 10px 0;
}

.terminal-home :deep(.terminal-nickname-field:focus-within) {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  outline: none !important;
}

.terminal-home :deep(.terminal-nickname-field input::placeholder),
.terminal-home :deep(.terminal-field-label input::placeholder) {
  color: var(--terminal-muted);
}

.terminal-home :deep(.terminal-connect-button) {
  min-width: 96px;
  min-height: 40px;
  padding: 0 16px;
  color: var(--terminal-button-text);
  background: var(--terminal-button-bg);
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
  transition: background .2s ease, opacity .2s ease, transform .1s ease;
}

.terminal-home :deep(.terminal-connect-button:hover:not(:disabled)) {
  background: var(--terminal-button-hover);
}

.terminal-home :deep(.terminal-connect-button:active:not(:disabled)) {
  transform: scale(.98);
}

.terminal-home :deep(.terminal-connect-button:disabled) {
  color: var(--terminal-button-disabled-text);
  background: var(--terminal-button-disabled-bg);
  cursor: wait;
}

.terminal-home :deep(.terminal-advanced) {
  margin-top: 0;
  padding: 9px 6px 0;
  border-top: 1px solid var(--terminal-border);
}

.terminal-home :deep(.terminal-advanced summary) {
  display: flex;
  min-height: 23px;
  align-items: center;
  gap: 6px;
  color: var(--terminal-muted);
  cursor: pointer;
  font-size: 11px;
  list-style: none;
  outline: 0;
  user-select: none;
}

.terminal-home :deep(.terminal-advanced summary::-webkit-details-marker) {
  display: none;
}

.terminal-home :deep(.terminal-advanced summary::marker) {
  content: "";
}

.terminal-home :deep(.terminal-advanced summary:hover),
.terminal-home :deep(.terminal-advanced summary:focus-visible) {
  color: var(--terminal-text);
}

.terminal-home :deep(.terminal-advanced summary:focus-visible) {
  border-radius: 5px;
  box-shadow: none;
  text-decoration: underline;
  text-decoration-color: var(--terminal-accent);
  text-underline-offset: 4px;
}

.terminal-home :deep(.terminal-advanced-arrow) {
  display: inline-block;
  color: var(--terminal-accent);
  font-size: 16px;
  line-height: 1;
  transition: transform .2s ease;
}

.terminal-home :deep(.terminal-advanced[open] .terminal-advanced-arrow) {
  transform: rotate(90deg);
}

.terminal-home :deep(.terminal-advanced summary small) {
  margin-left: auto;
  color: var(--terminal-subtle);
  font-size: 9px;
}

.terminal-home :deep(.terminal-advanced-content) {
  display: grid;
  gap: 10px;
  padding: 11px 0 4px;
}

.terminal-home :deep(.terminal-inline-notice) {
  display: flex;
  min-width: 0;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 9px 10px;
  color: var(--terminal-muted);
  background: var(--terminal-field-bg-soft);
  border: 1px solid var(--terminal-border);
  border-radius: 7px;
  font-size: 10px;
}

.terminal-home :deep(.terminal-inline-notice) {
  justify-content: flex-start;
  color: var(--terminal-warning);
  background: var(--terminal-warning-bg);
  border-color: var(--terminal-warning-border);
  line-height: 1.45;
}

.terminal-home :deep(.terminal-target-grid) {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 120px;
  gap: 8px;
}

.terminal-home :deep(.terminal-field-label) {
  display: grid;
  min-width: 0;
  gap: 5px;
  color: var(--terminal-muted);
  font-size: 10px;
}

.terminal-home :deep(.terminal-field-label > span) {
  display: flex;
  align-items: baseline;
  gap: 5px;
}

.terminal-home :deep(.terminal-field-label em) {
  color: var(--terminal-subtle);
  font-size: 9px;
  font-style: normal;
}

.terminal-home :deep(.terminal-field-label input) {
  padding: 9px 10px;
  background: var(--terminal-field-bg);
  border: 1px solid var(--terminal-border);
  border-radius: 7px;
  transition: border-color .2s ease, box-shadow .2s ease;
}

.terminal-home :deep(.terminal-field-label input:focus) {
  border-color: var(--terminal-border);
  box-shadow: inset 0 -1px 0 var(--terminal-accent);
}

.terminal-home :deep(.terminal-relay-choice) {
  display: flex;
  min-width: 0;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 9px 10px;
  background: var(--terminal-field-bg-soft);
  border: 1px solid var(--terminal-border);
  border-radius: 7px;
}

.terminal-home :deep(.terminal-relay-choice > div) {
  display: grid;
  min-width: 0;
  gap: 2px;
}

.terminal-home :deep(.terminal-relay-choice strong),
.terminal-home :deep(.terminal-relay-choice small) {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.terminal-home :deep(.terminal-relay-choice strong) {
  color: var(--terminal-text);
  font-size: 10px;
}

.terminal-home :deep(.terminal-relay-choice small) {
  color: var(--terminal-muted);
  font-size: 9px;
}

.terminal-home :deep(.terminal-relay-choice select) {
  min-width: 120px;
  max-width: 46%;
  padding: 6px 8px;
  color: var(--terminal-text);
  background: var(--terminal-surface-hover);
  border: 1px solid var(--terminal-border);
  border-radius: 6px;
  outline: 0;
  font-size: 10px;
}

.terminal-home :deep(.terminal-relay-choice select:focus) {
  border-color: var(--terminal-border);
  box-shadow: inset 0 -1px 0 var(--terminal-accent);
}

.terminal-home :deep(.terminal-identity button) {
  min-width: 0;
  padding: 5px 7px;
  overflow: hidden;
  color: var(--terminal-muted);
  background: transparent;
  border: 1px solid var(--terminal-border);
  border-radius: 5px;
  cursor: pointer;
  font-size: 9px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.terminal-home :deep(.terminal-identity button:hover:not(:disabled)),
.terminal-home :deep(.terminal-identity button:focus-visible:not(:disabled)) {
  color: var(--terminal-text);
  border-color: var(--terminal-border-focus);
  outline: 0;
}

.terminal-home :deep(.terminal-identity) {
  display: flex;
  min-width: 0;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-top: 2px;
}

.terminal-home :deep(.terminal-remember-identity) {
  display: flex;
  min-width: 0;
  align-items: flex-start;
  gap: 8px;
  color: var(--terminal-text);
  cursor: pointer;
}

.terminal-home :deep(.terminal-remember-identity input) {
  width: 14px;
  height: 14px;
  flex: 0 0 14px;
  margin: 2px 0 0;
  accent-color: var(--terminal-accent);
}

.terminal-home :deep(.terminal-remember-identity span) {
  display: grid;
  min-width: 0;
  gap: 2px;
}

.terminal-home :deep(.terminal-remember-identity strong) {
  font-size: 10px;
  font-weight: 600;
}

.terminal-home :deep(.terminal-remember-identity small),
.terminal-home :deep(.terminal-identity-warning) {
  color: var(--terminal-muted);
  font-size: 9px;
  line-height: 1.4;
}

.terminal-home :deep(.identity-actions) {
  display: flex;
  flex: 0 0 auto;
  gap: 6px;
}

.terminal-home :deep(.terminal-identity button:disabled) {
  cursor: not-allowed;
  opacity: .4;
}

.terminal-home :deep(.terminal-identity-warning) {
  margin: -4px 0 0 22px;
}

.terminal-home :deep(.terminal-cancel-connect) {
  justify-self: end;
  padding: 4px 7px;
  color: var(--terminal-muted);
  background: transparent;
  border: 1px solid var(--terminal-border);
  border-radius: 5px;
  cursor: pointer;
  font-size: 10px;
}

.terminal-home :deep(.terminal-cancel-connect:hover),
.terminal-home :deep(.terminal-cancel-connect:focus-visible) {
  color: var(--terminal-text);
  border-color: var(--terminal-border-focus);
  outline: 0;
}

.terminal-notice {
  display: flex;
  align-items: flex-start;
  gap: 9px;
  margin: 0 4px 8px;
  padding: 9px 10px;
  border: 1px solid transparent;
  border-radius: 8px;
  font-size: 11px;
  line-height: 1.45;
}

.terminal-notice-error {
  color: var(--terminal-error);
  background: var(--terminal-error-bg);
  border-color: var(--terminal-error-border);
}

.terminal-notice-warning {
  color: var(--terminal-warning);
  background: var(--terminal-warning-bg);
  border-color: var(--terminal-warning-border);
}

.terminal-notice-symbol {
  display: grid;
  width: 16px;
  height: 16px;
  flex: 0 0 16px;
  place-items: center;
  border: 1px solid currentColor;
  border-radius: 50%;
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 10px;
  font-weight: 700;
}

.terminal-notice-copy {
  display: grid;
  gap: 3px;
  min-width: 0;
}

.terminal-notice-copy code {
  color: inherit;
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 9px;
  opacity: .72;
}

.terminal-notice a {
  color: inherit;
  font-weight: 700;
}

.terminal-security-note {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 7px 4px 2px;
  color: var(--terminal-muted);
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 9px;
  text-align: center;
}

.terminal-security-mark {
  color: var(--terminal-accent);
  font-size: 12px;
}

.terminal-facts {
  display: flex;
  justify-content: center;
  gap: 8px;
  color: var(--terminal-secondary);
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 10px;
  letter-spacing: .04em;
  text-align: center;
}

.terminal-fact-separator,
.terminal-footer-separator {
  color: var(--terminal-separator);
}

.terminal-footer {
  position: relative;
  z-index: 2;
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  color: var(--terminal-muted);
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  font-size: 9px;
  letter-spacing: .025em;
}

.terminal-footer-left,
.terminal-footer-right {
  display: flex;
  min-width: 0;
  align-items: center;
  gap: 8px;
}

.terminal-footer-left > span,
.terminal-footer-right > span,
.terminal-footer-right > button {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.terminal-footer-accent {
  color: var(--terminal-accent);
}

.terminal-footer-right button {
  padding: 0;
  color: inherit;
  background: transparent;
  font: inherit;
  cursor: pointer;
}

.terminal-footer-right button:hover,
.terminal-footer-right button:focus-visible {
  color: var(--terminal-text);
}

@keyframes terminal-cursor-blink {
  0%, 45% { opacity: 1; }
  46%, 100% { opacity: 0; }
}

@keyframes terminal-ambient-drift {
  0% { transform: translate3d(-1.5%, -1%, 0) scale(1.02); }
  100% { transform: translate3d(1.5%, 1%, 0) scale(1.06); }
}

@media (prefers-reduced-motion: reduce) {
  .terminal-cursor { animation: none; }
  .terminal-ambient::before { animation: none; }
  .terminal-launch-card,
  .terminal-home :deep(.terminal-nickname-field),
  .terminal-home :deep(.terminal-nickname-field)::after,
  .terminal-home :deep(.terminal-connect-button),
  .terminal-home :deep(.terminal-advanced-arrow),
  .terminal-home :deep(.terminal-field-label input) {
    transition: none;
  }
}

@media (max-width: 740px) {
  .terminal-home {
    overflow: auto;
    padding: calc(17px + env(safe-area-inset-top, 0px)) max(20px, env(safe-area-inset-right, 0px)) calc(17px + env(safe-area-inset-bottom, 0px)) max(20px, env(safe-area-inset-left, 0px));
  }

  .terminal-home :deep(.join-header) {
    min-height: 36px;
    align-items: flex-start;
  }

  .terminal-home :deep(.header-tools) {
    display: flex !important;
    gap: 7px;
  }

  .terminal-home :deep(.github-link),
  .terminal-home :deep(.join-skin-switcher) {
    display: none;
  }

  .terminal-home :deep(.brand-lockup > div) {
    gap: 5px;
  }

  .terminal-home :deep(.brand-lockup small) {
    max-width: 34vw;
  }

  .terminal-home :deep(.join-language-switcher .language-trigger) {
    min-width: 0;
    padding-inline: 0;
  }

  .terminal-home :deep(.terminal-entry-row) {
    grid-template-columns: minmax(0, 1fr);
  }

  .terminal-home :deep(.terminal-connect-button) {
    width: 100%;
    min-height: 42px;
  }

  .terminal-home :deep(.terminal-advanced summary) {
    min-height: 30px;
  }

  .terminal-home :deep(.terminal-advanced summary small) {
    max-width: 42%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .terminal-home :deep(.terminal-target-grid) {
    grid-template-columns: minmax(0, 1fr);
  }

  .terminal-home :deep(.terminal-relay-choice),
  .terminal-home :deep(.terminal-identity) {
    align-items: stretch;
    flex-direction: column;
  }

  .terminal-home :deep(.terminal-relay-choice select) {
    width: 100%;
    max-width: none;
  }

  .terminal-home :deep(.terminal-identity .identity-actions) {
    width: 100%;
  }

  .terminal-home :deep(.terminal-identity .identity-actions button) {
    flex: 1 1 0;
  }

  .terminal-corner {
    display: none;
  }

  .terminal-content {
    width: min(520px, 100%);
    margin: auto 0;
    padding: 44px 0 34px;
  }

  .terminal-hero h1 {
    font-size: clamp(26px, 8vw, 32px);
  }

  .terminal-hero p {
    font-size: 12px;
  }

  .terminal-launch-card {
    border-radius: 11px;
  }

  .terminal-facts {
    flex-wrap: wrap;
    line-height: 1.5;
  }

  .terminal-footer {
    align-items: flex-start;
    flex-direction: column;
    gap: 6px;
    padding-top: 4px;
    font-size: 8px;
  }

  .terminal-footer-left,
  .terminal-footer-right {
    width: 100%;
    gap: 6px;
  }

  .terminal-footer-right {
    justify-content: flex-end;
  }
}

@media (max-width: 420px) {
  .terminal-home {
    padding-inline: 14px;
  }

  .terminal-content {
    padding-top: 32px;
  }

  .terminal-footer-left > span:nth-child(2),
  .terminal-footer-left > span:nth-child(4),
  .terminal-footer-left > span:nth-child(5),
  .terminal-footer-right > span:nth-child(2),
  .terminal-footer-right > span:nth-child(4) {
    display: none;
  }

  .terminal-home :deep(.terminal-advanced summary small) {
    display: none;
  }

  .terminal-home :deep(.terminal-identity-warning) {
    margin-left: 0;
  }
}
</style>
