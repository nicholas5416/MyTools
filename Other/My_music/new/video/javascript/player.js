(function($) {
    var video = $("#my-video");
    var loop = 0;
    var qieh = 1;
    var loopture = 0;
    var videoIndex = 10;
    var ddd = document.getElementById('video-div');
    var full = false;
    var timer;
    var hidding = false;
    var isFull = true;
    var videoList = $('.player-list-video').length;
    var videoSpeed = 1;
    //播放列表切换
    function qiehuan(){
        video.prop("src",'source/' + videoIndex +'.mp4');
        video.prop("poster",'source/' + videoIndex + '.jpg');
        $('.timeBar').css('width', 0);
        video[0].play();
        $('.play-btn').removeClass('stop').addClass('play');
        $('.play-one').hide();
    }
    $('.player-list-video').on('click', function () {
        if (!full || !hidding){
            videoIndex = $(this).index();
            for(var i =0; i < videoList; i++){
                $('.player-list-video').eq(i).removeClass('video-now');
            }
            $(this).addClass('video-now');
            qiehuan();
            qieh = 0;
        }
    });
    // 读取初始时间
    function timeFormat(seconds) {
        var minite = Math.floor(seconds / 60);
        if(minite < 10) {
            minite = "0" + minite;
        }
        var second = Math.floor(seconds % 60);
        if(second < 10) {
            second = "0" + second;
        }
        return minite + ":" + second;
    }
    //更新时间进度条
    function updateProgress(x){
        if (!full || !hidding){
            var progress = $('.progress');
            var position = x - progress.offset().left;
            var percentage = 100 * position / progress.width();
            if(percentage > 100) {
                percentage = 100;
            }
            if(percentage < 0) {
                percentage = 0;
            }
            $('.timeBar').css('width', percentage+'%');
            video[0].currentTime = video[0].duration * percentage / 100;
        }
    }
    // 拖拽时间进度条
    function enableProgressDrag() {
        if (!full || !hidding){
            var progressDrag = false;
            $('.progress').on('mousedown', function(e) {
                progressDrag = true;
                updateProgress(e.pageX);
            });
            $(document).on('mouseup', function(e) {
                if(progressDrag) {
                    progressDrag = false;
                    updateProgress(e.pageX);
                }
            });
            $(document).on('mousemove', function(e) {
                if(progressDrag) {
                    updateProgress(e.pageX);
                }
            });
        }
    };
    // 控制栏展示消失
    function showControl(shouldShow) {
        if(shouldShow) {
            $('.yinyin').removeClass('yinyin-off').addClass('yinyin-on');
            $('.player-list').removeClass('player-list-off').addClass('player-list-on');
        } else {
            $('.yinyin').removeClass('yinyin-on').addClass('yinyin-off');
            $('.player-list').removeClass('player-list-on').addClass('player-list-off');
        }
    }
    function fillShow() {
        if (full){
            if(hidding){
                hidding = false;
                return;
            }
            if (timer) {
                clearTimeout(timer);
                timer = 0;
            }
            $('.yinyin').removeClass('yinyin-off').addClass('yinyin-on');
            $('.player-list').removeClass('player-list-off').addClass('player-list-on');
            timer = setTimeout(function () {
                hidding = true;
                $('.yinyin').removeClass('yinyin-on').addClass('yinyin-off');
                $('.player-list').removeClass('player-list-on').addClass('player-list-off');
            }, 2000)
        }
    }
    //声音按钮
    var soundAndMute = function() {
        if (!full || !hidding){
            if(video[0].muted) {
                video[0].muted = false;
                $('#soundBtn').removeClass("jinyin").addClass("sound");
                $('.volumeBar').css('height', (1 - video[0].volume) * 100 + '%');
                $('.sound-number').text(parseInt(video[0].volume * 100));
            } else {
                video[0].muted = true;
                $('#soundBtn').removeClass("sound").addClass("jinyin");
                $('.sound-number').text(0);
                $('.volumeBar').css({
                    "height": "50px",
                })
            }
        }
    };
    //声音拖拽
    function enableSoundDrag() {
        if (!full || !hidding){
            var volumeDrag = false;
            $('.volume').on('mousedown', function(e) {
                volumeDrag = true;
                updateVolume(e.pageY);
                video[0].muted = false;
                $('#soundBtn').removeClass("jinyin").addClass("sound");
            });
            $(document).on('mouseup', function(e) {
                if(volumeDrag) {
                    volumeDrag = false;
                    updateVolume(e.pageY);
                }
            });
            $(document).on('mousemove', function(e) {
                if(volumeDrag) {
                    updateVolume(e.pageY);
                }
            });
        }
    };
    // 更新声音
    function updateVolume(y, vol) {
        if (!full || !hidding){
            var volume = $('.volume');
            var soundTop = y - volume.offset().top;
            var percentage;
            if(vol) {
                percentage =100- (vol * 100);
            } else {
                var position = soundTop;
                percentage = 100 * position / 50;
            }
            if(percentage > 100) {
                $('#soundBtn').removeClass("sound").addClass("jinyin");
                percentage = 100;
            } else {
                $('#soundBtn').removeClass("jinyin").addClass("sound");
            }
            if(percentage < 0) {
                percentage = 0;
            }
            percentage = parseInt(percentage);
            $('.sound-number').text(100 -percentage);
            $('.volumeBar').css('height', percentage + '%');
            video[0].volume = (100 - percentage) / 100;
        }
    };
    //开始暂停
    function playAndPause() {
            if(video[0].paused || video[0].ended) {
                video[0].play();
                $('.play-btn').removeClass('stop').addClass('play');
                $('.play-one').hide();
                playSpeed(videoSpeed);
            }
            else {
                video[0].pause();
                $('.play-btn').removeClass('play').addClass('stop');
                $('.play-one').show();
            }
    }
    //播放速度
    function playSpeed(speed) {
        if (!full || !hidding){
            if(speed == 1) {
                $('#speed05Btn').removeClass("moren");
                $('#speed2Btn').removeClass("moren");
                $('#speed1Btn').addClass("moren");
                videoSpeed = 1;
            } else if(speed == 2) {
                $('#speed05Btn').removeClass("moren");
                $('#speed1Btn').removeClass("moren");
                $('#speed2Btn').addClass("moren");
                videoSpeed = 2;
            } else if(speed == 0.5) {
                $('#speed1Btn').removeClass("moren");
                $('#speed2Btn').removeClass("moren");
                $('#speed05Btn').addClass("moren");
                videoSpeed = 0.5;
            }
            video[0].playbackRate = speed;
        }
    }
    //循环播放
    function isloop() {
        if (!full || !hidding){
            if(loop == 0){
                $('#loop').removeClass('loop').addClass('loop-ture');
                video[0].loop = true;
                loop = 1;
            } else if(loop == 1){
                $('#loop').removeClass('loop-ture').addClass('loop');
                video[0].loop = false;
                loop = 0;
            }
        }
    }
    //全屏
    function launchFullScreen() {
        if (!full || !hidding){
            var element = document.documentElement;
            if (isFull){
                if(element.requestFullScreen) {
                    ddd.requestFullScreen();
                } else if(element.mozRequestFullScreen) {
                    ddd.mozRequestFullScreen();
                } else if(element.webkitRequestFullScreen) {
                    ddd.webkitRequestFullScreen();
                } else if (element.msRequestFullscreen) {
                    ddd.msRequestFullscreen();
                }
            }else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                }
                else if (document.msExitFullscreen) {
                    document.msExitFullscreen();
                }
                else if (document.mozCancelFullScreen) {
                    document.mozCancelFullScreen();
                }
                else if (document.webkitCancelFullScreen) {
                    document.webkitCancelFullScreen();
                }
            }
        }
    }
    //监听退出全屏事件
    document.addEventListener("fullscreenchange", function(e) {
        isFull = !isFull;
        full = !full;
        if (!full){
            clearTimeout(timer);
            $('.yinyin').removeClass('yinyin-off').addClass('yinyin-on');
            $('.player-list').removeClass('player-list-off').addClass('player-list-on');
        }
    });
    document.addEventListener("mozfullscreenchange", function(e) {
        isFull = !isFull;
        full = !full;
        if (!full){
            clearTimeout(timer);
            $('.yinyin').removeClass('yinyin-off').addClass('yinyin-on');
            $('.player-list').removeClass('player-list-off').addClass('player-list-on');
        }
    });
    document.addEventListener("webkitfullscreenchange", function(e) {
        isFull = !isFull;
        full = !full;
        if (!full){
            $('#video-div').css({
                "width": 800 + "px",
                "height": 450 + "px",
            });
            clearTimeout(timer);
            $('.yinyin').removeClass('yinyin-off').addClass('yinyin-on');
            $('.player-list').removeClass('player-list-off').addClass('player-list-on'); //处理不支持div
        }                                                                                //全屏带动video
        if ($('#my-video').width() == 800 && full){                                      //的情况
            $('#video-div').css({
                "width": window.screen.availWidth + "px",
                "height": window.screen.availHeight + "px",
            })
        }
    });
    document.addEventListener("MSFullscreenChange", function(e) {
        isFull = !isFull;
        full = !full;
        if (!full){
            $('#video-div').css({
                "width": 800 + "px",
                "height": 450 + "px",
            });
            clearTimeout(timer);
            $('.yinyin').removeClass('yinyin-off').addClass('yinyin-on');
            $('.player-list').removeClass('player-list-off').addClass('player-list-on');
        }
        if ($('#my-video').width() == 800 && full){
            $('#video-div').css({
                "width": window.screen.availWidth + "px",
                "height": window.screen.availHeight + "px",
            })
        }
    });
    updateVolume(0, 0.9);  // 初始化声音
    video.on("loadedmetadata", function(){
        if (qieh == 0){
            qiehuan();
            qieh = 1;
        }
        $('header').hover(function() {
            showControl(true);
        }, function() {
            showControl(false);
        });
        $('body').on('mousedown', function (e) {
            e.preventDefault();
        }).on('mousemove', function () {
            fillShow();
        })
        $('.play-one').on('click', function () {
            playAndPause();
        });
        $('.play-btn').on('click', function () {
            if (!full || !hidding){
                playAndPause();
            }
        });
        $('.all').on('click', launchFullScreen);
        $('#currentTime').text(timeFormat(0));
        $('#duration').text(timeFormat(video[0].duration));
        enableProgressDrag();
        enableSoundDrag();
        playSpeed(videoSpeed);
        $('#speed1Btn').on('click', function() {
            playSpeed(1);
        });
        $('#speed2Btn').on('click', function() {
            playSpeed(2);
        });
        $('#speed05Btn').on('click', function() {
            playSpeed(0.5);
        });
        //  阻止事件冒泡
        $('.sound-list').bind("click",function(event){
            event.stopPropagation();
        });
        $('.konge').bind("click",function(event){
            event.stopPropagation();
        });
        $('#soundBtn').on('click',soundAndMute);
        $(window).keypress(function(e) {
            if (e.keyCode == 0 || e.keyCode == 32) {
                playAndPause();
            }
        });
        $('#loop').on('click', isloop);
    })
    video.on('timeupdate', function() {
        var currentTime = video[0].currentTime;
        var duration = video[0].duration;
        var percent = 100 * currentTime / duration;
        $('.timeBar').css('width', percent + '%');
        $('#currentTime').text(timeFormat(currentTime));
    });
    video.on('canplay', function() {
        $('.loading').fadeOut(100);
    });
    video.on('ended', function() {
        $('.play-btn').removeClass("play").addClass("stop"); // 列表切换
        if(loopture == 0){
            videoIndex += 1;
            if(videoIndex == videoList){
                videoIndex = 0;
            }
            for(var i =0; i < videoList; i++){
                $('.player-list-video').eq(i).removeClass('video-now');
            }
            $('.player-list-video').eq(videoIndex).addClass('video-now');
            qiehuan();
            qieh = 0;
        }
    });
})(jQuery);
