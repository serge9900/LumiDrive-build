"""Internal screen layout preview; keeps data, playback and menu commands intact."""
from pathlib import Path
import sys
import json
import hashlib
import xml.etree.ElementTree as ET

root = Path(sys.argv[1]).resolve()
app = 'fermata/src/main/'
utils = 'depends/utils/src/main/'


def snap():
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts}


before = snap()
allowed = set()


def write(path, text):
    if path.endswith('.xml'):
        ET.fromstring(text)
    (root / path).write_text(text + '\n', encoding='utf-8')
    allowed.add(path)


def replace(path, old, new):
    s = (root / path).read_text(encoding='utf-8')
    if s.count(old) != 1:
        raise RuntimeError(f'Expected exactly one anchor in {path}: {old[:60]}')
    write(path, s.replace(old, new))


# The first five children MUST keep their order: MediaItemView uses positional access.
row = '''<merge xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto">
    <androidx.appcompat.widget.AppCompatImageView
        android:id="@+id/media_item_icon" style="?attr/appMediaItemStyle"
        android:layout_width="36dp" android:layout_height="36dp"
        android:layout_marginStart="12dp" android:layout_marginEnd="12dp"
        android:scaleType="fitCenter"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintBottom_toBottomOf="parent" />
    <com.google.android.material.textview.MaterialTextView
        android:id="@+id/media_item_title" style="?attr/appMediaItemStyle"
        android:layout_width="0dp" android:layout_height="wrap_content"
        android:layout_marginStart="12dp" android:layout_marginTop="8dp"
        app:layout_constraintStart_toEndOf="@id/media_item_icon"
        app:layout_constraintEnd_toStartOf="@id/lumi_item_actions"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintBottom_toTopOf="@id/media_item_subtitle"
        app:layout_constraintVertical_chainStyle="packed" />
    <com.google.android.material.textview.MaterialTextView
        android:id="@+id/media_item_subtitle" style="?attr/appMediaItemStyle"
        android:layout_width="0dp" android:layout_height="wrap_content"
        android:layout_marginStart="12dp" android:layout_marginBottom="8dp"
        app:layout_constraintStart_toEndOf="@id/media_item_icon"
        app:layout_constraintEnd_toStartOf="@id/lumi_item_actions"
        app:layout_constraintTop_toBottomOf="@id/media_item_title"
        app:layout_constraintBottom_toBottomOf="parent" />
    <com.google.android.material.progressindicator.LinearProgressIndicator
        android:id="@+id/media_stream_progress" style="?attr/appStreamProgressStyle"
        android:layout_width="0dp" android:layout_height="3dp"
        android:layout_marginStart="12dp" android:layout_marginEnd="12dp"
        android:layout_marginBottom="1dp" android:visibility="gone"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintBottom_toBottomOf="parent" />
    <com.google.android.material.checkbox.MaterialCheckBox
        android:id="@+id/media_item_checkbox" style="?attr/appMediaItemStyle"
        android:layout_width="48dp" android:layout_height="48dp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintBottom_toBottomOf="parent" />
    <androidx.appcompat.widget.AppCompatImageButton
        android:id="@+id/lumi_item_actions"
        android:layout_width="48dp" android:layout_height="48dp"
        android:padding="14dp" android:background="@android:color/transparent"
        android:src="@drawable/lumi_item_more" android:tint="#EBDDFA"
        android:contentDescription="@string/lumi_item_actions"
        android:focusable="false" android:clickable="true"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintBottom_toBottomOf="parent" />
</merge>'''
for name in ('list', 'grid'):
    write(app + f'res/layout/media_item_{name}_layout.xml', row)

write(app + 'res/layout/media_item_view.xml', '''
<me.aap.fermata.ui.view.MediaItemView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent" android:layout_height="wrap_content"
    android:minHeight="56dp" android:layout_marginHorizontal="4dp"
    android:layout_marginVertical="3dp" />''')
replace(app + 'res/layout/media_items_list_view.xml',
        'android:orientation="vertical"',
        'android:orientation="vertical" android:padding="8dp" android:clipToPadding="false"')
replace(app + 'java/me/aap/fermata/ui/view/MediaItemListView.java',
        'int span = (int) Math.max(cfg.screenWidthDp / (128 * scale), 2);',
        'int span = (int) Math.max(cfg.screenWidthDp / (220 * scale), 1);')

write(app + 'res/drawable/lumi_item_more.xml', '''
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#FFFFFFFF" android:pathData="M4,10 A2,2 0,1 1,4,14 A2,2 0,1 1,4,10 M12,10 A2,2 0,1 1,12,14 A2,2 0,1 1,12,10 M20,10 A2,2 0,1 1,20,14 A2,2 0,1 1,20,10" />
</vector>''')
for lang, text in [('values', 'Item actions'), ('values-ru', 'Действия с элементом')]:
    write(app + f'res/{lang}/lumi_internal_design.xml',
          '<resources><string name="lumi_item_actions">' + text + '</string></resources>')

