#!/usr/bin/env python3
"""
LaTeX to Quarto Converter for Disaster Dialysis Checklists
災害透析チェックシートのLaTeXファイルをQuarto形式(.qmd)に変換するスクリプト

Usage:
    python tex_to_quarto_converter.py
"""

import os
import re
import glob
from pathlib import Path
from datetime import datetime

class TexToQuartoConverter:
    def __init__(self):
        self.docs_dir = Path("docs")
        
    def find_tex_directories(self):
        """LaTeXファイルが含まれるディレクトリを検索"""
        tex_dirs = []
        for tex_file in self.docs_dir.glob("**/*.tex"):
            if tex_file.parent not in tex_dirs:
                tex_dirs.append(tex_file.parent)
        return sorted(tex_dirs)
    
    def extract_header_info(self, tex_content):
        """LaTeXファイルからヘッダー情報を抽出"""
        # ヘッダー情報のパターンマッチング
        header_pattern = r'\\def\\@oddhead\{\\hfill\\small\s+(\d+)\s+(.+?)\s+(.+?)版\}'
        match = re.search(header_pattern, tex_content)
        
        if match:
            number = match.group(1)
            title = match.group(2)
            version = match.group(3)
            return number, title, version
        
        # フォールバック: ファイル名から推測
        return None, None, None
    
    def extract_document_title(self, tex_content):
        """文書タイトルを抽出"""
        # \\Large\\textbf{...} パターンを検索
        title_pattern = r'\\Large\\textbf\{([^}]+)\}'
        match = re.search(title_pattern, tex_content)
        
        if match:
            return match.group(1)
        return None
    
    def convert_latex_commands(self, content):
        """LaTeX特有のコマンドをQuarto形式に変換"""
        
        # セクション変換
        content = re.sub(r'\\section\*\{([^}]+)\}', r'## \1', content)
        content = re.sub(r'\\subsection\*\{([^}]+)\}', r'### \1', content)
        content = re.sub(r'\\subsubsection\*\{([^}]+)\}', r'#### \1', content)
        
        # LaTeXコマンドを維持（Quartoでカスタムコマンドとして使用）
        # チェックボックスコマンドはそのまま維持
        
        # 改ページ
        content = re.sub(r'\\newpage', r'\n\\newpage\n', content)
        
        # 垂直スペース
        content = re.sub(r'\\vspace\{[^}]+\}', r'', content)
        
        # テキスト装飾
        content = re.sub(r'\\textbf\{([^}]+)\}', r'**\1**', content)
        
        # noindent削除
        content = re.sub(r'\\noindent\s*', '', content)
        
        # begin/end center環境
        content = re.sub(r'\\begin\{center\}', '', content)
        content = re.sub(r'\\end\{center\}', '', content)
        
        # quad spacing
        content = re.sub(r'\\quad', '    ', content)
        
        return content
    
    def extract_body_content(self, tex_content):
        """LaTeX文書のbody部分を抽出"""
        # \begin{document} から \end{document} までを抽出
        begin_match = re.search(r'\\begin\{document\}', tex_content)
        end_match = re.search(r'\\end\{document\}', tex_content)
        
        if begin_match and end_match:
            body = tex_content[begin_match.end():end_match.start()]
            return body.strip()
        
        return tex_content
    
    def create_yaml_header(self, number, title, version, filename):
        """Quartoのヤマルフロントマターを生成"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # ファイル名からフォルダ番号とタイトルを推測（フォールバック）
        if not number or not title:
            folder_name = Path(filename).parent.name
            if '_' in folder_name:
                parts = folder_name.split('_', 1)
                number = number or parts[0]
                title = title or parts[1] if len(parts) > 1 else folder_name
        
        yaml_header = f"""---
