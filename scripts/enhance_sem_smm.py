import os

files = [
    'index.html',
    'demo/index.html',
    'services-solutions/index.html',
    'benefits-testimonials/index.html',
    'case-studies-results/index.html',
    'affiliates-corporate-partnerships/index.html',
    'book-a-demo-contact/index.html',
    'blog/index.html'
]

sem_smm_script = '''
<!-- ─── SEM UTM TRACKING & SMM SOCIAL CONVERSION HOOKS ─── -->
<script>
(function() {
  // 1. Preserve UTM Parameters across internal links (SEM Optimization)
  var params = new URLSearchParams(window.location.search);
  var utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid'];
  var utmQuery = [];
  utmKeys.forEach(function(k) {
    if (params.has(k)) utmQuery.push(k + '=' + encodeURIComponent(params.get(k)));
  });
  if (utmQuery.length > 0) {
    var qs = utmQuery.join('&');
    document.querySelectorAll('a[href^="/"]').forEach(function(a) {
      var href = a.getAttribute('href');
      if (href && !href.includes('utm_')) {
        a.setAttribute('href', href + (href.includes('?') ? '&' : '?') + qs);
      }
    });
  }

  // 2. SMM Social Share Trigger Handler
  window.sharePage = function(platform) {
    var url = encodeURIComponent(window.location.href);
    var title = encodeURIComponent(document.title);
    var target = '';
    if (platform === 'linkedin') target = 'https://www.linkedin.com/sharing/share-offsite/?url=' + url;
    if (platform === 'twitter') target = 'https://twitter.com/intent/tweet?url=' + url + '&text=' + title;
    if (target) window.open(target, '_blank', 'width=600,height=400');
  };
})();
</script>
'''

for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
        if 'SEM UTM TRACKING' not in content:
            updated = content.replace('</body>', sem_smm_script + '\n</body>')
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(updated)
            print(f'Added SEM/SMM tracking hooks in {f}')
