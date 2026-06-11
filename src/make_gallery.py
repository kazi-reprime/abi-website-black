#!/usr/bin/env python3
"""Copy curated images from the archive into assets/img and generate the gallery partial."""
import os, re, shutil

ARCH = os.path.expanduser('~/Websites/abi-archive/images')
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(SITE, 'assets', 'img')
os.makedirs(IMG, exist_ok=True)

# named assets used across pages
NAMED = [
    'home-bg.jpg', '500hrs.jpg', '200-Hour-Barber-Fundamentals-Program-ban-1.jpg',
    '50-hour-program.jpg', '3-hours-program.jpg', 'abi-program-c.jpg',
    'abi-program-license.jpg', 'about.jpg', 'School-Mission-Statement.jpg',
    'requirement.jpg', 'IMG_9854.jpg', 'haircut1.jpg', 'haircut3.jpg', 'haircut4.jpg',
    'haircut5.jpg', 'haircut6.jpg', 'haircut7.jpg', 'free-haircut-coupon.jpg',
    'nysed-school-logo.png', 'abi-logo-white.png', 'testimonials-bg.jpg',
    'otherprograms-bg.jpg', 'homecontact-bg-1.jpg',
]
missing = []
for n in NAMED:
    src = os.path.join(ARCH, n)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(IMG, n))
    else:
        missing.append(n)
print('named copied:', len(NAMED) - len(missing), 'missing:', missing)

# og cover
if os.path.exists(os.path.join(IMG, 'home-bg.jpg')):
    shutil.copy2(os.path.join(IMG, 'home-bg.jpg'), os.path.join(IMG, 'og-cover.jpg'))

# gallery photos: clean abi-students-NNN.* and abi-nyc-NNN.* only
gal = sorted(n for n in os.listdir(ARCH)
             if re.match(r'^abi-(students|nyc)-\d{3}\.(jpe?g|png)$', n)
             and os.path.getsize(os.path.join(ARCH, n)) > 8000)
for n in gal:
    shutil.copy2(os.path.join(ARCH, n), os.path.join(IMG, n))
print('gallery copied:', len(gal))

students = [n for n in gal if 'students' in n]
campus = [n for n in gal if 'nyc' in n]

def grid(items, alt_prefix):
    return '\n'.join(
        f'      <a href="assets/img/{n}"><img src="assets/img/{n}" alt="{alt_prefix} {i+1}" loading="lazy" width="400" height="400"></a>'
        for i, n in enumerate(items))

partial = f'''<div class="page-hero">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> / Gallery</p>
    <h1>Our Gallery</h1>
    <p>Student work, client cuts, and life inside our 3,000 sq ft Midtown Manhattan campus. Click any photo to view it full size.</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="section-head">
      <p class="kicker">Student Work</p>
      <h2>Cuts By Our Students</h2>
    </div>
    <div class="gallery-grid">
{grid(students, "ABI student work photo")}
    </div>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <div class="section-head">
      <p class="kicker">The Campus</p>
      <h2>Inside The School</h2>
    </div>
    <div class="gallery-grid">
{grid(campus, "American Barber Institute campus photo")}
    </div>
  </div>
</section>
'''
open(os.path.join(SITE, 'src', 'pages', 'gallery.html'), 'w').write(partial)
print(f'gallery.html partial written ({len(students)} student + {len(campus)} campus photos)')
