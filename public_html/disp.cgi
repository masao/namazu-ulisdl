#!/usr/local/bin/perl -wT

## ULIS-DL のメタデータを表示するための CGI スクリプト。

use strict;
use CGI qw/:standard/;

# メタデータの置き場所
my $PREFIX = '/opt/DLsystem/metadata/ucmetadata/';

# UCMETAの要素名と背景色を設定する
my %ELEMENTS =
    ('Title' => 'タイトル:#ffccff',
     'Creator' => '著者:#ffff99',
     'Subject' => '主題:#ccffff',
     'Description' => '内容記述:#ffe4b5',
     'Publisher' => '公開者:#ccff99',
     'Contributor' => '寄与者:#99cc99',
     'Date' => '日付:#f5f5dc',
     'Type' => 'タイプ:#dcf5dc',
     'Format' => '形式:#dcffcc',
     'Identifier' => '識別子:#ccccff',
     'Source' => '情報源:#ccffcc',
     'Language' => '言語:#ffe4cc',
     'Relation' => '関係:#beccbe',
     'Coverage' => '対象範囲:#bebecc',
     'Rights' => '権利管理:#87ceeb',

     ## ULIS original...
     'Country' => '出版国:#ffffe0',
     'CharCode' => '文字コード:#ebce87'
     );

# 出力する HTML の最初の部分
my $HTML_HEAD = <<EOF;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<title>図書館情報大学・図書館情報学関係メタデータ検索システム</title>
<style type="text/css">
body { background-color: #e8e8e8; }
h1 { text-align: center; }
</style>
</head>
<body>
EOF

# 出力する HTML の最後の部分
my $HTML_FOOT = <<EOF;
<hr>
<a href="javascript:history.back()">戻る</a>
</body></html>
EOF

# ブラウザから送られてくる情報...
my $PATHINFO = path_info() || error("ファイル名がありません");
if ($PATHINFO =~ m#^(/\w+/\d+\.sgm)$#) {
    $PATHINFO = $1;
} else {
    error("ファイル名が不正です: $PATHINFO");
}

main();
sub main {
    my $file = $PREFIX . $PATHINFO;
    error("ファイルがありません。") unless -f $file;
    open(F, $file) || die "open error: $file: $!";

    # output
    print header("text/html; charset=EUC-JP");
    print $HTML_HEAD;
    print "<p><strong>該当メタデータの表示</strong></p>\n";
    print "<table width=\"100%\" border=\"2\">\n";
    while (defined(my $line = <F>)) {
        for my $elem (keys %ELEMENTS) {
	    if ($line =~ m#<$elem[^>]*>(.*)</$elem>#i) {
		my $str = escape_html($1);
		my ($label, $color) = split(/:/, $ELEMENTS{$elem});
		print "<tr><td bgcolor=\"$color\" nowrap>$label</td><td>$str</td></tr>\n";
	    }
	}
    }
    print "</table>\n";
    print $HTML_FOOT;
}

# HTML風に変換
# （元のSGMLがきちんとDTDに沿っていないのを考慮すべし）
sub escape_html($) {
    my ($str) = @_;

    # 読みは除く
    $str =~ s#<transcription>([^<]*)</transcription>##gio;

    $str =~ s/&amp;/&/gio;
    $str =~ s/&lt;/</gio;
    $str =~ s/&gt;/>/gio;
    $str =~ s/&quot;/\"/gio;

    $str =~ s/&/&amp;/go;
    $str =~ s/</&lt;/go;
    $str =~ s/>/&gt;/go;
    $str =~ s/\"/&quot;/go;

    # URLらしき文字列にリンクをはる
    $str =~ s#((https?|ftp)://[;\/?:@&=+\$,A-Za-z0-9\-_.!~*'()]+)#<a href="$1">$1</a>#gi;

    return $str;
}

sub error($) {
    my ($msg) = @_;
    print header("text/html; charset=EUC-JP");
    print $HTML_HEAD;
    print <<EOF;
<h1>Error</h1>
<p>エラー: <strong>$msg</strong></p>
EOF
    print $HTML_FOOT;
    exit;
}
