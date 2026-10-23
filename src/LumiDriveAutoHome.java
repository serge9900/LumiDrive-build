package me.aap.fermata.ui.activity;

import android.content.Context;
import android.content.res.ColorStateList;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import androidx.constraintlayout.widget.ConstraintLayout;

import me.aap.fermata.FermataApplication;
import me.aap.fermata.R;
import me.aap.fermata.addon.AddonManager;

/**
 * LumiDrive Auto UI 1.0, experimental dashboard for the parked car screen.
 *
 * A removable overlay on the existing car activity's main layout. All media,
 * playback, fragment navigation and Android Auto transport implementation
 * remain in the existing classes. Never used on the phone or mirroring.
 */
public final class LumiDriveAutoHome {
    public static final String HOME_TAG = "LumiDriveAutoHome";

    private static final int BG_TOP = 0xFF130B26;
    private static final int BG_BOTTOM = 0xFF1B112E;
    private static final int TEXT = 0xFFF8F3FF;
    private static final int SUBTEXT = 0xFFB7A8D0;
    private static final int PURPLE = 0xFFBDA0FF;
    private static final int PINK = 0xFFFF8DCD;
    private static final int CYAN = 0xFF94E6FF;
    private static final int EDGE = 0xFF5A4279;

    private LumiDriveAutoHome() {}

    /** The existing bottom-navigation "Home" action works on phone and car. */
    public static void showForCurrentActivity(MainActivityDelegate activity) {
        if (activity.getAppActivity().isCarActivity()) show(activity);
        else LumiDriveDashboard.show(activity);
    }

    public static boolean isVisible(View root) {
        return root != null && root.findViewWithTag(HOME_TAG) != null;
    }

    /** The car Back key can dismiss the dashboard without exiting the app. */
    public static boolean hide(View root) {
        if (!(root instanceof ViewGroup host)) return false;
        View home = host.findViewWithTag(HOME_TAG);
        if (home == null || home.getParent() != host) return false;
        host.removeView(home);
        return true;
    }

    private static void dismiss(ViewGroup host, View home) {
        if (home.getParent() == host) host.removeView(home);
    }

