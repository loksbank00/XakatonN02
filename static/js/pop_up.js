const openPopUp = document.getElementsByClassName("img");
        const closePopUp = document.getElementsByClassName("pop_up_close");
        const popUp = document.getElementsByClassName("pop_up");
        const popUpImg = document.getElementById('pop_up_img');
        const rd = document.getElementById("f");
        const teg = document.getElementById("teg_area");

        console.log(rd)

        for (var index = 0; index < openPopUp.length; index++) {
            openPopUp[index].addEventListener('click', function(e){
                popUp[0].classList.add('active');
                popUpImg.src = this.src;
                document.body.style.overflow = 'hidden';
                console.log(rd.innerHTML)
                rd.innerHTML = this.name;
                teg.innerHTML = this.title;


        });}
        closePopUp[0].addEventListener('click', function(e){
            popUp[0].classList.remove('active');
            document.body.style.overflow = 'scroll';

        });
