package me.aap.utils.log;

import java.io.File;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Privacy-aware formatting for LumiDrive diagnostics.
 *
 * <p>Never write full stream URLs or authentication data to a diagnostic log.
 * This is intentionally conservative: the scheme and hostname are enough to
 * identify the service while the entire URL path, query and userinfo are hidden.
 * Used both at log-write time and when viewing/sharing legacy log entries.</p>
 */
public final class LumiDriveLogTools {
    public static final int FILTER_ALL = 0;
    public static final int FILTER_ERROR = 1;
    public static final int FILTER_WARN = 2;
    public static final int FILTER_AUTO = 3;
    public static final int FILTER_WEB = 4;
    public static final int FILTER_IPTV = 5;

    private static final int DISPLAY_LIMIT = 48000;
    private static final Pattern URL = Pattern.compile(
            "(?i)(?<![a-z0-9_])(?:https?|rtsp|rtmp|udp)://[^\\s\\x22\\x27<>\\[\\]{}()]+");
    private static final Pattern SECRET = Pattern.compile(
            "(?i)\\b(password|passwd|token|api[_-]?key|authorization|secret|access[_-]?token)" +
                    "\\s*[:=]\\s*[^\\s,;}&]+");
    private static final Pattern HEADER = Pattern.compile(
            "^\\[\\d{2}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}\\]\\[(DEBUG|INFO|WARN|ERROR)\\]");

    private LumiDriveLogTools() {
    }

    /**
     * Mask all full URL paths, queries, userinfo and common credential fields.
     * If a URL cannot be parsed, mask the whole URL rather than leaking it.
     */
    public static String redact(String input) {
        if (input == null || input.isEmpty()) return input == null ? "" : input;

        Matcher links = URL.matcher(input);
        StringBuffer safe = new StringBuffer(input.length());
        while (links.find()) {
            String value = links.group();
            String replacement = "[redacted-url]";
            try {
                URI uri = URI.create(value);
                String host = uri.getHost();
                String scheme = uri.getScheme();
                if (host != null && scheme != null) {
                    replacement = scheme.toLowerCase(Locale.ROOT) + "://" +
                            host.toLowerCase(Locale.ROOT) + "/[redacted]";
                }
            } catch (RuntimeException ignored) {
                // Invalid URL: hide the whole original value.
            }
            links.appendReplacement(safe, Matcher.quoteReplacement(replacement));
        }
        links.appendTail(safe);

        Matcher secrets = SECRET.matcher(safe.toString());
        StringBuffer cleaned = new StringBuffer(safe.length());
        while (secrets.find()) {
            secrets.appendReplacement(cleaned,
                    Matcher.quoteReplacement(secrets.group(1) + "=[redacted]"));
        }
        secrets.appendTail(cleaned);
        return cleaned.toString();
    }

    /** Return a bounded tail without reading multi-megabyte legacy files. */
    public static String readTail(File logFile, int maxBytes) throws IOException {
        if (logFile == null || !logFile.isFile() || maxBytes <= 0) return "";
        try (RandomAccessFile input = new RandomAccessFile(logFile, "r")) {
            long len = input.length();
            if (len == 0) return "";
            int take = (int) Math.min(len, maxBytes);
            byte[] bytes = new byte[take];
            input.seek(len - take);
            input.readFully(bytes);
            String text = new String(bytes, StandardCharsets.UTF_8);
            if (len > take) {
                int firstNewline = text.indexOf('\n');
                if (firstNewline >= 0) text = text.substring(firstNewline + 1);
            }
            return text;
        }
    }

    /**
     * Filter by complete log event, keeping stack-trace lines following each
     * selected entry. Always redact before filtering/displaying.
     */
    public static String preview(String untrustedLogText, int filter) {
        String clean = redact(untrustedLogText);
        if (clean.length() > DISPLAY_LIMIT) {
            clean = clean.substring(clean.length() - DISPLAY_LIMIT);
            int lineEnd = clean.indexOf('\n');
            if (lineEnd >= 0) clean = clean.substring(lineEnd + 1);
        }
        if (filter == FILTER_ALL) return clean;

        StringBuilder result = new StringBuilder();
        String[] lines = clean.split("\\r?\\n", -1);
        boolean keep = false;
        for (String line : lines) {
            Matcher header = HEADER.matcher(line);
            if (header.find()) {
                keep = shouldKeep(filter, header.group(1), line);
            }
            if (keep) result.append(line).append('\n');
        }
        return result.toString();
    }

    private static boolean shouldKeep(int filter, String level, String line) {
        switch (filter) {
            case FILTER_ERROR:
                return "ERROR".equals(level);
            case FILTER_WARN:
                return "WARN".equals(level);
            case FILTER_AUTO:
                return line.contains("[LumiDrive][AUTO]") ||
                        line.contains("[LumiDrive][MEDIA]") ||
                        line.contains("me.aap.fermata.auto.") ||
                        line.contains("KEYCODE_MEDIA_PLAY");
            case FILTER_WEB:
                return line.contains("[LumiDrive][WEB]") ||
                        line.contains("FermataWebClient");
            case FILTER_IPTV:
                return line.contains("[LumiDrive][IPTV]") ||
                        line.contains("MediaSessionCallback.onEngineError") ||
                        line.contains("MediaSessionCallback.engineEnded") ||
                        line.contains("VlcEngine") ||
                        line.contains("ExoPlayerEngine");
            default:
                return true;
        }
    }

    /** Quick counts for a diagnostics header (not individual stack lines). */
    public static String summary(String untrustedLogText) {
        int errors = 0;
        int warnings = 0;
        int info = 0;
        for (String line : untrustedLogText.split("\\r?\\n")) {
            Matcher m = HEADER.matcher(line);
            if (!m.find()) continue;
            switch (m.group(1)) {
                case "ERROR": errors++; break;
                case "WARN": warnings++; break;
                case "INFO": info++; break;
                default: break;
            }
        }
        return "ERROR " + errors + "  |  WARN " + warnings + "  |  INFO " + info;
    }
}
