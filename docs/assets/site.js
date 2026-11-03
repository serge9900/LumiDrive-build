/* LumiDrive website — no analytics, cookies, tracking or personal data. */
(() => {
  "use strict";
  const repository = "serge9900/LumiDrive-build";
  const fallback = "https://github.com/" + repository + "/releases/latest";
  const status = document.querySelector("[data-latest-version]");
  const buttons = document.querySelectorAll("[data-download]");
  const english = document.documentElement.lang.toLowerCase().startsWith("en");
  const defaultLabel = status?.dataset.fallback || (english ? "Latest published release" : "Последний опубликованный релиз");

  // Progressive enhancement: if the public GitHub API isn't available, the
  // download button remains a valid link to the official latest Release page.
  const fallbackStatus = () => {
    if (status) status.textContent = defaultLabel;
    for (const link of buttons) link.setAttribute("href", fallback);
  };

  fetch("https://api.github.com/repos/" + repository + "/releases/latest", {
    headers: { "Accept": "application/vnd.github+json" },
    mode: "cors",
    credentials: "omit",
    cache: "no-store",
  })
    .then((response) => {
      if (!response.ok) throw new Error("Release API unavailable");
      return response.json();
    })
    .then((release) => {
      const tag = String(release?.tag_name || "");
      if (!/^v\d+\.\d+\.\d+$/.test(tag) || release?.draft || release?.prerelease) {
        fallbackStatus();
        return;
      }
      const expected = "LumiDrive-" + tag + "-arm64.apk";
      const base = "https://github.com/" + repository + "/releases/download/" + tag + "/";
      const assets = Array.isArray(release?.assets) ? release.assets : [];
      const asset = assets.find(a =>
        a?.name === expected &&
        typeof a?.browser_download_url === "string" &&
        a.browser_download_url === base + expected
      );
      if (status) {
        status.textContent = "LumiDrive " + tag.substring(1) + " · Android ARM64";
      }
      for (const link of buttons) {
        link.href = asset?.browser_download_url || fallback;
        link.title = asset
          ? (english ? "Download " : "Скачать ") + expected
          : defaultLabel;
      }
    })
    .catch(fallbackStatus);
})();
