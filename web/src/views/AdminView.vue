<template>
  <div class="admin-root">
    <div
      v-if="loading"
      class="center-card compact"
      ><span class="spinner"></span><p>{{ tr("loading") }}</p></div
    >

    <main
      v-else-if="screen === 'change-password'"
      class="login-page auth-terminal"
      :data-auth-state="authTerminalState"
    >
      <div
        class="auth-terminal-ambient"
        aria-hidden="true"
      ></div>
      <div class="auth-terminal-header">
        <WebClientHeader
          v-model:language="language"
          brand-name="WebSpeak"
          :dark-theme="darkTheme"
          :t="publicTr"
          @theme-toggle="cycleTheme"
          @language-change="persistLanguage"
        />
      </div>
      <div class="auth-terminal-corner auth-terminal-corner-tl">
        <span class="auth-terminal-dot" aria-hidden="true"></span>
        WEBSPEAK // ADMIN_GATEWAY
      </div>
      <div class="auth-terminal-corner auth-terminal-corner-tr">STATUS: {{ authTerminalCode }} // ACCESS: RESTRICTED</div>
      <div class="auth-terminal-corner auth-terminal-corner-bl">
        <span>SYS_LOG: {{ authTerminalCode }}</span>
        <span class="auth-terminal-cursor" aria-hidden="true"></span>
      </div>
      <div class="auth-terminal-corner auth-terminal-corner-br">AUTH_MODE: PASSWORD_ROTATION</div>
      <div class="auth-terminal-layout">
        <aside class="auth-terminal-context">
          <div class="auth-context-kicker"><span class="auth-context-dot" aria-hidden="true"></span>ADMIN / CONTROL PLANE</div>
          <div class="auth-context-brand"
            ><span><Icon name="waveform" :size="21" /></span
            ><div><strong>WebSpeak</strong><small>{{ tr("adminConsole") }}</small></div
          ></div>
          <div class="auth-context-copy">
            <span class="auth-context-label">PASSWORD_ROTATION</span>
            <h2>{{ tr("adminConsole") }}</h2>
            <p>{{ tr("changePasswordLead") }}</p>
          </div>
          <div class="auth-context-readouts">
            <div><span>AUTH_STATE</span><strong>{{ authTerminalCode }}</strong></div>
            <div><span>ACCESS</span><strong>RESTRICTED</strong></div>
          </div>
        </aside>
        <section class="login-card">
          <div class="auth-card-topline"><span>AUTH / PASSWORD_ROTATION</span><span>{{ authTerminalCode }}</span></div>
        <header
          ><h1>{{ tr("changePasswordTitle") }}</h1
          ><p>{{ tr("changePasswordLead") }}</p></header
        >
        <form @submit.prevent="changePassword"
          ><div
            v-if="errorMessage"
            class="alert error"
            >{{ errorMessage }}</div
          ><label
            ><span>{{ tr("newPassword") }}</span
            ><input
              v-model="newPassword"
              type="password"
              autocomplete="new-password"
              maxlength="1024"
              autofocus
              :placeholder="tr('passwordPlaceholder')" /></label
          ><label
            ><span>{{ tr("confirmPassword") }}</span
            ><input
              v-model="confirmNewPassword"
              type="password"
              autocomplete="new-password"
              maxlength="1024" /></label
          ><div class="strength"><i :style="{ width: `${passwordStrength}%` }"></i></div
          ><button
            class="primary-button wide"
            :disabled="submitting"
            type="submit"
            ><span
              v-if="submitting"
              class="spinner small"
            ></span
            >{{ tr("savePassword") }}</button
          ></form
        >
        <p class="security-note">{{ tr("defaultCredentialNotice") }}</p>
        </section>
      </div>
      <footer class="auth-terminal-footer">
        <div class="auth-terminal-footer-left">
          <span>WEBSPEAK // ADMIN_GATEWAY</span>
          <span class="auth-terminal-footer-separator" aria-hidden="true">·</span>
          <span>{{ publicTr("browserWorkspace") }}</span>
          <span class="auth-terminal-footer-separator" aria-hidden="true">·</span>
          <span class="auth-terminal-footer-accent">ACCESS: RESTRICTED</span>
        </div>
        <div class="auth-terminal-footer-right">
          <span>AUTH_STATE: {{ authTerminalCode }}</span>
          <span class="auth-terminal-footer-separator" aria-hidden="true">·</span>
          <span>CONTROL PLANE ONLINE</span>
        </div>
      </footer>
    </main>

    <main
      v-else-if="screen === 'login'"
      class="login-page auth-terminal"
      :data-auth-state="authTerminalState"
    >
      <div
        class="auth-terminal-ambient"
        aria-hidden="true"
      ></div>
      <div class="auth-terminal-header">
        <WebClientHeader
          v-model:language="language"
          brand-name="WebSpeak"
          :dark-theme="darkTheme"
          :t="publicTr"
          @theme-toggle="cycleTheme"
          @language-change="persistLanguage"
        />
      </div>
      <div class="auth-terminal-corner auth-terminal-corner-tl">
        <span class="auth-terminal-dot" aria-hidden="true"></span>
        WEBSPEAK // ADMIN_GATEWAY
      </div>
      <div class="auth-terminal-corner auth-terminal-corner-tr">STATUS: {{ authTerminalCode }} // ACCESS: RESTRICTED</div>
      <div class="auth-terminal-corner auth-terminal-corner-bl">
        <span>SYS_LOG: {{ authTerminalCode }}</span>
        <span class="auth-terminal-cursor" aria-hidden="true"></span>
      </div>
      <div class="auth-terminal-corner auth-terminal-corner-br">AUTH_MODE: LOGIN</div>
      <div class="auth-terminal-layout">
        <aside class="auth-terminal-context">
          <div class="auth-context-kicker"><span class="auth-context-dot" aria-hidden="true"></span>ADMIN / CONTROL PLANE</div>
          <div class="auth-context-brand"
            ><span><Icon name="waveform" :size="21" /></span
            ><div><strong>WebSpeak</strong><small>{{ tr("adminConsole") }}</small></div
          ></div>
          <div class="auth-context-copy">
            <span class="auth-context-label">SECURE_LOGIN</span>
            <h2>{{ tr("adminConsole") }}</h2>
            <p>{{ tr("loginLead") }}</p>
          </div>
          <div class="auth-context-readouts">
            <div><span>AUTH_STATE</span><strong>{{ authTerminalCode }}</strong></div>
            <div><span>ACCESS</span><strong>RESTRICTED</strong></div>
          </div>
        </aside>
        <section class="login-card">
          <div class="auth-card-topline"><span>AUTH / SECURE_LOGIN</span><span>{{ authTerminalCode }}</span></div>
        <header
          ><h1>{{ tr("welcomeAdmin") }}</h1
          ><p>{{ tr("loginLead") }}</p></header
        >
        <form @submit.prevent="login"
          ><div
            v-if="errorMessage"
            class="alert error"
            >{{ errorMessage }}</div
          ><label
            ><span>{{ tr("adminUsername") }}</span
            ><input
              v-model.trim="loginUsername"
              autocomplete="username"
              autofocus /></label
          ><label
            ><span>{{ tr("adminPassword") }}</span
            ><input
              v-model="loginPassword"
              type="password"
              autocomplete="current-password" /></label
          ><button
            class="primary-button wide"
            :disabled="submitting"
            type="submit"
            ><span
              v-if="submitting"
              class="spinner small"
            ></span
            >{{ tr("login") }}</button
          ></form
        >
        <div class="login-actions"
          ><RouterLink
            to="/"
            class="home-link"
            ><Icon
              name="home"
              :size="15"
            />{{ tr("backHome") }}</RouterLink
        /></div>
        </section>
      </div>
      <footer class="auth-terminal-footer">
        <div class="auth-terminal-footer-left">
          <span>WEBSPEAK // ADMIN_GATEWAY</span>
          <span class="auth-terminal-footer-separator" aria-hidden="true">·</span>
          <span>{{ publicTr("browserWorkspace") }}</span>
          <span class="auth-terminal-footer-separator" aria-hidden="true">·</span>
          <span class="auth-terminal-footer-accent">ACCESS: RESTRICTED</span>
        </div>
        <div class="auth-terminal-footer-right">
          <span>AUTH_STATE: {{ authTerminalCode }}</span>
          <span class="auth-terminal-footer-separator" aria-hidden="true">·</span>
          <span>CONTROL PLANE ONLINE</span>
        </div>
      </footer>
    </main>

    <div
      v-else
      class="admin-shell"
    >
      <aside class="admin-sidebar">
        <div class="admin-brand"
          ><span
            ><Icon
              name="waveform"
              :size="22" /></span
          ><div
            ><strong>WebSpeak</strong><small>{{ tr("adminConsole") }}</small></div
          ></div
        >
        <nav
          ><RouterLink
            to="/admin"
            exact-active-class="active"
            ><Icon
              name="activity"
              :size="18"
            />{{ tr("overview") }}</RouterLink
          ><RouterLink
            to="/admin/server"
            active-class="active"
            ><Icon
              name="server"
              :size="18"
            />{{ tr("server") }}</RouterLink
          ><RouterLink
            to="/admin/operations"
            active-class="active"
            ><Icon
              name="users"
              :size="18"
            />{{ tr("operations") }}</RouterLink
          ><RouterLink
            to="/admin/skins"
            active-class="active"
            ><Icon
              name="compass"
              :size="18"
            />{{ tr("skinLibrary") }}</RouterLink
          ></nav
        >
        <div class="sidebar-bottom"
          ><a
            href="/"
            target="_blank"
            ><Icon
              name="share"
              :size="16"
            />{{ tr("openGuest") }}</a
          ><button
            type="button"
            :disabled="loggingOut"
            @click="logout"
            ><Icon
              name="door"
              :size="16"
            />{{ tr("logout") }}</button
          ></div
        >
      </aside>

      <main
        class="admin-main"
        :inert="loggingOut || undefined"
        :aria-busy="loggingOut"
      >
        <header class="admin-topbar">
          <div class="admin-page-title"
            ><small>{{ tr("adminConsole") }}</small
            ><h1>{{ currentPageTitle }}</h1></div
          >
          <div class="admin-tools">
            <span
              class="gateway-status"
              role="status"
              :title="tr('gatewayRunning')"
              ><span
                class="running-dot"
                aria-hidden="true"
              ></span
              ><span class="gateway-status-label">{{ tr("gatewayRunning") }}</span></span
            >
            <button
              type="button"
              class="theme-toggle"
              :title="themeLabel"
              :aria-label="themeLabel"
              :aria-pressed="darkTheme"
              @click="cycleTheme"
              ><span
                class="theme-toggle-track"
                :class="{ dark: darkTheme }"
                aria-hidden="true"
              ><span class="theme-toggle-option theme-toggle-moon"><Icon name="moon" :size="12" /></span
              ><span class="theme-toggle-option theme-toggle-sun"><Icon name="sun" :size="12" /></span
              ><span class="theme-toggle-thumb"></span></span></button
            >
            <LanguageSwitcher
              v-model="language"
              compact
              :menu-label="tr('languageMenu')"
              @change="persistLanguage"
            />
          </div>
        </header>

        <div
          v-if="errorMessage"
          class="alert error page-alert"
          >{{ errorMessage }}</div
        >
        <AdminServerSettings
          v-if="route.path === '/admin/server'"
          :model="serverSettings"
          :i18n="i18n"
          v-model:welcome-language="welcomeLanguage"
          @webrtc-toggle="handleWebRtcToggle"
        />
        <AdminOperations
          v-else-if="route.path === '/admin/operations'"
          :model="adminOperations"
          :i18n="i18n"
        />
        <AdminSkins
          v-else-if="route.path === '/admin/skins'"
          :model="adminSkins"
          :i18n="i18n"
        />

        <section
          v-else
          class="page-content overview-page"
        >
          <div
            v-if="overview.legacyConfigImported"
            class="alert info import-notice"
            ><span>{{ tr("legacyImported") }}</span
            ><button
              type="button"
              @click="dismissLegacyNotice"
              >{{ tr("gotIt") }}</button
            ></div
          >
          <div class="hero-status"
            ><div
              ><small>{{ tr("systemStatus") }}</small
              ><h2>{{ tr("everythingRunning") }}</h2
              ><p>{{ tr("overviewLead") }}</p></div
            ><span class="status-badge"><i></i>{{ tr("running") }}</span></div
          >
          <div class="metric-grid"
            ><article
              ><span
                ><Icon
                  name="activity"
                  :size="20" /></span
              ><small>{{ tr("gateway") }}</small
              ><strong>{{ overview.gateway.version || "—" }}</strong
              ><em>{{ formatUptime(overview.gateway.uptimeSeconds) }}</em></article
            ><article
              ><span
                ><Icon
                  name="server"
                  :size="20" /></span
              ><small>{{ tr("teamSpeakTarget") }}</small
              ><strong>{{ overview.teamSpeak.target || "—" }}</strong
              ><em>{{ targetStatusText }}</em></article
            ><article
              ><span
                ><Icon
                  name="users"
                  :size="20" /></span
              ><small>{{ tr("activeSessions") }}</small
              ><strong>{{ overview.sessions.active }} / {{ overview.sessions.limit }}</strong
              ><em>{{ tr("peakSessions", { count: overview.sessions.peak }) }}</em></article
            ></div
          >
          <div class="overview-columns"
            ><article class="overview-card target-health-card"
              ><header
                ><div
                  ><h3>{{ tr("targetHealth") }}</h3
                  ><p>{{ tr("targetHealthLead") }}</p></div
                ><RouterLink to="/admin/server">{{ tr("manage") }}</RouterLink></header
              ><dl
                ><div
                  ><dt>{{ tr("status") }}</dt
                  ><dd><i :class="overview.teamSpeak.status"></i>{{ targetStatusText }}</dd></div
                ><div
                  ><dt>{{ tr("lastTest") }}</dt
                  ><dd>{{ formatDate(overview.teamSpeak.lastTestAt) }}</dd></div
                ><div
                  ><dt>{{ tr("latency") }}</dt
                  ><dd>{{
                    overview.teamSpeak.latencyMs == null
                      ? "—"
                      : `${overview.teamSpeak.latencyMs} ms`
                  }}</dd></div
                ></dl
              ></article
            ><article class="overview-card recent-events-card"
              ><header
                ><div
                  ><h3>{{ tr("recentEvents") }}</h3
                  ><p>{{ tr("recentEventsLead") }}</p></div
                ></header
              ><ul class="event-list"
                ><li
                  v-for="event in overview.recentEvents"
                  :key="`${event.event}-${event.createdAt}`"
                  ><span
                    ><Icon
                      name="check"
                      :size="14" /></span
                  ><div
                    ><strong>{{ eventName(event.event) }}</strong
                    ><small>{{ formatDate(event.createdAt) }}</small></div
                  ></li
                ><li
                  v-if="!overview.recentEvents.length"
                  class="empty-event"
                  >{{ tr("noRecentEvents") }}</li
                ></ul
              ></article
            ></div
          >
        </section>
        <div
          v-if="webrtcPortNoticeOpen"
          class="modal-backdrop"
          @click.self="webrtcPortNoticeOpen = false"
          ><section
            class="modal-card"
            role="dialog"
            aria-modal="true"
            :aria-label="tr('webrtcPortNoticeTitle')"
            ><div class="modal-icon"
              ><Icon
                name="info"
                :size="21" /></div
            ><h2>{{ tr("webrtcPortNoticeTitle") }}</h2
            ><p>{{ tr("webrtcPortNotice", { range: webrtcPortRangeText }) }}</p
            ><button
              class="primary-button wide"
              type="button"
              @click="webrtcPortNoticeOpen = false"
              >{{ tr("gotIt") }}</button
            ></section
          ></div
        >
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from "vue";
import { createAdminApi, isAdminRequestCancelled, type AdminApiError as ApiError } from "../services/admin-api.js";
import { useAdminI18n } from "../composables/useAdminI18n.js";
import { RouterLink, useRoute, useRouter } from "vue-router";
import Icon from "../components/Icon.vue";
import AdminServerSettings from "../components/admin/AdminServerSettings.vue";
import AdminOperations from "../components/admin/AdminOperations.vue";
import AdminSkins from "../components/admin/AdminSkins.vue";
import WebClientHeader from "../components/web-client/WebClientHeader.vue";
import LanguageSwitcher from "../components/LanguageSwitcher.vue";
import { createAdminRequests } from "../services/admin-requests.js";
import { useAdminServerSettings } from "../composables/useAdminServerSettings.js";
import { useAdminOperations } from "../composables/useAdminOperations.js";
import { useAdminSkins } from "../composables/useAdminSkins.js";
import { useWebClientI18n } from "../composables/useWebClientI18n.js";
import type { SiteLanguage } from "../../../src/site-copy.js";
import { applyTheme, getStoredTheme, isDarkTheme, nextTheme, saveTheme, type ThemeMode } from "../services/theme.js";

