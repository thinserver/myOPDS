<?php

	$thumbnails = "thumbnails";
	$files = "files";

	$md5 = md5_file($files.'/'.$_GET['filename']);
	readfile($thumbnails.'/'.$md5.'.png');

?>
