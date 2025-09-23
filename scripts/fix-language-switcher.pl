#!/usr/bin/env perl
use strict;
use warnings;
use File::Find;

my $root = shift || '.';
my @files;
find(
  sub {
    return unless -f $_ && $_ =~ /\.html$/i;
    push @files, $File::Find::name;
  },
  $root
);

sub norm {
  my ($u) = @_;
  return undef unless defined $u;
  return $u unless $u =~ /^https:\/\/affordable-handbags\.com/i;
  $u =~ s/\/index\.html$/\//i;
  $u =~ s/\.html$/\//i;
  return $u;
}

for my $file (@files) {
  local $/ = undef;
  open my $fh, '<:utf8', $file or next;
  my $html = <$fh>;
  close $fh;

  my ($enAlt) = $html =~ /<link\s+rel=\"alternate\"[^>]*hreflang=\"en\"[^>]*href=\"([^\"]+)\"/i;
  my ($esAlt) = $html =~ /<link\s+rel=\"alternate\"[^>]*hreflang=\"es\"[^>]*href=\"([^\"]+)\"/i;
  $enAlt = norm($enAlt);
  $esAlt = norm($esAlt);

  my $orig = $html;
  if ($html =~ /(<!--\s*Language Switcher\s*-->[\s\S]*?<div\s+class=\"language-switcher\"[\s\S]*?>)([\s\S]*?)(<\/div>)/i) {
    my ($open, $inner, $close) = ($1, $2, $3);
    my $upd = $inner;
    if ($esAlt) {
      $upd =~ s/(<a\b[^>]*href=)(["'])([^"']*)(\2)([^>]*>\s*ES\s*<\/a>)/$1.$2.$esAlt.$2.$5/ie;
    }
    if ($enAlt) {
      $upd =~ s/(<a\b[^>]*href=)(["'])([^"']*)(\2)([^>]*>\s*EN\s*<\/a>)/$1.$2.$enAlt.$2.$5/ie;
    }
    # also remove .html to trailing slash for any remaining hrefs within the switcher (no eval)
    $upd =~ s/(href=(["'])[^"']+)\.html(\2)/$1\/$3/gi;
    $html =~ s/(<!--\s*Language Switcher\s*-->[\s\S]*?<div\s+class=\"language-switcher\"[\s\S]*?>)[\s\S]*?(<\/div>)/$1$upd$2/i;
  }

  if ($html ne $orig) {
    open(my $out, '>:encoding(UTF-8)', $file) or die $!;
    print $out $html;
    close $out;
    print "Updated: $file\n";
  }
}


