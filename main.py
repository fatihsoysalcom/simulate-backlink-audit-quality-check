import urllib.parse
from collections import defaultdict

# Simulate a backlink profile for a target website
TARGET_DOMAIN = "example.com"

# Each backlink entry: (source_url, target_url, anchor_text, link_type, source_authority_score)
# link_type: "dofollow", "nofollow", "ugc", "sponsored"
# source_authority_score: 0-100 (higher is better, a simplified metric like Domain Authority)
BACKLINKS_DATA = [
    ("https://www.authoritativeblog.com/post1", f"https://www.{TARGET_DOMAIN}/page1", "SEO Rehberi", "dofollow", 90),
    ("https://www.nicheforum.net/thread/123", f"https://www.{TARGET_DOMAIN}/page2", "backlink izleme", "nofollow", 65),
    ("https://www.spammyblog.xyz/bad-link", f"https://www.{TARGET_DOMAIN}/page1", "bedava seo", "dofollow", 15),
    ("https://www.partnerwebsite.com/services", f"https://www.{TARGET_DOMAIN}/contact", "hizmetlerimiz", "sponsored", 75),
    ("https://www.anotherblog.com/review", f"https://www.{TARGET_DOMAIN}/product", "ürün incelemesi", "dofollow", 80),
    ("https://www.olddirectory.info/listing", f"https://www.{TARGET_DOMAIN}/", "site adı", "dofollow", 30),
    ("https://www.forum-spam.ru/post", f"https://www.{TARGET_DOMAIN}/page3", "tıklayın", "dofollow", 5),
]

def get_domain(url):
    """Extracts the domain from a URL."""
    try:
        return urllib.parse.urlparse(url).netloc
    except:
        return ""

def perform_backlink_audit(backlinks, target_domain):
    """
    Performs a simulated SEO audit on a list of backlinks.
    Identifies potential issues and positive signals based on simple rules.
    """
    audit_results = {
        "total_backlinks": len(backlinks),
        "dofollow_count": 0,
        "nofollow_count": 0,
        "ugc_count": 0,
        "sponsored_count": 0,
        "high_quality_links": [],
        "low_quality_links": [],
        "potential_spam_links": [],
        "anchor_text_distribution": defaultdict(int),
        "domain_diversity": set(),
    }

    print(f"--- Backlink Audit for {target_domain} ---")
    print(f"Total Backlinks Found: {audit_results['total_backlinks']}\n")

    for i, (source_url, target_url, anchor_text, link_type, source_authority) in enumerate(backlinks):
        source_domain = get_domain(source_url)
        audit_results["domain_diversity"].add(source_domain)
        audit_results["anchor_text_distribution"][anchor_text.lower()] += 1

        print(f"[{i+1}] Source: {source_domain} (Authority: {source_authority}) -> Target: {urllib.parse.urlparse(target_url).path}")
        print(f"    Anchor: '{anchor_text}' | Type: {link_type}")

        # --- SEO Audit Rules (simulated) ---
        is_bad_link = False
        reasons = []

        # Rule 1: Flag very low source authority (e.g., below 20)
        if source_authority < 20:
            reasons.append("Very low source authority (potential spam/weak link)")
            is_bad_link = True
        # Rule 2: Flag suspicious or overly generic/keyword-stuffed anchor text
        if anchor_text.lower() in ["tıklayın", "buradan", "bedava seo"] or len(anchor_text.split()) > 5:
            reasons.append("Suspicious or overly long/generic anchor text")
            is_bad_link = True
        # Rule 3: Flag known spammy domains (simplified check for demonstration)
        if "spammyblog" in source_domain or ".ru" in source_domain: 
            reasons.append("Source domain appears spammy")
            is_bad_link = True
        # Rule 4: Flag dofollow links from low-quality sources as higher risk
        if link_type == "dofollow" and source_authority < 30:
            reasons.append("Dofollow link from a low-authority source (high risk)")
            is_bad_link = True

        if is_bad_link:
            audit_results["low_quality_links"].append((source_url, target_url, anchor_text, reasons))
            # Identify links that might need disavowing
            if "potential spam" in " ".join(reasons).lower() or "high risk" in " ".join(reasons).lower():
                audit_results["potential_spam_links"].append((source_url, target_url, anchor_text))
            print(f"    Status: 🔴 Low Quality/Potential Spam - {'; '.join(reasons)}")
        elif source_authority >= 70 and link_type == "dofollow":
            # Identify high-quality dofollow links
            audit_results["high_quality_links"].append((source_url, target_url, anchor_text))
            print(f"    Status: 🟢 High Quality Dofollow Link")
        else:
            print(f"    Status: 🟡 Acceptable Link")

        # Count link types for overall profile analysis
        if link_type == "dofollow":
            audit_results["dofollow_count"] += 1
        elif link_type == "nofollow":
            audit_results["nofollow_count"] += 1
        elif link_type == "ugc":
            audit_results["ugc_count"] += 1
        elif link_type == "sponsored":
            audit_results["sponsored_count"] += 1
        print("-" * 40)

    print("\n--- Audit Summary ---")
    print(f"Total Backlinks: {audit_results['total_backlinks']}")
    print(f"Dofollow Links: {audit_results['dofollow_count']}")
    print(f"Nofollow Links: {audit_results['nofollow_count']}")
    print(f"UGC Links: {audit_results['ugc_count']}")
    print(f"Sponsored Links: {audit_results['sponsored_count']}")
    print(f"High Quality Dofollow Links: {len(audit_results['high_quality_links'])}")
    print(f"Low Quality/Risky Links: {len(audit_results['low_quality_links'])}")
    print(f"Potential Spam Links (Disavow Consideration): {len(audit_results['potential_spam_links'])}")
    print(f"Unique Linking Domains: {len(audit_results['domain_diversity'])}")

    print("\n--- Anchor Text Distribution ---")
    for anchor, count in sorted(audit_results["anchor_text_distribution"].items(), key=lambda item: item[1], reverse=True):
        print(f"'{anchor}': {count} times")

    if audit_results['potential_spam_links']:
        print("\n--- Recommended Action: Review Potential Spam Links for Disavow ---")
        for source_url, _, _, in audit_results['potential_spam_links']:
            print(f"  - {get_domain(source_url)}")

    print("\n--- End of Audit ---")
    return audit_results

if __name__ == "__main__":
    audit_results = perform_backlink_audit(BACKLINKS_DATA, TARGET_DOMAIN)
