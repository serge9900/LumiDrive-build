import me.aap.utils.log.LumiDriveLogTools;

/** No Android SDK needed: runs with javac as a GitHub Actions unit test. */
public final class LumiDriveLogToolsTest {
    public static void main(String[] args) {
        String secret = "A6898KEYVZ6C3GDHNLBBN5AY";
        String line = "[22-10-26 21:15:02][INFO][main][MediaSessionCallback] Start playing " +
                "http://viewer:pass@example.com/iptv/" + secret + "/31553/index.m3u?token=abc";
        String safe = LumiDriveLogTools.redact(line);
        check(!safe.contains(secret), "Stream auth token leaked");
        check(!safe.contains("viewer"), "Stream userinfo leaked");
        check(!safe.contains("pass"), "Stream password leaked");
        check(!safe.contains("31553/index"), "Stream URL path leaked");
        check(!safe.contains("token=abc"), "URL query leaked");
        check(safe.contains("http://example.com/[redacted]"), "Host and scheme missing");

        check("[redacted-url]".equals(LumiDriveLogTools.redact(
                "https://%malformed")), "Malformed URL was not concealed");
        check("password=[redacted]".equals(
                LumiDriveLogTools.redact("password=abc123")), "Password key leaked");

        String entries = "[27-10-26 11:00:00][INFO][main][LumiDrive] Hello\n" +
                "[27-10-26 11:00:01][ERROR][main][FermataWebClient] HTTP error\n" +
                "java.lang.Exception: Failed\n  at MyClass.run(MyClass.java:3)\n" +
                "[27-10-26 11:00:02][WARN][main][MediaSessionCallback.onEngineError] Stream failed\n" +
                "[27-10-26 11:00:03][INFO][main][LumiDrive] [LumiDrive][AUTO] Connection begun\n" +
                "[27-10-26 11:00:04][INFO][main][LumiDrive] [LumiDrive][IPTV] Player started\n";

        String errors = LumiDriveLogTools.preview(entries, LumiDriveLogTools.FILTER_ERROR);
        check(errors.contains("HTTP error"), "Error filtering failed");
        check(errors.contains("at MyClass.run"), "Stack trace was lost");
        check(!errors.contains("Stream failed"), "Error filter included warning");

        String warnings = LumiDriveLogTools.preview(entries, LumiDriveLogTools.FILTER_WARN);
        check(warnings.contains("Stream failed"), "Warning filtering failed");
        check(!warnings.contains("HTTP error"), "Warning filter included error");

        String auto = LumiDriveLogTools.preview(entries, LumiDriveLogTools.FILTER_AUTO);
        check(auto.contains("Connection begun"), "Android Auto filter failed");
        check(!auto.contains("Player started"), "Android Auto filter included IPTV");

        String iptv = LumiDriveLogTools.preview(entries, LumiDriveLogTools.FILTER_IPTV);
        check(iptv.contains("Player started"), "IPTV filter failed");

        String web = LumiDriveLogTools.preview(entries, LumiDriveLogTools.FILTER_WEB);
        check(web.contains("HTTP error"), "Web filter failed");

        check(LumiDriveLogTools.summary(entries).equals(
                "ERROR 1  |  WARN 1  |  INFO 3"), "Summary is incorrect");

        System.out.println("LumiDriveLogTools privacy and filter tests PASSED");
    }

    private static void check(boolean ok, String message) {
        if (!ok) throw new AssertionError(message);
    }
}
