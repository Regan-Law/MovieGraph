let pre_time;
info = $('#info')
send = $('#send')
chat = $('#chat')

// 将问题发送到后台，并接收相应
function sendtoserver(text) {
    let xmlhttp;
    if (window.XMLHttpRequest) {
        // IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
        xmlhttp = new XMLHttpRequest();
    } else {
        // IE6, IE5 浏览器执行代码
        xmlhttp = new ActiveXObject("Microsoft.XML HTTP");
    }
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            //  相应完成，则显示出来
            const answer = xmlhttp.responseText;
            show($.trim(answer));
        }
    }
    xmlhttp.open("POST", "/query", true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send("id=bei&q=" + $.trim(text));
}

send.click(function () {
    let p;
// 获取当前日期，并添加到对话框中
    const d = new Date();
    if (!pre_time || (pre_time && diff_time(d))) {
        p = "<div><span>" + d.getHours() + ':' + (d.getMinutes().toString().length === 1 ? '0' + d.getMinutes() : d.getMinutes()) + '</span></div>';
        pre_time = d;
        chat.append(p);
    }
    // 获取当前问题信息
    const text = info.val();
    // 判断问题是否为空
    if ($.trim(text) === "") {
        // $('#send').css(setDisabled);
        show("聊点啥吧！");
    } else {
        // 清空发送框
        $('#info').val('');
        // 把发送内容添加到聊天框
        p = "<div class='me'><div class='qipao'></div><div class='item'>" + text + '</div></div>';
        chat.append(p);
        chat.scrollTop(chat[0].scrollHeight);
        // 将问题信息发送到服务
        sendtoserver(text);
    }
})

// 按回车触发提问
$('body').keydown(function (e) {
    if (e.keyCode === 13) {
        send.click();
    }
});

function show(data) {
    const p = "<div class='robot'><div class='qipao'></div><div class='item'>" + data + '</div></div>';
    chat.append(p);
    chat.scrollTop(chat[0].scrollHeight);
}

// 处理时间的函数
function diff_time(time) {
    if (time.getHours() - pre_time.getHours() === 0) {
        if (time.getMinutes() - pre_time.getMinutes() <= 5)
            return false;
    } else
        return true;
}