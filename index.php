<?php

readfile('header.xml');

$folder = 'publications';

$publications = scandir($folder);
foreach ($publications as $file) {
	if (strpos($file, '.xml') > -1) {
		$name = $folder.'/'.$file;
		readfile($name);
		}
	}
?>
</feed>
