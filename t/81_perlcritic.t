#!/usr/bin/perl -w
use strict;
use Test::More tests => 1;
use Test::Perl::Critic;

critic_ok('wakeonlan');

# vim:set ai ts=4 sw=4 sts=4 et syntax=perl:
