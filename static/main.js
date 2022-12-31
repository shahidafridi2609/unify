console.log('1')
var but=document.getElementById("conn1");
console.log(but.value)
but.addEventListener('click', Est());
    function Est(){
                    console.log('start');
                    var your_id = document.getElementById('id1-input').value;
                    var friend_id = document.getElementById('id2-input').value;
                    document.querySelector("#ws1-id").textContent = your_id;
                    document.querySelector("#ws2-id").textContent = friend_id;
                    document.getElementById('id1-input').style.display='none';
                    document.getElementById('id2-input').style.display='none';
                    document.getElementById('connect').style.display='none';
                    var ws = new WebSocket('ws://192.168.0.105/EstablishConn/${your_id}');}
                    ws.onmessage = function(event) {
                        var messages = document.getElementById('messages')
                        var message = document.createElement('li')
                        var content = document.createTextNode(event.data)
                        message.appendChild(content)
                        messages.appendChild(message)
                    };
                    function sendMessage(event) {
                        var input = document.getElementById("messageText");
                        var friend_id=document.getElementById('ws2-id').value;
                        var msgdata= new Object();
                        msgdata.msg=input.value;
                        msgdata.friend_id=friend_id
                        ws.send(JSON.stringify(msgdata));
                        input.value = ''
                        event.preventDefault()
                    }