use strict;
use warnings;

use v5.10.1;                # ExtUtils::MakeMaker 6.46+ for META_MERGE support

use ExtUtils::MakeMaker;

WriteMakefile(
    'NAME'          => 'wakeonlan',
    'VERSION_FROM'  => 'wakeonlan',
    'ABSTRACT'      => "Script to send 'magic packets' to wakeable computers",
    'AUTHOR'        => 'José Pedro Oliveira <jose.p.oliveira.oss@gmail.com>',
    'LICENSE'       => 'perl',
    'INSTALLDIRS'   => 'site',
    'EXE_FILES'     => ['wakeonlan'],
    'PREREQ_PM'     => {},
    'TEST_REQUIRES' => {
        'Test::More'          => 0,
        'Test::Pod::Coverage' => '1.00',
        'Test::Pod'           => '1.00',
        'Test::Spelling'      => 0,
        'Test::Perl::Critic'  => 0,
    },
    # META_MERGE requires ExtUtils::MakeMaker 6.46+
    'META_MERGE'    => {
        'meta-spec' => { version => 2 },
        'resources' => {
            'repository' => {
                'type' => 'git',
                'url'  => 'https://github.com/jpoliv/wakeonlan.git',
                'web'  => 'https://github.com/jpoliv/wakeonlan',
            },
            'bugtracker' => {
                'web'  => 'https://github.com/jpoliv/wakeonlan/issues',
            },
        },
    },
);

# vim:set ai ts=4 sw=4 sts=4 et syntax=perl:
