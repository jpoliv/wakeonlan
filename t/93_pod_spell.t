#!/usr/bin/perl -w
use strict;
use Test::More;
use Test::Spelling;

add_stopwords(qw(José Oliveira));
add_stopwords(qw(Ico Doornekamp));
add_stopwords(qw(ARP IP UDP NIC));
add_stopwords(qw(lan ethernet subnet));
add_stopwords(qw(subdirectory));
add_stopwords(qw(WOL wol wakeonlan wakeable));
add_stopwords(qw(0xFF));
add_stopwords(qw(lab001));

all_pod_files_spelling_ok();

# vim:set ai ts=4 sw=4 sts=4 et syntax=perl:
