$(document).ready(function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    function showMessage() {
        var params = new window.URLSearchParams(window.location.search);
        if(params.get('message') !== null) {
            $('body').prepend(`
                <div class="p-3" style="position: absolute; top: 0; right: 0; z-index: 1000">
                    <div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-delay="5000">
                        <div class="toast-header">
                            <i class="fas fa-exclamation-circle text-danger"></i>
                            <strong class="ml-2 mr-auto text-danger">Error</strong>
                            <small class="text-muted">just now</small>
                            <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="toast-body">
                            ${params.get('message')}
                        </div>
                    </div>
                </div>
            `);
            $('.toast').toast('show');
        }
    }

    showMessage();
    
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
        var heightHeaderFooterRight = $('.card-right .card-chat-header').height() + $('.card-right .card-chat-footer').outerHeight();
        $('#chat-left-tab-content .tab-pane .list-group').height($(window).height() - heightHeaderLeft);
        $('.chat-container').height($(window).height() - heightHeaderFooterRight);
    }
    $(window).resize(resizeWindow);
    resizeWindow();

    
    socket.on('my_response', function (message, cb) {
        if (message.type === 'message') {
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
            prependLastMessage(message.room);
        } else if (message.type === 'seen') {
            if(ids.indexOf(message.id) === -1) {
                updateLastMessage(message.room, true);
            } else {
                ids = ids.filter(id => id === message.id);
            }
        } else if(message.type === 'friend-request') {
            addFriend(message);
            removeNotificationEmpty('#list-add-friend');
            $('.btn-add-friend').click(addFriendEvent);
        } else if(message.type === 'create-room') {
            if ($(`#list-${message.data.channel_id}`).length === 0) {
                createRoom(message.data);
                $('.room').click(roomClickEvent);
            }
        } else if (message.type === 'online-status') {
            updateOnlineStatus(message.friend_id, message.online)
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

    function getAjaxSeen(channel_id) {
        $.get(`/seen-user/${channel_id}`, function(data) {
            updateLastMessage(channel_id, data.status);
        })
    }

    function updateAjaxSeen(channel_id) {
        $.get(`/seen/${channel_id}`, function(data) {
            updateNotSeen(channel_id, {count: 0, time: getLastMessage(channel_id).time});
            var id = create_UUID();
            ids.push(id);
            socket.emit('seen_event', {
                room: channel_id,
                id: id
            });
        })
    }

    $.get("/channels", function (channels) {
            for(channel of channels) {
                createRoom(channel);
            }

            $('.room').click(roomClickEvent);

            if(channels.length !== 0) {
                room = `${channels[0].channel_id}`
                $(`#list-${channels[0].channel_id}-list`).tab('show');
                updateHeaderChat(channels[0].channel_id);
            }
    });

    function createRoom(channel) {
        socket.emit('join', {
            room: channel.channel_id
        });
        linkRoom(channel);
        containerRoom(channel);
        loadMessage(channel);
        getAjaxNotSeen(channel.channel_id);
        getAjaxSeen(channel.channel_id);
    }

    function roomClickEvent(e) {
        e.preventDefault();
        room = $(this).attr('data-room');
        updateHeaderChat(room);
        updateAjaxSeen(room);
        $('.room-chat a').on('shown.bs.tab', function() {
            $(`#list-${room}`).scrollTop($(`#list-${room}`)[0].scrollHeight);
        });
    }

    $.get("/friends", function(data) {
        for(friend of data) {
            $('#list-contact .list-group').append(`
            <a
                id="friend-request-${friend.friend_id}"
                class="list-group-item list-group-item-action d-flex justify-content-between align-items-center add-friend">
                <div class="user-avatar">
                    <img src="https://ui-avatars.com/api/?name=${friend.username}&size=60" />
                    <div class="status ${friend.online ? 'online' : 'offline'}"></div>
                </div>
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
                console.log(message.data.time)
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
            $(`#list-${channel_id}-list`).append(`<small class="badge-chat">${data.count}</small>`)
        }
    }

    function getLastMessage(room) {
        return {
            content: $(`#list-${room} .message:last-child p`).text().trim(),
            time: $(`#list-${room} .message:last-child .message-time`).text().trim()
        }
    }

    function updateLastMessage(room, status = false) {
        $(`#list-${room}-list .room-content small`).text(getLastMessage(room).content);

        $(`#list-${room} .message .send-status`).remove();
        $(`#list-${room} .message:last-child .bubble-right .d-flex`).append(`<small class="send-status ml-3">${status ? 'Seen' : 'Sent'}</small>`);
    }

    function prependLastMessage(room) {
        $(`#list-${room}-list`).prependTo($('.room-chat'));
    }

    function updateHeaderChat(room) {
        var src = $(`#list-${room}-list img`).attr('src');
        var name = $(`#list-${room}-list .room-content b`).text().trim();
        $('.card-right .card-chat-header img').attr('src', src);
        $('.card-right .card-chat-header h3').text(name)
    }

    function bubbleLeft(data) {
        return `
        <div class="d-flex message" >
            <div class="bubble bubble-left">
                <p class="m-0">${data.content}</p>
                <div class="d-flex justify-content-between">
                    <small class="message-time">${convertToTime(data.time)}</small>
                </div>
            </div>
        </div>
        `;
    }

    function bubbleRight(data) {
        return `
        <div class="d-flex message justify-content-end">
            <div class="bg-ui bubble bubble-right">
                <p class="m-0">${data.content}</p>
                <div class="d-flex justify-content-between">
                    <small class="message-time">${convertToTime(data.time)}</small>
                </div>
            </div>
        </div>
        `;
    }

    function linkRoom(room) {
        $('.room-chat').append(`
        <a class="list-group-item list-group-item-action d-flex justify-content-between align-items-center room"
                    data-room="${room.channel_id}"
                    data-user-id="${room.friend.id}"
                    id="list-${room.channel_id}-list" data-toggle="list" href="#list-${room.channel_id}" role="tab" aria-controls="${room.friend.name}">
            <div class="user-avatar">
                <img src="https://ui-avatars.com/api/?name=${room.friend.name}&size=60" />
                ${room.friend.online === undefined ? '' : `<div class="status ${room.friend.online ? 'online' : 'offline'}"></div>`}
            </div>
            <div class="room-content">
                <b class="m-0">${room.friend.name}</b>
                <small>Hello boy!!!</small>
            </div>
        </a>`)
    }

    function updateOnlineStatus(friend_id, online) {
        $(`.room[data-user-id='${friend_id}'] .user-avatar .status`).remove();
        $(`#friend-request-${friend_id} .user-avatar .status`).remove();

        $(`.room[data-user-id='${friend_id}'] .user-avatar`).append(`<div class="status ${online ? 'online' : 'offline'}"></div>`)
        $(`#friend-request-${friend_id} .user-avatar`).append(`<div class="status ${online ? 'online' : 'offline'}"></div>`)
    }

    function containerRoom(room) {
        $('.chat-container').append(`
        <div class="tab-pane fade show chat-pane p-3" id="list-${room.channel_id}" role="tabpanel"
                aria-labelledby="list-${room.channel_id}-list">
        </div>
        `);
    }

    function addNotificationEmpty(className, messasge) {
        $(`${className}`).append(`<p style="display: none;" class="text-center my-3">${messasge}</p>`);
        $(`${className} .list-group`).css({'display': 'none'});
        $(`${className} p`).fadeIn();
    }

    function removeNotificationEmpty(className) {
        if($(`${className} p`).length > 0) {
            $(`${className} p`).remove();
            $(`${className} .list-group`).fadeIn();
        }
    }

    $.get('/friend-requests', function(data) {
        if(data.length === 0) {
            addNotificationEmpty('#list-add-friend', 'There are not friend invitations');
        }
        for (request of data) {
            addFriend(request);
        }

        $('.btn-add-friend').click(addFriendEvent);

    });

    function addFriendEvent() {
        var accept = $(this).attr('data-accept');
        var friend_id = $(this).attr('data-user-id');
        $.post('/friend-requests', {accept, friend_id}, function(data) {
            $(`#friend-request-${friend_id}`).slideUp(400, function() {
                    $(`#friend-request-${friend_id}`).remove();
                    if($('#list-add-friend .list-group a').length === 0) {
                        addNotificationEmpty('#list-add-friend', 'There are not friend invitations');
                    }
            });
        });
    }

    function addFriend(request) {
        $('#list-add-friend .list-group').append(`
        <a
            id="friend-request-${request.friend_id}"
            class="list-group-item list-group-item-action d-flex justify-content-between align-items-center add-friend">
            <div class="user-avatar">
                <img src="https://ui-avatars.com/api/?name=${request.username}&size=60" />     
            </div>
            <b>${request.username}</b>
            <div class="d-flex">
                <button class="btn btn-add-friend" data-accept=1 data-user-id=${request.friend_id}><i class="fas fa-check"></i></button>
                <button class="btn btn-add-friend" data-accept=2 data-user-id=${request.friend_id}><i class="fas fa-times"></i></button>
            </div>
        </a>
        `);
    }

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

    function checkUserExist(username) {
        $.get(`/check-user/${username}`, function(data) {
            if(data.error === undefined && data.exist) {
                $('.chip-group').append(`
                    <div class="chip">
                        <img src="https://ui-avatars.com/api/?name=${username}&size=60" alt="Person">
                        <div class="chip-name">${username}</div>
                        <span class="closebtn" onclick="this.parentElement.style.display='none'">&times;</span>
                    </div>
                `)
            }
        });
    }

    $('#form-new-group').submit(function(e) {
        var username = $('#form-new-group input[type=text]').val();
        if(username !== '') {
            checkUserExist(username);
            $('#form-new-group input[type=text]').val('');
        }
        return false;
    });

    $('#btn-new-group').click(function(e) {
        var friends = [];
        $('.chip-group .chip .chip-name').each(function() {
            friends.push($(this).text());
        });
        $.post('/channels', {friends}, function(data) {
            createRoom(data);
            $('.room').click(roomClickEvent);
        });
    })

    $('#form-add-friend').submit(function(e) {
        var text = $('#form-add-friend input[type=text]').val();
        if(text !== '') {
            $('.modal .modal-body').append(`
                <div class="d-flex justify-content-center spinner">
                    <div class="spinner-border" role="status">
                        <span class="sr-only">Loading...</span>
                    </div>    
                </div>
            `)
            $.get(`/add-friend/${text}`, function(data) {
                $('.modal .modal-body .spinner').fadeOut(200, function() {
                    $('.modal .modal-body .spinner').remove();
                    if(data.error) {
                        $('.modal .modal-body').append(`
                        <div class="alert alert-danger alert-dismissible fade show mt-3" style="display:none" role="alert">
                            <strong>Error! </strong>${data.error}
                            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        `);
                        $('.modal .modal-body .alert').fadeIn();
                        setTimeout(3000, function() {
                            $('.modal .modal-body .alert').remove();
                        });
                    } else {
                        $('#addFriendModal').modal('toggle');
                    }
                })
            });
        }
        return false;
    });
    
});