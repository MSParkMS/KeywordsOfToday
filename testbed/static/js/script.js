//test
var isMobile = false;
var filter = "win16|win32|win64|mac";

if (navigator.platform) {
    isMobile = filter.indexOf(navigator.platform.toLowerCase()) < 0;
}

function movie_reserv(theather, link, theaterCd){
    var cgv_link = "http://www.cgv.co.kr";
    var cgv_mobile_link = "http://m.cgv.co.kr/WebApp/Reservation/schedule.aspx?tc=";
    var lottecinema_link = "https://www.lottecinema.co.kr/NLCHS/Ticketing";
    var megabox_link = "https://www.megabox.co.kr/on/oh/ohz/PcntSeatChoi/selectPcntSeatChoi.do?megaboxLanguage=kr&playSchdlNo=";
    
    if(theather == 'LOTTE'){
        alert("롯데시네마는 상영관, 영화 자동선택서비스를 제공하지 않습니다. 예매사이트로 이동합니다.");
    }
    if(link == '#' && theaterCd == '#'){
        alert("좌석이 없거나 예매서비스가 불가능한 상영관, 영화관 입니다.");
        return;
    }
    
    if(!isMobile){ /** PC **/
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
    }else{ /** MOBILE**/
        switch (theather) {
            case 'CGV' :
                window.open(cgv_mobile_link+theaterCd.split("-")[1]);
                break;
            case 'LOTTE' :
                window.open(lottecinema_link+theaterCd.split("-")[1]);
                break;
            case 'MEGABOX' :
                window.open(megabox_link+theaterCd.split("-")[1]);
                break;
        }
    }
}