type Screen = "login" | "change-password" | "admin";

const route = useRoute();
const router = useRouter();
const storedLanguage = localStorage.getItem("webspeak:language");
const language = ref<SiteLanguage>(storedLanguage === "en" || storedLanguage === "de" || storedLanguage === "ru" || storedLanguage === "ja" ? storedLanguage : typeof navigator !== "undefined" && navigator.language.toLowerCase().startsWith("ru") ? "ru" : typeof navigator !== "undefined" && navigator.language.toLowerCase().startsWith("ja") ? "ja" : "zh");
const i18n = useAdminI18n(language);
const { tr, formatDate, formatUptime, eventName, errorText } = i18n;
function getInitialTheme(): ThemeMode {
  try {
    if (localStorage.getItem("webspeak:theme") == null) {
      localStorage.setItem("webspeak:theme", "dark");
      return "dark";
    }
  } catch {
    return "dark";
  }
  return getStoredTheme();
}
const themeMode = ref<ThemeMode>(getInitialTheme());
const darkTheme = computed(() => isDarkTheme(themeMode.value));
const themeLabel = computed(() => darkTheme.value ? tr("switchToLightTheme") : tr("switchToDarkTheme"));
const { t: publicTr } = useWebClientI18n(language);
applyTheme(themeMode.value);
const loading = ref(true);
const screen = ref<Screen>("login");
const csrfToken = ref("");
const pageRequests = createAdminRequests();
const adminApi = createAdminApi({
  csrfToken: () => csrfToken.value,
  onUnauthorized: () => {
    cancelPendingWork();
    resetPrivateState();
    csrfToken.value = "";
    if (screen.value !== "login") { screen.value = "login"; void router.replace("/admin/login"); }
  },
});
const submitting = ref(false);
const loggingOut = ref(false);
const errorMessage = ref("");
const loginUsername = ref("admin");
const loginPassword = ref("");
const newPassword = ref("");
const confirmNewPassword = ref("");
const welcomeLanguage = ref<SiteLanguage>("zh");
const emptyOverview = () => ({ gateway: { version: "", uptimeSeconds: 0 }, teamSpeak: { target: "", status: "unknown", lastTestAt: null as string | null, latencyMs: null as number | null }, sessions: { active: 0, peak: 0, limit: 100 }, recentEvents: [] as Array<{ event: string; createdAt: string }>, legacyConfigImported: false });
const overview = reactive(emptyOverview());
const webrtcPortNoticeOpen = ref(false);
const serverSettings = useAdminServerSettings({ api: adminApi, errorMessage, errorText, refreshOverview: loadOverview });
const { serverForm, loadServerSettings } = serverSettings;
const adminOperations = useAdminOperations({ api: adminApi, errorMessage, errorText, tr, refreshOverview: loadOverview });
const { loadOperations } = adminOperations;
const adminSkins = useAdminSkins({ api: adminApi, tr });
const { loadSkinCatalog } = adminSkins;

