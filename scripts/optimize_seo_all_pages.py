import os
import re

files = [
    ('index.html', 'https://pipefishlabs.io/', 'PipeFish Labs - Enterprise AI Automation & Multi-Agent Orchestration', 'PipeFish Labs is an enterprise AI automation agency specializing in autonomous multi-agent orchestration, zero-trust security, post-quantum cryptography, scalable data pipelines, and strategic management consulting.'),
    ('services-solutions/index.html', 'https://pipefishlabs.io/services-solutions/', 'Full Service Catalog - Enterprise AI Automation & Security Services | PipeFish Labs', 'Explore PipeFish Labs full catalog of 20+ technical disciplines including multi-agent orchestration, zero-trust architecture, NIST post-quantum cryptography, and AI compliance.'),
    ('case-studies-results/index.html', 'https://pipefishlabs.io/case-studies-results/', 'Case Studies & Measurable Business ROI Results | PipeFish Labs', 'Discover how PipeFish Labs autonomous agent chains deliver 87.4%+ task reduction, $240K+ annual department cost savings, and zero-downtime security modernization.'),
    ('benefits-testimonials/index.html', 'https://pipefishlabs.io/benefits-testimonials/', 'Client Benefits & Verified Industry Impact | PipeFish Labs', 'Read client verification metrics and business benefits of partnering with PipeFish Labs for enterprise AI infrastructure and management consulting.'),
    ('affiliates-corporate-partnerships/index.html', 'https://pipefishlabs.io/affiliates-corporate-partnerships/', 'Corporate Partnerships & Affiliate Program Tracks | PipeFish Labs', 'Join the PipeFish Labs partner ecosystem for consultants, technology vendors, and agencies. Aligned incentives, zero exclusivity, and high commissions.'),
    ('book-a-demo-contact/index.html', 'https://pipefishlabs.io/book-a-demo-contact/', 'Book an Operational Audit Session | PipeFish Labs', 'Schedule a complimentary 90-minute technical architecture and automation audit session with PipeFish Labs senior engineers.'),
    ('demo/index.html', 'https://pipefishlabs.io/demo/', 'Interactive Agent Simulator - Live 8-Node Graph | PipeFish Labs', 'Experience live interactive 8-node multi-agent chain execution with real-time HMAC-signed state handoffs across enterprise workflows.'),
    ('blog/index.html', 'https://pipefishlabs.io/blog/', 'Engineering & Security Blog - AI Architecture Insights | PipeFish Labs', 'Deep-dive technical papers on multi-agent DAG graphs, eBPF threat monitoring, NIST post-quantum cryptography, and EU AI Act Annex IV compliance.'),
    ('legal-privacy-policy/index.html', 'https://pipefishlabs.io/legal-privacy-policy/', 'Privacy Policy, Terms of Service & Security Disclosure | PipeFish Labs', 'Read PipeFish Labs official Privacy Policy, Terms of Service, AI Ethics statement, and Security Disclosure Policy.')
]

for rel_path, url, title, desc in files:
    if os.path.exists(rel_path):
        with open(rel_path, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        # Check canonical tag
        if 'rel="canonical"' not in content:
            canonical_tag = f'  <link rel="canonical" href="{url}">\n'
            content = content.replace('</title>', f'</title>\n{canonical_tag}')

        # Check OpenGraph tags
        if 'property="og:url"' not in content:
            og_tags = f'''  <meta property="og:site_name" content="PipeFish Labs">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="https://pipefishlabs.io/logo.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@pipefishlabs">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="https://pipefishlabs.io/logo.png">
'''
            content = content.replace('<link rel="preconnect"', og_tags + '  <link rel="preconnect"')

        with open(rel_path, 'w', encoding='utf-8') as fp:
            fp.write(content)
        print(f"Optimized meta tags in {rel_path}")
