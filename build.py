#!/usr/bin/env python3
"""Static site generator for Knit & Denim Sourcing. Run: python3 build.py  (writes ./site/*.html)"""
import json, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "site"
DOMAIN = "https://knitanddenimsourcing.com"
EMAIL = "hello@knitanddenimsourcing.com"  # PLACEHOLDER - confirm
NAME = "Knit & Denim Sourcing"

ARR = '<span class="arr" aria-hidden="true">&rarr;</span>'
CHECK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'

NAV = [
    ("index.html", "Home"), ("about.html", "About"), ("knitwear-sourcing.html", "Knitwear"),
    ("denim-sourcing.html", "Denim"), ("product-development.html", "Product Development"),
    ("apparel-manufacturing.html", "Manufacturing"), ("quality-control.html", "Quality"),
]

def head(title, desc, path, schema=""):
    url = DOMAIN + "/" + ("" if path == "index.html" else path)
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#243B63">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=DM+Sans:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/css/styles.css">
<script>document.documentElement.className=document.documentElement.className.replace('no-js','js')</script>
{schema}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def header(active):
    items = ""
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        items += f'<li><a class="link" href="{href}"{cur}>{label}</a></li>\n'
    items += f'<li><a class="btn sm" href="contact.html">Request a Quote {ARR}</a></li>'
    return f'''<header class="site-header">
<div class="wrap nav">
<a class="brand" href="index.html" aria-label="{NAME} home">Knit <span>&amp;</span> Denim <small style="font-family:var(--sans);font-size:.62rem;letter-spacing:.24em;text-transform:uppercase;font-weight:500;margin-left:.3rem">Sourcing</small></a>
<button class="nav-toggle" aria-expanded="false" aria-controls="nav-list">Menu</button>
<nav aria-label="Primary"><ul id="nav-list">
{items}
</ul></nav>
</div>
</header>
<main id="main">
'''

FOOT = f'''</main>
<footer class="site-footer">
<div class="wrap">
<div class="foot-grid">
<div><p class="foot-brand">From fabric concept to <em>finished garment.</em></p></div>
<div><h4>Capabilities</h4><ul>
<li><a href="knitwear-sourcing.html">Knitwear Sourcing</a></li>
<li><a href="denim-sourcing.html">Denim Sourcing</a></li>
<li><a href="product-development.html">Product Development</a></li>
<li><a href="apparel-manufacturing.html">Apparel Manufacturing</a></li>
<li><a href="quality-control.html">Quality Control</a></li></ul></div>
<div><h4>Company</h4><ul>
<li><a href="about.html">About</a></li>
<li><a href="contact.html">Request a Quote</a></li>
<li><a href="contact.html#brief">Submit Your Product Brief</a></li></ul></div>
<div><h4>Contact</h4><ul>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li>Replies to qualified briefs within a stated window (to be confirmed)</li></ul></div>
</div>
<div class="foot-base"><span>&copy; <span id="yr">2026</span> {NAME}. All rights reserved.</span><span>knitanddenimsourcing.com</span></div>
</div>
</footer>
<script src="assets/js/main.js" defer></script>
</body>
</html>
'''

def cta(title="Tell us what you want to make.", text="Share a sketch, a reference garment or a full tech pack. We will respond with sourcing options, a development path and the questions that matter.", dark="on-indigo"):
    return f'''<section class="{dark} cta-band"><div class="wrap">
<div class="eyebrow reveal">Start a project</div>
<h2 class="reveal">{title}</h2>
<p class="lede reveal">{text}</p>
<div class="btn-row reveal">
<a class="btn" href="contact.html">Request a Sourcing Consultation {ARR}</a>
<a class="btn ghost" href="contact.html#brief">Submit Your Product Brief</a>
</div></div></section>
'''