title: "{title or '災害透析チェックシート'}"
subtitle: "{number or ''} {title or ''}"
date: "{current_date}"
format: 
  html:
    toc: true
    toc-depth: 3
    number-sections: true
    css: custom.css
  pdf:
    documentclass: jarticle
    geometry: 
      - top=30mm
      - bottom=30mm  
      - left=20mm
      - right=20mm
      - footskip=18mm
      - headsep=12mm
    include-in-header:
      - text: |
          \\usepackage{{setspace}}
          \\setstretch{{1.3}}
          \\usepackage{{array}}
          \\usepackage{{longtable}}
          \\usepackage{{amssymb}}
          \\usepackage{{multirow}}
          \\usepackage{{booktabs}}
          \\newcommand{{\\checkbox}}{{$\\square$\\ }}
          \\newcommand{{\\checkedbox}}{{$\\blacksquare$\\ }}
          \\newcommand{{\\underlinespace}}[1]{{\\underline{{\\hspace{{#1}}}}}}
          \\newcommand{{\\circlecheck}}{{$\\bigcirc$\\ }}
lang: ja
version: "{version or current_date}版"
header-right: "{number or ''} {title or ''} {version or current_date}版"
---
"""
        return yaml_header
    
    def convert_tex_file(self, tex_file_path):
        """単一のLaTeXファイルをQuartoに変換"""
        with open(tex_file_path, 'r', encoding='utf-8') as f:
            tex_content = f.read()
        
        # ヘッダー情報を抽出
        number, title, version = self.extract_header_info(tex_content)
        doc_title = self.extract_document_title(tex_content)
        
        # 文書タイトルを使用（利用可能な場合）
        if doc_title:
            title = doc_title
        
        # body部分を抽出
        body_content = self.extract_body_content(tex_content)
        
        # LaTeXコマンドを変換
        converted_content = self.convert_latex_commands(body_content)
        
        # YAMLヘッダーを作成
        yaml_header = self.create_yaml_header(number, title, version, tex_file_path)
        
        # 完全なQuartoファイルを構成
        quarto_content = yaml_header + "\n" + converted_content
        
        return quarto_content
    
    def convert_directory(self, dir_path):
        """ディレクトリ内のLaTeXファイルをすべて変換"""
        tex_files = list(dir_path.glob("*.tex"))
        
        if not tex_files:
            print(f"警告: {dir_path} にLaTeXファイルが見つかりません")
            return
        
        print(f"変換中: {dir_path} ({len(tex_files)}個のファイル)")
        
        # 各LaTeXファイルを変換
        for tex_file in tex_files:
            try:
                # 重複ファイル名や日付付きファイルをスキップ
                if "20250904" in tex_file.name or "チェックシートチェックシート" in tex_file.name:
                    print(f"  スキップ: {tex_file.name} (重複または古いバージョン)")
                    continue
                
                quarto_content = self.convert_tex_file(tex_file)
                
                # 出力ファイル名を決定
                qmd_filename = tex_file.stem + ".qmd"
                qmd_path = dir_path / qmd_filename
                
                # Quartoファイルを書き込み
                with open(qmd_path, 'w', encoding='utf-8') as f:
                    f.write(quarto_content)
                
                print(f"  変換完了: {tex_file.name} → {qmd_filename}")
                
            except Exception as e:
                print(f"  エラー: {tex_file.name} の変換に失敗しました: {e}")
        
        # index.qmdファイルを作成
        self.create_index_qmd(dir_path)
    
    def create_index_qmd(self, dir_path):
        """ディレクトリのindex.qmdファイルを作成"""
        folder_name = dir_path.name
        qmd_files = list(dir_path.glob("*.qmd"))
        
        # index.qmdは除外
        qmd_files = [f for f in qmd_files if f.name != "index.qmd"]
        
        if not qmd_files:
            return
        
        # フォルダ名からタイトルを生成
        if '_' in folder_name:
            parts = folder_name.split('_', 1)
            number = parts[0]
            title = parts[1] if len(parts) > 1 else folder_name
        else:
            number = ""
            title = folder_name
        
        index_content = f"""---
title: "{title}"
subtitle: "{number} {title}"
format: 
  html:
    toc: true
    toc-depth: 2
lang: ja
---

# {title}

このセクションには以下のチェックシートが含まれます：

"""
        
        # 各Quartoファイルへのリンクを追加
        for qmd_file in sorted(qmd_files):
            file_title = qmd_file.stem.replace('_', ' ')
            index_content += f"- [{file_title}]({qmd_file.name})\n"
        
        # index.qmdファイルを作成
        index_path = dir_path / "index.qmd"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"  作成完了: index.qmd ({len(qmd_files)}個のファイルをリンク)")
    
    def run_conversion(self):
        """メイン変換プロセスを実行"""
        print("災害透析チェックシート LaTeX→Quarto変換を開始...")
        
        # LaTeXファイルが含まれるディレクトリを検索
        tex_dirs = self.find_tex_directories()
        
        if not tex_dirs:
            print("エラー: LaTeXファイルが見つかりません")
            return
        
        print(f"対象ディレクトリ: {len(tex_dirs)}個")
        
        # 各ディレクトリを変換
        for dir_path in tex_dirs:
            self.convert_directory(dir_path)
        
        print("\n変換完了！")
        print(f"合計 {len(tex_dirs)} 個のディレクトリを処理しました。")
        
        # カスタムCSSファイルを作成
        self.create_custom_css()
    
    def create_custom_css(self):
        """Quartoで使用するカスタムCSSファイルを作成"""
        css_content = """/* 災害透析チェックシート用カスタムCSS */

/* フォームレイアウト */
.form-field {
    margin: 10px 0;
    padding: 5px 0;
}

/* チェックボックス風スタイル */
.checkbox {
    font-family: monospace;
    font-size: 1.2em;
}

/* アンダーラインスペース */
.underline-space {
    border-bottom: 1px solid #000;
    display: inline-block;
    min-width: 100px;
}

/* セクション見出し */
h2 {
    color: #2c5aa0;
    border-bottom: 2px solid #2c5aa0;
    padding-bottom: 5px;
}

h3 {
    color: #5a8bc4;
    margin-top: 20px;
}

/* 印刷用スタイル */
@media print {
    body {
        font-size: 12pt;
        line-height: 1.3;
    }
    
    h1, h2, h3 {
        page-break-after: avoid;
    }
    
    .form-field {
        page-break-inside: avoid;
    }
}
"""
        
        css_path = self.docs_dir / "custom.css"
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print(f"カスタムCSSファイルを作成: {css_path}")

def main():
    """メイン関数"""
    converter = TexToQuartoConverter()
    converter.run_conversion()

if __name__ == "__main__":
    main()