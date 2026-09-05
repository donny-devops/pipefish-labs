# LCP Patterns & Edge Optimization Reference

## 1. High-Priority Preload Tag Pattern
Place this tag early within `<head>`, before external fonts and stylesheets:
```html
<link rel="preload" as="image" href="/hero-logo.webp" type="image/webp" fetchpriority="high">
```

Key attributes:
- `as="image"`: Tells the browser resource scheduler to treat this as an image.
- `type="image/webp"`: Enables preloading only if the browser supports WebP.
- `fetchpriority="high"`: Bumps network queue priority above secondary stylesheets and scripts.

---

## 2. Picture Fallback Element Pattern
Always wrap hero images in `<picture>` with explicit dimensions to prevent Cumulative Layout Shift (CLS):
```html
<picture>
  <source srcset="/hero-logo.webp" type="image/webp">
  <img src="/hero-logo.png" alt="Hero Logo" class="hero-img" width="1024" height="813" fetchpriority="high" decoding="async">
</picture>
```

Key attributes:
- `width` and `height`: Reserves aspect ratio box in the DOM before image bits arrive.
- `decoding="async"`: Decodes image off the main rendering thread.

---

## 3. Render-Delay Elimination in CSS
Never hide the hero container or above-the-fold elements behind `opacity: 0` animations:
```css
/* BAD: Causes artificial LCP delay waiting for JavaScript or keyframe trigger */
#hero .ai { opacity: 0; transform: translateY(24px); }

/* GOOD: Render hero content immediately on first paint */
#hero .ai {
  opacity: 1 !important;
  transform: none !important;
  transition: none !important;
}
```

---

## 4. Edge Caching Directives (`_headers`)
Ensure immutable or long-lived public caching for WebP static assets:
```
/*.webp
  Cache-Control: public, max-age=2592000
```
