<template>
  <form
    v-if="props.layout === 'terminal'"
    class="join-form terminal-join-form"
    data-ws-part="home.form"
    :data-ws-state="connecting ? 'connecting' : 'ready'"
    @submit.prevent="submitTerminal"
  >
    <div
      class="terminal-entry-row"
      data-ws-part="home.primary-entry"
    >
      <label
        class="terminal-nickname-field"
        data-ws-part="home.field"
        for="terminal-nickname"
      >
        <input
          id="terminal-nickname"
          v-model="nickname"
          autocomplete="nickname"
          maxlength="30"
          :autofocus="autofocusNickname"
          :placeholder="t('nicknameEnterPlaceholder')"
        />
      </label>
      <button
        class="primary-button connect-button terminal-connect-button"
        data-ws-part="home.connect"
        :disabled="joinDisabled || connecting"
        type="submit"
      >
        <span
          v-if="connecting"
          class="button-spinner"
        ></span>
        <span>{{ connecting ? t("connecting") : t("joinVoice") }}</span>
      </button>
    </div>

    <details
      class="terminal-advanced"
      data-ws-part="home.advanced"
      :data-ws-state="terminalAdvancedOpen ? 'open' : 'closed'"
      @toggle="onTerminalAdvancedToggle"
    >
      <summary data-ws-part="home.advanced.toggle">
        <span class="terminal-advanced-arrow" aria-hidden="true">›</span>
        <span>{{ t("serverOptions") }}</span>
        <small>{{ t("advancedSettings") }}</small>
      </summary>

      <div
        class="terminal-advanced-content"
        data-ws-part="home.advanced.content"
      >
        <div
          v-if="accessMode === 'open'"
          class="terminal-target-grid"
          data-ws-part="home.server-target"
        >
          <label
            class="terminal-field-label"
            data-ws-part="home.field-label"
            for="terminal-server-address"
          >
            <span>{{ t("serverAddress") }}</span>
            <input
              id="terminal-server-address"
              v-model="serverHost"
              autocomplete="url"
              inputmode="url"
              autocapitalize="none"
              autocorrect="off"
              :spellcheck="false"
              :placeholder="t('serverAddressPlaceholder')"
            />
          </label>
          <label
            class="terminal-field-label"
            data-ws-part="home.field-label"
            for="terminal-server-port"
          >
            <span>{{ t("serverPort") }}</span>
            <input
              id="terminal-server-port"
              v-model="serverPort"
              inputmode="numeric"
              type="text"
              maxlength="5"
              :placeholder="t('serverPortPlaceholder')"
            />
          </label>
        </div>

        <div
          v-if="openTargetPrefillBlocked"
          class="terminal-inline-notice"
          data-ws-part="home.notice"
          data-ws-state="target-prefill-blocked"
        >{{ t("openTargetDefaultNotPrefilled") }}</div>

        <label
          v-if="accessMode === 'open'"
          class="terminal-field-label"
          data-ws-part="home.field-label"
          for="terminal-server-password"
        >
          <span>{{ t("serverPassword") }} <em>{{ t("optional") }}</em></span>
          <input
            id="terminal-server-password"
            v-model="serverPassword"
            type="password"
            autocomplete="off"
            :placeholder="t('optionalPassword')"
          />
        </label>

        <label
          class="terminal-field-label"
          data-ws-part="home.field-label"
          for="terminal-channel"
        >
          <span>{{ t("targetChannel") }} <em>{{ t("optional") }}</em></span>
          <input
            id="terminal-channel"
            v-model="channel"
            :placeholder="t('emptyDefault')"
          />
        </label>

        <div
          v-if="accelerationRelays.length"
          class="terminal-relay-choice"
          data-ws-part="home.relay-choice"
        >
          <div data-ws-part="home.relay-choice.copy">
            <strong>{{ t("relayAcceleration") }}</strong>
            <small>{{ t("relayAccelerationHint") }}</small>
          </div>
          <select
            v-model="accelerationRelayId"
            :aria-label="t('relayAcceleration')"
          >
            <option value="">{{ t("directConnection") }}</option>
            <option
              v-for="relay in accelerationRelays"
              :key="relay.id"
              :value="relay.id"
            >{{ relay.name }}</option>
          </select>
        </div>

        <div
          class="terminal-identity"
          data-ws-part="home.identity"
        >
          <label class="terminal-remember-identity">
            <input
              v-model="rememberIdentity"
              type="checkbox"
            />
            <span>
              <strong>{{ t("rememberIdentity") }}</strong>
              <small>{{ t("rememberIdentityHint") }}</small>
            </span>
          </label>
          <div
            class="identity-actions"
            data-ws-part="home.identity-actions"
          >
            <button
              type="button"
              data-ws-part="home.identity-import.open"
              @click="emit('importIdentity')"
            >{{ t("identityImport") }}</button>
            <button
              type="button"
              data-ws-part="home.identity-export.button"
              :disabled="identityExportBusy || !rememberIdentity || !hasIdentity"
              @click="emit('exportIdentity')"
            >{{ t("identityExport") }}</button>
          </div>
        </div>
        <p
          v-if="rememberIdentity"
          class="terminal-identity-warning"
        >{{ t("rememberIdentityConcurrentWarning") }}</p>
      </div>
    </details>

    <button
      v-if="connecting"
      type="button"
      class="cancel-connect-button terminal-cancel-connect"
      @click="emit('disconnect')"
    >{{ t("cancel") }}</button>
  </form>

  <form
    v-else
    class="join-form"
    data-ws-part="home.form"
    @submit.prevent="emit('connect')"
  >
    <div
      v-if="accessMode === 'open'"
      class="field-grid target-fields"
      data-ws-part="home.server-target"
    >
      <label
        class="field-label"
        data-ws-part="home.field-label"
        for="server-address"
        ><span>{{ t("serverAddress") }}</span
        ><div
          class="field-wrap"
          data-ws-part="home.field"
          ><Icon
            name="server"
            :size="17" /><input
            id="server-address"
            v-model="serverHost"
            autocomplete="url"
            inputmode="url"
            autocapitalize="none"
            autocorrect="off"
            :spellcheck="false"
            enterkeyhint="next"
            :placeholder="t('serverAddressPlaceholder')" /></div
      ></label>
      <label
        class="field-label"
        data-ws-part="home.field-label"
        for="server-port"
        ><span>{{ t("serverPort") }}</span
        ><div
          class="field-wrap"
          data-ws-part="home.field"
          ><Icon
            name="hash"
            :size="17" /><input
            id="server-port"
            v-model="serverPort"
            inputmode="numeric"
            enterkeyhint="next"
            type="text"
            maxlength="5"
            :placeholder="t('serverPortPlaceholder')" /></div
      ></label>
    </div>
    <div
      v-if="openTargetPrefillBlocked"
      class="notice warning-notice"
      data-ws-part="home.notice"
      data-ws-state="target-prefill-blocked"
      ><span class="notice-symbol">i</span
      ><span>{{ t("openTargetDefaultNotPrefilled") }}</span></div
    >
    <div
      v-if="accelerationRelays.length"
      class="acceleration-choice"
      data-ws-part="home.relay-choice"
      ><div
        class="acceleration-copy"
        data-ws-part="home.relay-choice.copy"
        ><strong>{{ t("relayAcceleration") }}</strong
        ><small>{{ t("relayAccelerationHint") }}</small></div
      ><select
        v-model="accelerationRelayId"
        :aria-label="t('relayAcceleration')"
        ><option value="">{{ t("directConnection") }}</option
        ><option
          v-for="relay in accelerationRelays"
          :key="relay.id"
          :value="relay.id"
          >{{ relay.name }}</option
        ></select
      ></div
    >
    <div
      v-if="accessMode === 'open' && (favoriteServers.length || recentServers.length)"
      class="local-servers"
      data-ws-part="home.server-history"
    >
      <div
        v-if="favoriteServers.length"
        class="local-server-group"
        data-ws-part="home.server-history.group"
        data-ws-state="favorite"
        ><span>{{ t("favoriteServers") }}</span
        ><button
          v-for="favorite in favoriteServers"
          :key="favorite.id"
          type="button"
          @click="emit('selectServer', favorite.address, favorite.nickname)"
          >{{ favorite.label }}</button
        ></div
      >
      <div
        v-if="recentServers.length"
        class="local-server-group"
        data-ws-part="home.server-history.group"
        data-ws-state="recent"
        ><span>{{ t("recentServers") }}</span
        ><button
          v-for="recent in recentServers"
          :key="recent.id"
          type="button"
          @click="emit('selectServer', recent.address, recent.nickname)"
          >{{ recent.address }}</button
        ></div
      >
    </div>
    <button
      v-if="accessMode === 'open' && serverHost.trim()"
      type="button"
      class="favorite-toggle"
      data-ws-part="home.favorite-toggle"
      @click="emit('toggleFavorite')"
      >{{ isFavorite ? t("removeFavorite") : t("saveFavorite") }}</button
    >

    <template v-if="accessMode === 'open'">
      <label
        class="field-label"
        data-ws-part="home.field-label"
        for="server-password"
        >{{ t("serverPassword") }} <span>{{ t("optional") }}</span></label
      >
      <div
        class="field-wrap"
        data-ws-part="home.field"
        ><Icon
          name="lock"
          :size="17" /><input
          id="server-password"
          v-model="serverPassword"
          type="password"
          autocomplete="off"
          :placeholder="t('optionalPassword')"
      /></div>
    </template>

    <label
      class="field-label"
      data-ws-part="home.field-label"
      for="nickname"
      >{{ t("nickname") }}</label
    >
    <div
      class="field-wrap"
      data-ws-part="home.field"
    >
      <Icon
        name="users"
        :size="17"
      />
      <input
        id="nickname"
        v-model="nickname"
        autocomplete="nickname"
        maxlength="30"
        :placeholder="t('nicknamePlaceholder')"
        :autofocus="autofocusNickname"
      />
    </div>

    <details
      class="identity-options"
      data-ws-part="home.identity"
      ><summary>{{ t("identityOptions") }}</summary
      ><label
        class="field-label"
        data-ws-part="home.field-label"
        for="channel"
        >{{ t("targetChannel") }} <span>{{ t("optional") }}</span></label
      ><div class="field-wrap" data-ws-part="home.field"><Icon name="hash" :size="17" /><input
        id="channel"
        v-model="channel"
        :placeholder="t('emptyDefault')"
        @keyup.enter="emit('connect')"
      /></div
      ><div class="identity-controls"
        ><label class="remember-identity"
          ><input
            v-model="rememberIdentity"
            type="checkbox"
          /><span
            ><strong>{{ t("rememberIdentity") }}</strong
            ><small>{{ t("rememberIdentityHint") }}</small></span
          ></label
        ><div
          class="identity-actions"
          data-ws-part="home.identity-actions"
          ><button
            type="button"
            class="identity-action-button"
            data-ws-part="home.identity-import.open"
            @click="emit('importIdentity')"
            >{{ t("identityImport") }}</button
          ><button
            type="button"
            class="identity-action-button"
            data-ws-part="home.identity-export.button"
            :disabled="identityExportBusy || !rememberIdentity || !hasIdentity"
            @click="emit('exportIdentity')"
            >{{ t("identityExport") }}</button
          ></div
        ></div
      ></details
    ><p
      v-if="rememberIdentity"
      class="identity-warning"
      >{{ t("rememberIdentityConcurrentWarning") }}</p
    >

    <button
      class="primary-button connect-button"
      data-ws-part="home.connect"
      :disabled="joinDisabled"
      type="submit"
    >
      <span
        v-if="connecting"
        class="button-spinner"
      ></span>
      <span>{{ connecting ? t("connecting") : t("joinVoice") }}</span>
      <Icon
        v-if="!connecting"
        name="chevron-right"
        :size="17"
      />
    </button>
    <button
      v-if="connecting"
      type="button"
      class="cancel-connect-button"
      @click="emit('disconnect')"
      >{{ t("cancel") }}</button
    >
  </form>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Icon from "../Icon.vue";
