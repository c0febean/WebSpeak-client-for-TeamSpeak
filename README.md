<div align="center">
  <a id="readme-top"></a>

  <h1>WebSpeak</h1>

  <p><strong>让 TeamSpeak 自然地进入浏览器。</strong></p>
  <p>A self-hosted browser voice client for TeamSpeak 3 and TeamSpeak 6.</p>

  [![License](https://img.shields.io/badge/license-AGPL--3.0--only-0f766e?style=flat-square)](./LICENSE)

  <p>
    <a href="./docs/README.zh-CN.md">简体中文文档</a> ·
    <a href="./docs/README.en.md">English documentation</a> ·
    <a href="./docs/README.de.md">Deutsche Dokumentation</a> ·
    <a href="./docs/README.ru.md">Русская документация</a> ·
    <a href="./docs/README.ja.md">日本語ドキュメント</a>
  </p>
</div>

## 项目简介 · Overview

| 逻辑 | 中文 | English |
| --- | --- | --- |
| **WHAT** | WebSpeak 是一个可自行部署的 TeamSpeak 3 / TeamSpeak 6 网页客户端与语音网关。 | WebSpeak is a self-hosted browser client and voice gateway for TeamSpeak 3 and TeamSpeak 6. |
| **WHY** | 无需安装桌面客户端，用户打开网页即可加入频道；部署者仍然掌控目标服务器、访问策略和数据。 | Users can join a voice channel from a browser without installing a desktop client, while the operator keeps control of servers, access, and data. |
| **HOW** | 部署后在管理员控制台配置 TeamSpeak 目标和访问方式，浏览器负责交互与音频，WebSpeak 负责网关连接。 | Configure the TeamSpeak target and access policy in the administration console. The browser handles interaction and audio; WebSpeak provides the gateway connection. |

## Fork 与许可证 · Fork and license

本仓库是 [上游 WebSpeak](https://github.com/EchoSixHIYA/WebSpeak-client-for-TeamSpeak) 的 fork，当前维护地址为 [c0febean/WebSpeak-client-for-TeamSpeak](https://github.com/c0febean/WebSpeak-client-for-TeamSpeak)。这是一个基于上游项目修改的版本，首次修改日期为 **2026-10-08**；原项目的来源、版权和许可证要求继续适用。

WebSpeak 使用 [GNU Affero General Public License v3.0 only](./LICENSE) 发布。软件按“现状”提供，不提供任何明示或默示保证。若通过网络提供本 fork 的修改版本，应向用户免费提供实际运行版本的对应源代码，并提供便于获取的方式；仅当本仓库内容与运行版本一致时，才能作为源代码入口。

This fork remains under the [GNU Affero General Public License v3.0 only](./LICENSE). It is provided “as is” without warranty. When a modified version is offered over a network, the Corresponding Source for the running version must be available to users at no charge through a convenient means.

## 文档 · Documentation

- [简体中文](./docs/README.zh-CN.md)
- [English](./docs/README.en.md)
- [Deutsch](./docs/README.de.md)
- [Русский](./docs/README.ru.md)
- [日本語](./docs/README.ja.md)
- [皮肤开发规范 / Skin Development Guide](./docs/SKIN_DEVELOPMENT.md)
- [皮肤开发 Agent Skill / Skin Development Agent Skill](./.agents/skills/webspeak-skin-development/SKILL.md)

<div align="right"><a href="#readme-top">返回顶部 · Back to top ↑</a></div>
