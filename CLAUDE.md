# CLAUDE.md

このファイルは、このリポジトリでClaude Code (claude.ai/code) が作業する際のガイダンスを提供します。

## プロジェクト概要

これは福井県の透析患者向け災害対応マニュアルのJekyllベースのウェブサイトです。透析患者、その家族、医療従事者向けの包括的な災害準備・対応ガイダンスを提供するよう設計されています。

## サイト構造とコンテンツ

プロジェクトは日本語コンテンツを含むJekyll静的サイトとして構成されています：

- **メインサイト**: `/fukuitouseki.com/` - Jekyllサイトルート
- **ドキュメント**: `/fukuitouseki.com/docs/` - 段階別に整理されたマニュアルコンテンツ:
  - `00-平時の準備.md` - 災害前の準備
  - `01-初動対応.md` - 初期災害対応  
  - `02-施設別対応.md` - 施設別対応
  - `03-ネットワーク調整.md` - ネットワーク調整
  - `index.md` - マニュアル目次
- **参考資料**: `/references/` - 他県からの参考資料

## Jekyll設定

サイトは以下の主要設定でJekyllを使用しています：
- **テーマ**: minima
- **言語**: 日本語 (ja)
- **タイムゾーン**: Asia/Tokyo
- **プラグイン**: jekyll-feed, jekyll-sitemap
- **Markdown**: kramdown with rouge highlighter

## Claude Code設定

このプロジェクトでは**Claude Sonnet**をデフォルトモデルとして使用します：

```bash
# デフォルトモデルをSonnetに設定
/model sonnet
```

理由：
- 日本語コンテンツの高品質な編集・翻訳能力
- 医療・災害対応という専門分野での正確性
- 長文マニュアルの一貫性維持
- PDF生成ワークフローとの統合における安定性

## 開発コマンド

Jekyllサイトのため、一般的なコマンドは：
```bash
# 依存関係をインストール（Gemfileが存在する場合）
bundle install

# ローカルサーバー起動
bundle exec jekyll serve

# サイトビルド
bundle exec jekyll build
```

注：現在のリポジトリ構造にはGemfileが見つからないため、ローカル開発が必要な場合はJekyllのセットアップが必要かもしれません。

## コンテンツガイドライン

- 全コンテンツは日本語
- 透析患者の災害準備に焦点
- 段階別対応構造（0-3段階）で整理
- 対象読者には医療従事者、患者、家族、管理者を含む
- コンテンツは災害シナリオで実用的で行動可能であること

## コミュニケーションガイドライン

この日本語災害対応マニュアルリポジトリで作業する際：

- **言語**: ユーザーの入力が英語か日本語かに関わらず、常に日本語で応答する
- **コミットメッセージ**: 日本語コンテンツ、テンプレート、ドキュメントを追加・修正する際は、コミットメッセージとコメントを日本語で書く
- **例**: "Add initial response templates" ではなく "初動対応用の様式テンプレートを追加" を使用
- **理由**: これは日本の医療従事者向けの日本語災害対応マニュアルであるため、すべてのコミュニケーションを日本語で行うことで、対象読者により良いコンテキストとアクセシビリティを提供する

## ファイルの場所

- サイト設定: `fukuitouseki.com/_config.yml`
- メインコンテンツ: `fukuitouseki.com/docs/*.md`
- サイトインデックス: `fukuitouseki.com/index.md`
- プロジェクト概要: `fukuitouseki.com/README.md`

## PandocによるPDF生成

このリポジトリには、GitHub Actions（`.github/workflows/booklet.yml`）による自動PDF生成が含まれています。将来のメンテナンスのために考慮すべき学習事項は以下の通りです：

### よくあるPandoc + YAML問題と解決策

**以前のPDF生成失敗の根本原因：**

1. **YAMLフロントマターの競合**
   - **問題**: 個別のYAMLフロントマターを持つ複数のMarkdownファイルをPandocで結合する際の競合
   - **エラー**: `YAML parse exception at line 1, column 9: did not find expected <document start>`
   - **解決策**: 個別のYAMLフロントマターを削除し、統一されたYAMLヘッダーを使用

2. **YAMLフロントマターの不足**
   - **問題**: YAMLフロントマターなしで直接コンテンツで始まるMarkdownファイル（例：`# 第0段階：平時の準備`）
   - **Pandocの動作**: 最初の行を不正なYAMLとして解釈
   - **解決策**: すべてのファイルに適切なYAMLフロントマターを追加：
     ```yaml
     ---
     title: "ドキュメントタイトル"
     ---
     ```

3. **コマンドラインでの日本語ファイル名**
   - **問題**: `docs/00-平時の準備.md` のようなファイルがシェルコマンドで正しく処理されない場合
   - **解決策**: 常にファイル名を引用符で囲む：`"docs/00-平時の準備.md"`

4. **xargs互換性問題**
   - **問題**: 複数ファイルでの`xargs -0 pandoc`コマンド解析問題
   - **解決策**: 明示的なファイルリストまたはファイル結合アプローチで直接pandocコマンドを使用

### 動作するPDF生成アプローチ

現在の成功している方法は、Pandoc処理前にファイルを結合します：

```bash
# 統一YAMLヘッダーの作成
echo "---" > combined.md
echo "title: 災害時透析医療オペレーション手引き" >> combined.md
echo "author: 福井透析ネットワーク本部" >> combined.md
echo "lang: ja" >> combined.md
echo "CJKmainfont: 'Noto Sans CJK JP'" >> combined.md
# ... 追加メタデータ

# ファイルの結合、個別YAMLフロントマターを削除
for file in [ファイルリスト]; do
  echo "\\newpage" >> combined.md
  sed '1,/^---$/d; /^---$/,/^---$/d' "$file" >> combined.md
done

# 結合されたファイルからPDF生成
pandoc combined.md --pdf-engine=xelatex --toc --number-sections -o output.pdf
```

### PDF生成のファイル要件

PDF生成に含まれる予定のすべてのMarkdownファイルには以下が必要：
- `---`区切り文字による適切なYAMLフロントマター
- 日本語コンテンツ用のUTF-8エンコーディング
- 目次生成のための一貫した見出し構造

### 日本語コンテンツのフォント設定

- **エンジン**: XeLaTeX（CJKフォントサポートに必要）
- **フォント**: `CJKmainfont: 'Noto Sans CJK JP'`（GitHub Actions Ubuntuで利用可能）
- **言語**: 適切なドキュメント書式設定のための`lang: ja`