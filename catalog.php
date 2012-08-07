<?php

header ("Content-Type:application/xml");
print '<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:dc="http://purl.org/dc/terms/"
      xmlns:opds="http://opds-spec.org/2010/catalog">
  <id>Catalog</id>
 
  <title>Catalog</title>
  <author>
    <name>Matthias Bock</name>
  </author>
 
';

$folder = 'files';

$files = scandir($folder);
foreach ($files as $file) {
	if (strpos($file, '.xml') > -1) {
		$name = $folder.'/'.$file;
		readfile($name);
		}
	}

print '</feed>';

?>