import type { FavoriteServer, RecentServer } from "../../services/local-persistence.js";

const serverHost = defineModel<string>("serverHost", { required: true });
const serverPort = defineModel<string>("serverPort", { required: true });
const serverPassword = defineModel<string>("serverPassword", { required: true });
const nickname = defineModel<string>("nickname", { required: true });
const channel = defineModel<string>("channel", { required: true });
const rememberIdentity = defineModel<boolean>("rememberIdentity", { required: true });
const accelerationRelayId = defineModel<string>("accelerationRelayId", { required: true });

const props = defineProps<{
  layout?: "classic" | "terminal";
  autofocusNickname?: boolean;
  accessMode: "fixed" | "open";
  openTargetPrefillBlocked: boolean;
  accelerationRelays: ReadonlyArray<{ id: string; name: string }>;
  favoriteServers: readonly FavoriteServer[];
  recentServers: readonly RecentServer[];
  isFavorite: boolean;
  identityExportBusy: boolean;
  hasIdentity: boolean;
  connecting: boolean;
  joinDisabled: boolean;
  t: (key: string, variables?: Record<string, string | number>) => string;
}>();

const emit = defineEmits<{
  connect: [];
  disconnect: [];
  importIdentity: [];
  exportIdentity: [];
  toggleFavorite: [];
  selectServer: [address: string, nickname?: string];
}>();

