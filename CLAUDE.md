# CLAUDE.md

このファイルは、このリポジトリでClaude Code (claude.ai/code) が作業する際のガイダンスを提供します。

## プロジェクト概要

これは福井県の透析患者向け災害対応マニュアルのJekyllベースのウェブサイトです。透析患者、その家族、医療従事者向けの包括的な災害準備・対応ガイダンスを提供するよう設計されています。

## サイト構造とコンテンツ

プロジェクトは日本語コンテンツを含むJekyll静的サイトとして構成されています：

- **メインサイト**: `/fukuitouseki.com/` - Jekyllサイトルート
- **ドキュメント**: `/fukuitouseki.com/docs/` - 時系列に整理されたマニュアルコンテンツ:
  - `01-各施設の役割と対応.md` - 各施設の災害対応（平時の準備から復旧まで）
  - `02-福井県透析施設ネットワークの役割と対応.md` - ネットワーク調整（平時の準備から復旧まで）
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

### ネットワーク設定（福井大学内LAN）

福井大学内LANから接続する場合、以下のプロキシ設定が必要です：

```bash
# 福井大学内LANからの接続の場合のみプロキシを適用
if [[ $(hostname) == *"u-fukui.ac.jp" ]]; then
    export http_proxy="http://ufproxy.m.cii.u-fukui.ac.jp:8080/"
    export https_proxy="http://ufproxy.m.cii.u-fukui.ac.jp:8080/"
    echo "福井大学内LANから接続中: プロキシを設定しました"
    echo "  HTTP Proxy: $http_proxy"
    echo "  HTTPS Proxy: $https_proxy"
else
    echo "大学外からの接続: プロキシ設定をスキップします"
fi
```

このスクリプトにより：
- 福井大学内のホスト名（`*u-fukui.ac.jp`）を検出した場合のみプロキシを設定
- Git操作やWebアクセスが大学のファイアウォールを通過可能
- 大学外からの接続時は不要なプロキシ設定を回避
- 手動での接続確認（y/n）が不要で自動判定

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
   - **問題**: YAMLフロントマターなしで直接コンテンツで始まるMarkdownファイル（例：`# 平時の準備`）
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

## Git管理とPDF生成ワークフロー

### 自動PDF生成の仕組み

このプロジェクトは **GitHub Actions** による自動PDF生成ワークフローを採用しています：

1. **トリガー**: `main`ブランチへのpushで自動実行
2. **処理内容**: 
   - Markdownファイルを結合
   - PandocでPDF生成（XeLaTeX + 日本語フォント対応）
   - 生成されたPDFを `booklet-pdf/fukuitouseki_booklet.pdf` に配置
   - 自動コミット・プッシュでリポジトリに反映

### コミット・プッシュのタイミング

**重要**: マニュアル内容を修正した場合は、以下のワークフローに従ってください：

#### 1. 作業完了後の必須手順
```bash
# 変更状況を確認
git status

# 最新版を取得（PDF更新を反映）
git pull

# 変更をステージング
git add .

# 日本語で意味のあるコミットメッセージでコミット
git commit -m "マニュアル修正内容の概要

詳細な変更内容
- 具体的な修正点1
- 具体的な修正点2

🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>"

# リモートにプッシュ
git push
```

