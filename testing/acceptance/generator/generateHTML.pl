#! /usr/bin/perl
use strict;
use warnings;
# get input filename

my $inHandle = *STDIN;
if (@ARGV > 0) {
	my $inFilename = shift;
	open($inHandle, '<', "$inFilename") or die $!;
}

my $outHandle = *STDOUT;

if (@ARGV > 0) {
	my $filename = shift;
	open($outHandle, '>', "$filename") or die $!;
}

open(my $template, '<', "template.html") or die $!;

my @lines = <$inHandle>;
while (<$template>) {
	if (m/TITLESTRING/) {
		my $title = shift @lines;
		s/TITLESTRING/$title/;
		print $outHandle $_;
	}
	elsif (m/YOUR ROWS HERE/) {
		my $count = 1;
		while (@lines > 0) {
			my $line = shift @lines;
			if ($line =~ m/['"](.*?)['"],['"](.*?)['"],['"](.*?)['"],['"](.*?)['"]/) {
				print $outHandle "<tr>\n";
				print $outHandle "<td align=\"center\"><p>$count</p></td>\n";
				print $outHandle "<td><p>$1</p></td>\n";
				print $outHandle "<td><p>$2</p></td>\n";
				print $outHandle "<td><p>$3</p></td>\n";
				print $outHandle "<td><p>$4</p></td>\n";
				print $outHandle "</tr>\n";
				$count++;
			}
		}
	}
	else {
		print $outHandle $_;
	}
	
}

$outHandle eq *STDOUT or close($outHandle);
close($template);
