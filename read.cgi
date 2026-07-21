#!/usr/bin/perl
use strict;
use warnings;

# --- HTMLエスケープ用の関数 ---
# 元のJavaScriptにあった escapeHtml と同様の処理を行います[cite: 1]。
sub escape_html {
    my $str = shift;
    return '' unless defined $str;
    $str =~ s/&/&amp;/g;
    $str =~ s/</&lt;/g;
    $str =~ s/>/&gt;/g;
    return $str;
}

# --- HTTPヘッダーの出力 ---
print "Content-Type: text/html; charset=Shift_JIS\n\n";

# --- HTMLの上部（静的部分）を出力 ---
print <<'HTML_TOP';
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://w3.org">
<HEAD>
    <meta charset="Shift_JIS">
    <TITLE>none</TITLE>
    <style type="text/css">
        body {
            background-image: url("kkb.png");
            background-repeat: repeat;
            background-position: left top;
            background-attachment: scroll;
        }
    </style>
</HEAD>

<form align="right" action="index.htm" method="GET">
  <input type="submit" value="javascriptモードで表示">
</form>

<table align="center" bgcolor="#C4FFCA" border="1" width="90%"  cellpadding="2" cellspacing="7">
<tr>
<td>
<font size="4">&emsp;<strong>テスト@掲示板</strong></font>
<br>
<br>&emsp;テスト用の板です。何でも書いてください。
<br></td>
</tr>
<tr>
<td align="center"><a href="m"><small>書き込む前に読んでね</small></a>&emsp;<a href="k"><small>ガイドライン</small></a></td>
</tr>
</table>
<br>
<div id="threads">
HTML_TOP

# --- subject.txt の読み込みとスレッド一覧の構築 ---
if (open(my $subj_fh, '<', 'subject.txt')) {
    while (my $line = <$subj_fh>) {
        chomp $line;
        $line =~ s/\x0D$//; # 改行コード(CR)の除去
        
        # subject.txtを <> で分割し、datファイル名とタイトルを取得[cite: 1]
        my ($dat, $rest) = split(/<>/, $line, 2);
        next unless defined $rest;
        
        # datファイル名から拡張子を削除してkeyを取得[cite: 1]
        my $key = $dat;
        $key =~ s/\.dat$//;
        
        print qq|<div class="thread">\n|;
        print qq|<br>\n|;
        print qq|<table bgcolor="#F0F0F0" align="center" border="1" width="90%" cellpadding="2" cellspacing="7">\n|;
        print qq|<tr>\n|;
        print qq|<td>\n|;
        print qq|<div><b></b><font size="5" color="red"><b>$rest</b></font></div><br>\n|;
        
        # --- 個別スレッドのdatファイル（dat/{key}.dat）を読み込む ---
        my $dat_file = "dat/$key.dat";
        if (open(my $dat_fh, '<', $dat_file)) {
            while (my $dat_line = <$dat_fh>) {
                chomp $dat_line;
                $dat_line =~ s/\x0D$//;
                
                # 行を <> で分割し、各項目を取得[cite: 1]
                my @cols = split(/<>/, $dat_line);
                my $no   = $cols[0] // '';
                my $name = escape_html($cols[1]);
                my $mail = escape_html($cols[2]);
                my $time = escape_html($cols[3]);
                my $body = escape_html($cols[4]);
                
                # メールアドレスが入力されている場合はリンク化[cite: 1]
                my $name_tag = ($mail ne '') ? qq|<a href="mailto:$mail">$name</a>| : $name;
                
                print qq|$no 名前：<font color="green"><strong>$name_tag</strong></font> ：$time<br>\n|;
                print qq|&emsp;&emsp;&ensp;$body<br><br>\n|;
            }
            close($dat_fh);
        }
        
        # --- スレッド固有の書き込みフォームを出力 ---
        # hiddenタグにスレッドのkeyをセットしてPOSTする仕組みを再現[cite: 1]
        print <<"HTML_FORM";
<br>
<br>
<form action="/bbs/bbs.cgi" method="post"> 
<input name="key" type="hidden" value="$key">
<button type="submit">書き込む</button>
<label for="username">名前：</label>
<input type="text" id="username" width="100" name="FROM" placeholder="名無し"> 
<label for="useremail">メアド：</label>
<input type="text" id="useremail" name="mail"> 
<br>
<br>
<textarea id="usermessage" name="MESSAGE" rows="5" cols="65" required></textarea>
</form>
<a href="."><strong>リロード</strong></a>&ensp;<a href="/"><strong>板のトップ</strong></a>
</td>
</tr>
</table>
</div>
HTML_FORM
    }
    close($subj_fh);
} else {
    print "<!-- Error: Cannot open subject.txt -->\n";
}

# --- HTMLの下部（静的部分）を出力 ---
print <<'HTML_BOTTOM';
</div>
<br>
<table align="center" bgcolor="#C4FFCA" border="1" width="90%"  cellpadding="2" cellspacing="7">
<tr>
<td align="center"><a href="tate.htm"><small>すれたて</small></a></td>
</tr>
</table>
</HTML>
HTML_BOTTOM