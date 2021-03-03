const addFriend = document.querySelector('#addfriendBtn')
const delFriend = document.querySelector('#delfriendBtn')
const friendList = document.querySelector('.friends__list')
const friendEmail = document.querySelector('#friendEmail')


function isEamilVaild(asValue) {
  const regExp = /^[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]/;
  return regExp.test(asValue);

}

window.addEventListener('load', () => {
  // 친구 목록 뿌려주기
  $.ajax({
    type: "GET",
    url: "/api/friends",
    data: {
    },
    success: function (response) {
      const firends_list = response['friends_list']
      for (let i = 0; i < firends_list.length; i++) {
        let firend = `
          <li class="friend">
            <a href="">${firends_list[i].email}</a>
            <button class="delete is-large" id="delfriendBtn"></button>
          </li>`
      }
      friendList.append(firend)
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
      if (result === false) {
        alert("친구 조회가 실패했습니다.")
      }
      let firend = `
          <li class="friend">
            <a href="">${response['friend_email']}</a>
            <button class="delete is-large" id="delfriendBtn"></button>
          </li>`
      friendList.append(firend)
    }
  })

})

delFriend.addEventListener('click', (event) => {
  // $.ajax({
  //   type: "DELETE",
  //   url: "/api/friends",
  //   data: {
  //     friends_email
  //   },
  //   success: function (response) {

  //   }
  // })
  const friend = event.target.parentNode
  friendList.removeChild(friend)
})