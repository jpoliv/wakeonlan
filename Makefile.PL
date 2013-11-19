
use ExtUtils::MakeMaker;

WriteMakefile
(
    'INSTALLDIRS' => 'site',
    'DISTNAME' => 'wakeonlan',
    'EXE_FILES' => [
                    'wakeonlan'
                    ],
    'VERSION_FROM' => 'wakeonlan',
    'PREREQ_PM' => {
                    'Test::More' => 0,
                    'Test::Pod::Coverage' => '1.00',
                    'Test::Pod' => '1.00',
                    'Test::Spelling' => 0,
                    'Test::Perl::Critic' => 0,
                    },
    ($] ge '5.005') ? (
        'AUTHOR'    => 'José Pedro Oliveira <jpo@di.uminho.pt>',
        'ABSTRACT'  => "Script to send 'magic packets' to wakeable computers"
    ) : (
    ),
);

# vim:set ai ts=4 sw=4 sts=4 et syntax=perl:
