#!/usr/bin/env python3
"""Generate blog post partials from the abi-archive raw HTML pages."""
import html as H
import os, re, json

ARCH = os.path.expanduser('~/Websites/abi-archive/pages')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pages')

POSTS = [
    ('why-should-i-go-to-barber-school', 'Why Should I Go to Barber School?'),
    ('a-women-barber-the-benefits-of-barber-school', 'A Woman Barber: The Benefits of Barber School'),
    ('are-barbershops-profitable-everything-you-need-to-know', 'Are Barbershops Profitable? Everything You Need to Know'),
    ('first-things-first-what-happens-after-barber-school', 'First Things First: What Happens After Barber School'),
    ('how-to-successfully-market-your-barbershop', 'How to Successfully Market Your Barbershop'),
    ('modern-day-barbering-problem-overcome-them', 'Modern-Day Barbering Problems & How to Overcome Them'),
    ('diverse-haircut-training-at-american-barber-institute', 'Diverse Haircut Training at American Barber Institute'),
    ('barber-school-instructors-in-nyc', 'Barber School Instructors in NYC'),
    ('exploring-the-benefits-of-enrolling-in-the-american-barber-institute-your-path-to-barbering-excellence', 'Exploring the Benefits of Enrolling at ABI: Your Path to Barbering Excellence'),
]

def extract_body(raw):
    """Pull the main article content from the WP page markup."""
    # main content lives inside the entry/post content div; fall back to between H1 and footer
    m = re.search(r'<div class="(?:entry-content|post-content|fl-module-content[^"]*)"[^>]*>(.*?)</div>\s*(?:</div>|<footer|<div class="(?:fl-sidebar|footer))', raw, re.S)
    seg = None
    if m:
        seg = m.group(1)
    else:
        # Take from "Book a Tour" CTA to the financial assistance / footer block
        i = raw.find('Book a Tour')
        j = raw.find('Financial Assistance Is Available', i)
        if j == -1:
            j = raw.find('Get More Info Today', i)
        if i != -1 and j != -1:
            seg = raw[i:j]
    if not seg:
        return None
    # keep h2/h3/p/li structure
    seg = re.sub(r'<(script|style|noscript|form|svg)[^>]*>.*?</\1>', ' ', seg, flags=re.S | re.I)
    out = []
    for tag, attrs, text in re.findall(r'<(h[2-4]|p|li)([^>]*)>(.*?)</\1>', seg, re.S | re.I):
        t = re.sub(r'<[^>]+>', ' ', text)
        t = H.unescape(re.sub(r'\s+', ' ', t)).strip()
        if not t or len(t) < 3:
            continue
        if t in ('Book a Tour', 'Call now', 'Learn More!'):
            continue
        tag = tag.lower()
        if tag == 'li':
            out.append(('li', t))
        elif tag.startswith('h'):
            out.append(('h3', t))
        elif len(t) < 75 and (re.match(r'^\d+\.', t) or not t.rstrip().endswith(('.', '!', '?', ':'))):
            out.append(('h3', t))  # short headline-like paragraph
        else:
            out.append(('p', t))
    # build html merging li runs
    parts, in_ul = [], False
    for tag, t in out:
        esc = H.escape(t, quote=False)
        if tag == 'li':
            if not in_ul:
                parts.append('<ul>'); in_ul = True
            parts.append(f'<li>{esc}</li>')
        else:
            if in_ul:
                parts.append('</ul>'); in_ul = False
            parts.append(f'<{tag}>{esc}</{tag}>')
    if in_ul:
        parts.append('</ul>')
    return '\n'.join(parts)

index_cards = []
made = []
for slug, title in POSTS:
    src = os.path.join(ARCH, f'{slug}.html')
    if not os.path.exists(src):
        print('missing archive page:', slug)
        continue
    raw = open(src, encoding='utf-8', errors='ignore').read()
    body = extract_body(raw)
    if not body or len(body) < 400:
        print('thin body:', slug, len(body or ''))
        continue
    partial = f'''<div class="page-hero">
  <div class="wrap">
    <p class="crumbs"><a href="../index.html">Home</a> / <a href="index.html">Blog</a></p>
    <h1 style="font-size:clamp(1.9rem,4.4vw,3.2rem)">{H.escape(title, quote=False)}</h1>
    <p>From the American Barber Institute blog.</p>
  </div>
</div>
<section>
  <div class="wrap prose" style="max-width:800px">
{body}
    <hr style="border:0;border-top:1px solid #e3d9c5;margin:40px 0">
    <p><b>Ready to start your barbering career?</b> <a href="../programs/500-hour-master-barber.html">Explore the 500-Hour Master Barber Program</a> or <a href="../contact.html">book a free tour</a>.</p>
  </div>
</section>
'''
    fn = f'blog-{slug[:48].rstrip("-")}.html'
    open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(partial)
    made.append((fn, slug, title))
    first_p = re.search(r'<p>(.*?)</p>', body)
    excerpt = (first_p.group(1)[:180] + '…') if first_p else ''
    index_cards.append((slug, title, excerpt))
    print('made', fn)

json.dump([{'partial': f, 'slug': s[:48].rstrip('-'), 'title': t} for f, s, t in made],
          open(os.path.join(OUT, '..', 'blog_manifest.json'), 'w'), indent=1)

# blog index partial
cards = '\n'.join(f'''      <article class="card reveal">
        <div class="card-body">
          <h3 style="font-size:1.15rem">{H.escape(t, quote=False)}</h3>
          <p>{H.escape(e, quote=False)}</p>
          <div class="card-foot"><a class="link" href="{s[:48].rstrip('-')}.html">Read Article →</a></div>
        </div>
      </article>''' for s, t, e in index_cards)
idx = f'''<div class="page-hero">
  <div class="wrap">
    <p class="crumbs"><a href="../index.html">Home</a> / Blog</p>
    <h1>The ABI Blog</h1>
    <p>Career advice, licensing know-how and industry insight from New York's only dedicated barber school.</p>
  </div>
</div>
<section>
  <div class="wrap">
    <div class="cards">
{cards}
    </div>
  </div>
</section>
'''
open(os.path.join(OUT, 'blog-index.html'), 'w', encoding='utf-8').write(idx)
print('made blog-index.html with', len(index_cards), 'cards')