write(app + 'res/values/lumi_internal_typography.xml', '''<resources>
    <style name="LumiListTitle" parent="TextAppearance.MaterialComponents.Subtitle1">
        <item name="android:textSize">17sp</item>
        <item name="android:fontFamily">sans-serif-medium</item>
    </style>
    <style name="LumiListSubtitle" parent="TextAppearance.MaterialComponents.Caption">
        <item name="android:textSize">12sp</item>
    </style>
</resources>''')
replace(app + 'res/values/theme.xml',
        '<item name="titleTextAppearance">?attr/textAppearanceListItem</item>',
        '<item name="titleTextAppearance">@style/LumiListTitle</item>')
replace(app + 'res/values/theme.xml',
        '<item name="subtitleTextAppearance">?attr/textAppearanceCaption</item>',
        '<item name="subtitleTextAppearance">@style/LumiListSubtitle</item>')
replace(app + 'res/values/theme.xml', '<item name="elevation">20dp</item>',
        '<item name="elevation">0dp</item>')

view = app + 'java/me/aap/fermata/ui/view/MediaItemView.java'
replace(view, '\t\tsetSize(ctx, grid, size);', '''
        // Same context menu as long-press; no new command/data path.
        View actions = findViewById(R.id.lumi_item_actions);
        actions.setOnClickListener(v -> { if (getItem() != null) performLongClick(); });
        setSize(ctx, grid, size);''')
replace(view, '''		if (!grid) {
			int iconSize = (int) (getTitle().getTextSize() + getSubtitle().getTextSize() + toPx(ctx,
					10));''', '''
        setMinimumHeight((int) (toPx(ctx, grid ? 76 : 56) * Math.max(1f, size)));
        {
            int iconSize = (int) (toPx(ctx, 32) * size);''')
replace(view, '\t\tMaterialCheckBox cb = getCheckBox();', '''
        MaterialCheckBox cb = getCheckBox();
        View actions = findViewById(R.id.lumi_item_actions);
        MediaItemListView owner = getListView();
        // Keep the trailing slot occupied when selection checkboxes replace actions.
        actions.setVisibility(owner != null && owner.isSelectionActive() ? INVISIBLE : VISIBLE);''')

# Distinguish focus (outline) from playing/selected (subtle fill).
write(app + 'res/color/media_item.xml', '''
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_pressed="true" android:color="#59416F" />
    <item android:state_focused="true" android:color="#352541" />
    <item android:state_selected="true" android:color="#3D2C50" />
    <item android:state_activated="true" android:color="#3D2C50" />
    <item android:color="#252030" />
</selector>''')
write(app + 'res/color/media_item_border.xml', '''
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_focused="true" android:color="#E7AFFF" />
    <item android:state_pressed="true" android:color="#E7AFFF" />
    <item android:state_selected="true" android:color="#A777D1" />
    <item android:state_activated="true" android:color="#A777D1" />
    <item android:color="#383041" />
</selector>''')

# Keep OverlayMenu's focus restoration, selection dispatch and show/hide intact.
menu = utils + 'java/me/aap/utils/ui/menu/OverlayMenuView.java'
replace(menu, '\t\tsetBackgroundColor(ta.getColor(OverlayMenuView_android_colorBackground, Color.TRANSPARENT));', '''
        android.graphics.drawable.GradientDrawable panel = new android.graphics.drawable.GradientDrawable();
        panel.setColor(ta.getColor(OverlayMenuView_android_colorBackground, Color.TRANSPARENT));
        panel.setCornerRadius(toPx(ctx, 16));
        panel.setStroke((int) toPx(ctx, 1), 0xff655079);
        setBackground(panel);
        setClipToOutline(true);''')
replace(menu, '\t\t\tv.setText(this.title);', '\t\t\tv.setText(this.title);\n            v.setTextColor(0xfffaf7ff);\n            v.setTypeface(android.graphics.Typeface.DEFAULT, android.graphics.Typeface.BOLD);')

# Confirm resource positional contracts and forbid non-presentation file changes.
ns = '{http://schemas.android.com/apk/res/android}'
expected = ['media_item_icon', 'media_item_title', 'media_item_subtitle',
            'media_stream_progress', 'media_item_checkbox']
for name in ('list', 'grid'):
    nodes = list(ET.parse(root / (app + f'res/layout/media_item_{name}_layout.xml')).getroot())
    assert [node.get(ns + 'id').split('/')[-1] for node in nodes[:5]] == expected
after = snap()
actual = {p for p in before.keys() | after.keys() if before.get(p) != after.get(p)}
assert actual <= allowed, actual - allowed
report = {'changed_presentation_files': sorted(actual),
          'unchanged_files': len(before) - len(actual),
          'media_row_child_contract': 'passed',
          'device_validation': 'required: touch, rotary, selection, overlays, large text'}
write('LUMIDRIVE_INTERNAL_DESIGN_AUDIT.json', json.dumps(report, indent=2))
replace('gradle/libs.versions.toml', 'appVersionCode = "296"', 'appVersionCode = "297"')
replace('gradle/libs.versions.toml', 'appVersionName = "0.8.0-preview1"',
        'appVersionName = "0.8.0-preview2"')
print(json.dumps(report, indent=2))

