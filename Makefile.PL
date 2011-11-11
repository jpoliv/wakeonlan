use ExtUtils::MakeMaker;
# See lib/ExtUtils/MakeMaker.pm for details of how to influence
# the contents of the Makefile that is written.
WriteMakefile(
	'NAME'	=> 'wakeonlan',
	'EXE_FILES' => [wakeonlan],
	'VERSION_FROM' => 'wakeonlan', # finds $VERSION
);
