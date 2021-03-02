
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


joinBtn.addEventListener('click', () => {

  console.log(nameInput.value, birthInput.value, emailInput.value, pwInput.value)

  if (!isNameVaild()) {
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
  console.log("성공")
})

checkOverlapBtn.addEventListener('click', () => {
  alert("hhoh")
  return
})
