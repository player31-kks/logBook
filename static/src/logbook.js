

$(window).on("load", function () {
  const url = document.location.href.split("/");
  let num = Number(url[url.length - 1]);
  const title = document.querySelector(".title");
  title.textContent = `항해일지 ${num} 일차`;

  const user = document.querySelector('.user-info');

  $.ajax({
    type: "GET",
    url: "/api/get_userlist",
    data: {},
    success: function (response) {

      let url = document.location.href.split("/");
      let email = url[url.length - 2]
      let name = ''

      let articles = response['all_users']
      for (let i = 0; i < articles.length; i++) {
        if (articles[i]['email'] == email) {
          name = articles[i]['name']
          break;
        }
      }
      user.innerHTML = name + "님 항해일지 입니다."
    }
  });

});

function save() {
  const url = document.location.href.split("/");
  let num = Number(url[url.length - 1]);
  let text = $('#text').val()
  let file = $('#image')[0].files[0]
  console.log(file)
  if (file == undefined) {
    console.log(file)
    $.ajax({
      type: "POST",
      url: "/api/logbook",
      data: {
        text_give: text,
        num_give: num,
      },
      success: function (response) {
        alert(response["msg"])
        modal_close();
        window.location.reload();
      }
    });

  } else {
    let form_data = new FormData()
    form_data.append("text_give", text)
    form_data.append("num_give", num)
    form_data.append("file_give", file)


    $.ajax({
      type: "POST",
      url: "/api/logbook",
      data: form_data,
      cache: false,
      contentType: false,
      processData: false,
      success: function (response) {
        alert(response["msg"])
        modal_close();
        window.location.reload();
      }
    });

  }
}

function go_main() {
  let url = document.location.href.split("/");
  let email = url[url.length - 2];
  window.location.href = '/main/' + email
}

function modal_active() {
  const signup = document.querySelector('.modal');
  signup.classList.add('is-active');
  bsCustomFileInput.init();
}
function modal_close() {
  const modalClose = document.querySelector('.modal');
  modalClose.classList.remove('is-active');
}

function move(direction) {
  let url = document.location.href.split("/");
  let num = Number(url[url.length - 1]);
  let length = 0;

  if (num >= 10) {
    length = 2
  }
  else {
    length = 1
  }

  if (direction === "R") {
    num = num + 1 > 99 ? 1 : num + 1;
  } else if (direction === "L") {
    console.log("here");
    num = num - 1 < 1 ? 99 : num - 1;
  }

  let url_str = ''
  url = document.location.href;

  for (let i = 0; i < url.length - length; i++) {
    url_str += url[i];
  }
  url_str += num;
  window.location.href = url_str;
}

function like(obj) {
  let find_img = $(obj.closest('.card')).children('.card-content').children('#img').attr('src').split("/")
  let img = find_img[3]
  let url = document.location.href.split("/");
  let num = Number(url[url.length - 1]);
  let email = url[url.length - 2];

  $.ajax({
    type: 'POST',
    url: '/api/like',
    data: {
      num_give: num,
      email_give: email,
      file_give: img,
    },
    success: function (response) {
      if (response['result'] == true) {
        alert('좋아요.');
        window.location.reload();
      } else {
        alert('에러 발생');
      }
    }
  });
}

function delete_card(obj) {
  let find_img = $(obj.closest('.card')).children('.card-content').children('#img').attr('src').split("/")
  let img = find_img[3]
  let url = document.location.href.split("/");
  let num = Number(url[url.length - 1]);
  let email = url[url.length - 2];

  $.ajax({
    type: 'DELETE',
    url: '/api/logbook',
    data: {
      num_give: num,
      email_give: email,
      file_give: img,
    },
    success: function (response) {
      if (response['result'] == true) {

        alert('삭제되었습니다.');
        window.location.reload();
      } else {
        alert('에러 발생');
      }
    }
  });

  //   $.ajax({
  //     type: 'DELETE',
  //     url: '/api/logbook',
  //     data: form_data,
  //     success: function (response) {
  //         alert(response['msg']);
  //         window.location.reload();
  //     }
  // });
}