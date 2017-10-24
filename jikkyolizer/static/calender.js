function InitCalender(year=0, month=0, f_day=0, day=0){
    var TodayDate=new Date(); 
    //年・月・曜日・日付を取得する
        year = TodayDate.getFullYear();
        month = TodayDate.getMonth()+1;
        week = TodayDate.getDay();
        day = TodayDate.getDate();
    if(f_day){
        MakeCalender(year, month, week, day); 
    }else{
        MakeCalender(year, month, week, day); 
        SenceClick(year, month, day);
    }
} 

function GetMaxDate(year, month){
    MaxDate=[31,28,31,30,31,30,31,31,30,31,30,31];
    if((year%4==0) && (year%100!=0)){
        MaxDate[1]=29;
    }
    if(year%400==0){
        MaxDate[1]=29;
    }
    return MaxDate[month-1];
}

function GetMonthName(month){
    MonthName = ['January',"February","March","April","May","June","July","August","September","October","November","December"];
    return MonthName[month-1]
}

function GoPrevMonth(year, month, FirstWeekDate){
    month--;
    if(month==0){
        year--;
        month=12;
    }
    FirstWeekDate--;
    if(FirstWeekDate==-1){
        FirstWeekDate==6;
    }
    day=GetMaxDate(year, month);
    MakeCalender(year, month, FirstWeekDate, day);
}

function GoNextMonth(year, month, FirstWeekDate){
    FirstWeekDate+=GetMaxDate(year, month);
    month++;
    if(month==13){
        year++;
        month=1;
    }
    FirstWeekDate %= 7;
    day=1;
    MakeCalender(year, month, FirstWeekDate, day);
}

function GetFirstWeek(CurrentWeek, CurrentDay){
    CurrentWeek += 35;
    CurrentWeek -= (CurrentDay - 1)
    CurrentWeek %= 7;
    return CurrentWeek;
}

function SenceClick(year, month, day){
    if(month<10){Smonth='0'+String(month);}else{Smonth=String(month);}
    if(day<10){Sday='0'+String(day);}else{Sday=String(day);}
    document.getElementById('id_used_at').value=String(year)+'-'+Smonth+'-'+Sday;
    MaxDate=GetMaxDate(year, month);
    for(EachDay=1;EachDay<=MaxDate;EachDay++){
        document.getElementById(year+"-"+month+"-"+EachDay).style.backgroundColor = '#ffffff';
    }
    document.getElementById(year+"-"+month+"-"+day).style.backgroundColor = '#e0ffff';
}

function MakeCalender(year, month, week, day){
    //document.getElementById("calender").innerHTML="<table><tr>";
    MaxDate=GetMaxDate(year, month);
    MonthName=GetMonthName(month);
    WeekDate=GetFirstWeek(week, day);
    CalenderTitle = String(year) + "-" + MonthName;
    CalenderHtml = CalenderTitle;
    CalenderHtml += "&emsp;&emsp;&emsp;&emsp;&emsp;<span onclick=\"GoPrevMonth("+year+","+month+","+WeekDate+")\" style=\"cursor: pointer\">Prev</span>   &emsp;&emsp;&emsp;<span onclick=\"GoNextMonth("+year+","+month+","+WeekDate+")\" style=\"cursor: pointer\">Next</span>";
    CalenderHtml += "<table border=\"1\" width=\"350\"><tr>"+
    "<td width=\"50\"><center>Mon</center></td><td width=\"50\"><center>Tue</center></td><td width=\"50\"><center>Wed</center></td><td width=\"50\"><center>Thu</center></td><td width=\"50\"><center>Fri</center></td><td width=\"50\"><center><font color=\"blue\">Sat</font></center></td><td width=\"50\"><center><font color=\"red\">Sun</font></center></td></tr><tr>";
    InsertDay=1;
    //WeekDate=week;
    BreakFlag=0;
    InsertDate=0;
    if(WeekDate==0){WeekDate=7;}
    while(InsertDate<WeekDate-1){
        CalenderHtml+="<td></td>";
        InsertDate++;
    }
    while(1){
        while(WeekDate<8){
            CalenderHtml+="<td style=\"cursor: pointer\" id=\""+year+"-"+month+"-"+InsertDay+"\" onclick=\"SenceClick("+year+","+month+","+InsertDay+")\"><center>";
            if(WeekDate==6){CalenderHtml+="<font color=\"blue\">";}
            if(WeekDate==7){CalenderHtml+="<font color=\"red\">";}
            CalenderHtml+=InsertDay;
            if(WeekDate==6){CalenderHtml+="</font>";}
            if(WeekDate==7){CalenderHtml+="</font>";}
            CalenderHtml+="</center></td>";
            if(InsertDay>=MaxDate){
                BreakFlag=1;
                break;
            }
            InsertDay++;
            WeekDate++;
        }
        if(BreakFlag==1){
            while(WeekDate<7){
                CalenderHtml+="<td></td>";
                WeekDate++;
            }
            break;
        }
        WeekDate=1;
        CalenderHtml+="</tr><tr>";
    }
    CalenderHtml += "</tr></table>";
    document.getElementById("calender").innerHTML=CalenderHtml;
}
