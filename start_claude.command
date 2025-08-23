#!/bin/bash
cd "$(dirname "$0")"
echo "災害透析マニュアル作業ディレクトリに移動しました"

# 福井大学内LANからの接続かチェック
echo "福井大学内のLANから接続していますか？ (y/n)"
read -r proxy_response

if [[ $proxy_response == "y" || $proxy_response == "Y" ]]; then
    echo "プロキシ設定を適用します..."
    export http_proxy="http://ufproxy.m.cii.u-fukui.ac.jp:8080/"
    export https_proxy="http://ufproxy.m.cii.u-fukui.ac.jp:8080/"
    echo "プロキシが設定されました:"
    echo "  HTTP Proxy: $http_proxy"
    echo "  HTTPS Proxy: $https_proxy"
else
    echo "プロキシ設定をスキップします"
fi

echo "GitHubリポジトリをバックグラウンドで開いています..."
open -g https://github.com/ttoyama/fukuitouseki.com

echo "Claude Codeを起動します..."
claude
exec bash