const passwordStrength = computed(() => Math.min(100, Math.max(8, newPassword.value.length * 5 + (/[\s\W]/.test(newPassword.value) ? 15 : 0))));
const authTerminalState = computed(() => {
  if (loading.value) return "loading";
  if (submitting.value) return screen.value === "change-password" ? "password-saving" : "authenticating";
  if (errorMessage.value) return "auth-error";
  if (screen.value === "change-password") return "password-rotation";
  return "ready";
});
const authTerminalCode = computed(() => authTerminalState.value.toUpperCase());
const currentPageTitle = computed(() => route.path === "/admin/server" ? tr('server') : route.path === "/admin/operations" ? tr('operations') : route.path === "/admin/skins" ? tr('skinLibrary') : tr('overview'));
const targetStatusText = computed(() => overview.teamSpeak.status === "reachable" ? tr('reachable') : overview.teamSpeak.status === "unreachable" ? tr('unreachable') : tr('notTested'));
const webrtcPortRangeText = computed(() => `${serverForm.webRtcUdpStart}–${serverForm.webRtcUdpEnd}`);

onMounted(loadAdminView);
onBeforeUnmount(() => { cancelPendingWork(); resetPrivateState(); });
watch(() => route.path, (path, previous) => {
  errorMessage.value = "";
  pageRequests.cancel("overview");
  if (previous === "/admin/server") serverSettings.cancelRequests();
  if (previous === "/admin/operations") adminOperations.cancelRequests();
  if (previous === "/admin/skins") adminSkins.cancelRequests();
  if (screen.value !== "admin" || loading.value || submitting.value || loggingOut.value) return;
  if (path === "/admin/operations") void loadOperations();
  else if (path === "/admin/skins") void loadSkinCatalog();
  else if (path === "/admin") void loadOverview();
});