    public static void show(MainActivityDelegate activity) {
        if (!activity.getAppActivity().isCarActivity()
                || FermataApplication.get().isMirroringMode()) return;

        View rootView = activity.getAppActivity().findViewById(R.id.main_activity);
        if (!(rootView instanceof ConstraintLayout host)
                || host.findViewWithTag(HOME_TAG) != null) return;

        Context ctx = activity.getContext();
        FrameLayout home = new FrameLayout(ctx);
        home.setTag(HOME_TAG);
        home.setClickable(true);
        home.setFocusableInTouchMode(true);
        home.setContentDescription(ctx.getString(R.string.lumidrive_auto_home));
        home.setBackground(gradient(BG_TOP, BG_BOTTOM, 0, 0));

        ScrollView scroll = new ScrollView(ctx);
        scroll.setFillViewport(true);
        scroll.setVerticalScrollBarEnabled(false);
        scroll.setClipToPadding(false);

        LinearLayout content = new LinearLayout(ctx);
        content.setOrientation(LinearLayout.VERTICAL);
        content.setPadding(dp(ctx, 17), dp(ctx, 13), dp(ctx, 17), dp(ctx, 13));

        LinearLayout header = new LinearLayout(ctx);
        header.setGravity(Gravity.CENTER_VERTICAL);
        header.setOrientation(LinearLayout.HORIZONTAL);

        TextView logo = label(ctx, "L", 22, TEXT, true);
        logo.setGravity(Gravity.CENTER);
        logo.setBackground(gradient(0xFF7F4BC2, 0xFFE05FA8, dp(ctx, 14), 0));
        header.addView(logo, new LinearLayout.LayoutParams(dp(ctx, 44), dp(ctx, 44)));

        LinearLayout identity = new LinearLayout(ctx);
        identity.setOrientation(LinearLayout.VERTICAL);
        identity.setPadding(dp(ctx, 12), 0, 0, 0);
        identity.addView(label(ctx, "LumiDrive", 23, TEXT, true));
        identity.addView(label(ctx, ctx.getString(R.string.lumidrive_auto_tagline),
                10, SUBTEXT, false));
        header.addView(identity, new LinearLayout.LayoutParams(
                0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

        ImageView settings = icon(ctx, R.drawable.settings, CYAN, dp(ctx, 42));
        settings.setContentDescription(ctx.getString(R.string.lumidrive_auto_settings));
        settings.setFocusable(true);
        settings.setClickable(true);
        settings.setOnClickListener(v -> open(activity, host, home, R.id.settings_fragment));
        header.addView(settings, new LinearLayout.LayoutParams(dp(ctx, 44), dp(ctx, 44)));
        content.addView(header);

        space(ctx, content, 10);
        content.addView(label(ctx, ctx.getString(R.string.lumidrive_auto_welcome),
                20, TEXT, true));
        space(ctx, content, 2);
        content.addView(label(ctx, ctx.getString(R.string.lumidrive_auto_hint),
                12, SUBTEXT, false));
        space(ctx, content, 10);

        int[] titles = {
                R.string.lumidrive_auto_iptv,
                R.string.lumidrive_auto_youtube,
                R.string.lumidrive_auto_browser,
                R.string.lumidrive_auto_library
        };
        int[] subtitles = {
                R.string.lumidrive_auto_channels,
                R.string.lumidrive_auto_video,
                R.string.lumidrive_auto_websites,
                R.string.lumidrive_auto_files
        };
        int[] icons = {R.drawable.tv, R.drawable.youtube, R.drawable.web, R.drawable.video};
        int[] colors = {PINK, PURPLE, CYAN, PURPLE};
        int[] tileBgs = {0xFF352041, 0xFF302249, 0xFF193449, 0xFF2C2047};

        // Two-by-two, landscape-first grid. ScrollView keeps it usable
        // on unusually short head units without placing controls over video.
        for (int row = 0; row < 2; row++) {
            LinearLayout line = new LinearLayout(ctx);
            line.setOrientation(LinearLayout.HORIZONTAL);
            for (int col = 0; col < 2; col++) {
                final int itemIndex = row * 2 + col;
                LinearLayout tile = tile(ctx,
                        ctx.getString(titles[itemIndex]),
                        ctx.getString(subtitles[itemIndex]),
                        icons[itemIndex], colors[itemIndex], tileBgs[itemIndex]);
                tile.setContentDescription(ctx.getString(titles[itemIndex]));
                tile.setOnClickListener(v -> openDestination(activity, host, home, itemIndex));
                LinearLayout.LayoutParams tileLp =
                        new LinearLayout.LayoutParams(0, dp(ctx, 112), 1f);
                tileLp.setMargins(dp(ctx, 3), dp(ctx, 3), dp(ctx, 3), dp(ctx, 4));
                line.addView(tile, tileLp);
            }
            content.addView(line);
        }

        space(ctx, content, 10);
        LinearLayout quickLinks = new LinearLayout(ctx);
        quickLinks.setOrientation(LinearLayout.HORIZONTAL);
        quickLinks.setGravity(Gravity.CENTER_VERTICAL);

        quickLink(ctx, quickLinks,
                ctx.getString(R.string.lumidrive_auto_favorites), PINK,
                () -> open(activity, host, home, R.id.favorites_fragment));
        quickLink(ctx, quickLinks,
                ctx.getString(R.string.lumidrive_auto_settings), CYAN,
                () -> open(activity, host, home, R.id.settings_fragment));
        content.addView(quickLinks);

        space(ctx, content, 12);
        TextView foot = label(ctx,
                ctx.getString(R.string.lumidrive_auto_parked),
                10, SUBTEXT, false);
        foot.setGravity(Gravity.CENTER);
        content.addView(foot);

        scroll.addView(content);
        home.addView(scroll, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT));

        ConstraintLayout.LayoutParams overlay = new ConstraintLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT);
        overlay.startToStart = ConstraintLayout.LayoutParams.PARENT_ID;
        overlay.endToEnd = ConstraintLayout.LayoutParams.PARENT_ID;
        overlay.topToTop = ConstraintLayout.LayoutParams.PARENT_ID;
        overlay.bottomToBottom = ConstraintLayout.LayoutParams.PARENT_ID;
        host.addView(home, overlay);

        // The vehicle's software D-pad cursor must remain on top of the cards.
        View cursor = host.findViewById(R.id.cursor);
        if (cursor != null && cursor.getParent() == host) host.bringChildToFront(cursor);
        home.requestFocus();
    }

