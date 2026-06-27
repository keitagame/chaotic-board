#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use Encode qw(encode decode);

# my $q = CGI->new;

# my $bbs   = $q->param('bbs');
# my $title = $q->param('title');
# my $name  = $q->param('FROM') || '名無しさん';
# my $mail  = $q->param('mail') || '';
# my $body  = $q->param('MESSAGE') || '';
my $q = CGI->new;


my $bbs   = decode('Shift_JIS', $q->param('bbs')   || '');
my $title = decode('Shift_JIS', $q->param('title') || '');
my $name  = decode('Shift_JIS', $q->param('FROM')  || '名無しさん');
my $mail  = decode('Shift_JIS', $q->param('mail')  || '');
my $body  = decode('Shift_JIS', $q->param('MESSAGE') || '');

if (!$bbs || !$title || !$body) {
    print "Content-Type: text/html; charset=UTF-8\n\n";
    print "<html><body>入力が不足しています。</body></html>";
    exit;
}

my $dir = "/var/www/html/$bbs";
my $datdir = "$dir/dat";

mkdir $datdir if !-d $datdir;


my $key = time();

my $dat = "$datdir/$key.dat";

my @t = localtime();
my $time = sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",
    $t[5]+1900, $t[4]+1, $t[3],
    (qw(日 月 火 水 木 金 土))[$t[6]],
    $t[2], $t[1], $t[0]
);

my $ip = $ENV{'REMOTE_ADDR'} || "0.0.0.0";
my $id = substr( unpack("H*", pack("C*", split(/\./, $ip))), 0, 8 );
my $timecol = "$time ID:$id";


my $firstline = join("<>",
    1,
    $name,
    $mail,
    $timecol,
    $body,
    $title,
    ""
) . "\n";


open my $fh, ">:encoding(UTF-8)", $dat or die "Cannot write dat: $!";
print $fh $firstline;
close $fh;


my $subject = "$dir/subject.txt";
open my $sfh, ">>:encoding(UTF-8)", $subject or die "Cannot write subject: $!";
print $sfh "$key.dat<>$title (1)\n";
close $sfh;


print "Content-Type: text/html; charset=UTF-8\n\n";
print <<"HTML";
<html>
<head><title>スレ立て完了</title></head>
<body>
スレッドを作成しました。<br>
<a href="/thread.html?bbs=$bbs&key=$key">スレを開く</a>
</body>
</html>
HTML
