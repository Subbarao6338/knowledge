# HTMX Cheatsheet

HTMX lets you drive AJAX, WebSockets, and SSE directly from HTML attributes, returning HTML fragments from the server rather than JSON — no separate frontend framework or JS build step required.

## Setup

```html
<script src="https://unpkg.com/htmx.org@2.0.0"></script>
<!-- or self-hosted: <script src="/static/htmx.min.js"></script> -->
```

## Core Request Attributes

```html
<button hx-get="/data">Load Data</button>
<button hx-post="/submit">Submit</button>
<button hx-put="/update/1">Update</button>
<button hx-patch="/patch/1">Patch</button>
<button hx-delete="/delete/1">Delete</button>
```

Each of these issues the corresponding HTTP request when the element's trigger event fires (default: `click` for most elements, `submit` for forms, `change` for inputs).

## Targeting Where the Response Goes

```html
<div id="result"></div>
<button hx-get="/data" hx-target="#result">Load</button>

<!-- Special target keywords -->
hx-target="this"           <!-- the triggering element itself -->
hx-target="closest div"       <!-- nearest ancestor matching selector -->
hx-target="next .item"           <!-- next sibling matching selector -->
hx-target="previous .item"          <!-- previous sibling matching selector -->
hx-target="find span"                  <!-- first descendant matching selector -->
```

## Swap Strategies (`hx-swap`)

```html
<div hx-get="/data" hx-swap="innerHTML">...</div>       <!-- default: replace inner content -->
<div hx-get="/data" hx-swap="outerHTML">...</div>          <!-- replace the whole element -->
<div hx-get="/data" hx-swap="beforebegin">...</div>           <!-- insert before the element -->
<div hx-get="/data" hx-swap="afterbegin">...</div>               <!-- insert as first child -->
<div hx-get="/data" hx-swap="beforeend">...</div>                   <!-- insert as last child (great for infinite lists) -->
<div hx-get="/data" hx-swap="afterend">...</div>                       <!-- insert after the element -->
<div hx-get="/data" hx-swap="delete">...</div>                            <!-- remove the element, ignore response -->
<div hx-get="/data" hx-swap="none">...</div>                                 <!-- do nothing with the response body -->

<!-- Modifiers -->
hx-swap="innerHTML swap:1s"      <!-- delay before swap -->
hx-swap="innerHTML settle:1s"       <!-- delay before CSS transition settle classes are applied -->
hx-swap="innerHTML scroll:top"         <!-- scroll target to top after swap -->
hx-swap="innerHTML show:top"              <!-- scroll target into view -->
```

## Triggers (`hx-trigger`)

```html
<input hx-get="/search" hx-trigger="keyup changed delay:300ms" hx-target="#results">
<!-- fires on keyup, only if value changed, debounced 300ms -->

<div hx-get="/poll" hx-trigger="every 2s">...</div>          <!-- polling -->
<div hx-get="/data" hx-trigger="load">...</div>                 <!-- fires once on page load -->
<div hx-get="/data" hx-trigger="revealed">...</div>                <!-- fires when scrolled into view -->
<div hx-get="/data" hx-trigger="intersect once">...</div>             <!-- IntersectionObserver-based -->
<button hx-get="/data" hx-trigger="click once">...</button>              <!-- only fires once ever -->
<button hx-get="/data" hx-trigger="click[ctrlKey]">...</button>             <!-- conditional trigger -->

<input hx-get="/validate" hx-trigger="blur">
<div hx-get="/refresh" hx-trigger="myCustomEvent from:body">...</div>          <!-- custom event listener -->

<!-- Multiple triggers -->
<div hx-get="/data" hx-trigger="click, keyup[key=='Enter']">...</div>
```

## Sending Extra Data

```html
<button hx-post="/action" hx-vals='{"key": "value"}'>Send</button>
<button hx-post="/action" hx-vals='js:{timestamp: Date.now()}'>Send with JS</button>

<div hx-get="/data" hx-include="#other-input">...</div>          <!-- include another element's value -->
<div hx-get="/data" hx-params="not password">...</div>              <!-- exclude specific form params -->
<div hx-get="/data" hx-params="none">...</div>                          <!-- send no params -->

<!-- Headers -->
<div hx-get="/data" hx-headers='{"X-Custom-Header": "value"}'>...</div>
```

## Forms

```html
<form hx-post="/submit" hx-target="#result" hx-swap="outerHTML">
  <input type="text" name="username" required>
  <button type="submit">Submit</button>
</form>

<!-- Disable a button while a request is in flight -->
<button hx-post="/submit" hx-disabled-elt="this">Submit</button>

<!-- Form validation respects native HTML5 validation before firing the request -->
```

## Indicators (loading states)

```html
<button hx-get="/data" hx-indicator="#spinner">
  Load
</button>
<img id="spinner" class="htmx-indicator" src="/spinner.gif">
```

