import os

files = [
    'services-solutions/index.html',
    'case-studies-results/index.html',
    'benefits-testimonials/index.html',
    'affiliates-corporate-partnerships/index.html',
    'book-a-demo-contact/index.html',
    'demo/index.html',
    'blog/index.html',
    'legal-privacy-policy/index.html'
]

icon_tags = '  <link rel="icon" type="image/png" href="https://pipefishlabs.io/logo.png">\n  <link rel="apple-touch-icon" href="https://pipefishlabs.io/logo.png">\n'

for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
        if 'rel="icon"' not in content:
            updated = content.replace('<link rel="preconnect"', icon_tags + '  <link rel="preconnect"')
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(updated)
            print(f'Updated icon tags in {f}')
