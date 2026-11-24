"""Reference-image presentation, applied only when Vice Sunset is selected."""
from pathlib import Path


def apply(root, write, replace):
    app = 'fermata/src/main/'
    util = 'depends/utils/src/main/'
    h = 'me.aap.utils.ui.LumiThemeColors'
    write(app + 'res/drawable/lumi_vice_banner.xml',
          (Path(__file__).parent / 'src/vice_sunset_banner.xml').read_text(encoding='utf-8'))
    dashboard = app + 'java/me/aap/fermata/ui/activity/LumiDriveDashboard.java'
    replace(dashboard, '        Context ctx = activity.getContext();',
            f'        Context ctx = activity.getContext();\n        boolean vice = {h}.vice(ctx);')
    replace(dashboard, 'TextView title = label(ctx, "LumiDrive", 26, TEXT, true);',
            'TextView title = label(ctx, "LumiDrive", 26, vice ? PINK : TEXT, true);')
    replace(dashboard, 'brand.addView(label(ctx, "Твой медиацентр", 12, MUTED, false));',
            'brand.addView(label(ctx, vice ? "VICE SUNSET" : "Твой медиацентр", 12, MUTED, false));')
    replace(dashboard, '''        space(ctx, content, 30);
        content.addView(label(ctx, "Добро пожаловать", 24, TEXT, true));''', '''        space(ctx, content, vice ? 16 : 30);
        if (vice) {
            ImageView sunset = new ImageView(ctx);
            sunset.setImageResource(R.drawable.lumi_vice_banner);
            sunset.setAdjustViewBounds(true);
            sunset.setScaleType(ImageView.ScaleType.FIT_CENTER);
            sunset.setImportantForAccessibility(View.IMPORTANT_FOR_ACCESSIBILITY_NO);
            sunset.setBackground(round(ctx, PANEL, dp(ctx, 20), 0));
            sunset.setClipToOutline(true);
            content.addView(sunset, new LinearLayout.LayoutParams(-1, -2));
            space(ctx, content, 16);
        }
        content.addView(label(ctx, vice ? "Твои медиа. Твой стиль." : "Добро пожаловать",
                vice ? 20 : 24, TEXT, true));''')
    replace(dashboard, '"Всё, что любишь смотреть — в одном месте",',
            'vice ? "Night drive • Neon sunset" : "Всё, что любишь смотреть — в одном месте",')
    replace(dashboard, '        content.addView(label(ctx, "Разделы", 19, TEXT, true));',
            '        if (!vice) content.addView(label(ctx, "Разделы", 19, TEXT, true));')
    replace(dashboard, 'String[] names = {"IPTV", "YouTube", "Браузер", "Медиатека"};',
            'String[] names = {"IPTV", "YouTube", "Браузер", vice ? "Медиа" : "Медиатека"};')
    replace(dashboard, '''String[] descriptions = {"Каналы и плейлисты", "Видео", "Открывай сайты",
                "Файлы и видео"};''', '''String[] descriptions = vice ? new String[]{"Каналы", "Видео", "Интернет", "Медиатека"}
                : new String[]{"Каналы и плейлисты", "Видео", "Открывай сайты", "Файлы и видео"};''')
    replace(dashboard, 'int[] accents = {PINK, PURPLE, CYAN, PURPLE};',
            'int[] accents = vice ? new int[]{CYAN, PINK, 0xFFFFAA7D, PURPLE}\n                : new int[]{PINK, PURPLE, CYAN, PURPLE};')
    replace(dashboard, 'int[] icons = {R.drawable.tv, R.drawable.youtube, R.drawable.web, R.drawable.video};',
            'int[] icons = {R.drawable.tv, R.drawable.youtube, R.drawable.web, vice ? R.drawable.audiotrack : R.drawable.video};')
    replace(dashboard, '                space(ctx, card, 20);', '                space(ctx, card, vice ? 8 : 20);')
    replace(dashboard, '0, dp(ctx, 176), 1f);', '0, vice ? ViewGroup.LayoutParams.WRAP_CONTENT : dp(ctx, 176), 1f);')
    replace(dashboard, '                card.setContentDescription(names[index]);',
            '                if (vice) card.setMinimumHeight(dp(ctx, 144));\n                card.setContentDescription(names[index]);')
    replace(dashboard, 'card.addView(image, new LinearLayout.LayoutParams(dp(ctx, 54), dp(ctx, 54)));',
            '''if (vice) {
                    image.setPadding(0, 0, 0, 0);
                    image.setBackground(null);
                }
                card.addView(image, new LinearLayout.LayoutParams(dp(ctx, vice ? 28 : 54), dp(ctx, vice ? 28 : 54)));''')
    colors = util + 'java/me/aap/utils/ui/LumiThemeColors.java'
    replace(colors, '                default -> text(c);',
            '                case 0xFFFFAA7D -> 0xFFFFAA7D;\n                default -> text(c);')
    # Softer neutral borders for cards; cyan remains the distinct focus outline.
    replace(colors, '? 0xFF45E5DD : 0xFFBD97FF;', '? 0xFF45E5DD : 0xFF70577F;')

    # Style overrides are Vice-only; keep Classic and Light resources untouched.
    theme = app + 'res/values/theme_vice_sunset.xml'
    replace(theme, '<item name="colorPrimary">#302341</item>', '<item name="colorPrimary">#140F24</item>')
    replace(theme, '<item name="boxStrokeColor">#BD97FF</item>', '<item name="boxStrokeColor">#70577F</item>')
    replace(theme, '<item name="lumiViceSunset">true</item>', '''<item name="lumiViceSunset">true</item>
    <item name="appMediaItemStyle">@style/LumiViceMediaItem</item>
    <item name="bottomNavigationStyle">@style/LumiViceNavBar</item>''')
    replace(theme, '</resources>', '''<style name="LumiViceMediaItem" parent="AppTheme.MediaItemStyle">
    <item name="iconColor">#45E5DD</item>
    <item name="tint">#45E5DD</item>
</style>
<style name="LumiViceNavBar" parent="Theme.Utils.Base.NavBarStyle">
    <item name="tint">#B7A6D0</item>
    <item name="android:colorBackground">#140F24</item>
</style>
</resources>''')
    # Clear hierarchy in rows: white title, secondary subtitle, cyan icon, pink actions.
    media = app + 'java/me/aap/fermata/ui/view/MediaItemView.java'
    replace(media, '\t\tv.setTextColor(textTint);', f'''        if ({h}.vice(ctx)) {{
            v.setTextColor(v == getTitle() ? 0xFFF8EEFF : 0xFFB7A6D0);
        }} else v.setTextColor(textTint);''')
    replace(media, '        setSize(ctx, grid, size);', f'''        if ({h}.vice(ctx)) {{
            ((ImageView) actions).setImageTintList(ColorStateList.valueOf(0xFFFF5DA6));
        }}
        setSize(ctx, grid, size);''')

    def selector(selected=False):
        def shape(fill, border):
            return f'<shape><solid android:color="{fill}"/><stroke android:width="1dp" android:color="{border}"/><corners android:radius="10dp"/></shape>'
        states = [('state_focused', '#38283F', '#45E5DD'),
                  ('state_pressed', '#50304F', '#FF5DA6')]
        if selected:
            states.append(('state_selected', '#773E70', '#FF5DA6'))
        return '<selector xmlns:android="http://schemas.android.com/apk/res/android">' + ''.join(
            f'<item android:{state}="true">{shape(fill, border)}</item>' for state, fill, border in states) + \
            '<item>' + shape('#302341' if selected else '#00000000', '#70577F' if selected else '#00000000') + '</item></selector>'

    write(util + 'res/drawable/lumi_vice_nav.xml', selector(True))
    write(util + 'res/drawable/lumi_vice_toolbar.xml', selector())
    toolbar = util + 'java/me/aap/utils/ui/view/ToolBarView.java'
    replace(toolbar, 'b.setBackgroundResource(R.drawable.lumidrive_toolbar_button);',
            f'b.setBackgroundResource({h}.vice(b.getContext())\n                    ? R.drawable.lumi_vice_toolbar : R.drawable.lumidrive_toolbar_button);')
    nav = util + 'java/me/aap/utils/ui/view/NavBarView.java'
    replace(nav, 'b.setBackgroundResource(R.drawable.lumidrive_nav_button);',
            f'''b.setBackgroundResource({h}.vice(b.getContext())
                    ? R.drawable.lumi_vice_nav : R.drawable.lumidrive_nav_button);
            if ({h}.vice(b.getContext())) {{
                int gap = (int) me.aap.utils.ui.UiUtils.toPx(b.getContext(), 3);
                lp.setMargins(gap, gap, gap, gap);
                b.setLayoutParams(lp);
            }}''')
    navbutton = util + 'java/me/aap/utils/ui/view/NavButtonView.java'
    replace(navbutton, '\t\timg.setAlpha(0.5f);', f'\t\timg.setAlpha({h}.vice(ctx) ? 1f : 0.5f);')
    replace(navbutton, '\t\tTextView t = getText();\n\t\tif (t != null) t.setVisibility(selected ? VISIBLE : GONE);',
            f'''        if ({h}.vice(getContext())) {{
            i.setAlpha(1f);
            ImageViewCompat.setImageTintList(i,
                    ColorStateList.valueOf(selected ? 0xFFF8EEFF : 0xFFB7A6D0));
        }}
\t\tTextView t = getText();
\t\tif (t != null) t.setVisibility(selected ? VISIBLE : GONE);''')
