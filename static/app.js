$(document).ready(function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    
    function heightHeader() {
        var left = $('.card-left .card-chat-header').height();
        var right = $('.card-right .card-chat-header').height();
        if(left > right) {
            $('.card-chat .card-chat-header').height(left);
        } else {
            $('.card-chat .card-chat-header').height(right);
        }
    }

    function resizeWindow() {
        heightHeader();
        var heightHeaderLeft = $('.card-left .card-chat-header').height() + $('#chat-left-tab').height();
        var heightHeaderFooterRight = $('.card-right .card-chat-header').height() + $('.card-right .card-chat-footer').height();
        $('#chat-left-tab-content .tab-pane .list-group').height($(window).height() - heightHeaderLeft);
        $('.chat-container').height($(window).height() - heightHeaderFooterRight);
    }
    $(window).resize(resizeWindow);
    resizeWindow();

    
    socket.on('my_response', function (message, cb) {
        if (message.room !== undefined) {
            if ($(`#list-${message.room}`).length === 0) {
                linkRoom(message.room);
                containerRoom(message.room);
            }
            if(ids.indexOf(message.id) === -1) {
                $(`#list-${message.room}`).append(bubbleLeft(message.data));
                if(message.room !== room) {
                    var countNotSeen = parseInt($(`#list-${message.room}-list .badge-chat`).text().trim());
                    countNotSeen = isNaN(countNotSeen) ? 1 : countNotSeen + 1;
                    updateNotSeen(message.room, {count: countNotSeen})
                }
            } else {
                ids = ids.filter(id => id === message.id);
                $(`#list-${message.room}`).append(bubbleRight(message.data));
                updateNotSeen(message.room, {count: 0, time: convertToTime(message.data.time)})
            }
            $(`#list-${message.room}`).animate({scrollTop: $(`#list-${message.room}`)[0].scrollHeight}, 1000);
            updateLastMessage(message.room);
        } else {
            // console.log(message.data)
        }
        // console.log(message);
    });

    function convertToTime(time) {
        return moment(new Date(time.substring(0, time.length - 4))).format('HH:mm')
    }

    function getAjaxNotSeen(channel_id) {
        $.get(`/no-seen/${channel_id}`, function(data) {
            updateNotSeen(channel_id, {count: data.count, time: convertToTime(data.time)});
        });
    }

    function updateAjaxSeen(channel_id) {
        $.get(`/seen/${channel_id}`, function(data) {
            updateNotSeen(channel_id, {count: 0, time: getLastMessage(channel_id).time})
        });
    }

    $.get("/channels", function (data) {
            for(friend of data) {
                socket.emit('join', {
                    room: friend.channel_id
                });
                linkRoom(friend);
                containerRoom(friend);
                loadMessage(friend);
                getAjaxNotSeen(friend.channel_id);
            }

            $('.room').click(function (e) {
                e.preventDefault();
                room = $(this).attr('data-room');
                updateHeaderChat(room);
                updateAjaxSeen(room);
                $('.room-chat a').on('shown.bs.tab', function() {
                    $(`#list-${room}`).scrollTop($(`#list-${room}`)[0].scrollHeight);
                });
            });

            if(data.length !== 0) {
                room = `${data[0].channel_id}`
                $(`#list-${data[0].channel_id}-list`).tab('show');
                updateHeaderChat(data[0].channel_id);
            }
    });

    $.get("/friends", function(data) {
        for(friend of data) {
            $('#list-contact .list-group').append(`
            <a
                id="friend-request-${friend.friend_id}"
                class="list-group-item list-group-item-action d-flex justify-content-between align-items-center add-friend">
                <img src="https://ui-avatars.com/api/?name=${friend.username}&size=60" />
                <b>${friend.username}</b>
            </a>
            `);
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

        $.get(`/messages/${room.channel_id}`, function(messages) {
            for (message of messages) {
                messageHTML = ''
                if(message.author_id !== -1) {
                    messageHTML = bubbleLeft(message.data);
                } else {
                    messageHTML = bubbleRight(message.data);
                }

                $(`#list-${room.channel_id}`).append(messageHTML);
            }
            $(`#list-${room.channel_id}`).scrollTop($(`#list-${room.channel_id}`)[0].scrollHeight);
            updateLastMessage(room.channel_id);
        })
    }
    
    function updateNotSeen(channel_id, data) {
        if($(`#list-${channel_id}-list>small`).length > 0) {
            $(`#list-${channel_id}-list>small`).remove()
        }

        if(data.count == 0) {
            $(`#list-${channel_id}-list`).append(`<small>${data.time}</small>`)
        } else {
            console.log(`#list-${channel_id}-list`);
            $(`#list-${channel_id}-list`).append(`<small class="badge-chat">${data.count}</small>`)
        }
    }

    function getLastMessage(room) {
        return {
            content: $(`#list-${room} .message:last-child p`).text().trim(),
            time: $(`#list-${room} .message:last-child small`).text().trim()
        }
    }

    function updateLastMessage(room) {
        $(`#list-${room}-list .room-content small`).text(getLastMessage(room).content);
    }

    function updateHeaderChat(room) {
        var src = $(`#list-${room}-list img`).attr('src');
        var name = $(`#list-${room}-list .room-content b`).text().trim();
        $('.card-right .card-chat-header img').attr('src', src);
        $('.card-right .card-chat-header h3').text(name)
    }

    function bubbleLeft(data) {
        return `
        <div class="d-flex message">
            <div class="bubble bubble-left" >
                <p class="m-0">${data.content}</p>
                <small>${convertToTime(data.time)}</small>
            </div>
        </div>
        `;
    }

    function bubbleRight(data) {
        return `
        <div class="d-flex message justify-content-end">
            <div class="bg-ui bubble bubble-right">
                <p class="m-0">${data.content}</p>
                <small>${convertToTime(data.time)}</small>
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
        </a>`)
    }

    function containerRoom(room) {
        $('.chat-container').append(`
        <div class="tab-pane fade show chat-pane p-3" id="list-${room.channel_id}" role="tabpanel"
                aria-labelledby="list-${room.channel_id}-list">
        </div>
        `);
    }

    function addNotificationEmpty(className, messasge) {
        $(`#${className}`).append(`<p style="display: none;" class="text-center my-3">${messasge}</p>`);
        $(`#${className} .list-group`).css({'display': 'none'});
        $(`#${className} p`).fadeIn();
    }

    $.get('/friend-requests', function(data) {
        if(data.length === 0) {
            addNotificationEmpty('list-add-friend', 'There are not friend invitations');
        }
        for (request of data) {
            $('#list-add-friend .list-group').append(`
            <a
                id="friend-request-${request.friend_id}"
                class="list-group-item list-group-item-action d-flex justify-content-between align-items-center add-friend">
                <img src="https://ui-avatars.com/api/?name=${request.username}&size=60" />
                <b>${request.username}</b>
                <div class="d-flex">
                    <button class="btn btn-add-friend" data-accept=1 data-user-id=${request.friend_id}><i class="fas fa-check"></i></button>
                    <button class="btn btn-add-friend" data-accept=2 data-user-id=${request.friend_id}><i class="fas fa-times"></i></button>
                </div>
            </a>
            `);
        }

        $('.btn-add-friend').click(function() {
            var accept = $(this).attr('data-accept');
            var friend_id = $(this).attr('data-user-id');
            $.post('/friend-requests', {accept, friend_id}, function(data) {
                $(`#friend-request-${friend_id}`).slideUp(400, function() {
                        $(`#friend-request-${friend_id}`).remove();
                        if($('#list-add-friend .list-group a').length === 0) {
                            addNotificationEmpty('list-add-friend', 'There are not friend invitations');
                        }
                });
            });
        });

    });

    $('#join').submit(function (e) {
        socket.emit('join', {
            room: $('#join_room').val()
        });

        linkRoom($('#join_room').val());
        containerRoom($('#join_room').val());

        $('.room').click(function (e) {
            e.preventDefault();
            room = $(this).attr('data-room');
            // console.log(room);
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
        if (room !== '' && $('#room_data').val() != '') {
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
        $('#chat-left-tab-content .tab-pane .list-group ').animate({height: `${down ? 440 : 500}px`}, 500)
        $('.add-friend-form').slideToggle(500)
        down = !down
    })
});