#!/usr/local/bin/perl -wT

## ULIS-DL �Υ᥿�ǡ�����ɽ�����뤿��� CGI ������ץȡ�

use strict;
use CGI qw/:standard/;

# �᥿�ǡ������֤����
my $PREFIX = '/opt/DLsystem/metadata/ucmetadata/';

# UCMETA������̾���طʿ������ꤹ��
my %ELEMENTS =
    ('Title' => '�����ȥ�:#ffccff',
     'Creator' => '����:#ffff99',
     'Subject' => '����:#ccffff',
     'Description' => '���Ƶ���:#ffe4b5',
     'Publisher' => '������:#ccff99',
     'Contributor' => '��Ϳ��:#99cc99',
     'Date' => '����:#f5f5dc',
     'Type' => '������:#dcf5dc',
     'Format' => '����:#dcffcc',
     'Identifier' => '���̻�:#ccccff',
     'Source' => '����:#ccffcc',
     'Language' => '����:#ffe4cc',
     'Relation' => '�ط�:#beccbe',
     'Coverage' => '�о��ϰ�:#bebecc',
     'Rights' => '��������:#87ceeb',

     ## ULIS original...
     'Country' => '���ǹ�:#ffffe0',
     'CharCode' => 'ʸ��������:#ebce87'
     );

# ���Ϥ��� HTML �κǽ����ʬ
my $HTML_HEAD = <<EOF;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<title>�޽�۾�����ء��޽�۾���شط��᥿�ǡ������������ƥ�</title>
<style type="text/css">
body { background-color: #e8e8e8; }
h1 { text-align: center; }
</style>
</head>
<body>
EOF

# ���Ϥ��� HTML �κǸ����ʬ
my $HTML_FOOT = <<EOF;
<hr>
<a href="javascript:history.back()">���</a>
</body></html>
EOF

# �֥饦�����������Ƥ������...
my $PATHINFO = path_info() || error("�ե�����̾������ޤ���");
if ($PATHINFO =~ m#^(/\w+/\d+\.sgm)$#) {
    $PATHINFO = $1;
} else {
    error("�ե�����̾�������Ǥ�: $PATHINFO");
}

main();
sub main {
    my $file = $PREFIX . $PATHINFO;
    error("�ե����뤬����ޤ���") unless -f $file;
    open(F, $file) || die "open error: $file: $!";

    # output
    print header("text/html; charset=EUC-JP");
    print $HTML_HEAD;
    print "<p><strong>�����᥿�ǡ�����ɽ��</strong></p>\n";
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

# HTML�����Ѵ�
# �ʸ���SGML���������DTD�˱�äƤ��ʤ��Τ��θ���٤���
sub escape_html($) {
    my ($str) = @_;

    # �ɤߤϽ���
    $str =~ s#<transcription>([^<]*)</transcription>##gio;

    $str =~ s/&amp;/&/gio;
    $str =~ s/&lt;/</gio;
    $str =~ s/&gt;/>/gio;
    $str =~ s/&quot;/\"/gio;

    $str =~ s/&/&amp;/go;
    $str =~ s/</&lt;/go;
    $str =~ s/>/&gt;/go;
    $str =~ s/\"/&quot;/go;

    # URL�餷��ʸ����˥�󥯤�Ϥ�
    $str =~ s#((https?|ftp)://[;\/?:@&=+\$,A-Za-z0-9\-_.!~*'()]+)#<a href="$1">$1</a>#gi;

    return $str;
}

sub error($) {
    my ($msg) = @_;
    print header("text/html; charset=EUC-JP");
    print $HTML_HEAD;
    print <<EOF;
<h1>Error</h1>
<p>���顼: <strong>$msg</strong></p>
EOF
    print $HTML_FOOT;
    exit;
}
