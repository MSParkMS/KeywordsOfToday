//test
function movie_reserv(theather, link){
    var cgv_link = "http://www.cgv.co.kr";
    var lottecinema_link = "https://www.lottecinema.co.kr";
    var megabox_link = "https://www.megabox.co.kr/on/oh/ohz/PcntSeatChoi/selectPcntSeatChoi.do?megaboxLanguage=kr&playSchdlNo=";
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