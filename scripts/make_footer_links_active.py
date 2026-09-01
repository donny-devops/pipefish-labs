import os

files = [
    'index.html',
    'demo/index.html',
    'services-solutions/index.html',
    'benefits-testimonials/index.html',
    'case-studies-results/index.html',
    'affiliates-corporate-partnerships/index.html',
    'book-a-demo-contact/index.html',
    'blog/index.html',
    'legal-privacy-policy/index.html'
]

# Blog subpages as well
for root, dirs, fnames in os.walk('blog'):
    for fn in fnames:
        if fn == 'index.html':
            files.append(os.path.join(root, fn))

files = list(set(files))

count = 0
for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
        
        modified = False
        # Replace span badge
        if '<span class="badge">pipefishlabs.io</span>' in content:
            content = content.replace(
                '<span class="badge">pipefishlabs.io</span>',
                '<a href="https://pipefishlabs.io/" class="badge" style="color:var(--cyan);text-decoration:none">pipefishlabs.io ↗</a>'
            )
            modified = True
        
        # Replace cyan text in footer
        if '<p style="font-family:var(--fm);font-size:11px;color:var(--cyan)">pipefishlabs.io</p>' in content:
            content = content.replace(
                '<p style="font-family:var(--fm);font-size:11px;color:var(--cyan)">pipefishlabs.io</p>',
                '<p style="font-family:var(--fm);font-size:11.5px;color:var(--cyan)"><a href="https://pipefishlabs.io/" style="color:var(--cyan);text-shadow:0 0 10px rgba(0,212,255,0.3);text-decoration:none">pipefishlabs.io ↗</a></p>'
            )
            modified = True

        # Replace static div contact item if any
        if '<div class="cd-item"><span class="cd-icon">🌐</span><span>pipefishlabs.io</span></div>' in content:
            content = content.replace(
                '<div class="cd-item"><span class="cd-icon">🌐</span><span>pipefishlabs.io</span></div>',
                '<div class="cd-item"><span class="cd-icon">🌐</span><a href="https://pipefishlabs.io/" style="color:var(--cyan);text-decoration:none">pipefishlabs.io ↗</a></div>'
            )
            modified = True

        if modified:
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(content)
            count += 1
            print(f'Made footer link active in {f}')

print(f'Successfully updated footer hyperlinks across {count} HTML files.')
