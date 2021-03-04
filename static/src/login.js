const joinBtn = document.querySelector('.join__btn');
const checkOverlapBtn = document.querySelector('.checkOverlapBtn')

const nameLabel = document.querySelector('.join__name')
const nameInput = nameLabel.querySelector('input')

const birthLabel = document.querySelector('.join__birth')
const birthInput = birthLabel.querySelector('input')
const emailLabel = document.querySelector('.join__email')
const emailInput = emailLabel.querySelector('input')
const pwLabel = document.querySelector('.join__password')
const pwInput = pwLabel.querySelector('input')
const loginBtn = document.querySelector('#login')
const modalCloseBtn = document.querySelector('#modalCloseBtn')
const modalOpenBtn = document.querySelector('#modalOpenBtn')


//validation
function isNameVaild(asValue) {
  if (asValue === "") {
    return false
  }
  return true
}
function isBirthVaild(asValue) {
  const regExp = /^[0-9]{6}$/;
  return regExp.test(asValue)
}
function isEamilVaild(asValue) {
  const regExp = /^[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]/;
  return regExp.test(asValue);

}
function isPasswordVaild(asValue) {
  //영문, 숫자는 1개 씩 무조건 포함, 일부 특수문자 사용 가능, 8-20자 길이
  const regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
  return regExp.test(asValue);
}

// 로그인 함수
function login() {
  let username = $("#username").val()
  let password = $("#password").val()

  if (username == null) {
    $("#help_id").text("아이디를 입력해주세요.")
    $("#username").focus()
    return;
  } else {
    $("#help_id").text("")
  }

  if (password == null) {
    $("#help_pw").text("비밀번호를 입력해주세요.")
    $("#password").focus()
    return;
  } else {
    $("#help_pw").text("")
  }
  $.ajax({
    type: "POST",
    url: "/api/login",
    data: { username_give: username, password_give: password },
    success: function (response) {
      if (response['result'] == 'success') {
        document.cookie = `token=${response['token']}`
        alert('로그인이 완료되었습니다.')
        console.log(response['token'])
        window.location.href = '/main/' + username
      } else {
        alert(response['msg'])
        window.location.reload();
      }
    }
  })
}
function modal_active() {
  const signup = document.querySelector('.modal');
  signup.classList.add('is-active');
}
function modal_close() {
  const modalClose = document.querySelector('.modal');
  modalClose.classList.remove('is-active');
}

function init() {
  loginBtn.addEventListener('click', login)
  modalCloseBtn.addEventListener('click', modal_close)
  modalOpenBtn.addEventListener('click', modal_active)

  //회원가입시에 event
  joinBtn.addEventListener('click', () => {

    if (!isNameVaild(nameInput.value)) {
      nameInput.textContent = ""
      alert("이름이 유효하지 않습니다.")
      return
    }
    if (!isBirthVaild(birthInput.value)) {
      birthInput.textContent = ""
      alert("생년월일이 유효하지 않습니다.")
      return
    }
    if (!isEamilVaild(emailInput.value)) {
      emailInput.textContent = ""
      alert("이메일이 유효하지 않습니다.")
      return
    }
    if (!isPasswordVaild(pwInput.value)) {
      pwInput.textContent = ""
      alert("패스워드가 유효하지 않습니다.영문, 숫자는 1개 씩 무조건 포함, 일부 특수문자 사용 가능, 8-20자 길이")
      return
    }

    $.ajax({
      type: "POST",
      url: "/api/signup",
      data: {
        name: nameInput.value,
        birth: birthInput.value,
        email: emailInput.value,
        password: pwInput.value,
      },
      success: function (response) {
        if (response['result'] == true) {
          window.location.href = "/"
        } else {
          alert("회원가입 오류")
        }
      }
    })
  })
  checkOverlapBtn.addEventListener('click', () => {
    if (!isEamilVaild(emailInput.value)) {
      emailInput.value = ""
      alert("이메일이 유효하지 않습니다.")
      return
    }

    console.log("here")
    $.ajax({
      type: "POST",
      url: "/api/duplicate",
      data: {
        email: emailInput.value,
      },
      success: function (response) {
        if (response['result'] == true) {
          alert("사용가능한 아이디 입니다.")
        } else {
          alert("아이디가 중복되었습니다.")
          emailInput.value = ""
        }
      }
    })

  })
}
init()
