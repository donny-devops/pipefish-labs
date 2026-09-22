#!/usr/bin/env python3
"""
LCP Optimization & Core Web Vitals Tool for Static & Edge Sites.
Part of the 'web-lcp-optimizer' skill.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def cmd_audit(args):
    """Audit HTML and CSS files for potential LCP and Core Web Vitals bottlenecks."""
    html_path = Path(args.html)
    css_path = Path(args.css) if args.css else None
    
    if not html_path.exists():
        sys.stderr.write(f"Error: HTML file '{html_path}' does not exist.\n")
        sys.exit(1)
        
    html_content = html_path.read_text(encoding="utf-8", errors="ignore")
    issues = []
    recommendations = []
    
    # 1. Check for video preload in head (heavy payload bottleneck)
    if re.search(r'<link[^>]*rel=["\']preload["\'][^>]*as=["\']video["\']', html_content, re.I):
        issues.append({
            "severity": "HIGH",
            "rule": "no-video-preload-in-head",
            "message": "Found <link rel='preload' as='video'> in <head>. This steals network bandwidth from critical LCP image and CSS assets."
        })
        recommendations.append("Remove the video preload link tag from <head> to prioritize above-the-fold content.")
        
    # 2. Check for high-priority hero image preload
    has_image_preload = bool(re.search(r'<link[^>]*rel=["\']preload["\'][^>]*as=["\']image["\']', html_content, re.I))
    has_fetchpriority_high = bool(re.search(r'<link[^>]*fetchpriority=["\']high["\']', html_content, re.I))
    
    if not has_image_preload:
        issues.append({
            "severity": "MEDIUM",
            "rule": "missing-hero-image-preload",
            "message": "No <link rel='preload' as='image'> found for hero/banner element."
        })
        recommendations.append("Add a <link rel='preload' as='image' href='...' fetchpriority='high'> tag in <head>.")
    elif not has_fetchpriority_high:
        issues.append({
            "severity": "LOW",
            "rule": "missing-fetchpriority-high",
            "message": "Image preload exists but lacks fetchpriority='high'."
        })
        recommendations.append("Add fetchpriority='high' to the image preload link tag.")
        
    # 3. Check for modern image format (<picture> or .webp / .avif)
    hero_imgs = re.findall(r'<img[^>]*class=["\'][^"\']*hero[^"\']*["\'][^>]*>', html_content, re.I)
    for img_tag in hero_imgs:
        if ".png" in img_tag.lower() or ".jpg" in img_tag.lower():
            if "<picture" not in html_content:
                issues.append({
                    "severity": "HIGH",
                    "rule": "unoptimized-hero-image-format",
                    "message": f"Hero image uses legacy format: {img_tag[:60]}..."
                })
                recommendations.append("Convert hero image to WebP/AVIF and wrap with a <picture> fallback element.")
                
    # 4. Check for CSS animation delays on hero element
    if css_path and css_path.exists():
        css_content = css_path.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'#hero[^{]*\{[^}]*opacity:\s*0', css_content, re.I):
            issues.append({
                "severity": "HIGH",
                "rule": "render-delay-hero-opacity-zero",
                "message": "Hero element has 'opacity: 0' in stylesheet, causing artificial LCP render delay."
            })
            recommendations.append("Set '#hero .ai { opacity: 1 !important; transform: none !important; }' to render LCP candidate immediately.")
            
    result = {
        "status": "FAIL" if any(i["severity"] == "HIGH" for i in issues) else "PASS",
        "html_file": str(html_path),
        "total_issues": len(issues),
        "issues": issues,
        "recommendations": recommendations
    }
    
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Audit completed. Results saved to: {out_path}")


def cmd_convert_images(args):
    """Convert an image to WebP format using Pillow."""
    try:
        from PIL import Image
    except ImportError:
        sys.stderr.write("Error: Pillow is required for image conversion. Run with 'uv run --with pillow'.\n")
        sys.exit(1)
        
    in_path = Path(args.input)
    out_path = Path(args.output)
    
    if not in_path.exists():
        sys.stderr.write(f"Error: Input image '{in_path}' does not exist.\n")
        sys.exit(1)
        
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    with Image.open(in_path) as img:
        orig_size = in_path.stat().st_size
        img.save(out_path, format="WEBP", quality=args.quality, method=6)
        new_size = out_path.stat().st_size
        
    savings_pct = round((1.0 - (new_size / orig_size)) * 100, 2)
    
    result = {
        "input_file": str(in_path),
        "output_file": str(out_path),
        "original_bytes": orig_size,
        "optimized_bytes": new_size,
        "savings_percent": f"{savings_pct}%",
        "width": img.width,
        "height": img.height
    }
    
    log_path = out_path.with_suffix(".meta.json")
    log_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Converted {in_path.name} to {out_path.name} ({orig_size}B -> {new_size}B, {savings_pct}% reduction).")


def cmd_inject_preload(args):
    """Inject high-priority WebP preload tag into HTML head."""
    html_path = Path(args.html)
    if not html_path.exists():
        sys.stderr.write(f"Error: HTML file '{html_path}' does not exist.\n")
        sys.exit(1)
        
    content = html_path.read_text(encoding="utf-8")
    img_url = args.image_url
    
    preload_tag = f'  <link rel="preload" as="image" href="{img_url}" type="image/webp" fetchpriority="high">\n'
    
    if preload_tag.strip() in content:
        print(f"Preload tag for {img_url} is already present.")
        return
        
    # Insert right after <head> or before fonts
    if "<head>" in content:
        new_content = content.replace("<head>", f"<head>\n{preload_tag}", 1)
    elif "<head " in content:
        idx = content.find(">") + 1
        new_content = content[:idx] + f"\n{preload_tag}" + content[idx:]
    else:
        sys.stderr.write("Error: Could not locate <head> tag in HTML file.\n")
        sys.exit(1)
        
    out_path = Path(args.output) if args.output else html_path
    out_path.write_text(new_content, encoding="utf-8")
    print(f"Preload tag successfully injected for {img_url}. Saved to: {out_path}")


def cmd_verify(args):
    """Verify DOM integrity and edge cache headers for WebP."""
    html_path = Path(args.html)
    headers_path = Path(args.headers_file) if args.headers_file else None
    
    if not html_path.exists():
        sys.stderr.write(f"Error: HTML file '{html_path}' does not exist.\n")
        sys.exit(1)
        
    html_content = html_path.read_text(encoding="utf-8", errors="ignore")
    checks = []
    
    # Check 1: WebP picture element
    has_picture_webp = "<picture" in html_content and "image/webp" in html_content
    checks.append({
        "check": "picture_webp_tag",
        "passed": has_picture_webp,
        "details": "HTML contains <picture> element referencing WebP source."
    })
    
    # Check 2: High priority preload
    has_high_preload = "fetchpriority=\"high\"" in html_content
    checks.append({
        "check": "fetchpriority_high_preload",
        "passed": has_high_preload,
        "details": "High priority preload tag present in <head>."
    })
    
    # Check 3: Edge headers cache control
    if headers_path and headers_path.exists():
        headers_content = headers_path.read_text(encoding="utf-8", errors="ignore")
        has_webp_header = "/*.webp" in headers_content and "max-age=" in headers_content
        checks.append({
            "check": "edge_webp_cache_header",
            "passed": has_webp_header,
            "details": "_headers contains long-lived public cache directives for /*.webp."
        })
        
    all_passed = all(c["passed"] for c in checks)
    result = {
        "status": "PASS" if all_passed else "FAIL",
        "html_file": str(html_path),
        "checks": checks
    }
    
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    
    if not all_passed:
        sys.stderr.write(f"Verification failed. Details in {out_path}\n")
        sys.exit(1)
        
    print(f"All LCP optimization verification checks passed! Report: {out_path}")


def main():
    parser = argparse.ArgumentParser(
        description="LCP Performance and Core Web Vitals Optimization Tool"
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    
    # Subcommand: audit
    p_audit = subparsers.add_parser("audit", help="Audit HTML & CSS for LCP bottlenecks")
    p_audit.add_argument("--html", required=True, help="Path to input HTML file")
    p_audit.add_argument("--css", required=False, help="Path to stylesheet file")
    p_audit.add_argument("--output", required=True, help="Path to write JSON audit report")
    
    # Subcommand: convert-images
    p_convert = subparsers.add_parser("convert-images", help="Convert image to WebP")
    p_convert.add_argument("--input", required=True, help="Path to source image (PNG/JPG)")
    p_convert.add_argument("--output", required=True, help="Path to target WebP image")
    p_convert.add_argument("--quality", type=int, default=85, help="WebP compression quality (default: 85)")
    
    # Subcommand: inject-preload
    p_preload = subparsers.add_parser("inject-preload", help="Inject high-priority preload tag into HTML")
    p_preload.add_argument("--html", required=True, help="Path to HTML file")
    p_preload.add_argument("--image-url", required=True, help="URL/path of the image to preload")
    p_preload.add_argument("--output", required=False, help="Path to write modified HTML (defaults to overwriting input)")
    
    # Subcommand: verify
    p_verify = subparsers.add_parser("verify", help="Verify LCP best practices and cache headers")
    p_verify.add_argument("--html", required=True, help="Path to HTML file")
    p_verify.add_argument("--headers-file", required=False, help="Path to edge _headers file")
    p_verify.add_argument("--output", required=True, help="Path to write JSON verification report")
    
    args = parser.parse_args()
    
    if args.subcommand == "audit":
        cmd_audit(args)
    elif args.subcommand == "convert-images":
        cmd_convert_images(args)
    elif args.subcommand == "inject-preload":
        cmd_inject_preload(args)
    elif args.subcommand == "verify":
        cmd_verify(args)


if __name__ == "__main__":
    main()
