<?php
	readfile('header.xml');

	$folder = 'files';

	$files = scandir($folder);
	foreach ($files as $file) {
		if (strpos($file, '.xml') > -1) {
			$name = $folder.'/'.$file;
			readfile($name);
			}
		}
?>
</feed>