def form_block(id_prefix=""):
    cats = ["Knitwear (T-shirts, polos, hoodies, joggers)", "Denim garments (jeans, jackets, shirts)", "Knit fabric sourcing", "Denim fabric sourcing", "Knit + denim collection", "Not sure yet"]
    qty = ["Under 300 pieces per style", "300 - 1,000 pieces per style", "1,000 - 5,000 pieces per style", "5,000+ pieces per style", "Fabric only / not sure"]
    tl = ["Within 1 month", "1 - 3 months", "3 - 6 months", "6+ months", "Flexible / exploring"]
    opt = lambda items: '<option value="">Select&hellip;</option>' + "".join(f'<option>{i}</option>' for i in items)
    def f(name, label, kind="text", extra="", full=False, required=True, auto=""):
        req = ' <span class="req" aria-hidden="true">*</span>' if required else ""
        aria = ' aria-required="true"' if required else ""
        a = f' autocomplete="{auto}"' if auto else ""
        return f'''<div class="field{' full' if full else ''}"><label for="f-{name}">{label}{req}</label>
<input id="f-{name}" name="{name}" type="{kind}"{aria}{a} {extra}><div class="err" aria-live="polite"></div></div>'''
    def s(name, label, items):
        return f'''<div class="field"><label for="f-{name}">{label} <span class="req" aria-hidden="true">*</span></label>
<select id="f-{name}" name="{name}" aria-required="true">{opt(items)}</select><div class="err" aria-live="polite"></div></div>'''
    return f'''<form id="inquiry-form" class="form-card" action="#" method="post" enctype="multipart/form-data" novalidate>
<div class="form-grid">
{f("name","Name",auto="name")}
{f("company","Company / brand",auto="organization")}
{f("email","Work email","email",auto="email")}
{f("country","Country",auto="country-name")}
{s("category","Product category",cats)}
{s("quantity","Estimated order quantity",qty)}
<div class="field full"><label for="f-description">Project description <span class="req" aria-hidden="true">*</span></label>
<textarea id="f-description" name="description" aria-required="true" placeholder="Garments or fabrics, target fit and weight, wash or finish, target market, price expectations, anything we should know."></textarea><div class="err" aria-live="polite"></div></div>
{s("timeline","Target timeline",tl)}
<div class="field" id="brief"><label for="f-brief">Product brief or tech pack (optional)</label>
<input id="f-brief" name="brief" type="file" accept=".pdf,.png,.jpg,.jpeg,.doc,.docx,.xls,.xlsx,.zip,.ai,.psd"><div class="err" aria-live="polite"></div></div>
<div class="hp" aria-hidden="true"><label>Leave blank <input name="website" tabindex="-1" autocomplete="off"></label></div>
</div>
<div class="btn-row"><button class="btn" type="submit">Send Brief {ARR}</button></div>
<p class="fine" style="margin-top:1rem">Fields marked * are required. Files up to 10 MB. We use your details only to respond to your inquiry.</p>
<div id="form-status" class="form-status" tabindex="-1" aria-live="polite"></div>
</form>'''

def page_head(crumb, h1, lede):
    return f'''<section class="page-head"><div class="wrap">
<p class="crumbs"><a href="index.html">Home</a> / {crumb}</p>
<div class="eyebrow">{crumb}</div>
<h1 class="reveal">{h1}</h1>
<p class="lede reveal">{lede}</p>
</div></section>
'''

def media(cls, tx, cap, tall=False):
    return f'<figure class="media{" tall" if tall else ""} reveal" style="margin:0"><div class="layer {tx}" role="img" aria-label="{cap}"></div><figcaption>{cap}</figcaption></figure>'

