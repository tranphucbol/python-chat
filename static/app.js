$(document).ready(function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port)
    socket.on('my_response', function (message, cb) {
        if (message.room !== undefined) {
            if ($(`#list-${message.room}`).length === 0) {
                linkRoom(message.room);
                containerRoom(message.room);
            }
            if(ids.indexOf(message.id) === -1) {
                $(`#list-${message.room}`).append(bubbleLeft(message.data));
            } else {
                ids = ids.filter(id => id === message.id);
                $(`#list-${room}`).append(bubbleRight(message.data));
            }
            $(`#list-${room}`).animate({scrollTop: $(`#list-${room}`)[0].scrollHeight}, 1000);
        } else {
            console.log(message.data)
        }
        console.log(message);
    });

    $.get("/friends", function (data) {
            for(friend of data) {
                socket.emit('join', {
                    room: friend.channel_id
                });
                linkRoom(friend)
                containerRoom(friend)
                loadMessage(friend)
                $('.room').click(function (e) {
                    e.preventDefault();
                    room = $(this).attr('data-room');
                });
            }

            if(data.length !== 0) {
                room = `${data[0].channel_id}`
                $(`#list-${data[0].channel_id}-list`).tab('show');
            }
    });

    function create_UUID() {
        var dt = new Date().getTime();
        var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = (dt + Math.random() * 16) % 16 | 0;
            dt = Math.floor(dt / 16);
            return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
        });
        return uuid;
    }

    var room = '';

    function loadMessage(room) {

        $.get(`/messages/${room.channel_id}`, function(data) {
            for (message of data) {
                messageHTML = ''
                if(message.author_id !== -1) {
                    messageHTML = bubbleLeft(message.content);
                } else {
                    messageHTML = bubbleRight(message.content);
                }

                $(`#list-${room.channel_id}`).append(messageHTML);
            }
            $(`#list-${room.channel_id}`).scrollTop($(`#list-${room.channel_id}`)[0].scrollHeight);
        })
    }

    function bubbleLeft(message) {
        return `
        <div class="d-flex">
            <div class="card mb-3 bubble-left" >
                <div class="card-body">
                    ${message}
                </div>
            </div>
        </div>
        `;
    }

    function bubbleRight(message) {
        return `
        <div class="d-flex justify-content-end">
            <div class="card text-white bg-ui mb-3 bubble-right">
                <div class="card-body">
                    ${message}
                </div>
            </div>
        </div>
        `;
    }

    function linkRoom(room) {
        $('.room-chat').append(`
        <a class="list-group-item list-group-item-action d-flex justify-content-between align-items-center room"
                    data-room="${room.channel_id}"
                    id="list-${room.channel_id}-list" data-toggle="list" href="#list-${room.channel_id}" role="tab" aria-controls="${room.friend}">
            <img src="https://ui-avatars.com/api/?name=${room.friend}&size=60" />
            <div class="room-content">
                <b class="m-0">${room.friend}</b>
                <small>Hello boy!!!</small>
            </div>
            <span class="badge-chat">12</span>
        </a>`)
    }

    function containerRoom(room) {
        $('.chat-container').append(`
        <div class="tab-pane fade show chat-pane p-3" id="list-${room.channel_id}" role="tabpanel"
                aria-labelledby="list-${room.channel_id}-list">
        </div>
        `);
    }

    $('#join').submit(function (e) {
        socket.emit('join', {
            room: $('#join_room').val()
        });

        linkRoom($('#join_room').val());
        containerRoom($('#join_room').val());

        $('.room').click(function (e) {
            e.preventDefault();
            room = $(this).attr('data-room');
            console.log(room);
        });

        return false;
    });

    $('#leave').submit(function (e) {
        socket.emit('leave', {
            room: $('#leave_room').val()
        });
        return false;
    });

    var ids = [];

    $('#send_room').submit(function (e) {
        if (room !== '') {
            var id = create_UUID();
            ids.push(id);
            socket.emit('my_room_event', {
                room: room,
                data: $('#room_data').val(),
                id: id
            });
        }
        $('#room_data').val('');
        return false;
    });

    var down = true;

    $('.btn-add').click(function(e) {
        $('.room-chat').animate({height: `${down ? 440 : 500}px`}, 1000)
        $('.add-friend-form').slideToggle(1000)
        down = !down
    })
});