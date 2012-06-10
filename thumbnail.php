<?php

	$thumbnails = "thumbnails";
	readfile($thumbnails.'/'.$_GET['filename'][:-4].'.png');

?>
