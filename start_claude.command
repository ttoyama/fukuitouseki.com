#!/bin/bash
cd "$(dirname "$0")"
echo "災害透析マニュアル作業ディレクトリに移動しました"

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

echo "GitHubリポジトリをバックグラウンドで開いています..."
open -g https://github.com/ttoyama/fukuitouseki.com

echo "Claude Codeを起動します..."
claude --dangerously-skip-permissions
exec bash