<?php

header("Content-Type: application/atom+xml;profile=opds-catalog");

print '<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:dc="http://purl.org/dc/terms/"
      xmlns:opds="http://opds-spec.org/2010/catalog"/>

  <title>myOPDS Library</title>
  <author>
    <name>Matthias Bock</name>
  </author>

';

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
