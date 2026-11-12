# Content, editor and route ownership

## Preserve editable content

CustomPages are owner-editable content; master pages are shared shell/chrome. Do not bake each page into a separate master just to make it render. Preserve the established shell and its content injection point:

```html
<Piranya:ContentPlaceHolder id="piranya-page" runat="server" />
```

The placeholder's `id` is exactly `piranya-page`, not an arbitrary element ID. Keep existing valid syntax unless a verified change requires replacing it.

Use the native editable structure rather than replacing a page with loose raw HTML:

- `section` and `img` are native editable elements.
- `piranya:grid` and `piranya:layoutcontainer` provide editable columns/containers.
- `piranya:texteditor` holds ordinary rich text.
- `piranya:scripting` holds template bindings, scripts and genuinely coupled composed markup; it is not a reason to turn every paragraph into code-only content.

Preserve existing `piranya:uniqueelementid` values. Give each new grid, layout container, text editor and scripting wrapper a distinct UUID v4. A scripting wrapper without an identity can break opening the whole frontend editor even if guest rendering looks fine. Do not duplicate IDs by copying sections. Rich-text sanitization can remove empty presentational icon markup; keep such markup outside the text editor or in a suitable scripting sibling. After wrapping content, inspect actual wrapper sizes and direct-child layout: editor wrappers can alter flex/grid sizing.

Preserve native forms, price/quantity/variant controls, validation, event handlers and server bindings. Scope cosmetic selectors narrowly so generic names such as product/header do not leak into native detail, basket or checkout markup. Guest rendering is not proof the editor remains usable, and DOM counts are not proof controls work.

## Route ownership and defaults

Read page `public_path`, direct `master_page_id`, `list_page_url_rules` and applicable start/master defaults before changing routing. A matching URL rule can override the simple page path. URL-rule inspection is read-only; do not invent a URL-rule write tool. Domain-specific settings may override platform defaults; corroborate the actual requested address.

`set_page_path` changes or clears one CustomPage path. `set_page_master_page` assigns or clears its direct shell; clearing is a fallback change, not proof the same shell will remain. `site_config` default start/master changes are site-wide operations, not incidental steps in creating a page.

`piranya.shop.list_views` describes native Shop route templates, not CustomPages or a complete inventory of every module. Verify route parameters and actual installed behavior. Do not create CustomPages shadowing catalog, product detail, checkout or checkout-success routes. A product teaser embedded inside an ordinary page is different: retain its native binding, using only discovered supported parameters and real authorized catalog references. Do not silently replace an exact curated selection with a category-wide list.

## Preview and privacy gate

Before creating a supposedly hidden preview, establish supported access controls and actual guest/sitemap behavior. An unlinked URL, separate master or `noindex` tag does not establish privacy, authentication or sitemap exclusion. Workspace creation alone provides no general draft/access-control guarantee. If privacy cannot be enforced, prepare content without publishing it using an available private authoring surface, or obtain explicit acceptance of an unlinked **public** preview. Do not change live defaults or navigation to isolate a preview. A preview CustomPage's shell also does not prove native checkout uses that shell.