function cancelPendingWork() {
  adminApi.invalidate();
  pageRequests.reset();
  serverSettings.cancelRequests();
  adminOperations.cancelRequests();
  adminSkins.cancelRequests();
  loading.value = false;
  submitting.value = false;
  loggingOut.value = false;
}
function resetPrivateState() {
  serverSettings.reset(); adminOperations.reset(); adminSkins.reset();
  Object.assign(overview, emptyOverview());
  loginPassword.value = ""; newPassword.value = ""; confirmNewPassword.value = "";
  errorMessage.value = "";
  webrtcPortNoticeOpen.value = false;
}
function report(error: unknown) {
  if (!isAdminRequestCancelled(error)) errorMessage.value = errorText((error as ApiError).code);
}
async function loadAdminData(request: { isCurrent(): boolean }) {
  await Promise.all([loadOverview(), loadServerSettings()]);
  if (!request.isCurrent()) return;
  if (route.path === "/admin/operations") await loadOperations();
  else if (route.path === "/admin/skins") await loadSkinCatalog();
}
async function loadAdminView() {
  const request = pageRequests.begin("auth");
  loading.value = true;
  try {
    const session = await adminApi.session(request.signal);
    if (!request.isCurrent()) return;
    if (!session.authenticated) {
      resetPrivateState(); csrfToken.value = ""; screen.value = "login";
      if (route.path !== "/admin/login") await router.replace("/admin/login");
    } else {
      csrfToken.value = session.csrfToken || "";
      screen.value = session.mustChangePassword ? "change-password" : "admin";
      if (session.mustChangePassword) await router.replace("/admin/change-password");
      else {
        if (route.path === "/admin/login" || route.path === "/admin/change-password") await router.replace("/admin");
        if (request.isCurrent()) await loadAdminData(request);
      }
    }
  } catch (error) { if (request.isCurrent()) report(error); }
  finally { if (request.isCurrent()) loading.value = false; request.finish(); }
}
async function login() {
  if (submitting.value) return;
  cancelPendingWork();
  const request = pageRequests.begin("auth");
  submitting.value = true; errorMessage.value = "";
  try {
    const result = await adminApi.login(loginUsername.value, loginPassword.value, request.signal);
    if (!request.isCurrent()) return;
    csrfToken.value = result.csrfToken;
    loginPassword.value = "";
    screen.value = result.mustChangePassword ? "change-password" : "admin";
    await router.replace(result.mustChangePassword ? "/admin/change-password" : "/admin");
    if (request.isCurrent() && !result.mustChangePassword) await loadAdminData(request);
  } catch (error) { if (request.isCurrent()) report(error); }
  finally { if (request.isCurrent()) submitting.value = false; request.finish(); }
}
async function changePassword() {
  if (submitting.value) return;
  errorMessage.value = "";
  if (newPassword.value.length < 12) { errorMessage.value = tr("setupPasswordShort"); return; }
  if (newPassword.value !== confirmNewPassword.value) { errorMessage.value = tr("setupPasswordsMismatch"); return; }
  const request = pageRequests.begin("auth");
  submitting.value = true;
  try {
    await adminApi.changePassword(newPassword.value, request.signal);
    if (!request.isCurrent()) return;
    newPassword.value = ""; confirmNewPassword.value = ""; screen.value = "admin";
    await router.replace("/admin");
    if (request.isCurrent()) await loadAdminData(request);
  } catch (error) { if (request.isCurrent()) report(error); }
  finally { if (request.isCurrent()) submitting.value = false; request.finish(); }
}
async function logout() {
  if (loggingOut.value) return;
  cancelPendingWork();
  const request = pageRequests.begin("auth");
  loggingOut.value = true; errorMessage.value = "";
  try {
    await adminApi.logout(request.signal);
    if (!request.isCurrent()) return;
    cancelPendingWork(); resetPrivateState(); csrfToken.value = ""; screen.value = "login";
    await router.replace("/admin/login");
  } catch (error) { if (request.isCurrent()) report(error); }
  finally { if (request.isCurrent()) loggingOut.value = false; request.finish(); }
}
async function loadOverview() {
  const request = pageRequests.begin("overview");
  try {
    const result = await adminApi.overview(request.signal);
    if (request.isCurrent()) Object.assign(overview, result);
  } catch (error) { if (request.isCurrent()) report(error); }
  finally { request.finish(); }
}

function handleWebRtcToggle() { if (serverForm.webRtcEnabled) webrtcPortNoticeOpen.value = true; }
async function dismissLegacyNotice() {
  const request = pageRequests.begin("legacy-notice");
  try {
    await adminApi.dismissLegacyNotice(request.signal);
    if (request.isCurrent()) overview.legacyConfigImported = false;
  } catch (error) { if (request.isCurrent()) report(error); }
  finally { request.finish(); }
}
function persistLanguage() { localStorage.setItem("webspeak:language", language.value); }
function cycleTheme() { themeMode.value = nextTheme(themeMode.value); saveTheme(themeMode.value); }
</script>

<style scoped src="../styles/admin.css"></style>
