function  setValue(){
    var uid = document.getElementById("uid").value;
    var reg = /^[0-9]*$/;
    if (reg.test(uid) && uid != '') {
        window.location.href = "/user/"+uid;
    }else{
        mdui.snackbar({
            message: '请输入正确的用户ID'
        })
    }
}
function share() {
    var myText = document.createElement("textarea")
    var userName = "{{ userName }}";
    myText.value = userName+"的edusrc详情统计："+window.location.href;
    console.log(myText.value);
    document.body.appendChild(myText)
    myText.select();
    document.execCommand('copy');
    document.body.removeChild(myText);
    mdui.snackbar("当前链接已复制");
}
