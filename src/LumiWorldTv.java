package me.aap.fermata.addon.tv;

import android.content.Context;
import android.graphics.Color;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.view.ViewGroup;
import android.widget.*;
import java.util.*;
import me.aap.fermata.R;
import me.aap.fermata.ui.activity.MainActivityDelegate;
import me.aap.utils.ui.menu.OverlayMenu;
import me.aap.utils.ui.view.DialogBuilder;
import me.aap.utils.ui.view.DialogView;

/** Uses the existing in-screen overlay; never creates an Android window on a car context. */
final class LumiWorldTv {
    static void chooseSource(TvFragment fragment, Runnable own) {
        if (!active(fragment)) return;
        fragment.getMainActivity().getContextMenu().show(builder -> {
            builder.setTitle(R.string.lumi_iptv_source);
            builder.addItem(R.id.lumi_world_tv, R.drawable.tv, R.string.lumi_world_tv)
                    .setHandler(item -> { show(fragment); return true; });
            builder.addItem(View.generateViewId(), R.string.lumi_own_playlist)
                    .setHandler(item -> { if (active(fragment)) own.run(); return true; });
        });
    }

    static void show(TvFragment fragment) {
        if (!active(fragment)) return;
        MainActivityDelegate activity = fragment.getMainActivity();
        DialogBuilder dialog = dialog(activity);
        Context context = dialog.getContext();
        Locale locale = context.getResources().getConfiguration().getLocales().get(0);
        List<String> all = LumiWorldCountries.codes(locale);
        List<String> visible = new ArrayList<>(all);
        LinearLayout content = new LinearLayout(context);
        content.setOrientation(LinearLayout.VERTICAL);
        content.setBackgroundColor(0xff24173d);
        int pad = (int) (12 * context.getResources().getDisplayMetrics().density);
        content.setPadding(pad, pad / 2, pad, 0);
        TextView info = new TextView(context);
        info.setText(R.string.lumi_world_info);
        info.setTextColor(Color.WHITE);
        content.addView(info);
        // CarActivity supplies CarEditText and Android Auto's input connection.
        EditText search = activity.createEditText(context);
        search.setSingleLine(true);
        search.setHint(R.string.lumi_country_search);
        search.setTextColor(Color.WHITE);
        search.setHintTextColor(0xffcccccc);
        content.addView(search);
        ListView list = new ListView(context);
        List<String> names = new ArrayList<>();
        for (String code : visible) names.add(LumiWorldCountries.name(code, locale));
        ArrayAdapter<String> rows = adapter(context, names);
        list.setAdapter(rows);
        TextView empty = new TextView(context);
        empty.setText(R.string.lumi_no_countries);
        empty.setTextColor(Color.WHITE);
        content.addView(empty);
        list.setEmptyView(empty);
        // Measure against the actual car/phone view, not the phone display behind projection.
        int available = fragment.getView().getHeight();
        if (available <= 0) available = context.getResources().getDisplayMetrics().heightPixels;
        int height = Math.max((int) (48 * context.getResources().getDisplayMetrics().density),
                (int) (available * .4f));
        content.addView(list, new LinearLayout.LayoutParams(-1, height));
        dialog.setTitle(R.string.lumi_world_tv).setView(content)
                .setNegativeButton(android.R.string.cancel, null);
        search.addTextChangedListener(new TextWatcher() {
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {}
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                visible.clear();
                rows.clear();
                for (String code : all) if (LumiWorldCountries.matches(code, s.toString(), locale)) {
                    visible.add(code);
                    rows.add(LumiWorldCountries.name(code, locale));
                }
                rows.notifyDataSetChanged();
            }
            public void afterTextChanged(Editable e) {}
        });
        boolean[] loading = {false};
        list.setOnItemClickListener((parent, view, position, id) -> {
            if (loading[0] || !active(fragment)) return;
            String code = visible.get(position);
            loading[0] = true;
            list.setEnabled(false);
            search.setEnabled(false);
            info.setText(R.string.lumi_country_loading);
            fragment.getRootItem().openWorldCountry(code, LumiWorldCountries.name(code, locale))
                    .main().onCompletion((item, error) -> {
                        // Back/cancel/navigation must not reopen a stale dialog or switch screens.
                        if (!active(fragment) || !content.isAttachedToWindow()) return;
                        activity.getContextMenu().hide();
                        if (error != null || item == null) {
                            dialog(activity)
                                    .setTitle(R.string.lumi_world_tv)
                                    .setMessage(R.string.lumi_country_failed)
                                    .setPositiveButton(R.string.lumi_try_again, (d, which) -> show(fragment))
                                    .setNegativeButton(android.R.string.cancel, null).show();
                        } else {
                            fragment.openFolder(item);
                        }
                    });
        });
        dialog.show();
        list.post(() -> { if (content.isAttachedToWindow()) list.requestFocus(); });
    }

    private static boolean active(TvFragment fragment) {
        return fragment.isAdded() && fragment.getView() != null && !fragment.isHidden();
    }

    private static ArrayAdapter<String> adapter(Context context, List<String> items) {
        return new ArrayAdapter<String>(context, android.R.layout.simple_list_item_1, items) {
            @Override public View getView(int position, View convertView, ViewGroup parent) {
                TextView view = (TextView) super.getView(position, convertView, parent);
                view.setTextColor(Color.WHITE);
                view.setTextSize(18);
                return view;
            }
        };
    }

    private static DialogBuilder dialog(MainActivityDelegate activity) {
        // Same DialogView/OverlayMenu path as MainActivityDelegate.createDialogBuilder.
        // Keep the contrast explicit without a platform AlertDialog or window token.
        OverlayMenu menu = activity.getContextMenu();
        return new DialogView.Builder(menu.getContext()) {
            @Override public void show() {
                DialogView view = build(menu::hide);
                view.setBackgroundColor(0xff24173d);
                whiteText(view);
                menu.show(builder -> builder.setView(view));
            }
        };
    }

    private static void whiteText(View view) {
        if (view instanceof TextView) ((TextView) view).setTextColor(Color.WHITE);
        if (view instanceof ViewGroup) {
            ViewGroup group = (ViewGroup) view;
            for (int i = 0; i < group.getChildCount(); i++) whiteText(group.getChildAt(i));
        }
    }
}
