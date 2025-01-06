// 获取头像的URL
const avatarUrl_user = '../static/imgs/avatar_user.jpg';
const avatarUrl_assistant = '../static/imgs/avatar_assistant.jpg';

// 获取元素
const messageInput = document.getElementById('message-input');
const submitBtn = document.getElementById('submit-btn');
const chatDisplay = document.querySelector('.chat-display');


function createNewMessage(role, message="") {
    // 添加新的消息元素
    const newMessage = document.createElement('div');
    newMessage.classList.add('message');
    // 设置消息内容和样式
    newMessage.innerHTML = message;
    newMessage.style.color = 'whitesmoke';
    newMessage.style.padding = '5px 10px';
    newMessage.style.marginBottom = '10px';
    newMessage.style.marginLeft = '20px';   
    newMessage.style.marginTop = '5px'
    newMessage.style.marginBottom = '40px'; // 模拟换行
    newMessage.style.letterSpacing = '1px';
    return newMessage
}

function createNewHeader(role) {
    // 创建并设置头像元素
    const avatar = document.createElement('img');
    avatar.width = 30;
    avatar.height = 30;

    // 创建一个新的消息头
    const newHeader = document.createElement('div');
    newHeader.classList.add('message-header');
    newHeader.style.color = "whitesmoke";

    // console.log(role);
    if (role == "user") {
        // console.log("this is user avatar.");
        avatar.src = avatarUrl_user;
        newHeader.innerHTML = "   User";
    }
    else {
        // console.log("this is assistant avatar.");
        avatar.src = avatarUrl_assistant;
        newHeader.innerHTML = "   Assistant";
    }

    newHeader.insertBefore(avatar, newHeader.firstChild);
    return newHeader;
}

// 定义函数：发送消息
function sendMessage(role="user", message="This is sendMessage test.") {
    chatDisplay.appendChild(createNewHeader(role))
    chatDisplay.appendChild(createNewMessage(role, message));
}

// // 功能演示
// sendMessage(role="user", message="总睡眠时间:7小时30分钟 入睡时间:23:00(晚上11点) 醒来次数:3次 深睡时间:2小时15分钟 浅睡时间:3小时45分钟 REM 睡眠:1小时30分钟 睡眠效率:92% 睡眠周期:4个完整的睡眠周期 心率变异性:在睡眠期间，心率在每分钟60到70次之间波动 呼吸率:每分钟14到16次 体温:入睡时36.8°C，最低降至36.4°C 体动:翻身12次，大幅度移动2次 入睡时长:30分钟 睡眠中断:最长中断持续15分钟，总共中断时间30分钟 睡眠评分:85分(满分100分)");
// sendMessage(role="assistant", message="你好呀!根据你提供的睡眠数据，我可以给你一些关于如何改善睡眠质量的建议哦~首先呢，你的睡眠时间还是蛮充足的，达到了7小时30分钟呢。从你的数据来看，入睡时间是23:00，这个时间算是比较晚的了，可能需要提前一些时间来帮助你更好地进入睡眠状态。你每晚醒来三次，每次持续时间都在15分钟以内，这可能是因为你在睡眠中可能会受到一些干扰，比如室内温度过高或过低，或者身体不舒服等等。建议你检查一下卧室的环境，确保它适合睡眠，并且保持一个舒适的温度。\n\n深睡时间和浅睡时间的比例还不错，说明你在睡眠过程中的深度和浅度都比较均衡。然而，你应该注意到REM睡眠的时间相对较少，只有1小时30分钟。这种睡眠阶段对于记忆和学习非常重要，所以如果你能增加这段时间的话，对提高你的认知能力会有帮助。睡眠效率很高，达到92%，这意味着你在整个睡眠过程中清醒的时间很少。这是一个很好的信号，说明你的睡眠质量很好。\n\n睡眠周期数为4，这也表明你的睡眠状况比较稳定。不过，如果希望获得更好的睡眠质量，可以尝试逐渐增加睡眠周期数，让你的身体得到更好的休息。心率和呼吸率都处于正常范围，表明你的身体在睡眠中得到了充分的放松。体温下降也表明了良好的代谢状态。");
