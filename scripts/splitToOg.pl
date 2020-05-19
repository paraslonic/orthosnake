use v5.10.0;
use warnings;
use Data::Dumper;

my $OrthologousGroups = $ARGV[0];
my $Full= $ARGV[1];
my $Out=$ARGV[2];
my $Filter=$ARGV[3];

my %core; 

open(F, "<", "$Filter");
while (<F>) {
	chomp;
	$core{$_} = 1;
}
close(F);
open(F, "<", "$OrthologousGroups");
my %hash=();
while (<F>) {
  @P = split(' ');
  $og = shift @P;
  $og =~ s/://;
  next if(!exists($core{$og}));
  foreach $gene (@P){
	my @p = split('\|',$gene);
	$hash{$p[0]}{$p[1]}=$og;
	}	
}
close(F);

#print Dumper(%hash);

open (S,"<","$Full");
my $strain;
my $id;
while (<S>){
	if (/>/)
	{
		@abc=split('\|');
		$strain = $abc[0];
		$strain =~ s/>//;
		$id = $abc[1];
		next if(!exists($hash{$strain}{$id}));
		open (W,">>","$Out/$hash{$strain}{$id}.fasta");
                print W ">$strain|$id\n";
                close(W);

	}
	else
	{
		next if(!exists($hash{$strain}{$id}));				
		open (W,">>","$Out/$hash{$strain}{$id}.fasta");
		print W "$_";
		close(W);
	}
}

