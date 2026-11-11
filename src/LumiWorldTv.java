package me.aap.fermata.addon.tv;

import android.app.AlertDialog;
import android.content.Context;
import android.graphics.Color;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.view.ViewGroup;
import android.widget.*;
import java.util.*;
import me.aap.fermata.R;

/** UI only; playback and user playlists continue through the existing TV module. */
final class LumiWorldTv {
    static void chooseSource(TvFragment fragment, Runnable own) {
        Context context = fragment.getMainActivity().getContext();
        String[] choices = {context.getString(R.string.lumi_world_tv),
                context.getString(R.string.lumi_own_playlist)};
        AlertDialog dialog = new AlertDialog.Builder(context)
                .setTitle(R.string.lumi_iptv_source)
                .setAdapter(adapter(context, Arrays.asList(choices)), (d, position) -> {
                    if (position == 0) show(fragment); else own.run();
                }).setNegativeButton(android.R.string.cancel, null).create();
        showDialog(dialog);
    }

    static void show(TvFragment fragment) {
        Context context = fragment.getMainActivity().getContext();
        Locale locale = context.getResources().getConfiguration().getLocales().get(0);
        List<String> all = LumiWorldCountries.codes(locale);
        List<String> visible = new ArrayList<>(all);
        LinearLayout content = new LinearLayout(context);
        content.setOrientation(LinearLayout.VERTICAL);
        int pad = (int) (16 * context.getResources().getDisplayMetrics().density);
        content.setPadding(pad, pad / 2, pad, 0);
        TextView info = new TextView(context);
        info.setText(R.string.lumi_world_info);
        info.setTextColor(Color.WHITE);
        content.addView(info);
        EditText search = new EditText(context);
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
        int height = (int) (context.getResources().getDisplayMetrics().heightPixels * .42f);
        content.addView(list, new LinearLayout.LayoutParams(-1, height));
        AlertDialog dialog = new AlertDialog.Builder(context)
                .setTitle(R.string.lumi_world_tv).setView(content)
                .setNegativeButton(android.R.string.cancel, null).create();
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
        list.setOnItemClickListener((parent, view, position, id) -> {
            String code = visible.get(position);
            dialog.dismiss();
            Toast.makeText(context, R.string.lumi_country_loading, Toast.LENGTH_SHORT).show();
            fragment.getRootItem().openWorldCountry(code, LumiWorldCountries.name(code, locale))
                    .main().onCompletion((item, error) -> {
                        if (!fragment.isAdded() || fragment.getView() == null) return;
                        if (error != null || item == null) {
                            AlertDialog failure = new AlertDialog.Builder(context)
                                    .setTitle(R.string.lumi_world_tv)
                                    .setMessage(R.string.lumi_country_failed)
                                    .setPositiveButton(R.string.lumi_try_again, (d, which) -> show(fragment))
                                    .setNegativeButton(android.R.string.cancel, null).create();
                            showDialog(failure);
                        } else if (!fragment.isHidden()) {
                            fragment.openFolder(item);
                        }
                    });
        });
        showDialog(dialog);
        dialog.getWindow().setSoftInputMode(
                android.view.WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_HIDDEN);
        list.requestFocus();
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

    private static void showDialog(AlertDialog dialog) {
        dialog.show();
        whiteText(dialog.getWindow().getDecorView());
    }
    private static void whiteText(View view) {
        if (view instanceof TextView) ((TextView) view).setTextColor(Color.WHITE);
        if (view instanceof ViewGroup) {
            ViewGroup group = (ViewGroup) view;
            for (int i = 0; i < group.getChildCount(); i++) whiteText(group.getChildAt(i));
        }
    }
}
