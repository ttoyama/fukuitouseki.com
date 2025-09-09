#!/bin/bash
# 福井県透析防災マニュアル PDF生成用引き金スクリプト

echo "📚 福井県透析防災マニュアル PDF生成開始..."
echo ""

# メインの自動化スクリプトを実行
./sh/update_date_and_generate_pdf.sh

echo ""
echo "🎯 PDFファイルは booklet-pdf/ フォルダにあります"
echo "💡 使い方: QMDファイルを編集後、./make_pdf.sh を実行するだけ！"