def build_pages():
    P = {}

    # ---------------- HOME ----------------
    schema = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "Organization", "name": NAME, "url": DOMAIN,
        "description": "End-to-end knitwear and denim sourcing, product development and apparel manufacturing coordination for clothing brands and retailers.",
        "email": EMAIL}) + '</script>'
    body = head("Knitwear & Denim Sourcing Company | Knit & Denim Sourcing",
                "End-to-end partner for knitwear and denim sourcing, garment product development and private-label apparel manufacturing for brands, retailers and wholesalers.",
                "index.html", schema) + header("index.html")
    body += f'''<section class="hero"><div class="wrap">
<div class="hero-grid">
<div>
<div class="eyebrow">Knitwear &amp; denim sourcing partner</div>
<h1><span class="line"><span style="--d:.05s">From fabric concept</span></span><span class="line"><span style="--d:.18s">to <em>finished</em></span></span><span class="line"><span style="--d:.31s">garment.</span></span></h1>
<p class="lede reveal" style="--d:.4s">Your end-to-end partner for knitwear and denim sourcing, product development, and apparel manufacturing.</p>
<div class="btn-row reveal" style="--d:.5s">
<a class="btn" href="contact.html">Request a Sourcing Consultation {ARR}</a>
<a class="btn ghost" href="#capabilities">Explore Our Capabilities</a>
</div>
</div>
<figure class="hero-media curtain" style="margin:0" role="img" aria-label="Indigo denim twill above a cream ribbed knit, illustrating our two specialisms">
<div class="layer l1"></div><div class="layer l2"></div>
<figcaption><span>Denim</span><span>Knitwear</span></figcaption>
</figure>
</div>
<div class="hero-meta reveal">
<div><strong>Two specialisms</strong>Knitwear and denim, sourced and developed with focus.</div>
<div><strong>One point of contact</strong>Fabric, sampling, production and finishing coordinated together.</div>
<div><strong>Specification first</strong>Your tech pack and target price set the brief, not our catalogue.</div>
</div></div></section>

<section id="capabilities" style="padding-top:0"><div class="wrap">
<div class="split-head"><div><div class="eyebrow reveal">Capabilities</div><h2 class="reveal">Two categories. Done properly.</h2></div>
<p class="lede reveal">We concentrate on knitwear and denim so that fabric knowledge, construction detail and finishing expertise are applied to every brief, from first swatch to final carton.</p></div>
<div class="cap-grid">
<div class="cap reveal"><span class="num">i.</span><h3>Knitwear</h3>
<ul><li>Single jersey, interlock, rib</li><li>Pique, fleece, French terry</li><li>Cotton and blended knits</li><li>T-shirts and polos</li><li>Hoodies and sweatshirts</li><li>Joggers</li></ul>
<p class="note">Organic cotton knitwear available subject to verified capability.</p>
<a class="btn ghost sm" href="knitwear-sourcing.html">Knitwear sourcing {ARR}</a></div>
<div class="cap reveal" style="--d:.1s"><span class="num">ii.</span><h3>Denim</h3>
<ul><li>Raw, rigid and stretch denim</li><li>Washed and finished denim</li><li>Jeans</li><li>Jackets and shirts</li><li>Shorts and skirts</li><li>Wash and finish development</li></ul>
<p class="note">Selvedge denim available subject to verified capability.</p>
<a class="btn ghost sm" href="denim-sourcing.html">Denim sourcing {ARR}</a></div>
</div></div></section>

<section class="on-dark"><div class="wrap">
<div class="split-head"><div><div class="eyebrow reveal">End-to-end process</div><h2 class="reveal">One thread from brief to shipment.</h2></div>
<p class="lede reveal">Most sourcing problems come from handoffs between fabric, sampling and production. We keep one line of ownership across all three.</p></div>
<ol class="process">
<li class="reveal"><h3>Brief &amp; specification</h3><p>We review your references, tech pack, target price and quantities, and flag risks early.</p></li>
<li class="reveal"><h3>Fabric &amp; material selection</h3><p>Fabric options matched to hand-feel, weight, performance and cost, with swatches for approval.</p></li>
<li class="reveal"><h3>Development &amp; sampling</h3><p>Pattern, fit and prototype rounds coordinated with comments consolidated into clear revisions.</p></li>
<li class="reveal"><h3>Production coordination</h3><p>Approved samples become the production standard. We track milestones and keep you informed.</p></li>
<li class="reveal"><h3>Quality, finishing &amp; packing</h3><p>Inspection at defined stages, garment finishing, labelling and packaging to your requirements.</p></li>
<li class="reveal"><h3>Shipment coordination</h3><p>Export documentation and logistics coordination where supported for your destination.</p></li>
</ol></div></section>

<section><div class="wrap split">
{media("", "tx-swatch", "Fabric swatches &amp; sampling")}
<div><div class="eyebrow reveal">Product development &amp; sampling</div>
<h2 class="reveal">Concept to approved sample, without the guesswork.</h2>
<p class="lede reveal">Whether you arrive with a full tech pack or a reference garment and a mood board, we translate intent into specification: fabric, construction, measurements, trims, washes.</p>
<ul class="check reveal"><li>{CHECK}<span><strong>Tech pack coordination.</strong> Gaps identified and closed before sampling begins.</span></li>
<li>{CHECK}<span><strong>Pattern and fit development.</strong> Measured fit rounds with clear, consolidated comments.</span></li>
<li>{CHECK}<span><strong>Fabric and trim approvals.</strong> Swatches and lab-dips before anything is committed.</span></li></ul>
<div class="btn-row"><a class="btn ghost" href="product-development.html">Product development {ARR}</a></div></div>
</div></section>

<section class="on-indigo"><div class="wrap split">
<div><div class="eyebrow reveal">Manufacturing &amp; quality control</div>
<h2 class="reveal">Production you can see into.</h2>
<p class="lede reveal">We coordinate private-label production against your approved sample and check quality at defined stages: materials in, in-line, and final. You see what we see.</p>
<div class="btn-row reveal"><a class="btn" href="apparel-manufacturing.html">Apparel manufacturing {ARR}</a><a class="btn ghost" href="quality-control.html">Quality control</a></div></div>
{media("", "tx-stitch", "Seam &amp; finishing detail")}
</div></section>

<section><div class="wrap">
<div class="split-head"><div><div class="eyebrow reveal">Who we work with</div><h2 class="reveal">Built for brands at every stage.</h2></div>
<p class="lede reveal">From first collections to repeat programmes, we adapt the level of support to where your business is.</p></div>
<div class="cols-3">
<div class="reveal"><h3>Startups &amp; emerging labels</h3><p>Founders launching a first collection who need guidance on fabrics, specifications and minimums.</p></div>
<div class="reveal" style="--d:.08s"><h3>Established apparel brands</h3><p>Product development and sourcing teams expanding ranges or consolidating suppliers.</p></div>
<div class="reveal" style="--d:.16s"><h3>Private-label businesses</h3><p>Retailers and wholesalers needing consistent programmes built to their own labels.</p></div>
<div class="reveal"><h3>E-commerce brands</h3><p>Online-first labels that need reliable replenishment and fast, clear communication.</p></div>
<div class="reveal" style="--d:.08s"><h3>International buyers</h3><p>Buyers seeking a single accountable contact for knitwear and denim programmes.</p></div>
<div class="reveal" style="--d:.16s"><h3>Designers</h3><p>Creative directors needing fabric development and sampling that respects the original idea.</p></div>
</div></div></section>

<section class="on-dark"><div class="wrap split top">
<div><div class="eyebrow reveal">Why work with us</div><h2 class="reveal">Sourcing that behaves like part of your team.</h2></div>
<ul class="check">
<li class="reveal">{CHECK}<span><strong>Category focus.</strong> Knitwear and denim only, so our attention goes deeper.</span></li>
<li class="reveal">{CHECK}<span><strong>Single accountable contact.</strong> One owner across fabric, sampling and production.</span></li>
<li class="reveal">{CHECK}<span><strong>Commercial clarity.</strong> Costings that show what drives price, so you can make informed trade-offs.</span></li>
<li class="reveal">{CHECK}<span><strong>Transparent communication.</strong> Clear milestones, honest feedback and early warning of risks.</span></li>
<li class="reveal">{CHECK}<span><strong>Specification discipline.</strong> Approved samples and written standards guide production.</span></li>
</ul></div></section>
''' + cta() + f'''<section><div class="wrap split top">
<div><div class="eyebrow reveal">Contact</div><h2 class="reveal">Send your brief.</h2>
<p class="lede reveal">The more detail you share, the more useful our first response will be. Attach a tech pack if you have one.</p>
<dl class="contact-aside"><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></dl></div>
<div class="reveal">{form_block()}</div></div></section>
''' + FOOT
    P["index.html"] = body

    # ---------------- ABOUT ----------------
    b = head("About Knit & Denim Sourcing | Textile Sourcing Partner",
             "Knit & Denim Sourcing is a specialist sourcing partner for knitwear and denim, coordinating fabric, product development, sampling and apparel manufacturing.",
             "about.html") + header("about.html")
    b += page_head("About", "A sourcing partner built around two categories.",
                   "We help clothing brands, retailers and wholesalers turn a concept into a finished, production-ready garment, with knitwear and denim at the centre of what we do.")
    b += f'''<section><div class="wrap split">
<div><div class="eyebrow reveal">Our approach</div><h2 class="reveal">Specification first. Then the supply chain.</h2>
<p class="reveal">Many brands begin by looking for a factory. We begin by understanding the garment: the fabric, the construction, the finish, the price point and the customer. Only then do we match the right materials and manufacturing partners to the brief.</p>
<p class="reveal">That sequence reduces rework in sampling, avoids mismatched expectations and gives you a production standard that is documented, not assumed.</p></div>
{media("", "tx-rolls", "Material selection", True)}
</div></section>
<section class="on-dark"><div class="wrap">
<div class="eyebrow reveal">Philosophy</div><h2 class="reveal" style="max-width:20ch">Fewer categories, clearer accountability.</h2>
<div class="cols-3" style="margin-top:3rem">
<div class="reveal"><h3>Depth over breadth</h3><p>We focus on knitwear and denim so our fabric and construction knowledge stays sharp.</p></div>
<div class="reveal" style="--d:.08s"><h3>Transparency</h3><p>Costs, timelines and risks are explained plainly, including when the answer is not what you hoped.</p></div>
<div class="reveal" style="--d:.16s"><h3>Commercial sense</h3><p>Great product that cannot be made at the right cost is not a good product. We design with margin in mind.</p></div>
</div></div></section>
<section><div class="wrap split top">
<div><div class="eyebrow reveal">How we work with buyers</div><h2 class="reveal">A relationship, not a transaction.</h2></div>
<div><p class="reveal">You get a single contact who understands your brief and your commercial goals. We consolidate feedback, keep sampling moving and report honestly on progress.</p>
<p class="reveal">For startups, that means practical guidance on minimums, fabric choices and development sequencing. For established brands, it means a dependable extension of your product development and sourcing team.</p>
<div class="btn-row reveal"><a class="btn" href="contact.html">Request a Sourcing Consultation {ARR}</a></div></div>
</div></section>
<section class="on-indigo"><div class="wrap"><div class="eyebrow">Capabilities at a glance</div>
<ul class="tag-row reveal"><li>Fabric sourcing</li><li>Material selection</li><li>Tech pack coordination</li><li>Pattern development</li><li>Sampling</li><li>Fit development</li><li>Fabric testing coordination</li><li>Quality control</li><li>Production coordination</li><li>Private-label manufacturing</li><li>Garment finishing</li><li>Packaging</li><li>Export coordination, where supported</li></ul></div></section>
''' + cta() + FOOT
    P["about.html"] = b

    # ---------------- KNITWEAR ----------------
    b = head("Knitwear Sourcing & Knitwear Manufacturer Support | Knit & Denim Sourcing",
             "Knitwear sourcing and garment development: jersey, interlock, rib, pique, fleece and French terry fabrics, plus T-shirts, polos, hoodies, sweatshirts and joggers.",
             "knitwear-sourcing.html") + header("knitwear-sourcing.html")
    b += page_head("Knitwear sourcing", "Knit fabrics and garments, specified with care.",
                   "From jersey and fleece to finished T-shirts, polos and hoodies, we source the right knit for the garment and manage development through to production.")
    b += f'''<section><div class="wrap split">
{media("", "tx-knit", "Rib &amp; jersey structure", True)}
<div><div class="eyebrow reveal">Knit fabric categories</div><h2 class="reveal">Choose the structure, then the yarn and finish.</h2>
<p class="reveal">Knit performance depends on structure, yarn, GSM and finishing. We help you balance hand-feel, shape retention, shrinkage and cost.</p>
<ul class="check reveal">
<li>{CHECK}<span><strong>Single jersey.</strong> Lightweight and versatile for tees and base layers.</span></li>
<li>{CHECK}<span><strong>Interlock.</strong> Smoother, more stable double-knit for premium basics.</span></li>
<li>{CHECK}<span><strong>Rib.</strong> Stretch and recovery for trims, tops and fitted styles.</span></li>
<li>{CHECK}<span><strong>Pique.</strong> Textured surface for polo shirts and sportswear.</span></li>
<li>{CHECK}<span><strong>Fleece &amp; French terry.</strong> Looped or brushed backs for hoodies, sweatshirts and joggers.</span></li>
<li>{CHECK}<span><strong>Cotton and blended knits.</strong> Fibre blends tuned for comfort, durability and price.</span></li></ul>
<p class="note">Organic cotton knitwear is offered subject to verified capability and certification at the time of enquiry.</p></div>
</div></section>
<section class="on-dark"><div class="wrap">
<div class="eyebrow reveal">Garment development</div><h2 class="reveal" style="max-width:18ch">Knitwear we develop and produce.</h2>
<div class="cols-3" style="margin-top:3rem">
<div class="reveal"><h3>T-shirts &amp; polos</h3><p>Fit blocks, collar and cuff construction, neck tape, labels, and wash treatments.</p></div>
<div class="reveal" style="--d:.08s"><h3>Hoodies &amp; sweatshirts</h3><p>Fabric weight, hood construction, ribbing, drawcords, prints and embroidery coordination.</p></div>
<div class="reveal" style="--d:.16s"><h3>Joggers</h3><p>Waist, cuff and pocket detail with fabric choice matched to wear and care.</p></div>
</div></div></section>
<section><div class="wrap split top">
<div><div class="eyebrow reveal">Applications</div><h2 class="reveal">Where our knitwear programmes fit.</h2></div>
<ul class="tag-row reveal"><li>Everyday basics</li><li>Streetwear</li><li>Loungewear</li><li>Uniforms &amp; team wear</li><li>Promotional apparel</li><li>Private-label ranges</li><li>Retail replenishment programmes</li></ul>
</div></section>
''' + cta("Planning a knitwear range?", "Tell us the styles, fabrics and quantities you have in mind and we will outline a development path.") + FOOT
    P["knitwear-sourcing.html"] = b

    # ---------------- DENIM ----------------
    b = head("Denim Sourcing & Denim Garment Manufacturing | Knit & Denim Sourcing",
             "Denim fabric sourcing and denim garment development: raw, washed, stretch and rigid denim for jeans, jackets, shirts, shorts and skirts.",
             "denim-sourcing.html") + header("denim-sourcing.html")
    b += page_head("Denim sourcing", "Denim, from fabric choice to final wash.",
                   "We source denim fabrics and coordinate the development of jeans and denim garments, including the washes and finishes that define the final product.")
    b += f'''<section><div class="wrap split">
<div><div class="eyebrow reveal">Denim fabric options</div><h2 class="reveal">The right denim for the right fit.</h2>
<p class="reveal">Weight, weave, stretch content and finish decide how a garment looks, wears and ages. We help you choose with the end customer and price point in mind.</p>
<ul class="check reveal">
<li>{CHECK}<span><strong>Raw denim.</strong> Unwashed, deep indigo, for brands that want fades to develop with wear.</span></li>
<li>{CHECK}<span><strong>Washed denim.</strong> Pre-finished for softness, colour and consistent shade.</span></li>
<li>{CHECK}<span><strong>Rigid denim.</strong> Structured, classic hand-feel.</span></li>
<li>{CHECK}<span><strong>Stretch denim.</strong> Comfort and recovery with varying elastane levels.</span></li>
<li>{CHECK}<span><strong>Selvedge denim.</strong> Available subject to verified capability.</span></li></ul></div>
{media("", "tx-denim", "Indigo twill", True)}
</div></section>
<section class="on-dark"><div class="wrap">
<div class="split-head"><div><div class="eyebrow reveal">Garment development</div><h2 class="reveal">Denim garments we develop.</h2></div>
<p class="lede reveal">Jeans, jackets, shirts, shorts and skirts, developed through fit, wash and finishing rounds until they match your approved reference.</p></div>
<div class="cols-3">
<div class="reveal"><h3>Jeans</h3><p>Fit blocks, rise and leg shapes, pocket and hardware detail, and wash development.</p></div>
<div class="reveal" style="--d:.08s"><h3>Jackets &amp; shirts</h3><p>Construction, topstitching, trims and washes coordinated across outerwear and shirting.</p></div>
<div class="reveal" style="--d:.16s"><h3>Shorts &amp; skirts</h3><p>Seasonal denim programmes with consistent fabric and shade across the range.</p></div>
</div></div></section>
<section><div class="wrap split">
{media("", "tx-stitch", "Topstitch &amp; seam detail")}
<div><div class="eyebrow reveal">Washes &amp; finishes</div><h2 class="reveal">Where denim gets its character.</h2>
<p class="reveal">Wash and finish choices change appearance, hand-feel and cost. We coordinate sampling against your reference so shade and fade are agreed before bulk production.</p>
<ul class="tag-row reveal"><li>Rinse</li><li>Stone and enzyme wash</li><li>Vintage looks</li><li>Whiskering &amp; hand finishes</li><li>Coatings &amp; overdyes</li></ul>
<p class="note">Available finishes depend on the manufacturing partner selected for each project.</p></div>
</div></section>
''' + cta("Developing a denim collection?", "Share your fits, fabric weights and wash references. We will map the route from sample to production.") + FOOT
    P["denim-sourcing.html"] = b

    # ---------------- PRODUCT DEVELOPMENT ----------------
    b = head("Garment Product Development & Sampling | Knit & Denim Sourcing",
             "Concept-to-sample garment product development for knitwear and denim: tech pack coordination, pattern and fit development, fabric sourcing and sampling.",
             "product-development.html") + header("product-development.html")
    b += page_head("Product development", "From concept to approved sample.",
                   "A clear development workflow that turns references, sketches and tech packs into production-ready garments.")
    b += f'''<section class="on-dark" style="padding-top:clamp(40px,6vw,80px)"><div class="wrap">
<ol class="process">
<li class="reveal"><h3>Concept &amp; references</h3><p>We review sketches, reference garments, mood boards and target price, then confirm the development scope.</p></li>
<li class="reveal"><h3>Tech pack coordination</h3><p>We help complete or refine your tech pack: measurements, construction, trims, labels, washes and packing.</p></li>
<li class="reveal"><h3>Fabric &amp; trim selection</h3><p>Fabric options, swatches and lab-dips for approval before sampling.</p></li>
<li class="reveal"><h3>Pattern &amp; first sample</h3><p>Patterns made to specification and first prototypes produced for review.</p></li>
<li class="reveal"><h3>Fit development</h3><p>Measured fit comments consolidated into clear revisions, with as many rounds as the garment needs.</p></li>
<li class="reveal"><h3>Pre-production sample</h3><p>The approved sample and written specification become the production standard.</p></li>
</ol></div></section>
<section><div class="wrap split">
<div><div class="eyebrow reveal">Product specifications</div><h2 class="reveal">What a good brief contains.</h2>
<ul class="check reveal"><li>{CHECK}<span>Garment type, fit and size range</span></li><li>{CHECK}<span>Fabric composition, weight and finish</span></li><li>{CHECK}<span>Construction and stitching detail</span></li><li>{CHECK}<span>Trims, labels and packaging</span></li><li>{CHECK}<span>Target price and quantities</span></li><li>{CHECK}<span>Timeline and destination market</span></li></ul>
<p class="note">No tech pack yet? We can help you build one.</p></div>
{media("", "tx-swatch", "Swatches &amp; sampling", True)}
</div></section>
''' + cta("Have a concept to develop?", "Send us what you have. We will tell you what is needed to move to sampling.") + FOOT
    P["product-development.html"] = b

    # ---------------- MANUFACTURING ----------------
    b = head("Apparel Manufacturing & Private-Label Clothing | Knit & Denim Sourcing",
             "Private-label clothing manufacturing coordination for knitwear and denim: production planning, garment finishing, packaging and export coordination.",
             "apparel-manufacturing.html") + header("apparel-manufacturing.html")
    b += page_head("Apparel manufacturing", "Production coordinated to your approved standard.",
                   "We manage private-label knitwear and denim production from approved sample through finishing, packing and shipment, with clear communication at every stage.")
    b += f'''<section><div class="wrap split">
{media("", "tx-rolls", "Materials in production planning", True)}
<div><div class="eyebrow reveal">Production coordination</div><h2 class="reveal">One schedule. One point of contact.</h2>
<p class="reveal">Once samples are approved, we plan material allocation, cutting, sewing, washing and finishing against your delivery window and keep you updated at agreed milestones.</p>
<ul class="check reveal"><li>{CHECK}<span><strong>Production planning.</strong> Milestones mapped back from your target delivery date.</span></li><li>{CHECK}<span><strong>Material coordination.</strong> Fabric, trims and labels aligned to the approved sample.</span></li><li>{CHECK}<span><strong>Progress reporting.</strong> Regular updates and early notice of risks.</span></li></ul></div>
</div></section>
<section class="on-dark"><div class="wrap">
<div class="eyebrow reveal">Private-label services</div><h2 class="reveal" style="max-width:20ch">Your label, your specification.</h2>
<div class="cols-3" style="margin-top:3rem">
<div class="reveal"><h3>Private-label manufacturing</h3><p>Programmes built to your brand, fit blocks, labels and packaging requirements.</p></div>
<div class="reveal" style="--d:.08s"><h3>Garment finishing</h3><p>Pressing, trimming, tagging and folding to a defined finishing standard.</p></div>
<div class="reveal" style="--d:.16s"><h3>Packaging &amp; export</h3><p>Packing to your requirements, with export coordination where supported.</p></div>
</div></div></section>
<section><div class="wrap split top"><div><div class="eyebrow reveal">Order sizes</div><h2 class="reveal">Minimums are project-specific.</h2></div>
<div><p class="reveal">Minimum order quantities and lead times depend on the garment, fabric and manufacturing partner. Share your target volume and we will outline realistic options, rather than quoting a one-size-fits-all number.</p>
<div class="btn-row reveal"><a class="btn" href="contact.html">Request a Quote {ARR}</a></div></div></div></section>
''' + cta("Ready to plan production?", "Send your approved sample or tech pack and target quantities.") + FOOT
    P["apparel-manufacturing.html"] = b

    # ---------------- QUALITY ----------------
    b = head("Quality Control for Knitwear & Denim Production | Knit & Denim Sourcing",
             "Quality assurance coordination for knitwear and denim garments: material checks, in-line inspection, final inspection and fabric testing coordination.",
             "quality-control.html") + header("quality-control.html")
    b += page_head("Quality control", "Quality checked at the stages that matter.",
                   "We build inspection into the workflow so issues are found early, documented clearly and resolved before they reach your warehouse.")
    b += f'''<section class="on-dark" style="padding-top:clamp(40px,6vw,80px)"><div class="wrap">
<ol class="process">
<li class="reveal"><h3>Material checks</h3><p>Incoming fabric and trims are checked against approved swatches, specification and shade.</p></li>
<li class="reveal"><h3>Pre-production review</h3><p>Pre-production samples are compared with the written specification before cutting starts.</p></li>
<li class="reveal"><h3>In-line inspection</h3><p>Checks during sewing and finishing to catch construction and measurement issues early.</p></li>
<li class="reveal"><h3>Final inspection</h3><p>Finished goods checked against the approved sample, measurement tolerances and packing instructions.</p></li>
<li class="reveal"><h3>Reporting</h3><p>Findings summarised in clear reports so decisions are quick and informed.</p></li>
</ol></div></section>
<section><div class="wrap split">
<div><div class="eyebrow reveal">Testing coordination</div><h2 class="reveal">Fabric testing, arranged for you.</h2>
<p class="reveal">Where your brief requires lab testing, such as shrinkage, colour fastness or composition, we coordinate sampling to accredited labs of your choosing or on your behalf, and share the results.</p>
<p class="note">Certifications and standards are stated only where verified. Ask us which apply to your project.</p></div>
{media("", "tx-stitch", "Seam inspection", True)}
</div></section>
''' + cta("Need a quality plan for your next order?", "Tell us your quality expectations and we will build them into the schedule.") + FOOT
    P["quality-control.html"] = b

    # ---------------- CONTACT ----------------
    b = head("Request a Sourcing Consultation | Knit & Denim Sourcing",
             "Request a quote or submit your product brief for knitwear and denim sourcing, development and apparel manufacturing.",
             "contact.html") + header("contact.html")
    b += page_head("Contact", "Request a sourcing consultation.",
                   "Tell us what you are making. We will respond with sourcing options, a development path and the questions that will shape your quote.")
    b += f'''<section style="padding-top:clamp(40px,6vw,80px)"><div class="wrap split top">
<aside class="contact-aside"><h2 style="font-size:clamp(1.8rem,3vw,2.6rem)">What happens next</h2>
<ol style="padding-left:1.2rem"><li>We review your brief and reply with questions or options.</li><li>We outline fabric, sampling and production routes with indicative costs.</li><li>You approve a development plan and we begin sampling.</li></ol>
<dl><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
<dt>Best for</dt><dd>Brands, retailers and wholesalers seeking knitwear or denim sourcing.</dd></dl></aside>
<div>{form_block()}</div></div></section>
''' + FOOT
    P["contact.html"] = b
    return P

def main():
    os.makedirs(OUT, exist_ok=True)
    pages = build_pages()
    for name, html in pages.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(html)
    urls = "".join(f"<url><loc>{DOMAIN}/{'' if n=='index.html' else n}</loc></url>" for n in pages)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    print("Built", len(pages), "pages")

main()
