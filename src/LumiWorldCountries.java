package me.aap.fermata.addon.tv;
import java.util.*;
import java.text.Collator;
/** Country playlist URLs supplied by IPTV-org. No channel streams bundled. */
public final class LumiWorldCountries {
    private static final String CODES = "af al dz ad ao ag ar am aw au at az bs bh bd bb by be bz bj bt bo bq ba br vg bn bg bf bi kh cm ca cv td cl cn co cr hr cu cw cy cz cd dk do ec eg sv gq er ee et fj fi fr gf pf gm ge de gh gr gp gu gt gg gn gy ht hn hk hu is in id ir iq ie il it ci jm jp jo kz ke xk kw kg la lv lb ly li lt lu mo my mv ml mt mq mr mu mx md mc mn me ma mz mm na np nl nc nz ni ne ng kp mk no om pk ps pa pg py pe ph pl pt pr qa cg re ro ru rw kn lc vc ws sm sa sn rs sl sg sx sk si so za kr es lk sd sr se ch sy tw tj tz th tg tt tn tr tm ug ua ae uk us uy uz va ve vn eh ye zw";
    public static List<String> codes(Locale locale) {
        List<String> result = new ArrayList<>(Arrays.asList(CODES.split(" ")));
        Collator order = Collator.getInstance(locale);
        result.sort((a,b) -> order.compare(name(a, locale), name(b, locale)));
        return result;
    }
    public static String name(String code, Locale locale) {
        return new Locale("", code.toUpperCase(Locale.ROOT)).getDisplayCountry(locale);
    }
    public static String url(String code) {
        if (!Arrays.asList(CODES.split(" ")).contains(code))
            throw new IllegalArgumentException("Unknown country");
        return "https://iptv-org.github.io/iptv/countries/" + code + ".m3u";
    }
    public static boolean matches(String code, String query, Locale locale) {
        String q = query.trim().toLowerCase(locale);
        return name(code, locale).toLowerCase(locale).contains(q)
            || name(code, Locale.ENGLISH).toLowerCase(Locale.ROOT).contains(q.toLowerCase(Locale.ROOT))
            || code.contains(q);
    }
}
