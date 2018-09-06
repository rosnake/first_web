function getCookie(name) {
	var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return x ? x[1] : undefined;
}
function isDigitNumber(inputData) {
	//isNaN(inputData)不能判断空串或一个空格
	//如果是一个空串或是一个空格，而isNaN是做为数字0进行处理的，而parseInt与parseFloat是返回一个错误消息，这个isNaN检查不严密而导致的。
	if (parseFloat(inputData).toString() == "NaN") {
		return false;
	} else {
		return true;
		　　
	}
}

$(document).ready(function () {

});