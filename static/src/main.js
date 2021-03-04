const addFriend = document.querySelector('#addfriendBtn')
const friendList = document.querySelector('.friends__list')
const friendEmail = document.querySelector('#friendEmail')
const email = document.querySelector('#email')


function isEamilVaild(asValue) {
  const regExp = /^[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]/;
  return regExp.test(asValue);

}

window.addEventListener('load', () => {

  // email.innerHTML = response['email'] + "님";

  // 친구 목록 뿌려주기
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