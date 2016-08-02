/**
 * Created by Angelica Yunshu Li on 8/2/2016.
 */
$(document).ready(function(){


    /* add url row */
    var newrow = "<tr> \
                    <td class='delete btn' align='right'><img src='/images/delete.png' class='icon'/></td>\
                    <td class='title'><input name='new-btn'></td>\
                    <td align='left' class='url'><input class='url' name='new-btn-url' text='{{courseinfo.get(course).get(name)}}'/></td>\
                    </tr>";
    $(".add").on("click",function(){
        var row = $(this).parent();
        $(row).before(newrow);
    });

    /* detele url row */
    $("table").on("click","td.delete",function(){
        var row = $(this).parent();
        $(row).fadeOut().remove();
    });
    $("table").on("mouseenter","td.delete",function(){
        $(this).find("img").remove();
       $(this).prepend("<span>Delete</span>");
    });
    $("table").on("mouseleave","td.delete",function(){
        $(this).find("span").remove();
        $(this).append("<img src='/images/delete.png' class='icon'/>");
    });

    /*TODO: edit courseid*/
    /*TODO: delete course*/
    /*TODO: add course*/


});