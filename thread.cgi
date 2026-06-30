#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use Digest::MD5 qw(md5_hex);
my $q = CGI->new;

my $bbs   = $q->param('bbs');
my $title = $q->param('title');
my $name  = $q->param('FROM') || '–¼–³‚µ‚³‚ñ';
my $mail  = $q->param('mail') || '';
my $body  = $q->param('MESSAGE') || '';

if (!$bbs || !$title || !$body) {
    print "Content-Type: text/html; charset=UTF-8\n\n";
    print "<html><body>“ü—Í‚ª•s‘«‚µ‚Ä‚¢‚Ü‚·B</body></html>";
    exit;
}

my $dir = "/var/www/html/";
my $datdir = "$dir/dat";

mkdir $datdir if !-d $datdir;

my $key = time();
my $dat = "$datdir/$key.dat";

my @t = localtime();
my $time = sprintf(
    "%04d/%02d/%02d(%s) %02d:%02d:%02d",
    $t[5]+1900, $t[4]+1, $t[3],
    (qw(“ú Œ ‰Î … –Ø ‹à “y))[$t[6]],
    $t[2], $t[1], $t[0]
);

my $ip = $ENV{'REMOTE_ADDR'} || "0.0.0.0";

my ($sec,$min,$hour,$mday,$mon,$year) = localtime;
my $date = sprintf("%04d%02d%02d", $year + 1900, $mon + 1, $mday);

my $id = uc substr(md5_hex("$ip$date"), 0, 8);
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

open my $fh, ">", $dat or die "Cannot write dat: $!";
print $fh $firstline;
close $fh;

my $subject = "$dir/subject.txt";
open my $sfh, ">>", $subject or die "Cannot write subject: $!";
print $sfh "$key.dat<>$title (1)\n";
close $sfh;


print "Status: 302 Found\n";
print "Location: index.htm\n\n";