const addFriend = document.querySelector('#addfriendBtn')
const friendList = document.querySelector('.friends__list')
const friendEmail = document.querySelector('#friendEmail')
const email = document.querySelector('#email')
const logoutBtn = document.querySelector('#logout')

// email validation
function isEamilVaild(asValue) {
  const regExp = /^[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]/;
  return regExp.test(asValue);
}
//logout
function logout() {
  // localStorage.removeItem("wtw-token");
  document.cookie = "token =; expires=Thu, 01 Jan 1999 00:00:10 GMT;";
  alert("로그아웃이 완료되었습니다.");
  window.location.href = "/";
}


function init() {
  //시작시에 
  window.addEventListener('load', () => {
    $.ajax({
      type: "GET",
      url: "/api/friends",
      data: {},
      success: function (response) {
        const friend_list = response['friend_list']
        for (let i = 0; i < friend_list.length; i++) {
          let friend = `
            <li class="friend">
              <a href="/main/${friend_list[i].friends_email}">${friend_list[i].friends_email}</a>
              <button class="delete is-large delfriendBtn"></button>
            </li>`
          friendList.innerHTML += friend
        }
      }
    })
  })
  $(function () {
    $(".imgMap").maphilight({
      fillColor: "008800",
      strokeColor: "ff0000",
      strokeWidth: 2,
    });
    var data = $('#star').mouseout().data('maphilight') || {};
    data.alwaysOn = true;
    console.log(data)
    $("area[class='on']").data("maphilight", data);
  });
  //친구추가
  addFriend.addEventListener('click', () => {
    const friends_email = friendEmail.value
    if (!isEamilVaild(friends_email)) {
      friendEmail.value = ""
      alert("이메일이 유효하지 않습니다.")
      return
    }

    $.ajax({
      type: "POST",
      url: "/api/friends",
      data: {
        friends_email
      },
      success: function (response) {
        const result = response['result']
        console.log(response)
        if (result === false) {
          alert("친구 조회가 실패했습니다.")
        }
        else {
          location.reload();
        }
        // let friend = `
        //     <li class="friend">
        //       <a href='/main/'>${response['friend']}</a>
        //       <button class="delete is-large"></button>
        //     </li>`
        // friendList.innerHTML += friend
      }
    })
  })
  //친구삭제
  friendList.addEventListener('click', (event) => {
    if (event.currentTarget !== event.target) {
      if (event.target.tagName = "BUTTON") {
        const friend = event.target.parentNode
        const friends_email = friend.querySelector('a')
        friendList.removeChild(friend)

        $.ajax({
          type: "DELETE",
          url: "/api/friends",
          data: {
            friends_email: friends_email.textContent
          },
          success: function (response) {
          }
        })
      }
    }
  })
  //로그아웃
  logoutBtn.addEventListener('click', logout)
}

init()


