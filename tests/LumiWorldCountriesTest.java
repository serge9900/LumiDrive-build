import java.util.*;
import me.aap.fermata.addon.tv.LumiWorldCountries;
public class LumiWorldCountriesTest {
 public static void main(String[] args) {
  List<String> codes = LumiWorldCountries.codes(Locale.ENGLISH);
  if (codes.size() < 150 || new HashSet<>(codes).size() != codes.size()) throw new AssertionError("Index");
  for (String code : codes) {
   if (!LumiWorldCountries.url(code).equals("https://iptv-org.github.io/iptv/countries/"+code+".m3u")) throw new AssertionError("URL");
   if (LumiWorldCountries.name(code, Locale.ENGLISH).isEmpty()) throw new AssertionError("Name");
  }
  if (!LumiWorldCountries.name("uk", Locale.ENGLISH).equals("United Kingdom")) throw new AssertionError("UK alias");
  if (!LumiWorldCountries.matches("am", "Армения", new Locale("ru"))) throw new AssertionError("Russian search");
  if (!LumiWorldCountries.matches("am", " ARMENIA ", new Locale("ru"))) throw new AssertionError("English search");
  if (LumiWorldCountries.matches("am", "zzzz", Locale.ENGLISH)) throw new AssertionError("Filter");
  for (String bad : new String[]{"../xx","AM","zz","am?foo",""}) {
   try { LumiWorldCountries.url(bad); throw new AssertionError("Accepted " + bad); }
   catch (IllegalArgumentException expected) {}
  }
  System.out.println("Country catalog tests passed: " + codes.size());
 }
}
