// function addList() {
//     let temp_html = `<div class="comment-box">안녕 나는 추가 되었어</div>`;
//     $('#comment').append(temp_html);
// }

// $(window).scroll(function () {
//     if ($(window).scrollTop() == $(document).height() - $(window).height()) {
//         addList();
//     }
// });

$(window).on("load", function () {
    const url = document.location.href.split("/");
    let num = Number(url[url.length - 1]);
    const title = document.querySelector(".title");
    title.textContent = `항해일지 ${num} 일차`;
  });
        
function save() {
    const url = document.location.href.split("/");
    let num = Number(url);
    let text = $('#text').val()

    let file = $('#image')[0].files[0]
    let form_data = new FormData()

    form_data.append("text_give", text)
    form_data.append("num_give", num)
    form_data.append("file_give", file)

    function update() {
        window.location.href = `/logbook/${num}`;
      }
    $.ajax({
        type: "POST",
        url: "/diary",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            alert(response["msg"])
            modal_close();
            update();
        }
    });
}
function showArticles() { 
}

function modal_active() {
    const signup = document.querySelector('.modal');
    signup.classList.add('is-active')
    bsCustomFileInput.init();
}
function modal_close() {
    const modalClose = document.querySelector('.modal');
    modalClose.classList.remove('is-active');
}

function move(direction) {
    const url = document.location.href.split("/");
    let num = Number(url[url.length - 1]);

    if (direction === "R") {
      num = num + 1 > 99 ? 1 : num + 1;
    } else if (direction === "L") {
      console.log("here");
      num = num - 1 < 1 ? 99 : num - 1;
    }
    console.log(num);
    window.location.href = `/logbook/${num}`;
  }