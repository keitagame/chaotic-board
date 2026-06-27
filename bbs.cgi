#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use Encode qw(encode decode);

my $q = CGI->new;

my $bbs  = decode('Shift_JIS', $q->param('bbs'));
my $key  = decode('Shift_JIS', $q->param('key'));
my $name = decode('Shift_JIS', $q->param('FROM') || '名無しさん');
my $mail = decode('Shift_JIS', $q->param('mail') || '');
my $body = decode('Shift_JIS', $q->param('MESSAGE') || '');

my $dir = "/var/www/html/$bbs";
my $dat = "$dir/dat/$key.dat";

if (!-e $dat) {
    print "Content-Type: text/html; charset=Shift_JIS\n\n";
    print encode('cp932', "<html><body>スレッドがありません。</body></html>");
    exit;
}

open my $fh, "<:encoding(cp932)", $dat or die "Cannot open dat: $!";
my @lines = <$fh>;
close $fh;

my $no = scalar(@lines) + 1;

my @t = localtime();
my $time = sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",
    $t[5]+1900, $t[4]+1, $t[3],
    (qw(日 月 火 水 木 金 土))[$t[6]],
    $t[2], $t[1], $t[0]
);

my $ip = $ENV{'REMOTE_ADDR'} || "0.0.0.0";
my $id = substr( unpack("H*", pack("C*", split(/\./, $ip))), 0, 8 );
my $timecol = "$time ID:$id";

my @c = split(/<>/, $lines[0]);
my $title = $c[5];

my $newline = join("<>",
    $no,
    $name,
    $mail,
    $timecol,
    $body,
    $title,
    ""
) . "\n";

open my $fh2, ">>:encoding(cp932)", $dat or die "Cannot write dat: $!";
print $fh2 encode('cp932', decode('Shift_JIS', $newline));
close $fh2;

my $subject = "$dir/subject.txt";
my @subjects;

if (-e $subject) {
    open my $sfh, "<:encoding(cp932)", $subject;
    @subjects = <$sfh>;
    close $sfh;
}

my @newsubjects;
foreach my $line (@subjects) {
    if ($line =~ /^$key\.dat<>\Q$title\E/) {
        push @newsubjects, encode('cp932', "$key.dat<>$title ($no)\n");
    } else {
        push @newsubjects, $line;
    }
}

open my $sfh2, ">:encoding(cp932)", $subject;
print $sfh2 @newsubjects;
close $sfh2;

print "Content-Type: text/html; charset=Shift_JIS\n\n";
print encode('cp932', <<'HTML');
<html>
<head><title>書きこみました。</title></head>
<body>書きこみました。</body>
</html>
HTML
