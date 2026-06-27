#!/usr/bin/perl
use strict;
use warnings;
use CGI;

my $q = CGI->new;


my $bbs  = $q->param('bbs');
my $key  = $q->param('key');
my $name = $q->param('FROM') || '名無しさん';
my $mail = $q->param('mail') || '';
my $body = $q->param('MESSAGE') || '';

my $dir = "/var/www/html/";
my $dat = "$dir/dat/$key.dat";


if (!-e $dat) {
    print "Content-Type: text/html; charset=UTF-8\n\n";
    print "<html><body>スレッドがありません。</body></html>";
    exit;
}


open my $fh, "<:encoding(UTF-8)", $dat or die "Cannot open dat: $!";
my @lines = <$fh>;
close $fh;

my $no = scalar(@lines) + 1;

my @t = localtime();
my $time = sprintf(
    "%04d/%02d/%02d(%s) %02d:%02d:%02d",
    $t[5]+1900, $t[4]+1, $t[3],
    (qw(日 月 火 水 木 金 土))[$t[6]],
    $t[2], $t[1], $t[0]
);

my $ip = $ENV{'REMOTE_ADDR'} || "0.0.0.0";
my $id = substr(unpack("H*", pack("C*", split(/\./, $ip))), 0, 8);
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


open my $fh2, ">>:encoding(UTF-8)", $dat or die "Cannot write dat: $!";
print $fh2 $newline;
close $fh2;


my $subject = "$dir/subject.txt";
my @subjects;

if (-e $subject) {
    open my $sfh, "<:encoding(UTF-8)", $subject;
    @subjects = <$sfh>;
    close $sfh;
}

my @newsubjects;
foreach my $line (@subjects) {
    if ($line =~ /^$key\.dat<>\Q$title\E/) {
        push @newsubjects, "$key.dat<>$title ($no)\n";
    } else {
        push @newsubjects, $line;
    }
}

open my $sfh2, ">:encoding(UTF-8)", $subject;
print $sfh2 @newsubjects;
close $sfh2;


print "Content-Type: text/html; charset=UTF-8\n\n";
print <<'HTML';
<html>
<head><title>書きこみました。</title></head>
<body>書きこみました。</body>
</html>
HTML
print "Location: index.htm\n\n"
