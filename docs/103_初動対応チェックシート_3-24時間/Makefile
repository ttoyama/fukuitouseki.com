# Makefile for 初動対応チェックシート_3-24時間

TEX_FILE = 初動対応チェックシート_3-24時間_20250904.tex
DVI_FILE = 初動対応チェックシート_3-24時間_20250904.dvi
PDF_FILE = 初動対応チェックシート_3-24時間_20250904.pdf

# デフォルトターゲット
all: $(PDF_FILE)

# PDFファイル生成
$(PDF_FILE): $(DVI_FILE)
	dvipdfmx $(DVI_FILE)

# DVIファイル生成
$(DVI_FILE): $(TEX_FILE)
	platex $(TEX_FILE)

# テスト用（コンパイル確認）
test: $(PDF_FILE)
	@echo "PDF生成完了: $(PDF_FILE)"

# クリーンアップ
clean:
	rm -f *.aux *.log *.dvi *.pdf

# 中間ファイルのみ削除
clean-temp:
	rm -f *.aux *.log *.dvi

.PHONY: all test clean clean-temp