const terminalAdvancedOpen = ref(false);

function submitTerminal(): void {
  if (props.connecting) return;
  emit("connect");
}

function onTerminalAdvancedToggle(event: Event): void {
  terminalAdvancedOpen.value = (event.currentTarget as HTMLDetailsElement).open;
}
</script>

<style scoped>
.terminal-join-form {
  display: grid;
  gap: 9px;
  min-width: 0;
}

.terminal-entry-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 8px;
  min-width: 0;
  align-items: stretch;
}

.terminal-nickname-field,
.terminal-nickname-field:focus-within {
  position: relative;
  display: flex;
  min-width: 0;
  align-items: center;
  gap: 0;
  padding: 0 8px;
  background: transparent !important;
  border: 0 !important;
  border-radius: 0;
  box-shadow: none !important;
  outline: none !important;
}

.terminal-nickname-field:focus-within {
  opacity: 1;
}

.terminal-nickname-field input,
.terminal-nickname-field input:focus,
.terminal-nickname-field input:focus-visible,
.terminal-field-label input {
  appearance: none;
  -webkit-appearance: none;
  min-width: 0;
  width: 100%;
  color: var(--terminal-text, #f4f4f5);
  background: transparent !important;
  border: 0 !important;
  border-radius: 0;
  box-shadow: none !important;
  outline: none !important;
  font-size: 13px;
}

.terminal-nickname-field input {
  flex: 1 1 auto;
  padding: 10px 0;
}

.terminal-nickname-field input::placeholder,
.terminal-field-label input::placeholder {
  color: var(--terminal-muted, #71717a);
}

.terminal-connect-button {
  min-width: 96px;
  min-height: 40px;
  padding: 0 16px;
  color: var(--terminal-button-text, #0b0c0e);
  background: var(--terminal-button-bg, #f4f4f5);
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
  transition: background .2s ease, opacity .2s ease, transform .1s ease;
}

.terminal-connect-button:hover:not(:disabled) {
  background: var(--terminal-button-hover, #fff);
}

.terminal-connect-button:active:not(:disabled) {
  transform: scale(.98);
}

.terminal-connect-button:disabled {
  color: var(--terminal-button-disabled-text, #71717a);
  background: var(--terminal-button-disabled-bg, #d4d4d8);
  cursor: wait;
}

.terminal-advanced {
  margin-top: 0;
  padding: 9px 6px 0;
  border-top: 1px solid var(--terminal-border, rgba(255, 255, 255, .08));
}

.terminal-advanced summary {
  display: flex;
  min-height: 23px;
  align-items: center;
  gap: 6px;
  color: var(--terminal-muted, #71717a);
  cursor: pointer;
  font-size: 11px;
  list-style: none;
  outline: 0;
  user-select: none;
}

.terminal-advanced summary::-webkit-details-marker {
  display: none;
}

.terminal-advanced summary::marker {
  content: "";
}

.terminal-advanced summary:hover,
.terminal-advanced summary:focus-visible {
  color: var(--terminal-text, #f4f4f5);
}

.terminal-advanced summary:focus-visible {
  border-radius: 5px;
  box-shadow: 0 0 0 3px var(--terminal-accent-soft, rgba(45, 212, 191, .12));
}

.terminal-advanced-arrow {
  display: inline-block;
  color: var(--terminal-accent, #2dd4bf);
  font-size: 16px;
  line-height: 1;
  transition: transform .2s ease;
}

.terminal-advanced[open] .terminal-advanced-arrow {
  transform: rotate(90deg);
}

.terminal-advanced summary small {
  margin-left: auto;
  color: var(--terminal-subtle, rgba(244, 244, 245, .48));
  font-size: 9px;
}

.terminal-advanced-content {
  display: grid;
  gap: 10px;
  padding: 11px 0 4px;
}

.terminal-inline-notice {
  display: flex;
  min-width: 0;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 9px 10px;
  color: var(--terminal-muted, #71717a);
  background: var(--terminal-field-bg-soft, rgba(0, 0, 0, .18));
  border: 1px solid var(--terminal-border, rgba(255, 255, 255, .08));
  border-radius: 7px;
  font-size: 10px;
}

.terminal-inline-notice {
  justify-content: flex-start;
  color: var(--terminal-warning, #d8b66d);
  background: var(--terminal-warning-bg, rgba(117, 83, 25, .12));
  border-color: var(--terminal-warning-border, rgba(214, 169, 72, .2));
  line-height: 1.45;
}

.terminal-target-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 120px;
  gap: 8px;
}

.terminal-field-label {
  display: grid;
  min-width: 0;
  gap: 5px;
  color: var(--terminal-muted, #71717a);
  font-size: 10px;
}

.terminal-field-label > span {
  display: flex;
  align-items: baseline;
  gap: 5px;
}

.terminal-field-label em {
  color: var(--terminal-subtle, rgba(244, 244, 245, .42));
  font-size: 9px;
  font-style: normal;
}

.terminal-field-label input {
  padding: 9px 10px;
  background: var(--terminal-field-bg, rgba(0, 0, 0, .22));
  border: 1px solid var(--terminal-border, rgba(255, 255, 255, .08));
  border-radius: 7px;
  transition: border-color .2s ease, box-shadow .2s ease;
}

.terminal-field-label input:focus {
  border-color: var(--terminal-border-focus, rgba(45, 212, 191, .46));
  box-shadow: 0 0 0 3px var(--terminal-accent-soft, rgba(45, 212, 191, .12));
}

.terminal-relay-choice {
  display: flex;
  min-width: 0;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 9px 10px;
  background: var(--terminal-field-bg-soft, rgba(0, 0, 0, .14));
  border: 1px solid var(--terminal-border, rgba(255, 255, 255, .08));
  border-radius: 7px;
}

.terminal-relay-choice > div {
  display: grid;
  min-width: 0;
  gap: 2px;
}

.terminal-relay-choice strong,
.terminal-relay-choice small {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.terminal-relay-choice strong {
  color: var(--terminal-text, #f4f4f5);
  font-size: 10px;
}

.terminal-relay-choice small {
  color: var(--terminal-muted, #71717a);
  font-size: 9px;
}

.terminal-relay-choice select {
  min-width: 120px;
  max-width: 46%;
  padding: 6px 8px;
  color: var(--terminal-text, #f4f4f5);
  background: var(--terminal-surface-hover, #1c1f24);
  border: 1px solid var(--terminal-border, rgba(255, 255, 255, .08));
  border-radius: 6px;
  outline: 0;
  font-size: 10px;
}

.terminal-relay-choice select:focus {
  border-color: var(--terminal-border-focus, rgba(45, 212, 191, .46));
  box-shadow: 0 0 0 3px var(--terminal-accent-soft, rgba(45, 212, 191, .12));
}

.terminal-identity button {
  min-width: 0;
  padding: 5px 7px;
  overflow: hidden;
  color: var(--terminal-muted, #71717a);
  background: transparent;
  border: 1px solid var(--terminal-border, rgba(255, 255, 255, .08));
  border-radius: 5px;
  cursor: pointer;
  font-size: 9px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.terminal-identity button:hover:not(:disabled),
.terminal-identity button:focus-visible:not(:disabled) {
  color: var(--terminal-text, #f4f4f5);
  border-color: var(--terminal-border-focus, rgba(45, 212, 191, .46));
  outline: 0;
}

.terminal-identity {
  display: flex;
  min-width: 0;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-top: 2px;
}

.terminal-remember-identity {
  display: flex;
  min-width: 0;
  align-items: flex-start;
  gap: 8px;
  color: var(--terminal-text, #f4f4f5);
  cursor: pointer;
}

.terminal-remember-identity input {
  width: 14px;
  height: 14px;
  flex: 0 0 14px;
  margin: 2px 0 0;
  accent-color: var(--terminal-accent, #2dd4bf);
}

.terminal-remember-identity span {
  display: grid;
  min-width: 0;
  gap: 2px;
}

.terminal-remember-identity strong {
  font-size: 10px;
  font-weight: 600;
}

.terminal-remember-identity small,
.terminal-identity-warning {
  color: var(--terminal-muted, #71717a);
  font-size: 9px;
  line-height: 1.4;
}

.identity-actions {
  display: flex;
  flex: 0 0 auto;
  gap: 6px;
}

.terminal-identity button:disabled {
  cursor: not-allowed;
  opacity: .4;
}

.terminal-identity-warning {
  margin: -4px 0 0 22px;
}

.terminal-cancel-connect {
  justify-self: end;
  padding: 4px 7px;
  color: var(--terminal-muted, #71717a);
  background: transparent;
  border: 1px solid var(--terminal-border, rgba(255, 255, 255, .08));
  border-radius: 5px;
  cursor: pointer;
  font-size: 10px;
}

.terminal-cancel-connect:hover,
.terminal-cancel-connect:focus-visible {
  color: var(--terminal-text, #f4f4f5);
  border-color: var(--terminal-border-focus, rgba(45, 212, 191, .46));
  outline: 0;
}

@media (prefers-reduced-motion: reduce) {
  .terminal-nickname-field,
  .terminal-connect-button,
  .terminal-advanced-arrow,
  .terminal-field-label input {
    transition: none;
  }
}

@media (max-width: 600px) {
  .terminal-entry-row {
    grid-template-columns: minmax(0, 1fr);
  }

  .terminal-connect-button {
    width: 100%;
    min-height: 42px;
  }

  .terminal-advanced summary {
    min-height: 30px;
  }

  .terminal-advanced summary small {
    max-width: 42%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .terminal-target-grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .terminal-relay-choice,
  .terminal-identity {
    align-items: stretch;
    flex-direction: column;
  }

  .terminal-relay-choice select {
    width: 100%;
    max-width: none;
  }

  .terminal-identity .identity-actions {
    width: 100%;
  }

  .terminal-identity .identity-actions button {
    flex: 1 1 0;
  }
}

@media (max-width: 380px) {
  .terminal-advanced summary small {
    display: none;
  }

  .terminal-identity-warning {
    margin-left: 0;
  }
}
</style>
