mkdir Release

set cmd=Compress-Archive -Force '.\MUA1 (2006 PC)\*' '.\Release\MUA1.MO2.Plugins.zip'; ^
        Compress-Archive -Force '.\MUA1 (Steam)\*' '.\Release\MUA1.Steam.MO2.Plugins.zip'; ^
        Compress-Archive -Force '.\MUA2\*' '.\Release\MUA2.MO2.Plugins.zip'; ^
        Compress-Archive -Force '.\XML2\*' '.\Release\XML2.MO2.Plugins.zip'
powershell "%cmd%"
