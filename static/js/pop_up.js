const openPopUp = document.getElementsByClassName("img");
        const closePopUp = document.getElementsByClassName("pop_up_close");
        const popUp = document.getElementsByClassName("pop_up");

        const rd = document.getElementById("f");
        const teg = document.getElementById("teg_area");
        const visDiv = document.getElementsByClassName('viiiis_photo');
        console.log(rd)

        const remove_inp = document.getElementsByClassName("flaf_for_remove");
        const remove_btn = document.getElementById("remode_photo");


        for (var index = 0; index < openPopUp.length; index++) {

            openPopUp[index].addEventListener('click', function(e){
                console.log(this.tagName)

                if (this.tagName=="IMG"){
                console.log(visDiv[0])
                visDiv[0].innerHTML = '<img src="" id="pop_up_img" alt="картинка">'
                const popUpImg = document.getElementById('pop_up_img');
                popUpImg.src = this.src;
                console.log(this.name);
                remove_inp.value =this.name
                rd.innerHTML = this.name;
                }
                else if(this.tagName=="VIDEO"){

                visDiv[0].innerHTML = '<video src="" id="pop_up_img" alt="картинка" controls autoplay></video>'
                const popUpImg = document.getElementById('pop_up_img');
                popUpImg.src = this.src;
                 rd.innerHTML = this.innerHTML;
                 remove_inp.value =this.innerHTML

                }
                popUp[0].classList.add('active');
                remove_btn.href='/photo/'+remove_inp.value+'/del'
                document.body.style.overflow = 'hidden';
                console.log(this.innerHTML)

                teg.innerHTML = this.title;



        });}
        closePopUp[0].addEventListener('click', function(e){
            popUp[0].classList.remove('active');
            document.body.style.overflow = 'scroll';

        });
