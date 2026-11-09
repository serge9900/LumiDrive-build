package me.aap.fermata.ui.activity;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

/** Bounded release-feed reads using the platform HTTP stack. */
public final class LumiDriveReleaseHttp {
    private LumiDriveReleaseHttp() {}
    private static final int MAX_BYTES = 2 * 1024 * 1024;
    public static String fetch(String url) throws IOException {
        IOException last = null;
        for (int attempt = 0; attempt < 3; attempt++) {
            if (Thread.currentThread().isInterrupted()) throw new InterruptedIOException();
            try {
                return read(new URL(url));
            } catch (PermanentFailure e) {
                throw e;
            } catch (IOException e) {
                last = e;
                if (attempt == 2) break;
                try { Thread.sleep(500L * (attempt + 1)); }
                catch (InterruptedException interrupted) {
                    Thread.currentThread().interrupt();
                    throw new InterruptedIOException();
                }
            }
        }
        throw last;
    }
    private static String read(URL url) throws IOException {
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        try {
            connection.setConnectTimeout(10000);
            connection.setReadTimeout(10000);
            connection.setUseCaches(false);
            connection.setInstanceFollowRedirects(false);
            connection.setRequestProperty("Accept", "application/vnd.github+json");
            connection.setRequestProperty("User-Agent", "LumiDrive-Updater");
            connection.setRequestProperty("Accept-Encoding", "identity");
            connection.setRequestProperty("Connection", "close");
            int status = connection.getResponseCode();
            if (status != 200) {
                if (status == 408 || status == 429 || status >= 500)
                    throw new IOException("Release server HTTP " + status);
                throw new PermanentFailure("Release server HTTP " + status);
            }
            long expected = connection.getContentLengthLong();
            if (expected > MAX_BYTES) throw new PermanentFailure("Release response too large");
            try (InputStream input = connection.getInputStream();
                 ByteArrayOutputStream output = new ByteArrayOutputStream()) {
                byte[] buffer = new byte[8192];
                int count;
                while ((count = input.read(buffer)) != -1) {
                    if (output.size() + count > MAX_BYTES)
                        throw new PermanentFailure("Release response too large");
                    output.write(buffer, 0, count);
                }
                if (expected >= 0 && output.size() != expected)
                    throw new EOFException("Incomplete release response");
                if (output.size() == 0) throw new EOFException("Empty release response");
                return new String(output.toByteArray(), StandardCharsets.UTF_8);
            }
        } finally { connection.disconnect(); }
    }
    private static final class PermanentFailure extends IOException {
        PermanentFailure(String message) { super(message); }
    }
}
