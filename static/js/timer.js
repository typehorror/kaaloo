    function time_from_second(seconds){
        var hours = parseInt(seconds / 3600000);
        var minutes = parseInt((seconds - hours * 3600000) / 60000);
        var seconds = parseInt((seconds % 60000) / 1000);
        if (hours < 10){ hours = "0" + hours;}
        if (minutes < 10){ minutes = "0" + minutes;}
        if (seconds < 10){ seconds = "0" + seconds;}
        result = new Array();
        result['hours'] = hours;
        result['minutes'] = minutes;
        result['seconds'] = seconds;
        return result;
    }

    function timer(place_holder, loop){
        var currentTime = new Date().getTime();
        var delta = currentTime - timer_start;
        result = time_from_second(delta)
        $(place_holder).html(result['hours'] + ":" + result['minutes'] + ":" +  result['seconds']);
    }
