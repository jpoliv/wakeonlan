use ExtUtils::MakeMaker;
# See lib/ExtUtils/MakeMaker.pm for details of how to influence
# the contents of the Makefile that is written.

WriteMakefile(
	'NAME'			=> 'wakeonlan',
	'VERSION_FROM'	=> 'wakeonlan',		# finds $VERSION
	'EXE_FILES'		=> [wakeonlan],
	($] ge '5.005') ? (
		'AUTHOR'	=> 'Jose Pedro Oliveira (jpo@di.uminho.pt)',
		'ABSTRACT' 	=> "Script to send 'magic packets' to wakeable computers"
	) : (
	),
);

# vim:set ai ts=4 sw=4:
