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
