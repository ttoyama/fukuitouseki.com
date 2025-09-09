#!/bin/bash

# 動的QMD統合スクリプト
# docs/内の全QMDファイルを統合してcombined.mdを生成

echo "🔄 QMDファイルから動的にcombined.mdを生成中..."

# 1. ヘッダー設定を_quarto_booklet.ymlから読み込み
if [ -f "_quarto_booklet.yml" ]; then
    cat "_quarto_booklet.yml" > combined.md
    echo "✅ ヘッダー設定を_quarto_booklet.ymlから読み込み完了"
else
    echo "❌ エラー: _quarto_booklet.ymlが見つかりません"
    exit 1
fi

# 2. 改ページを追加
echo "" >> combined.md
echo "\\newpage" >> combined.md
echo "" >> combined.md

# 3. docs/内の全QMDファイルを順次統合
QMD_COUNT=0
find docs/ -name "*.qmd" -type f | sort | while read file; do
    echo "📄 統合中: $file"
    echo "" >> combined.md
    echo "<!-- ファイル: $file -->" >> combined.md
    
    # ファイル名からヘッダー更新コマンドを生成
    BASENAME=$(basename "$file" .qmd)
    echo "\\updateheader{$BASENAME}" >> combined.md
    echo "" >> combined.md
    
    # YAMLフロントマターを除去してコンテンツを追加
    # HTMLタグも除去してPandoc+LaTeX互換性を向上
    awk '/^---$/{if(++count==2) skip=0; else skip=1; next} !skip' "$file" | \
    sed 's/<table>/\n| | | |\n|---|---|---|\n/g' | \
    sed 's/<\/table>//g' | \
    sed 's/<tr>//g' | \
    sed 's/<\/tr>//g' | \
    sed 's/<td[^>]*>//g' | \
    sed 's/<\/td>/ | /g' | \
    sed 's/<strong>/\*\*/g' | \
    sed 's/<\/strong>/\*\*/g' | \
    sed 's/<br>/  \n/g' | \
    sed 's/<img[^>]*>//g' | \
    sed 's/<small>/\*(/g' | \
    sed 's/<\/small>/)\*/g' | \
    sed 's/<[^>]*>//g' | \
    sed 's/\[\*\*\([^]]*\)\*\*\]/[\1]/g' | \
    sed 's/\*\*\([^*]*\)\*\*$/\*\*\1\*\* /g' >> combined.md
    
    # 次のファイルとの境界に改ページを挿入
    echo "" >> combined.md
    echo "\\newpage" >> combined.md
    echo "" >> combined.md
    
    QMD_COUNT=$((QMD_COUNT + 1))
done

echo "✅ 統合完了: ${QMD_COUNT}個のQMDファイルをcombined.mdに統合"
echo "📊 combined.md行数: $(wc -l < combined.md)行"
echo "🎯 combined.mdの生成が完了しました"