```css
.htmx-indicator { opacity: 0; transition: opacity 200ms ease-in; }
.htmx-request .htmx-indicator { opacity: 1; }
.htmx-request.htmx-indicator { opacity: 1; }
```

## Out-of-Band Swaps (`hx-swap-oob`)

Update multiple, unrelated parts of the page from a single response — the server returns extra fragments tagged with `hx-swap-oob`, and HTMX routes each to the matching element by ID, in addition to the normal target swap.

```html
<!-- Server response can include: -->
<div id="main-result">Primary content goes to hx-target as usual</div>
<div id="notification-count" hx-swap-oob="true">5</div>
<div id="cart-total" hx-swap-oob="innerHTML">$42.00</div>
```

## Confirmation & Safety

```html
<button hx-delete="/item/1" hx-confirm="Are you sure you want to delete this?">Delete</button>
<button hx-post="/action" hx-prompt="Type your name to confirm">Confirm</button>
```

## Boosting Regular Links & Forms (`hx-boost`)

```html
<body hx-boost="true">
  <!-- All <a> and <form> elements within become AJAX-driven automatically,
       replacing full page navigation with a smooth partial swap of <body> -->
  <a href="/page2">Go to Page 2</a>
</body>
```

## History & URL

```html
<div hx-get="/page/2" hx-push-url="true">Load Page 2</div>       <!-- pushes a new browser history entry -->
<div hx-get="/page/2" hx-push-url="/custom-url">...</div>            <!-- push a specific URL -->
<div hx-get="/page/2" hx-replace-url="true">...</div>                   <!-- replace current history entry, no new one -->
```

## Events (JavaScript Hooks)

```javascript
document.body.addEventListener('htmx:beforeRequest', (evt) => {
  console.log('About to make a request', evt.detail);
});

document.body.addEventListener('htmx:afterRequest', (evt) => {
  console.log('Request finished', evt.detail.xhr.status);
});

document.body.addEventListener('htmx:responseError', (evt) => {
  console.error('Server error', evt.detail.xhr.status);
});

document.body.addEventListener('htmx:configRequest', (evt) => {
  evt.detail.headers['Authorization'] = 'Bearer ' + getToken();   // inject auth dynamically
});

document.body.addEventListener('htmx:afterSwap', (evt) => {
  // run JS after new content is swapped in — good place to reinit widgets
});
```

**Common events:** `htmx:beforeRequest`, `htmx:afterRequest`, `htmx:beforeSwap`, `htmx:afterSwap`, `htmx:beforeSettle`, `htmx:afterSettle`, `htmx:responseError`, `htmx:sendError`, `htmx:timeout`, `htmx:load`.

## Server-Sent Events (SSE) Extension

```html
<script src="https://unpkg.com/htmx-ext-sse@2.0.0"></script>

<div hx-ext="sse" sse-connect="/events" sse-swap="message">
  Waiting for updates...
</div>
```

## WebSockets Extension

```html
<script src="https://unpkg.com/htmx-ext-ws@2.0.0"></script>

<div hx-ext="ws" ws-connect="/chatroom">
  <div id="chat-messages"></div>
  <form ws-send>
    <input name="message">
  </form>
</div>
```

## Common Backend Patterns

```python
# Flask example — return an HTML fragment, not JSON
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/search")
def search():
    query = request.args.get("q", "")
    results = do_search(query)
    return render_template("_results_fragment.html", results=results)
    # HTMX swaps this fragment into the DOM directly — no client-side JSON parsing/templating needed
```

```python
# Detecting an HTMX request server-side (HTMX sends this header on every request)
if request.headers.get("HX-Request") == "true":
    return render_template("_fragment.html", ...)   # partial
else:
    return render_template("full_page.html", ...)      # full page (e.g. direct URL visit)
```

**Useful request headers HTMX sends:** `HX-Request`, `HX-Trigger` (id of triggering element), `HX-Trigger-Name`, `HX-Target`, `HX-Current-URL`.

**Useful response headers you can send back:** `HX-Redirect` (client-side redirect), `HX-Refresh: true` (full page reload), `HX-Trigger` (fire a client-side custom event), `HX-Reswap`, `HX-Retarget` (override swap/target from the server).

## Common Gotchas

- HTMX expects **HTML fragments** back from the server, not JSON — if your endpoint returns JSON, HTMX will insert the raw JSON text into the DOM, which is usually not what you want.
- `hx-trigger="click"` is already the default for most elements — you rarely need to specify it unless customizing (debounce, filters, custom events).
- Swapped-in content doesn't automatically re-run inline `<script>` tags by default in some configurations — use the `htmx:afterSwap` event or `hx-on` attributes for JS that needs to run after a swap.
- `hx-boost` only intercepts same-origin links/forms by default — external links behave normally.
- Without `hx-indicator`, users get no visual feedback during slower requests — always add loading states for anything non-trivial.
