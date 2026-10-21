package me.aap.fermata.ui.activity;

import android.app.AlertDialog;
import android.content.Context;
import android.content.res.ColorStateList;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import me.aap.fermata.FermataApplication;
import me.aap.fermata.R;
import me.aap.fermata.addon.AddonManager;

/**
 * LumiDrive 0.5 phone home. Uses real existing fragment destinations.
 * Kept separate from Android Auto and mirroring views.
 */
public final class LumiDriveDashboard {
    private static final String HOME_TAG = "LumiDriveHome";
    private static final String LAUNCHER_TAG = "LumiDriveHomeShortcut";

    private static final int BACKGROUND = 0xFF10091E;
    private static final int PANEL = 0xFF24173D;
    private static final int TEXT = 0xFFF9F4FF;
    private static final int MUTED = 0xFFBBAED2;
    private static final int PURPLE = 0xFFAE8AFF;
    private static final int PINK = 0xFFFF7AC8;
    private static final int CYAN = 0xFF8FE7FF;

    private LumiDriveDashboard() {}

    /** Persistent, one-tap Home button on the regular phone views. */
    public static void ensureLauncherButton(MainActivityDelegate activity) {
        if (activity.getAppActivity().isCarActivity()
                || FermataApplication.get().isMirroringMode()) return;

        Context ctx = activity.getContext();
        ViewGroup host = activity.getAppActivity().findViewById(android.R.id.content);
        if (host == null) return;
        if (host.findViewWithTag(LAUNCHER_TAG) != null) return;

        TextView button = new TextView(ctx);
        button.setTag(LAUNCHER_TAG);
        button.setText("☰");
        button.setTextSize(27);
        button.setTextColor(TEXT);
        button.setTypeface(null, Typeface.BOLD);
        button.setGravity(Gravity.CENTER);
        button.setContentDescription("Главное меню LumiDrive");
        button.setFocusable(true);
        button.setElevation(dp(ctx, 12));
        button.setBackground(gradient(0xFF8050CC, 0xFFCC4B9C, dp(ctx, 29), CYAN));
        button.setOnClickListener(v -> show(activity));

        FrameLayout.LayoutParams position =
                new FrameLayout.LayoutParams(dp(ctx, 58), dp(ctx, 58));
        position.gravity = Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL;
        // Above the bottom navigation; don't obscure media transport buttons.
        position.bottomMargin = dp(ctx, 100);
        host.addView(button, position);
        setLauncherButtonVisible(host, host.findViewWithTag(HOME_TAG) == null);
    }

    private static void setLauncherButtonVisible(ViewGroup host, boolean visible) {
        View launcher = host.findViewWithTag(LAUNCHER_TAG);
        if (launcher != null) launcher.setVisibility(visible ? View.VISIBLE : View.GONE);
    }

    private static void dismissHome(ViewGroup host, View home) {
        if (home.getParent() == host) host.removeView(home);
        setLauncherButtonVisible(host, true);
    }

    public static boolean hide(MainActivity activity) {
        ViewGroup host = activity.findViewById(android.R.id.content);
        if (host == null) return false;
        View home = host.findViewWithTag(HOME_TAG);
        if (home == null) return false;
        dismissHome(host, home);
        return true;
    }

