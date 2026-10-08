export type SiteLanguage = "zh" | "en" | "de" | "ru" | "ja";

/**
 * Built-in welcome-page templates. An empty administrator value always falls
 * back to one of these strings, so adding a language never leaves the page
 * with a blank welcome message.
 */
export const DEFAULT_WELCOME_TEXTS: Record<SiteLanguage, string> = {
  zh: "无需安装 TeamSpeak 客户端，打开浏览器即可加入语音频道。",
  en: "No TeamSpeak client required. Open your browser to join a voice channel.",
  de: "Kein TeamSpeak-Client nötig. Öffne den Browser und tritt einem Sprachkanal bei.",
  ru: "Клиент TeamSpeak не нужен: откройте браузер и присоединитесь к голосовому каналу.",
  ja: "TeamSpeak クライアントは不要です。ブラウザを開くだけで音声チャンネルに参加できます。",
};

export function resolveWelcomeTexts(values: Partial<Record<SiteLanguage, string>>): Record<SiteLanguage, string> {
  return {
    zh: values.zh?.trim() || DEFAULT_WELCOME_TEXTS.zh,
    en: values.en?.trim() || DEFAULT_WELCOME_TEXTS.en,
    de: values.de?.trim() || DEFAULT_WELCOME_TEXTS.de,
    ru: values.ru?.trim() || DEFAULT_WELCOME_TEXTS.ru,
    ja: values.ja?.trim() || DEFAULT_WELCOME_TEXTS.ja,
  };
}