    private static LinearLayout tile(Context ctx, String title, String subtitle,
                                     int drawable, int accent, int background) {
        LinearLayout view = new LinearLayout(ctx);
        view.setOrientation(LinearLayout.VERTICAL);
        view.setPadding(dp(ctx, 15), dp(ctx, 10), dp(ctx, 12), dp(ctx, 9));
        view.setBackground(gradient(background, 0xFF24182F, dp(ctx, 18), EDGE));
        ImageView symbol = icon(ctx, drawable, accent, dp(ctx, 34));
        view.addView(symbol, new LinearLayout.LayoutParams(dp(ctx, 37), dp(ctx, 37)));
        space(ctx, view, 5);
        view.addView(label(ctx, title, 17, TEXT, true));
        space(ctx, view, 1);
        TextView sub = label(ctx, subtitle, 11, SUBTEXT, false);
        sub.setSingleLine(true);
        sub.setEllipsize(android.text.TextUtils.TruncateAt.END);
        view.addView(sub);
        view.setClickable(true);
        view.setFocusable(true);
        view.setOnFocusChangeListener((v, focused) ->
                v.setBackground(gradient(background, 0xFF24182F, dp(ctx, 18),
                        focused ? accent : EDGE)));
        return view;
    }

    private static void quickLink(Context ctx, LinearLayout row, String title,
                                  int accent, Runnable action) {
        TextView link = label(ctx, title, 14, accent, true);
        link.setGravity(Gravity.CENTER);
        link.setPadding(dp(ctx, 8), dp(ctx, 11), dp(ctx, 8), dp(ctx, 11));
        link.setBackground(round(0xFF2C203F, dp(ctx, 14), EDGE));
        link.setContentDescription(title);
        link.setFocusable(true);
        link.setOnClickListener(v -> action.run());
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
                0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
        lp.setMargins(dp(ctx, 3), 0, dp(ctx, 3), 0);
        row.addView(link, lp);
    }

    private static void openDestination(MainActivityDelegate activity,
                                        ViewGroup host, View home, int index) {
        switch (index) {
            case 0 -> openAddon(activity, host, home, R.id.tv_fragment);
            case 1 -> openAddon(activity, host, home, R.id.youtube_fragment);
            case 2 -> openAddon(activity, host, home, R.id.web_browser_fragment);
            case 3 -> open(activity, host, home, R.id.folders_fragment);
            default -> { }
        }
    }

    private static void openAddon(MainActivityDelegate activity,
                                  ViewGroup host, View home, int id) {
        if (AddonManager.get().hasAddon(id)) open(activity, host, home, id);
        else android.widget.Toast.makeText(activity.getContext(),
                R.string.lumidrive_auto_module_unavailable,
                android.widget.Toast.LENGTH_SHORT).show();
    }

    private static void open(MainActivityDelegate activity, ViewGroup host,
                             View home, int id) {
        dismiss(host, home);
        host.post(() -> activity.showFragment(id));
    }

    private static ImageView icon(Context ctx, int drawable, int color, int size) {
        ImageView icon = new ImageView(ctx);
        icon.setImageResource(drawable);
        icon.setImageTintList(ColorStateList.valueOf(color));
        int inset = dp(ctx, 6);
        icon.setPadding(inset, inset, inset, inset);
        icon.setBackground(round(0x553E315B, dp(ctx, 12), 0));
        icon.setScaleType(ImageView.ScaleType.FIT_CENTER);
        return icon;
    }

    private static TextView label(Context ctx, String label, int size,
                                  int color, boolean bold) {
        TextView view = new TextView(ctx);
        view.setText(label);
        view.setTextSize(size);
        view.setTextColor(color);
        view.setIncludeFontPadding(false);
        if (bold) view.setTypeface(null, Typeface.BOLD);
        return view;
    }

    private static void space(Context ctx, LinearLayout parent, int heightDp) {
        parent.addView(new View(ctx), new LinearLayout.LayoutParams(1, dp(ctx, heightDp)));
    }

    private static GradientDrawable round(int color, int radius, int border) {
        GradientDrawable drawable = new GradientDrawable();
        drawable.setColor(color);
        drawable.setCornerRadius(radius);
        if (border != 0) drawable.setStroke(dpForBorder(), border);
        return drawable;
    }

    private static GradientDrawable gradient(int first, int last, int radius, int border) {
        GradientDrawable drawable = new GradientDrawable(
                GradientDrawable.Orientation.TL_BR, new int[]{first, last});
        drawable.setCornerRadius(radius);
        if (border != 0) drawable.setStroke(dpForBorder(), border);
        return drawable;
    }

    private static int dpForBorder() {
        return 1;
    }

    private static int dp(Context ctx, float value) {
        return (int) (ctx.getResources().getDisplayMetrics().density * value + 0.5f);
    }
}
