// button绑定触发器
// send-button
function request_update_history(message) {
    fetch("/update_history", {
        method: "POST",
        body: JSON.stringify({
                "message": message,
            }),
        headers: { "Content-Type": "application/json" }
    })
    .then((response) => {console.log(response)})
    .catch((error) => {alert("update history request error!");})
}

submitBtn.addEventListener("click", function () {
    // 获取用户输入和选定的模型
    var user_input = messageInput.value;

    // 检查用户输入是否为空
    if (user_input === "") {
        alert("请输入有效的消息内容。");
        return; // 不发送请求
    }

    // 更新聊天框User
    sendMessage(role="user", message=user_input);
    sendMessage(role="assistant", message="");

    // 发送请求到服务器
    fetch("/streamResponse", {
            method: "POST",
            body: JSON.stringify({
                    message: user_input,
                }),
            headers: { "Content-Type": "application/json" }
        })
    .then(response => response.body.getReader()) // 获取可读流
    .then(reader => {
        // 获取要逐个字显示的文本框
        var gptResponse = chatDisplay.lastChild;
        var textContent = "";

        // 逐个字逐个字地将GPT回复添加到对话框中
        const decoder = new TextDecoder();
        reader.read().then(function processText({ done, value }) {
            if (done) {
                return;
            }
            console.log(decoder.decode(value))
            textContent += decoder.decode(value);
            gptResponse.innerHTML = textContent;
            chatDisplay.scrollTop = chatDisplay.scrollHeight; // 滚动到底部
            reader.read().then(processText);
        });

        // 清空用户输入框
        messageInput.value = "";
    })
    .catch(error => {
        console.error(error);
        // 如果发生错误，弹出错误提示框
        alert("发生错误：" + error.message);
    });
});

//clear-button
// document.getElementById("clear-button").addEventListener("click", function () {
function clearHistory() {
    // 向服务器发送清除请求
    fetch("/clear_history", {   // **unimplemented**
        method: "POST",
    })
    .then((response) => {
        // 清空用户输入和逐个字显示的文本框
        document.getElementById("user-input").value = "";
        document.getElementById("response-text").innerHTML = "";
    })
    .catch((error) => {
        console.error("清除请求失败: ", error);
    });
}
