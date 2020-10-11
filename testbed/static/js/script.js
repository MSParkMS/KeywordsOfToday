//test
function movie_reserv(theather, link){
    var cgv_link = "http://www.cgv.co.kr";
    var lottecinema_link = "https://www.lottecinema.co.kr";
    var megabox_link = "https://www.megabox.co.kr/on/oh/ohz/PcntSeatChoi/selectPcntSeatChoi.do?megaboxLanguage=kr&playSchdlNo=";
    
    if(link == '#'){
        alert("좌석이 없거나 예매서비스 불가능한 상영관, 영화관 입니다.");
        return;
    }
    
    switch (theather) {
        case 'CGV' :
            window.open(cgv_link+link);
            break;
        case 'LOTTE' :
            window.open(lottecinema_link+link);
            break;
        case 'MEGABOX' :
            window.open(megabox_link+link);
            break;
    }
}