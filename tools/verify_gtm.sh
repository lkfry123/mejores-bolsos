#!/bin/bash
# GTM Implementation Verification Script
# This script helps verify that GTM is properly implemented across your site

echo "=== GTM Implementation Verification ==="
echo "GTM Container ID: GTM-TCG7SMDD"
echo "GA4 Measurement ID: G-H1Q1KL01RP"
echo ""

# Check for GTM script in head
echo "1. Checking for GTM script in <head> sections..."
GTM_HEAD_COUNT=$(grep -r "googletagmanager.com/gtm.js" --include="*.html" . | wc -l)
echo "   Found GTM script in $GTM_HEAD_COUNT HTML files"

# Check for GTM noscript in body
echo "2. Checking for GTM noscript in <body> sections..."
GTM_NOSCRIPT_COUNT=$(grep -r "googletagmanager.com/ns.html" --include="*.html" . | wc -l)
echo "   Found GTM noscript in $GTM_NOSCRIPT_COUNT HTML files"

# Check for GTM container ID
echo "3. Checking for GTM container ID (GTM-TCG7SMDD)..."
GTM_ID_COUNT=$(grep -r "GTM-TCG7SMDD" --include="*.html" . | wc -l)
echo "   Found GTM container ID in $GTM_ID_COUNT locations"

# Check for any remaining gtag implementations
echo "4. Checking for any remaining gtag implementations..."
GTAG_COUNT=$(grep -r "gtag(" --include="*.html" . | wc -l)
if [ $GTAG_COUNT -eq 0 ]; then
    echo "   ✅ No gtag implementations found (good!)"
else
    echo "   ⚠️  Found $GTAG_COUNT gtag implementations (should be 0)"
fi

# Check for any remaining direct GA4 implementations
echo "5. Checking for any remaining direct GA4 implementations..."
GA4_DIRECT_COUNT=$(grep -r "googletagmanager.com/gtag" --include="*.html" . | wc -l)
if [ $GA4_DIRECT_COUNT -eq 0 ]; then
    echo "   ✅ No direct GA4 implementations found (good!)"
else
    echo "   ⚠️  Found $GA4_DIRECT_COUNT direct GA4 implementations (should be 0)"
fi

# Count total HTML files
echo "6. Total HTML files processed..."
TOTAL_HTML=$(find . -name "*.html" -not -path "./tools/*" -not -name "*.bak_gtmfix" | wc -l)
echo "   Total HTML files: $TOTAL_HTML"

echo ""
echo "=== Summary ==="
echo "✅ GTM script blocks: $GTM_HEAD_COUNT"
echo "✅ GTM noscript blocks: $GTM_NOSCRIPT_COUNT"
echo "✅ GTM container ID references: $GTM_ID_COUNT"
echo "✅ Direct gtag implementations: $GTAG_COUNT (should be 0)"
echo "✅ Direct GA4 implementations: $GA4_DIRECT_COUNT (should be 0)"

echo ""
echo "=== Next Steps ==="
echo "1. Test your site with GTM Preview mode:"
echo "   - Go to https://tagmanager.google.com/"
echo "   - Select your container (GTM-TCG7SMDD)"
echo "   - Click 'Preview' button"
echo "   - Enter your site URL to test"

echo ""
echo "2. Verify GA4 data in Google Analytics:"
echo "   - Go to https://analytics.google.com/"
echo "   - Select your GA4 property (G-H1Q1KL01RP)"
echo "   - Use 'Realtime' reports to see live data"
echo "   - Use 'DebugView' for detailed event tracking"

echo ""
echo "3. Check browser developer tools:"
echo "   - Open browser DevTools (F12)"
echo "   - Go to Console tab"
echo "   - Look for GTM-related messages"
echo "   - Check Network tab for gtm.js requests"

echo ""
echo "4. Test with Google Tag Assistant:"
echo "   - Install Google Tag Assistant Chrome extension"
echo "   - Visit your site and check for GTM container detection"
