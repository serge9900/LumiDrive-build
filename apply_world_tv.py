#!/usr/bin/env python3
"""Add IPTV-org country selection without changing playback or existing sources."""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

def apply(root, source):
    def replace(path, old, new):
        p = root / path
        text = p.read_text(encoding="utf-8")
        if text.count(old) != 1:
            raise RuntimeError(f"Expected one patch anchor in {path}: {old[:80]}")
        p.write_text(text.replace(old, new), encoding="utf-8")
    tv = "modules/tv/src/main/java/me/aap/fermata/addon/tv/"
    for name in ("LumiWorldCountries.java", "LumiWorldTv.java"):
        (root / tv / name).write_text((source / "src" / name).read_text(encoding="utf-8"), encoding="utf-8")
    replace(tv + "TvFragment.java", "public void addSource() {",
        "public void addSource() {\n        LumiWorldTv.chooseSource(this, this::addOwnSource);\n    }\n\n    private void addOwnSource() {")
    replace(tv + "TvFragment.java", "super.contributeToNavBarMenu(builder);",
        """super.contributeToNavBarMenu(builder);
        builder.addItem(me.aap.fermata.R.id.lumi_world_tv,
                me.aap.fermata.R.drawable.tv, me.aap.fermata.R.string.lumi_world_tv)
                .setHandler(item -> { LumiWorldTv.show(this); return true; });""")
    replace(tv + "TvRootItem.java", "public void addSource(TvM3uFile m3u) {",
        "public FutureSupplier<TvM3uItem> addSource(TvM3uFile m3u) {")
    replace(tv + "TvRootItem.java", "addItem(TvM3uItem.create(this, m3u, counter));",
        "TvM3uItem item = TvM3uItem.create(this, m3u, counter);\n        return addItem(item).map(v -> item);")
    replace(tv + "TvRootItem.java", "\n\tprivate FutureSupplier<TvM3uItem> create(int srcId) {",
        "\n    private final java.util.Map<String, me.aap.utils.async.Promise<TvM3uItem>> worldLoads =\n            new java.util.HashMap<>();\n\n    // Called on the main thread. Share concurrent requests before any asynchronous work.\n    public FutureSupplier<TvM3uItem> openWorldCountry(String code, String name) {\n        String url = LumiWorldCountries.url(code);\n        me.aap.utils.async.Promise<TvM3uItem> pending = worldLoads.get(url);\n        if (pending != null) return pending;\n        me.aap.utils.async.Promise<TvM3uItem> result = new me.aap.utils.async.Promise<>();\n        worldLoads.put(url, result);\n        getUnsortedChildren().main().then(children -> {\n            for (Item child : children) {\n                if (child instanceof TvM3uItem\n                        && url.equals(((TvM3uItem) child).getResource().getUrl()))\n                    return completed((TvM3uItem) child);\n            }\n            return new TvM3uFileSystemProvider().loadWorldCountry(url, name + \" · IPTV-org\")\n                    .main().then(this::addSource);\n        }).main().onCompletion((item, error) -> {\n            worldLoads.remove(url);\n            if (error != null) result.completeExceptionally(error);\n            else result.complete(item);\n        });\n        return result;\n    }\n" + "\n\tprivate FutureSupplier<TvM3uItem> create(int srcId) {")
    replace(tv + "m3u/TvM3uFileSystemProvider.java", "\n\tprivate FutureSupplier<Boolean> requestPrefs(",
        "\n    public FutureSupplier<TvM3uFile> loadWorldCountry(String url, String name) {\n        BasicPreferenceStore prefs = new BasicPreferenceStore();\n        prefs.applyStringPref(NAME, name);\n        prefs.applyStringPref(URL, url);\n        prefs.applyIntPref(RESP_TIMEOUT, 15);\n        return load(prefs, TvM3uFileSystem.getInstance()).cast();\n    }\n" + "\n\tprivate FutureSupplier<Boolean> requestPrefs(")
    keys = ["lumi_world_tv","lumi_own_playlist","lumi_iptv_source","lumi_world_info","lumi_country_search","lumi_no_countries","lumi_country_loading","lumi_country_failed","lumi_try_again"]
    translations = {"en":["World channels","My own playlist","Add IPTV source","Source: IPTV-org. Choose a country to save its playlist. Some streams may be unavailable.","Search countries","No countries found","Loading country playlist…","Could not load this country. Check your connection and try again.","Try again"],"ru":["Каналы мира","Свой плейлист","Добавить источник IPTV","Источник: IPTV-org. Выберите страну, чтобы сохранить её плейлист. Некоторые трансляции могут быть недоступны.","Поиск страны","Страны не найдены","Загружаем плейлист страны…","Не удалось загрузить страну. Проверьте подключение и повторите попытку.","Повторить"]}
    for lang, values in translations.items():
        directory = "values-ru" if lang == "ru" else "values"
        resources = ET.Element("resources")
        for key, value in zip(keys, values):
            ET.SubElement(resources, "string", name=key).text = value
        ET.indent(resources)
        (root / "fermata/src/main/res" / directory / "lumi_world_tv.xml").write_text(
            ET.tostring(resources, encoding="unicode"), encoding="utf-8")
    (root / "fermata/src/main/res/values/lumi_world_ids.xml").write_text(
        '<resources><item name="lumi_world_tv" type="id"/></resources>', encoding="utf-8")
    replace("gradle/libs.versions.toml", 'appVersionCode = "292"', 'appVersionCode = "293"')
    replace("gradle/libs.versions.toml", 'appVersionName = "0.7.10"', 'appVersionName = "0.7.11"')
    with (root / "LUMIDRIVE_CHANGES.md").open("a", encoding="utf-8") as output:
        output.write("\n## 0.7.11 World channels (test build)\n"
          "- IPTV source chooser and menu entry: searchable countries supplied by IPTV-org.\n"
          "- Selected countries use the normal saved-source, cache, favorites and playback path.\n"
          "- Reopening a saved country reuses its URL; simultaneous requests are shared.\n"
          "- User sources remain editable and removable; no automatic channel playback.\n"
          "- Country index bundled from IPTV-org PLAYLISTS.md; playlists downloaded on selection.\n")
if __name__ == "__main__":
    apply(Path(sys.argv[1]).resolve(), Path(__file__).resolve().parent)
