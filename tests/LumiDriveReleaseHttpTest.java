import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.atomic.AtomicInteger;
import me.aap.fermata.ui.activity.LumiDriveReleaseHttp;
public class LumiDriveReleaseHttpTest {
 public static void main(String[] args) throws Exception {
  HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
  AtomicInteger retry = new AtomicInteger(), denied = new AtomicInteger(), broken = new AtomicInteger();
  server.createContext("/retry", e -> {
   int status = retry.incrementAndGet() < 3 ? 503 : 200;
   byte[] b = "[]".getBytes(StandardCharsets.UTF_8);
   e.sendResponseHeaders(status, b.length); e.getResponseBody().write(b); e.close();
  });
  server.createContext("/denied", e -> { denied.incrementAndGet(); e.sendResponseHeaders(403,-1); e.close(); });
  server.createContext("/broken", e -> { broken.incrementAndGet(); e.sendResponseHeaders(200,20); e.getResponseBody().write(91); e.close(); });
  server.createContext("/chunked", e -> { e.sendResponseHeaders(200,0); e.getResponseBody().write("[]".getBytes(StandardCharsets.UTF_8)); e.close(); });
  server.start();
  String base = "http://127.0.0.1:" + server.getAddress().getPort();
  try {
   if (!"[]".equals(LumiDriveReleaseHttp.fetch(base+"/retry")) || retry.get()!=3) throw new AssertionError("retry");
   if (!"[]".equals(LumiDriveReleaseHttp.fetch(base+"/chunked"))) throw new AssertionError("chunked");
   try { LumiDriveReleaseHttp.fetch(base+"/denied"); throw new AssertionError("403 accepted"); } catch(java.io.IOException expected) {}
   if(denied.get()!=1) throw new AssertionError("403 retried");
   try { LumiDriveReleaseHttp.fetch(base+"/broken"); throw new AssertionError("truncated accepted"); } catch(java.io.IOException expected) {}
   if(broken.get()!=3) throw new AssertionError("truncated retry count");
   System.out.println("Release HTTP regression checks passed");
  } finally { server.stop(0); }
 }
}
