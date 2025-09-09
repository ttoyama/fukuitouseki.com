#!/bin/bash

echo "🚀 完全自動PDF生成を開始します..."

# 1. 既存のcombined.mdを使用（動的統合は一時的に無効化）
echo "📄 Step 1: 既存のcombined.mdを使用中..."
if [ ! -f "combined.md" ]; then
    if [ -f "archived/combined_old_static_version.md" ]; then
        cp "archived/combined_old_static_version.md" "combined.md"
        echo "✅ バックアップから復元しました"
    else
        echo "❌ エラー: combined.mdが見つかりません"
        exit 1
    fi
else
    echo "✅ 既存のcombined.mdを使用します"
fi

# 2. PDF生成
echo "📖 Step 2: PDFを生成中..."
export TZ='Asia/Tokyo'
DATETIME=$(date '+%Y%m%d_%H%M')
PDF_NAME="fukuitouseki_booklet_${DATETIME}.pdf"

pandoc combined.md --pdf-engine=xelatex --toc --toc-depth=2 --number-sections \
  -V linestretch=1.2 -V pagestyle=plain \
  -o "booklet-pdf/${PDF_NAME}"

if [ $? -ne 0 ]; then
    echo "❌ エラー: PDF生成に失敗しました"
    exit 1
fi

# 3. 古いPDFをアーカイブ
echo "📦 Step 3: 古いPDFファイルをアーカイブ中..."
mkdir -p booklet-pdf/archived

# 最新PDF以外をarchivedに移動
ARCHIVED_COUNT=0
find booklet-pdf/ -maxdepth 1 -name "fukuitouseki_booklet_*.pdf" -type f | \
sort -r | tail -n +2 | while read file; do
    mv "$file" booklet-pdf/archived/
    ARCHIVED_COUNT=$((ARCHIVED_COUNT + 1))
done

# 4. 中間ファイルの削除
echo "🗑️  Step 4: 中間生成ファイルを削除中..."
rm -f combined.md

echo ""
echo "✅ 完了！"
echo "📋 生成されたPDF: booklet-pdf/${PDF_NAME}"
if [ -f "booklet-pdf/${PDF_NAME}" ]; then
    echo "📊 PDFサイズ: $(ls -lh "booklet-pdf/${PDF_NAME}" | awk '{print $5}')"
fi
echo "🗂️  古いPDFファイルをarchived/に移動済み"
echo "🧹 中間ファイル（combined.md）を削除済み"