    public static void show(MainActivityDelegate activity) {
        if (activity.getAppActivity().isCarActivity()
                || FermataApplication.get().isMirroringMode()) return;

        Context ctx = activity.getContext();
        ViewGroup host = activity.getAppActivity().findViewById(android.R.id.content);
        if (host == null || host.findViewWithTag(HOME_TAG) != null) return;

        FrameLayout home = new FrameLayout(ctx);
        home.setTag(HOME_TAG);
        home.setClickable(true);
        home.setFocusableInTouchMode(true);
        home.setBackground(gradient(BACKGROUND, 0xFF201135, 0, 0));

        ScrollView scroll = new ScrollView(ctx);
        scroll.setFillViewport(true);
        scroll.setClipToPadding(false);
        LinearLayout content = new LinearLayout(ctx);
        content.setOrientation(LinearLayout.VERTICAL);
        int pad = dp(ctx, 20);
        // Draw below the status bar/camera cutout on edge-to-edge Android.
        content.setPadding(pad, dp(ctx, 52), pad, dp(ctx, 28));
        ViewCompat.setOnApplyWindowInsetsListener(home, (v, insets) -> {
            int top = insets.getInsets(WindowInsetsCompat.Type.statusBars()).top;
            content.setPadding(pad, Math.max(dp(ctx, 52), top + dp(ctx, 20)),
                    pad, dp(ctx, 28));
            return insets;
        });

        // Branded header and a functional Settings shortcut.
        LinearLayout header = new LinearLayout(ctx);
        header.setOrientation(LinearLayout.HORIZONTAL);
        header.setGravity(Gravity.CENTER_VERTICAL);

        TextView logo = new TextView(ctx);
        logo.setText("L");
        logo.setTypeface(null, Typeface.BOLD);
        logo.setTextColor(TEXT);
        logo.setTextSize(23);
        logo.setGravity(Gravity.CENTER);
        logo.setBackground(gradient(0xFF854BC7, 0xFFDA4B9E, dp(ctx, 17), 0));
        header.addView(logo, new LinearLayout.LayoutParams(dp(ctx, 50), dp(ctx, 50)));

        LinearLayout brand = new LinearLayout(ctx);
        brand.setOrientation(LinearLayout.VERTICAL);
        brand.setPadding(dp(ctx, 12), 0, 0, 0);
        TextView title = label(ctx, "LumiDrive", 26, TEXT, true);
        brand.addView(title);
        brand.addView(label(ctx, "Твой медиацентр", 12, MUTED, false));
        header.addView(brand, new LinearLayout.LayoutParams(0,
                ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

        ImageView settings = new ImageView(ctx);
        settings.setImageResource(R.drawable.settings);
        settings.setImageTintList(ColorStateList.valueOf(CYAN));
        settings.setPadding(dp(ctx, 12), dp(ctx, 12), dp(ctx, 12), dp(ctx, 12));
        settings.setBackground(round(0xFF302044, dp(ctx, 15), 0xFF57396E));
        settings.setContentDescription("Настройки");
        settings.setFocusable(true);
        settings.setOnClickListener(v -> open(activity, host, home, R.id.settings_fragment));
        header.addView(settings, new LinearLayout.LayoutParams(dp(ctx, 48), dp(ctx, 48)));
        content.addView(header);

        space(ctx, content, 30);
        content.addView(label(ctx, "Добро пожаловать", 24, TEXT, true));
        space(ctx, content, 6);
        content.addView(label(ctx, "Всё, что любишь смотреть — в одном месте",
                14, MUTED, false));
        space(ctx, content, 24);

        if (activity.hasCurrent()) {
            LinearLayout resume = new LinearLayout(ctx);
            resume.setOrientation(LinearLayout.HORIZONTAL);
            resume.setGravity(Gravity.CENTER_VERTICAL);
            resume.setPadding(dp(ctx, 19), dp(ctx, 17), dp(ctx, 18), dp(ctx, 17));
            resume.setBackground(gradient(0xFF493071, 0xFF321F56, dp(ctx, 20), CYAN));
            ImageView play = new ImageView(ctx);
            play.setImageResource(R.drawable.play);
            play.setImageTintList(ColorStateList.valueOf(CYAN));
            resume.addView(play, new LinearLayout.LayoutParams(dp(ctx, 32), dp(ctx, 32)));
            LinearLayout lines = new LinearLayout(ctx);
            lines.setOrientation(LinearLayout.VERTICAL);
            lines.setPadding(dp(ctx, 14), 0, 0, 0);
            lines.addView(label(ctx, "Продолжить просмотр", 17, TEXT, true));
            lines.addView(label(ctx, "Вернуться к последнему медиа", 12, MUTED, false));
            resume.addView(lines);
            resume.setContentDescription("Продолжить просмотр");
            resume.setFocusable(true);
            resume.setOnClickListener(v -> {
                dismissHome(host, home);
                host.post(() -> activity.goToCurrent());
            });
            content.addView(resume);
            space(ctx, content, 28);
        }

        content.addView(label(ctx, "Разделы", 19, TEXT, true));
        space(ctx, content, 14);

        String[] names = {"IPTV", "YouTube", "Браузер", "Медиатека"};
        String[] descriptions = {"Каналы и плейлисты", "Видео", "Открывай сайты",
                "Файлы и видео"};
        int[] icons = {R.drawable.tv, R.drawable.youtube, R.drawable.web, R.drawable.video};
        int[] accents = {PINK, PURPLE, CYAN, PURPLE};
        int[] darks = {0xFF382043, 0xFF302453, 0xFF193849, 0xFF30224B};

        for (int row = 0; row < 2; row++) {
            LinearLayout line = new LinearLayout(ctx);
            line.setOrientation(LinearLayout.HORIZONTAL);
            for (int col = 0; col < 2; col++) {
                int index = row * 2 + col;
                LinearLayout card = new LinearLayout(ctx);
                card.setOrientation(LinearLayout.VERTICAL);
                card.setPadding(dp(ctx, 16), dp(ctx, 17), dp(ctx, 12), dp(ctx, 14));
                card.setBackground(gradient(darks[index], PANEL, dp(ctx, 21), 0xFF503565));
                ImageView image = new ImageView(ctx);
                image.setImageResource(icons[index]);
                image.setImageTintList(ColorStateList.valueOf(accents[index]));
                image.setPadding(dp(ctx, 11), dp(ctx, 11), dp(ctx, 11), dp(ctx, 11));
                image.setBackground(round(0x773D315F, dp(ctx, 15), 0));
                card.addView(image, new LinearLayout.LayoutParams(dp(ctx, 54), dp(ctx, 54)));
                space(ctx, card, 20);
                card.addView(label(ctx, names[index], 19, TEXT, true));
                space(ctx, card, 5);
                card.addView(label(ctx, descriptions[index], 12, MUTED, false));
                card.setContentDescription(names[index]);
                card.setFocusable(true);
                final int destination = index;
                card.setOnClickListener(v -> {
                    dismissHome(host, home);
                    host.post(() -> openDestination(activity, destination));
                });
                LinearLayout.LayoutParams layout = new LinearLayout.LayoutParams(
                        0, dp(ctx, 176), 1f);
                layout.setMargins(dp(ctx, 3), dp(ctx, 3), dp(ctx, 3), dp(ctx, 7));
                line.addView(card, layout);
            }
            content.addView(line);
        }

        space(ctx, content, 19);
        content.addView(label(ctx, "Быстрый доступ", 19, TEXT, true));
        space(ctx, content, 12);

        LinearLayout shortcuts = new LinearLayout(ctx);
        shortcuts.setOrientation(LinearLayout.HORIZONTAL);
        quickLink(ctx, shortcuts, "★  Избранное", PINK, () ->
                open(activity, host, home, R.id.favorites_fragment));
        quickLink(ctx, shortcuts, "⚙  Настройки", CYAN, () ->
                open(activity, host, home, R.id.settings_fragment));
        content.addView(shortcuts);

        space(ctx, content, 30);
        TextView footer = label(ctx, "LumiDrive 0.5 · Сделано для твоего медиа",
                11, MUTED, false);
        footer.setGravity(Gravity.CENTER);
        content.addView(footer);

        scroll.addView(content);
        home.addView(scroll, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        setLauncherButtonVisible(host, false);
        host.addView(home, new ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        ViewCompat.requestApplyInsets(home);
        home.requestFocus();
    }

    private static void quickLink(Context ctx, LinearLayout row, String name,
                                  int color, Runnable action) {
        TextView button = label(ctx, name, 14, color, true);
        button.setGravity(Gravity.CENTER);
        button.setPadding(dp(ctx, 7), dp(ctx, 14), dp(ctx, 7), dp(ctx, 14));
        button.setBackground(round(0xFF251A3C, dp(ctx, 15), 0xFF503565));
        button.setFocusable(true);
        button.setOnClickListener(v -> action.run());
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
        params.setMargins(dp(ctx, 3), 0, dp(ctx, 3), 0);
        row.addView(button, params);
    }

    private static void open(MainActivityDelegate activity, ViewGroup host, View home,
                             int fragmentId) {
        dismissHome(host, home);
        host.post(() -> activity.showFragment(fragmentId));
    }

    private static void openDestination(MainActivityDelegate activity, int index) {
        switch (index) {
            case 0: openAddon(activity, R.id.tv_fragment); break;
            case 1: openAddon(activity, R.id.youtube_fragment); break;
            case 2: openAddon(activity, R.id.web_browser_fragment); break;
            case 3: activity.showFragment(R.id.folders_fragment); break;
            default: break;
        }
    }

    private static void openAddon(MainActivityDelegate activity, int fragmentId) {
        if (AddonManager.get().hasAddon(fragmentId)) {
            activity.showFragment(fragmentId);
        } else {
            new AlertDialog.Builder(activity.getContext())
                    .setMessage("Этот модуль недоступен в установленной сборке.")
                    .setPositiveButton(android.R.string.ok, null).show();
        }
    }

    private static TextView label(Context ctx, String value, int size,
                                  int color, boolean bold) {
        TextView view = new TextView(ctx);
        view.setText(value);
        view.setTextSize(size);
        view.setTextColor(color);
        if (bold) view.setTypeface(null, Typeface.BOLD);
        return view;
    }

    private static void space(Context ctx, LinearLayout content, int size) {
        View view = new View(ctx);
        content.addView(view, new LinearLayout.LayoutParams(1, dp(ctx, size)));
    }

    private static GradientDrawable round(int color, int radius, int border) {
        GradientDrawable shape = new GradientDrawable();
        shape.setColor(color);
        shape.setCornerRadius(radius);
        if (border != 0) shape.setStroke(1, border);
        return shape;
    }

    private static GradientDrawable gradient(int start, int end, int radius, int border) {
        GradientDrawable shape = new GradientDrawable(
                GradientDrawable.Orientation.TL_BR, new int[]{start, end});
        shape.setCornerRadius(radius);
        if (border != 0) shape.setStroke(1, border);
        return shape;
    }

    private static int dp(Context ctx, float amount) {
        return (int) (ctx.getResources().getDisplayMetrics().density * amount + 0.5f);
    }
}