#### 2. PDF生成の確認
- プッシュ後、GitHub Actionsが自動実行される（約2-3分）
- 生成されたPDFは次回 `git pull` で取得可能
- GitHub ActionsのStatusは[Actions タブ](https://github.com/ttoyama/fukuitouseki.com/actions)で確認

#### 3. 作業のベストプラクティス

**必ずプッシュする場面**：
- マニュアル内容の修正・追加が完了した時
- 新しい章や節を追加した時
- 重要な構造変更を行った時
- 作業セッション終了時

**プッシュのメリット**：
- 最新PDFが自動生成され、常に内容が同期される
- 他の協力者が最新版にアクセス可能
- バージョン履歴が適切に管理される
- GitHub Pagesでの公開内容が最新化される

#### 4. トラブルシューティング

**PDF生成が失敗した場合**：
1. GitHub Actionsログを確認
2. YAMLフロントマターの構文エラーをチェック
3. 日本語ファイル名の引用符漏れを確認
4. Pandoc互換性問題の対処（上記「よくあるPandoc + YAML問題」参照）

**コンフリクトが発生した場合**：
```bash
# 最新版を強制取得してマージ
git pull --rebase
# または
git pull --no-rebase
```

## PDF版のバージョン管理とアーカイブ化

### 自動PDF生成ファイル名の規則

GitHub ActionsによるPDF生成では、以下の命名規則を採用しています：

#### ファイル名の形式

- **基本形式**: `fukuitouseki_booklet_YYYYMMDD_HHMM.pdf`
- **例**: `fukuitouseki_booklet_20250902_0617.pdf`
- **同一時刻重複時**: `fukuitouseki_booklet_YYYYMMDD_HHMM-2.pdf`

#### タイムゾーンとバージョン管理

- **タイムゾーン**: JST（Asia/Tokyo）を使用
- **時刻形式**: 24時間形式（HHMM）
- **重複対応**: 同一時刻に複数回生成された場合は末尾に連番（-2, -3, ...）を追加

### PDFアーカイブ管理の実践

#### booklet-pdf/直下の管理方針

**重要**: `booklet-pdf/`直下には常に最新版のPDFファイル1つのみを配置します：

```bash
# 最新状態の確認
ls -la booklet-pdf/

# 期待される構成:
booklet-pdf/
├── archived/           # 古いバージョンのアーカイブ
└── fukuitouseki_booklet_YYYYMMDD_HHMM.pdf  # 最新版のみ

# 古いファイルが存在する場合の整理手順:
mv booklet-pdf/fukuitouseki_booklet_古い日時.pdf booklet-pdf/archived/
git add . && git commit -m "PDF版のアーカイブ化: 古いバージョンの整理"
```

#### pull後の自動整理

`git pull`で最新PDFを取得した後は必ず以下を実行：

1. **booklet-pdf/の内容確認**
2. **最新版以外をarchived/に移動**
3. **LaTeX中間ファイルの削除**（.dvi、.aux、.log）
4. **変更をコミット・プッシュ**

### アーカイブ化方針

重要な改訂があった際の履歴保持のために以下のアーカイブ化方針を採用します：

#### アーカイブ化の実施タイミング

以下のような重要な変更時にPDFをアーカイブ化します：

1. **大規模な構造変更**（例：双方向対応化のような全面改訂）
2. **新しい章・節の追加**
3. **内容の大幅な更新**（30%以上の変更）
4. **制度・法令の変更に伴う修正**
5. **年度更新時**

#### アーカイブ化の手順

重要な改訂完了後、以下の手順でPDFをアーカイブ化します：

```bash
# 1. 最新のPDFが生成されるまで待機（GitHub Actions完了後）
git pull

# 2. アーカイブディレクトリの作成（まだ存在しない場合）
mkdir -p booklet-pdf/archived

# 3. 重要版のアーカイブ化（日時付きファイル名から識別しやすい名前に）
cp "booklet-pdf/fukuitouseki_booklet_$(date +%Y%m%d_)*.pdf" "booklet-pdf/archived/fukuitouseki_booklet_$(date +%Y%m%d)_重要版.pdf"

# 4. アーカイブをコミット
git add "booklet-pdf/archived/fukuitouseki_booklet_$(date +%Y%m%d)_重要版.pdf"
git commit -m "PDF版をアーカイブ化: $(date +%Y%m%d) 重要版

主要変更内容:
- 変更内容の概要を記載

🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>"

# 5. プッシュ
git push
```

#### アーカイブファイルの命名規則

- **基本形式**: `fukuitouseki_booklet_YYYYMMDD.pdf`
- **例**: `fukuitouseki_booklet_20250901.pdf`
- **特別版**: 大きな改訂の場合は `fukuitouseki_booklet_YYYYMMDD_改訂内容.pdf`
  - 例: `fukuitouseki_booklet_20250901_双方向対応版.pdf`

#### アーカイブ管理の考慮事項

- **ファイルサイズ**: PDFファイルはサイズが大きいため、過度なアーカイブ化は避ける
- **保持期間**: 直近3-5版程度を保持し、古いバージョンは適宜削除
- **リリースノート**: 各アーカイブ版の変更内容をREADMEまたはCHANGELOGに記録
- **GitHub Releases**: 重要なマイルストーンではGitHub Releasesとしてタグ付けも検討

### 現在のアーカイブ状況

**双方向対応版（2025年9月1日）**: 次回のGitHub Actions完了後にアーカイブ化予定
- 主要変更: 被災地・支援地双方向対応構造の導入
- ファイルサイズ: 約90%増（188行→356行）

## 文書構造ガイドライン

### セクションレベル制限

**重要**: 本プロジェクトの全Markdownファイルは、セクションレベルを3つまでに制限します：

- **レベル1 (`#`)**: メインタイトル
- **レベル2 (`##`)**: 主要セクション
- **レベル3 (`###`)**: サブセクション
- **レベル4以下 (`####`, `#####`, `######`)**: **使用禁止**

#### 制限理由

1. **PDF生成時の見出し階層**：目次の深さが適切に制御される
2. **文書の可読性**：階層が深くなりすぎると読みにくくなる
3. **構造の一貫性**：全文書で統一された構造を維持

#### 構造見直しの方法

レベル4の項目がある場合は、以下のいずれかで対応：

1. **統合**: 上位レベルの項目に統合する
2. **昇格**: より重要な項目はレベル3に昇格させる
3. **箇条書き**: 詳細項目は箇条書きや**太字**で強調表示に変更

#### 実践的な修正例

**修正前（レベル4使用）:**
```markdown
### 施設設備の定期点検

#### 施設及び設備の定期的な自己点検
各施設で作成されたマニュアルに基づき...

#### ライフラインの点検と確保
- 医療機関の維持に必要な透析機器...

#### 透析装置等の転倒防止対策
- 透析液作成装置は、転倒、移動...
```

**修正後（レベル3以下）:**
```markdown
### 施設設備の定期点検

**定期点検の基本方針**

各施設で作成されたマニュアルに基づき、施設及び設備の定期的な自己点検を実施します。

**ライフラインの点検と確保**
- 医療機関の維持に必要な透析機器、電気、水道、燃料などの施設・設備の点検を平常時から定期的に実施します。
- 水道事務所や電力会社等の担当部門と相談し、透析用の水、電力等の確保の方法を確認しておきます。

**透析装置等の転倒防止対策**
- 透析液作成装置は、転倒、移動、揺れによる損傷を防止するために、床面にアンカーボルト等でしっかり固定します。
- 施設の構造（耐震/免振）に応じた適切なキャスター設定を行います。
```

#### 修正時の注意事項

1. **内容の論理的整理**: 関連する複数の4レベル項目は1つの太字見出しにまとめる
2. **重要度による選別**: 本当に重要な項目のみレベル3に昇格、その他は太字や箇条書きに
3. **読みやすさの維持**: 太字見出しと箇条書きを効果的に組み合わせて構造を明確化
4. **一貫性の確保**: 全文書で同じ修正方針を適用する

### PDF生成のバージョン管理

すべてのPDF生成は日付+連番形式で管理されます：

#### 基本ルール

**常に日付-連番形式**：
1. **初回生成**: `fukuitouseki_booklet_YYYYMMDD-1.pdf`
2. **同日2回目**: `fukuitouseki_booklet_YYYYMMDD-2.pdf`
3. **同日3回目以降**: `fukuitouseki_booklet_YYYYMMDD-3.pdf` (連番で継続)

#### GitHub Actions の動作

- GitHub ActionsはUTC時間でYYYYMMDD日付を生成
- 既存の同日版があれば自動的に連番を増やす
- 毎回必ず `-1`, `-2`, `-3`... の連番が付く

#### アーカイブ化の方針

重要な改訂時のアーカイブ化：

```bash
# 最新版以外をarchivedフォルダに移動
mv booklet-pdf/fukuitouseki_booklet_YYYYMMDD-1.pdf booklet-pdf/archived/
mv booklet-pdf/fukuitouseki_booklet_YYYYMMDD-2.pdf booklet-pdf/archived/

# 最新版のみルートに残す
# 例: fukuitouseki_booklet_20250902-3.pdf が最新版として残る

git commit -m "PDF版のアーカイブ化: YYYYMMDD-X 版

アーカイブした版:
- YYYYMMDD-1: 概要
- YYYYMMDD-2: 概要

🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>"
```

#### 利点

- **一貫性**: すべてのPDFが同じ命名規則
- **追跡性**: 連番でバージョン履歴が明確
- **自動化**: GitHub Actionsが自動的に適切な連番を生成

## LaTeX様式ファイルとローカルコンパイル

### 災害透析チェックシート様式集

本プロジェクトには、災害時透析医療対応のためのチェックシート様式がLaTeX形式で含まれています。

#### フォルダ構成

```
docs/資料/様式/
├── 211_施設設備点検チェックシート/
├── 212_備蓄物資点検チェックシート/
├── 214_患者緊急連絡先チェックシート/
├── 221_患者安全・スタッフ安否チェックシート/
├── 222_施設設備点検チェックシート/
├── 223_交通アクセス状況チェックシート/
├── 252_透析実施困難施設対応チェックシート/  # 詳細設計完了
├── 253_物資薬剤管理チェックシート/
├── 311_被災地情報集約チェックシート/
├── 321_初動調整チェックシート/
├── 322_緊急搬送調整チェックシート/
├── 324_支援準備状況チェックシート/
├── 325_患者受入調整チェックシート/
├── 351_患者搬送調整チェックシート/
├── 361_二次避難計画チェックシート/
├── 363_二次避難患者受入チェックシート/
└── README.md
```

#### LaTeXコンパイル環境

**必要な環境:**
- LaTeX（日本語対応：platex推奨）
- dvipdfmx（PDF変換用）
- 必要パッケージ：geometry, array, longtable, amssymb, multirow, booktabs

**コンパイル手順:**

```bash
# 個別チェックシートのコンパイル
cd "docs/資料/様式/252_透析実施困難施設対応チェックシート"

# LaTeXコンパイル（platex推奨、uplatexは文字化けの可能性）
platex "透析実施困難施設対応チェックシート.tex"

# PDF変換
dvipdfmx "透析実施困難施設対応チェックシート.dvi"

# または、Makefileを使用
make
# または
make test
```

**注意事項:**
- **文字エンコーディング**: ファイルはUTF-8で保存
- **日本語LaTeX**: `platex` + `dvipdfmx` の組み合わせを推奨
- **uplatex問題**: `uplatex`では日本語フォント設定でエラーが発生する場合があるため、`platex`を使用
- **出力**: A4サイズ、手書き記入用レイアウト

#### 完成済みチェックシート

**252_透析実施困難施設対応チェックシート** は完全に実装済み：

- **患者安否確認と病態把握**: 10名分の記録欄、緊急度評価
- **搬送先施設の選定**: ネットワーク情報確認、受入可能施設リスト
- **搬送手段の確保**: 搬送手段選択、関係機関連絡記録
- **情報伝達**: 患者情報伝達詳細チェック
- **家族への説明・同意記録**: 説明内容と同意確認

このチェックシートは5ページのPDFとして生成され、災害時の現場で実際に使用可能な形式で設計されています。

## ファイルアーカイブ化方針

### docsフォルダ内の古いファイル管理

**重要**: docsフォルダ以下で古いバージョンのファイルが生成された場合は、以下の方針でアーカイブ化します：

#### アーカイブ化の対象

1. **LaTeX様式ファイル**: 旧版のPDFのみ（dvi、aux、log等の中間ファイルは不要）
2. **Markdownファイル**: 構造変更前の旧版、ドラフト版
3. **参考資料**: 更新された資料の旧版
4. **テンプレートファイル**: 改訂前の様式テンプレート

#### アーカイブ化の手順

```bash
# 1. docs/archivedディレクトリの作成
mkdir -p docs/archived

# 2. 古いファイルの移動（PDFのみアーカイブ、LaTeX中間ファイルは削除）
mv "docs/資料/様式/古いファイル.pdf" "docs/archived/"
mv "docs/古いmarkdownファイル.md" "docs/archived/"
# LaTeX中間ファイルは削除（アーカイブしない）
rm -f "docs/資料/様式/"*.dvi "docs/資料/様式/"*.aux "docs/資料/様式/"*.log

# 3. アーカイブをコミット
git add docs/archived/
git commit -m "古いファイルをアーカイブ化: ファイル名

移動したファイル:
- 具体的なファイル名と理由

🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>"

git push
```

#### アーカイブ化のタイミング

- **新版完成時**: 新しいバージョンが完成し、検証が完了した時点で旧版をアーカイブ
- **構造変更時**: フォルダ構成や命名規則が変更された場合
- **定期整理**: 月次または重要なマイルストーン時の整理作業
- **容量削減**: リポジトリサイズが大きくなった場合

#### アーカイブファイルの命名

- **基本形式**: `元のファイル名_YYYYMMDD_旧版.拡張子`
- **例**: `透析実施困難施設対応チェックシート_20250903_旧版.pdf`
- **説明付き**: 必要に応じて変更理由を含める
  - 例: `マニュアル構成_20250901_レベル4廃止前.md`